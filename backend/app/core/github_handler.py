import httpx
import base64
from typing import Optional, List
from app.core.language_detect import is_valid_code_file

ALLOWED_EXTENSIONS = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rb", ".php", ".swift", ".kt", ".jsx", ".tsx"}

async def list_user_repos(access_token: str) -> dict:
    """List user repositories from GitHub"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.github.com/user/repos",
                headers={"Authorization": f"Bearer {access_token}"},
                params={"sort": "updated", "per_page": 30}
            )
            
            if response.status_code != 200:
                return {"error": "Failed to fetch repositories"}
            
            repos = response.json()
            return {
                "repos": [
                    {
                        "name": repo["name"],
                        "url": repo["html_url"],
                        "description": repo["description"],
                        "owner": repo["owner"]["login"],
                        "is_fork": repo["fork"]
                    }
                    for repo in repos
                ]
            }
    except Exception as e:
        return {"error": str(e)}

async def list_repo_contents(
    owner: str,
    repo: str,
    path: str,
    access_token: str
) -> dict:
    """List contents of a repository path"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if response.status_code != 200:
                return {"error": "Failed to fetch contents"}
            
            contents = response.json()
            if isinstance(contents, dict):
                contents = [contents]
            
            return {
                "contents": [
                    {
                        "name": item["name"],
                        "type": item["type"],
                        "path": item["path"],
                        "size": item.get("size", 0),
                        "url": item["html_url"]
                    }
                    for item in contents
                    if is_valid_code_file(item["name"]) or item["type"] == "dir"
                ]
            }
    except Exception as e:
        return {"error": str(e)}

async def get_file_content(
    owner: str,
    repo: str,
    path: str,
    access_token: str
) -> dict:
    """Get content of a file from GitHub"""
    try:
        if not is_valid_code_file(path):
            return {"error": "File type not supported"}
        
        async with httpx.AsyncClient() as client:
            url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if response.status_code != 200:
                return {"error": "Failed to fetch file"}
            
            data = response.json()
            
            # Decode base64 content
            try:
                content = base64.b64decode(data["content"]).decode("utf-8")
            except:
                return {"error": "Failed to decode file content"}
            
            return {
                "content": content,
                "size": len(content),
                "path": data["path"],
                "name": data["name"]
            }
    except Exception as e:
        return {"error": str(e)}
