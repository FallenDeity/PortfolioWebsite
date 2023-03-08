from __future__ import annotations

import re
import typing

import fastapi
from bs4 import BeautifulSoup
from github.AuthenticatedUser import AuthenticatedUser
from github.Gist import Gist
from github.GistComment import GistComment

from utils.constants import GITHUB_USERNAME
from utils.models import GistData

from . import Extension, route

# pyright: reportGeneralTypeIssues=false


class Blogs(Extension):
    async def get_stars(self, gist_url: str) -> int:
        async with self.app.client.get(gist_url) as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")
            social_count = soup.find("a", {"class": "social-count"})
            return int(str(social_count["aria-label"]).split(" ")[0]) if social_count else 0

    async def get_user(self, login: str = GITHUB_USERNAME) -> AuthenticatedUser:
        return await self.app.async_run(self.app.github.get_user, login)

    async def get_user_gists(self) -> list[Gist]:
        user = await self.get_user()
        return await self.app.async_run(user.get_gists)

    async def get_gist(self, gist_id: str) -> Gist:
        return await self.app.async_run(self.app.github.get_gist, gist_id)

    async def render_markdown(self, content: str) -> str:
        content = content.replace("user-content-", "")
        result = await self.app.async_run(self.app.github.render_markdown, content)
        if "[ ]" in result or "[x]" in result:
            soup = BeautifulSoup(result, "html.parser")
            for li in soup.find_all("li"):
                if "[ ]" in li.text or "[x]" in li.text:
                    ul = li.find_parent("ul") or li.find_parent("ol")
                    ul["class"] = "contains-task-list"
                    li["class"] = "task-list-item enabled"
                    checkbox = soup.new_tag("input")
                    checkbox["type"] = "checkbox"
                    checkbox["class"] = "task-list-item-checkbox"
                    checkbox["disabled"] = ""
                    if "[x]" in li.text:
                        checkbox["checked"] = ""
                    li.insert(0, checkbox)
            result = str(soup).replace("[ ]", "").replace("[x]", "")
        return result

    async def get_comments(self, gist: Gist) -> list[GistComment]:
        return await self.app.async_run(gist.get_comments)

    async def get_content(self, url: str) -> str:
        async with self.app.client.get(url) as resp:
            return await resp.text()

    async def bump_gist(self, gist: Gist, title: str | None = None) -> Gist:
        title = [i for i in gist.files.keys() if ".md" in i][0] if not title else title
        n_title = re.sub(r"[^a-zA-Z0-9.-]", " ", title).replace(".md", "").title()
        stars = await self.get_stars(gist.html_url)
        custom_description = re.sub(r"#+\s", "", gist.files[title].content[0:200])
        custom_description = re.sub(r"[^a-zA-Z0-9.]", " ", custom_description) + "..."
        rendered = await self.render_markdown(gist.files[title].content)
        data = GistData(title=n_title, stars=stars, description=custom_description, rendered=rendered)
        gist.gists = getattr(gist, "gists", []) + [data]
        return gist

    @route("/api/v1/image", method="POST", response_model=fastapi.responses.JSONResponse)
    async def feedback(self, data: typing.Dict[str, str]) -> fastapi.responses.JSONResponse:
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
        gist.gists = []
        comments = [i for i in await self.get_comments(gist)]
        for comment in comments:
            comment.custom_body = await self.render_markdown(comment.body)
        users = [gist.owner] + [i.user for i in gist.forks]
        gist = [await self.bump_gist(gist, i) for i in gist.files.keys() if ".md" in i][-1]
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
                "image": await self.app.get_meta_image(str(request.url)),
            },
        )

    @route(path="/blog", response_model=fastapi.responses.HTMLResponse)
    async def blog(self, request: fastapi.Request) -> fastapi.responses.Response:
        f_img = self.app.get_image("footers")
        user = await self.get_user()
        gists = await self.get_user_gists()
        for i in gists:
            i.gists = []
        gists = [await self.bump_gist(i) for i in gists]
        return self.app.templates.TemplateResponse(
            "blog.html",
            {
                "request": request,
                "title": "Blog",
                "f_img": f_img,
                "gists": gists,
                "user": user,
                "image": await self.app.get_meta_image(str(request.url)),
            },
        )

    @property
    def headers(self) -> typing.Dict[str, str]:
        auth = str(self.app.config.GITHUB_TOKEN)
        return {"Authorization": f"token {auth}"}
