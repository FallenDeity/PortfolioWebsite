from __future__ import annotations

import asyncio
import base64
import importlib
import inspect
import pathlib
import random
import re
import traceback
import typing as t
from functools import partial

import aiohttp
import fastapi
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from github import Github
from starlette.exceptions import HTTPException

from routes import Extension
from utils.cache import async_cache
from utils.constants import DESCRIPTION, LINKS, PATHS

from .environment import config
from .logger import Logger

__author__: str = "Triyan Mukherjee"
__version__: str = "0.0.1"
__all__: tuple[str, ...] = ("Website",)


class Website(fastapi.FastAPI):
    client: aiohttp.ClientSession
    templates: Jinja2Templates = Jinja2Templates(directory=str(PATHS.TEMPLATES))
    _static: list[fastapi.routing.Mount] = [
        fastapi.routing.Mount("/static", StaticFiles(directory=str(PATHS.STATIC), html=True), name="static"),
        fastapi.routing.Mount("/assets", StaticFiles(directory=str(PATHS.ASSETS), html=True), name="assets"),
    ]

    def __init__(
        self,
        *,
        title: str = __author__,
        description: str = DESCRIPTION,
        docs: str | None = None,
        redoc: str | None = None,
        debug: bool = False,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(
            title=title,
            description=description,
            on_startup=[self.on_startup],
            on_shutdown=[self.on_shutdown],
            docs_url=docs,
            redoc_url=redoc,
            debug=debug,
            **kwargs,
        )
        self.logger = Logger(name=__name__, file=False)
        self.config = config
        self.github = Github(str(self.config.GITHUB_TOKEN))
        self.exception_handler(HTTPException)(self._exception_handler)

    @staticmethod
    @async_cache()
    async def async_run(func: t.Callable[..., t.Any], *args: t.Any, **kwargs: t.Any) -> t.Any:
        return await asyncio.get_running_loop().run_in_executor(None, partial(func, *args, **kwargs))

    @staticmethod
    def get_image(path: str, format_: str = "jpg") -> str:
        images = [i.as_posix().split("/static")[-1] for i in (PATHS.ASSETS / path).glob(f"*.{format_}")]
        return random.choice(images)

    async def _exception_handler(self, request: fastapi.Request, _exc: HTTPException) -> fastapi.responses.Response:
        f_img = self.get_image("footers")
        error_traceback = traceback.format_exc()
        self.logger.error(error_traceback)
        return self.templates.TemplateResponse("error.html", {"request": request, "name": "Error", "f_img": f_img})

    def _mount_files(self) -> None:
        self.logger.info("Mounting files")
        self.routes.extend(self._static)
        self.logger.info("Files mounted")

    def _auto_setup(self, path: str) -> None:
        module = importlib.import_module(path)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Extension) and name != "Extension":
                router = obj(app=self)
                self.include_router(router)
                self.logger.info(f"Loaded {name} extension")

    def _load_files(self) -> None:
        self.logger.info("Loading extensions")
        for file in t.cast(pathlib.Path, PATHS.ROUTES).glob("*.py"):
            if file.name.startswith("_"):
                continue
            self._auto_setup(f"{PATHS.ROUTES.name}.{file.stem}")
        self.logger.info("Extensions loaded")

    async def get_meta_image(self, url: str) -> str:
        link = re.sub(r"(https?://)?(www\.)?", "", url).strip("/")
        link = re.sub(r"[^a-zA-Z0-9]", "_", link)
        key = base64.b64encode(f"{str(self.config.IMAGE_KIT)}:".encode()).decode("utf-8")
        headers, headers_img = {"key": str(self.config.SITE_SHOT)}, {"Authorization": f"Basic {key}"}
        search = {"name": f"{link}.jpg"}
        async with self.client.get("https://api.imagekit.io/v1/files", params=search, headers=headers_img) as resp:
            data = await resp.json()
            if not data or resp.status != 200:
                self.logger.error(f"Screenshot failed with {await resp.read()}")
                pass
            else:
                self.logger.info(f"Found {data[0]} in imagekit.io")
                return data[0]["url"]
        params = {"url": url, "dimension": "1400x900", "device": "desktop", "cacheLimit": "0"}
        params = params | {"delay": "1000"} if "blog" in url else params
        async with self.client.get("https://api.screenshotmachine.com", params=params | headers) as resp:
            if resp.status != 200:
                self.logger.error(f"Screenshot failed with {await resp.read()}")
                return LINKS.DEFAULT
            data = await resp.read()
            r_data = {"file": data, "fileName": f"{link}.jpg", "useUniqueFileName": "false"}
            async with self.client.post(
                "https://upload.imagekit.io/api/v1/files/upload", headers=headers_img, data=r_data
            ) as info:
                if info.status != 200:
                    self.logger.error(f"Screenshot failed with {await info.read()}")
                    return LINKS.DEFAULT
                file = await info.json()
                self.logger.info(f"Uploaded {file} to imagekit.io")
        return file["url"]

    async def on_startup(self) -> None:
        self.logger.info("Starting up...")
        self.client = aiohttp.ClientSession()
        self._mount_files()
        self._load_files()
        self.logger.flair("Started up successfully.")

    async def on_shutdown(self) -> None:
        self.logger.flair("Shutting down...")
        await self.client.close()
        self.logger.error("Shut down successfully.")

    def run(self) -> None:
        self.logger.flair("Running...")
        uvicorn.run(
            "main:app",
            reload=True,
            reload_dirs=[str(PATHS.ROUTES), str(PATHS.TEMPLATES)],
            use_colors=True,
        )
