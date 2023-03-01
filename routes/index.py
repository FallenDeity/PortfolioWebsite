from __future__ import annotations

import pathlib
import re

import aiofiles
import fastapi

from utils.cache import ExpiringEmailCache
from utils.constants import CERTIFICATES, DESCRIPTION, LINKS, PATHS, SKILLS, VIDEOS
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
            },
        )

    @route(path="/api/v1/screenshot", response_model=fastapi.responses.JSONResponse, method="POST")
    async def screenshot(self, url: dict[str, str]) -> fastapi.responses.JSONResponse:
        link = re.sub(r"(https?://)?(www\.)?", "", url["url"]).strip("/")
        link = re.sub(r"[^a-zA-Z0-9]", "_", link)
        headers = {"key": str(self.app.config.SITE_SHOT)}
        params = {"url": url["url"], "dimension": "1920x1080", "device": "desktop", "cache_limit": "7"}
        if pathlib.Path(f"{str(PATHS.SCREENSHOTS)}/{link}.jpg").exists():
            return fastapi.responses.JSONResponse({"status": "success", "url": f"/static/screenshots/{link}.jpg"})
        async with self.app.client.get("https://api.screenshotmachine.com", params=params | headers) as resp:
            if resp.status != 200:
                print(await resp.text())
                raise fastapi.exceptions.HTTPException(status_code=500, detail="Screenshot failed!")
            data = await resp.read()
            pathlib.Path(f"{str(PATHS.SCREENSHOTS)}").mkdir(parents=True, exist_ok=True)
            path = f"{str(PATHS.SCREENSHOTS)}/{link}.jpg"
            async with aiofiles.open(path, "wb") as f:
                await f.write(data)
        return fastapi.responses.JSONResponse({"status": "success", "url": f"/static/screenshots/{link}.jpg"})

    @route("/api/v1/feedback", method="POST", response_model=fastapi.responses.JSONResponse)
    async def feedback(self, data: Email) -> fastapi.responses.JSONResponse:
        if data.email in self._email_cache:
            raise fastapi.exceptions.HTTPException(status_code=429, detail="Too many requests!")
        self._email_cache[data.email] = (True, 3600.0)
        try:
            await self.app.async_run(send_email, data)
        except Exception as e:
            raise fastapi.exceptions.HTTPException(status_code=500, detail=str(e))
        return fastapi.responses.JSONResponse(
            {"status": "success", "message": "Feedback sent successfully!"}, status_code=200
        )

    @route(path="/contact", response_model=fastapi.responses.HTMLResponse)
    async def contact(self, request: fastapi.Request) -> fastapi.responses.Response:
        f_img = self.app.get_image("footers")
        return self.app.templates.TemplateResponse(
            "feedback-form.html",
            {
                "request": request,
                "title": "Feedback",
                "f_img": f_img,
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
