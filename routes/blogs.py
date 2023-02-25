from __future__ import annotations

import fastapi
from github.Gist import Gist

from . import Extension, route


class Profile(Extension):
    async def get_gist(self, gist_id: str) -> Gist:
        auth = self.app.config.GITHUB_TOKEN
        headers = {"Authorization": f"token {auth}"}
        async with self.app.client.request("GET", f"https://api.github.com/gists/{gist_id}", headers=headers) as resp:
            return Gist(self.app.client, headers, await resp.json(), completed=True)  # type: ignore

    async def render_markdown(self, content: str) -> str:
        auth = self.app.config.GITHUB_TOKEN
        headers = {"Authorization": f"token {auth}"}
        async with self.app.client.request(
            "POST", "https://api.github.com/markdown", headers=headers, json={"text": content}
        ) as resp:
            return await resp.text()

    @route(path="/blog", response_model=fastapi.responses.HTMLResponse)
    async def blog(self, request: fastapi.Request) -> fastapi.responses.Response:
        f_img = self.app.get_image("footers")
        gist = await self.get_gist("426ec7974f705303a2363c739dd82309")
        file = gist.files[list(gist.files.keys())[0]]
        name = file.filename.split(".")[0].replace("-", " ").title().replace("_", " ")
        content = file.content.replace("user-content-", "")
        return self.app.templates.TemplateResponse(
            "blog_template.html",
            {
                "request": request,
                "title": "Blog",
                "f_img": f_img,
                "name": name,
                "content": await self.render_markdown(content),
            },
        )
