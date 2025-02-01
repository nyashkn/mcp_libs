#!/usr/bin/env python3
from typing import Any, Dict, List, Optional
from modelcontextprotocol.server import Server, StdioServerTransport
from modelcontextprotocol.types import (
    CallToolRequestSchema,
    ErrorCode,
    ListToolsRequestSchema,
    McpError,
    TextContent,
    SamplingMessage,
)
from github import Github
import os

class GitHubServer:
    def __init__(self):
        self.server = Server(
            {
                "name": "github-server",
                "version": "0.1.0",
            },
            {
                "capabilities": {
                    "tools": {},
                }
            }
        )
        
        token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
        if not token:
            raise McpError(ErrorCode.InternalError, "GitHub token not found in environment")
        
        self.github = Github(token)
        
        self.setup_tool_handlers()
        self.server.onerror = lambda error: print(f"[MCP Error] {error}", file=os.sys.stderr)

    def setup_tool_handlers(self):
        self.server.set_request_handler(ListToolsRequestSchema, self.handle_list_tools)
        self.server.set_request_handler(CallToolRequestSchema, self.handle_call_tool)

    async def handle_list_tools(self, _):
        return {
            "tools": [
                {
                    "name": "list_repositories",
                    "description": "List repositories for the authenticated user",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "visibility": {
                                "type": "string",
                                "enum": ["all", "public", "private"],
                                "description": "Filter repositories by visibility"
                            }
                        }
                    }
                },
                {
                    "name": "create_issue",
                    "description": "Create a new issue in a repository",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "repo": {
                                "type": "string",
                                "description": "Repository name in format owner/repo"
                            },
                            "title": {
                                "type": "string",
                                "description": "Issue title"
                            },
                            "body": {
                                "type": "string",
                                "description": "Issue body/description"
                            },
                            "labels": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of label names to apply"
                            }
                        },
                        "required": ["repo", "title", "body"]
                    }
                },
                {
                    "name": "search_code",
                    "description": "Search for code in GitHub repositories",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "language": {
                                "type": "string",
                                "description": "Filter by programming language"
                            }
                        },
                        "required": ["query"]
                    }
                }
            ]
        }

    async def handle_call_tool(self, request):
        tool_name = request.params.name
        args = request.params.arguments

        try:
            if tool_name == "list_repositories":
                return await self.list_repositories(args)
            elif tool_name == "create_issue":
                return await self.create_issue(args)
            elif tool_name == "search_code":
                return await self.search_code(args)
            else:
                raise McpError(ErrorCode.MethodNotFound, f"Unknown tool: {tool_name}")
        except Exception as e:
            raise McpError(ErrorCode.InternalError, str(e))

    async def list_repositories(self, args: Dict[str, Any]):
        visibility = args.get("visibility", "all")
        repos = self.github.get_user().get_repos(visibility=visibility)
        repo_list = [
            {
                "name": repo.full_name,
                "description": repo.description,
                "url": repo.html_url,
                "visibility": "public" if repo.public else "private",
                "stars": repo.stargazers_count
            }
            for repo in repos
        ]
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Found {len(repo_list)} repositories:\n" + 
                         "\n".join([f"- {r['name']} ({r['visibility']}): {r['description'] or 'No description'}"
                                  for r in repo_list])
                )
            ]
        }

    async def create_issue(self, args: Dict[str, Any]):
        repo = self.github.get_repo(args["repo"])
        labels = args.get("labels", [])
        issue = repo.create_issue(
            title=args["title"],
            body=args["body"],
            labels=labels
        )
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Created issue #{issue.number}: {issue.title}\nURL: {issue.html_url}"
                )
            ]
        }

    async def search_code(self, args: Dict[str, Any]):
        query = args["query"]
        if "language" in args:
            query += f" language:{args['language']}"
        
        results = self.github.search_code(query)
        code_results = []
        for result in results[:5]:  # Limit to first 5 results
            code_results.append({
                "repository": result.repository.full_name,
                "path": result.path,
                "url": result.html_url
            })
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Search results:\n" +
                         "\n".join([f"- [{r['repository']}] {r['path']}\n  {r['url']}"
                                  for r in code_results])
                )
            ]
        }

    async def run(self):
        transport = StdioServerTransport()
        await self.server.connect(transport)
        print("GitHub MCP server running on stdio", file=os.sys.stderr)

if __name__ == "__main__":
    import asyncio
    server = GitHubServer()
    asyncio.run(server.run())