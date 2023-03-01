from __future__ import annotations

import base64
import re
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
            },
        )

    @route(path="/api/v1/screenshot", response_model=fastapi.responses.JSONResponse, method="POST")
    async def screenshot(self, url: typing.Dict[str, str]) -> fastapi.responses.JSONResponse:
        link = re.sub(r"(https?://)?(www\.)?", "", url.get("url", "https://website-1-j7943388.deta.app/")).strip("/")
        link = re.sub(r"[^a-zA-Z0-9]", "_", link)
        key = base64.b64encode(f"{str(self.app.config.IMAGE_KIT)}:".encode()).decode("utf-8")
        headers, headers_img = {"key": str(self.app.config.SITE_SHOT)}, {"Authorization": f"Basic {key}"}
        search = {"name": f"{link}.jpg"}
        async with self.app.client.get("https://api.imagekit.io/v1/files", params=search, headers=headers_img) as resp:
            data = await resp.json()
            if not data or resp.status != 200:
                self.app.logger.error(f"Screenshot failed with {await resp.read()}")
                pass
            else:
                self.app.logger.info(f"Found {data[0]} in imagekit.io")
                return fastapi.responses.JSONResponse({"status": "success", "url": f"{data[0]['url']}"})
        params = {"url": url["url"], "dimension": "1400x900", "device": "desktop"}
        async with self.app.client.get("https://api.screenshotmachine.com", params=params | headers) as resp:
            if resp.status != 200:
                self.app.logger.error(f"Screenshot failed with {await resp.read()}")
                raise fastapi.exceptions.HTTPException(status_code=500, detail="Screenshot failed!")
            data = await resp.read()
            r_data = {"file": data, "fileName": f"{link}.jpg", "useUniqueFileName": "false"}
            async with self.app.client.post(
                "https://upload.imagekit.io/api/v1/files/upload", headers=headers_img, data=r_data
            ) as info:
                if info.status != 200:
                    self.app.logger.error(f"Screenshot failed with {await info.read()}")
                    raise fastapi.exceptions.HTTPException(status_code=500, detail="Screenshot failed!")
                file = await info.json()
                self.app.logger.info(f"Uploaded {file} to imagekit.io")
        return fastapi.responses.JSONResponse({"status": "success", "url": f"{file['url']}"})

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
