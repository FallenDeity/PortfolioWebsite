from __future__ import annotations

import fastapi

from utils.constants import LINKS

from . import Extension, route


class Profile(Extension):
    @route(path="/profile", response_model=fastapi.responses.HTMLResponse, method="GET")
    async def profile(self, request: fastapi.Request) -> fastapi.responses.Response:
        f_img, a_img = self.app.get_image("footers"), self.app.get_image("avatars", "png")
        return self.app.templates.TemplateResponse(
            "profile.html",
            {
                "request": request,
                "title": "Profile",
                "web": LINKS.WEBSITE,
                "f_img": f_img,
                "a_img": a_img,
            },
        )
