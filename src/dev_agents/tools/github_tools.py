import httpx


class GitHubClient:
    def __init__(self, token: str):
        self.client = httpx.AsyncClient(
            base_url="https://api.github.com",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=30.0,
        )

    async def get_pull_request_diff(
        self,
        owner: str,
        repo: str,
        pr_number: int,
    ) -> str:
        response = await self.client.get(
            f"/repos/{owner}/{repo}/pulls/{pr_number}",
            headers={
                "Accept": "application/vnd.github.v3.diff"
            },
        )
        response.raise_for_status()
        return response.text

    async def close(self) -> None:
        await self.client.aclose()
