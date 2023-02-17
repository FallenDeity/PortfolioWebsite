import random
import time

import fastapi
from humanfriendly import format_timespan

from utils.cache import ExpiringFeedbackCache
from utils.constants import LINKS, PATHS
from utils.models import User

from . import Extension, route


class Home(Extension):
    feedback_cache = ExpiringFeedbackCache(seconds=3600)

    @route(path="/", response_class=fastapi.responses.HTMLResponse)
    async def home(self, request: fastapi.Request) -> fastapi.responses.Response:
        footer_images = [
            i.as_posix().split("/static")[-1] for i in (PATHS.ASSETS / "footers").glob("*.jpg")  # type: ignore
        ]
        f_img = random.choice(footer_images)
        return self.app.templates.TemplateResponse("index.html", {"request": request, "title": "Home", "f_img": f_img})

    @route(path="/source", response_class=fastapi.responses.RedirectResponse)
    async def source(self, _: fastapi.Request) -> fastapi.responses.RedirectResponse:
        return fastapi.responses.RedirectResponse(LINKS.SOURCE)

    @route(path="/api/v1/feedback", method="POST")
    async def feedback(self, feedback: dict[str, str]) -> fastapi.responses.JSONResponse:
        if (ip := feedback.get("ip", "")) in self.feedback_cache:
            left = format_timespan(3600 - (time.time() - self.feedback_cache[ip].time))
            return fastapi.responses.JSONResponse(
                {"message": f"Please wait {left} seconds before sending another " f"feedback."},
                status_code=429,
            )
        if not (message := feedback.get("feedback")):
            return fastapi.responses.JSONResponse({"message": "Please provide a message."}, status_code=400)
        self.feedback_cache[ip] = (User(ip=ip, time=time.time(), feedback=message),)
        return fastapi.responses.JSONResponse({"message": "Feedback sent!"}, status_code=200)

    @route(path="/github", response_class=fastapi.responses.RedirectResponse)
    async def github(self, _: fastapi.Request) -> fastapi.responses.RedirectResponse:
        return fastapi.responses.RedirectResponse(LINKS.GITHUB)

    @route(path="/discord", response_class=fastapi.responses.RedirectResponse)
    async def discord(self, _: fastapi.Request) -> fastapi.responses.RedirectResponse:
        return fastapi.responses.RedirectResponse(LINKS.DISCORD)

    @route(path="/email", response_class=fastapi.responses.RedirectResponse)
    async def twitter(self, _: fastapi.Request) -> fastapi.responses.RedirectResponse:
        return fastapi.responses.RedirectResponse(LINKS.GMAIL)

    @route(path="/linkedin", response_class=fastapi.responses.RedirectResponse)
    async def linkedin(self, _: fastapi.Request) -> fastapi.responses.RedirectResponse:
        return fastapi.responses.RedirectResponse(LINKS.LINKEDIN)
