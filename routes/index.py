from __future__ import annotations

import fastapi

from utils.constants import DESCRIPTION, LINKS, SKILLS, VIDEOS

from . import Extension, route


class Home(Extension):
    @route(path="/", response_model=fastapi.responses.HTMLResponse)
    async def home(self, request: fastapi.Request) -> fastapi.responses.Response:
        f_img, a_img = self.app.get_image("footers"), self.app.get_image("avatars", "png")
        return self.app.templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "Home",
                "f_img": f_img,
                "a_img": a_img,
                "videos": VIDEOS.get_as_list(),
                "desc": DESCRIPTION,
                "skills": SKILLS.get_lucky_4(),
            },
        )

    @route(path="/source", response_model=fastapi.responses.RedirectResponse)
    async def source(self, _: fastapi.Request) -> fastapi.responses.RedirectResponse:
        return fastapi.responses.RedirectResponse(LINKS.SOURCE)

    @route(path="/github", response_model=fastapi.responses.RedirectResponse)
    async def github(self, _: fastapi.Request) -> fastapi.responses.RedirectResponse:
        return fastapi.responses.RedirectResponse(LINKS.GITHUB)

    @route(path="/discord", response_model=fastapi.responses.RedirectResponse)
    async def discord(self, _: fastapi.Request) -> fastapi.responses.RedirectResponse:
        return fastapi.responses.RedirectResponse(LINKS.DISCORD)

    @route(path="/email", response_model=fastapi.responses.RedirectResponse)
    async def twitter(self, _: fastapi.Request) -> fastapi.responses.RedirectResponse:
        return fastapi.responses.RedirectResponse(LINKS.GMAIL)

    @route(path="/linkedin", response_model=fastapi.responses.RedirectResponse)
    async def linkedin(self, _: fastapi.Request) -> fastapi.responses.RedirectResponse:
        return fastapi.responses.RedirectResponse(LINKS.LINKEDIN)
