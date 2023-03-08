from __future__ import annotations

import typing

import fastapi

from utils.cache import ExpiringEmailCache
from utils.constants import CERTIFICATES, DESCRIPTION, LINKS, SKILLS, VIDEOS
from utils.mail import send_email
from utils.models import Email

from . import Extension, route


class Home(Extension):
    _email_cache: ExpiringEmailCache = ExpiringEmailCache(seconds=3600)

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
                "certs": CERTIFICATES.get_random(),
                "image": await self.app.get_meta_image(str(request.url)),
            },
        )

    @route(path="/api/v1/screenshot", response_model=fastapi.responses.JSONResponse, method="POST")
    async def screenshot(self, url: typing.Dict[str, str]) -> fastapi.responses.JSONResponse:
        link = url.get("url", "https://website-1-j7943388.deta.app/")
        return fastapi.responses.JSONResponse({"status": "success", "url": self.app.get_meta_image(link)})

    @route("/api/v1/feedback", method="POST", response_model=fastapi.responses.JSONResponse)
    async def feedback(self, data: Email) -> fastapi.responses.JSONResponse:
        if data.email in self._email_cache:
            raise fastapi.exceptions.HTTPException(status_code=429, detail="Too many requests!")
        self._email_cache[data.email] = (True, 3600.0)
        try:
            await self.app.async_run(send_email, self.app.config, data)
            self.app.logger.info(f"Feedback sent from {data.email}")
        except Exception as e:
            raise fastapi.exceptions.HTTPException(status_code=500, detail=str(e))
        return fastapi.responses.JSONResponse(
            {"status": "success", "message": "Feedback sent successfully!"}, status_code=200
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
