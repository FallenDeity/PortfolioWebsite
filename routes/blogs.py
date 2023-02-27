from __future__ import annotations

import re
import typing

import fastapi
from bs4 import BeautifulSoup
from github.AuthenticatedUser import AuthenticatedUser
from github.Gist import Gist
from github.GistComment import GistComment

from utils.constants import GITHUB_USERNAME

from . import Extension, route

# pyright: reportGeneralTypeIssues=false


class Profile(Extension):
    async def get_stars(self, gist_url: str) -> int:
        async with self.app.client.get(gist_url) as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")
            social_count = soup.find("a", {"class": "social-count"})
            return int(str(social_count["aria-label"]).split(" ")[0]) if social_count else 0

    async def get_user(self, login: str = GITHUB_USERNAME) -> AuthenticatedUser:
        return await self.app.async_run(self.app.github.get_user, login)

    async def get_user_gists(self) -> list[Gist]:
        return await self.app.async_run(self.app.github.get_user().get_gists)

    async def get_gist(self, gist_id: str) -> Gist:
        return await self.app.async_run(self.app.github.get_gist, gist_id)

    async def render_markdown(self, content: str) -> str:
        return await self.app.async_run(self.app.github.render_markdown, content)

    async def get_comments(self, gist: Gist) -> list[GistComment]:
        return await self.app.async_run(gist.get_comments)

    async def get_content(self, url: str) -> str:
        async with self.app.client.get(url) as resp:
            return await resp.text()

    async def bump_gist(self, gist: Gist) -> Gist:
        title = [i for i in gist.files.keys() if ".md" in i][0]
        gist.title = re.sub(r"[^a-zA-Z0-9.-]", " ", title).replace(".md", "").title()
        gist.stars = await self.get_stars(gist.html_url)
        gist.custom_description = re.sub(r"#+\s", "", gist.files[title].content[0:200])
        gist.custom_description = re.sub(r"[^a-zA-Z0-9.]", " ", gist.custom_description) + "..."
        gist.rendered = await self.render_markdown(gist.files[title].content.replace("user-content-", ""))
        return gist

    @route("/api/v1/image", method="POST", response_model=fastapi.responses.JSONResponse)
    async def feedback(self, data: dict[str, str]) -> fastapi.responses.JSONResponse:
        query = data.get("query", "github")
        google, engine = str(self.app.config.GOOGLE_API_KEY), str(self.app.config.SEARCH_ENGINE)
        async with self.app.client.get(
            f"https://www.googleapis.com/customsearch/v1?key={google}&cx={engine}&q={query}&searchType=image&num=10"
        ) as resp:
            data = (await resp.json())["items"]
            types_ = ("png", "jpg", "jpeg", "gif")
            img = [i for i in data if i["link"].endswith(types_)][0]
            return fastapi.responses.JSONResponse(
                {
                    "url": img["link"],
                }
            )

    @route(path="/posts", response_model=fastapi.responses.HTMLResponse)
    async def render(self, request: fastapi.Request, gist_id: str) -> fastapi.responses.Response:
        f_img = self.app.get_image("footers")
        gist = await self.get_gist(gist_id)
        comments = [i for i in await self.get_comments(gist)]
        for comment in comments:
            comment.custom_body = await self.render_markdown(comment.body)
        users = [gist.owner] + [i.user for i in gist.forks]
        gist = await self.bump_gist(gist)
        return self.app.templates.TemplateResponse(
            "blog_template.html",
            {
                "request": request,
                "title": "Blog",
                "f_img": f_img,
                "gist": gist,
                "comments": comments,
                "users": users,
                "len": len,
                "content": gist.rendered,  # type: ignore
            },
        )

    @route(path="/blog", response_model=fastapi.responses.HTMLResponse)
    async def blog(self, request: fastapi.Request) -> fastapi.responses.Response:
        f_img = self.app.get_image("footers")
        user = await self.get_user()
        gists = await self.get_user_gists()
        gists = [await self.bump_gist(i) for i in gists]
        return self.app.templates.TemplateResponse(
            "blog.html",
            {
                "request": request,
                "title": "Blog",
                "f_img": f_img,
                "gists": gists,
                "user": user,
            },
        )

    @property
    def headers(self) -> typing.Dict[str, str]:
        auth = str(self.app.config.GITHUB_TOKEN)
        return {"Authorization": f"token {auth}"}
