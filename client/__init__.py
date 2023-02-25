from __future__ import annotations

import asyncio
import importlib
import inspect
import pathlib
import random
import typing as t
from functools import partial

import aiohttp
import fastapi
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException

from routes import Extension
from utils.constants import DESCRIPTION, PATHS

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
        self.exception_handler(HTTPException)(self._exception_handler)

    @staticmethod
    async def async_run(func: t.Callable[..., t.Any], *args: t.Any, **kwargs: t.Any) -> t.Any:
        return await asyncio.get_running_loop().run_in_executor(None, partial(func, *args, **kwargs))

    @staticmethod
    def get_image(path: str, format_: str = "jpg") -> str:
        images = [i.as_posix().split("/static")[-1] for i in (PATHS.ASSETS / path).glob(f"*.{format_}")]
        return random.choice(images)

    async def _exception_handler(self, request: fastapi.Request, _exc: HTTPException) -> fastapi.responses.Response:
        f_img = self.get_image("footers")
        self.logger.error(f"Error: {_exc.detail}")
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
