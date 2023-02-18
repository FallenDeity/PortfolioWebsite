import importlib
import inspect
import pathlib
import typing as t

import aiohttp
import fastapi
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routes import Extension
from utils.constants import DESCRIPTION, PATHS
from utils.mail import Mail

from .environment import config
from .logger import Logger

__author__: str = "Triyan Mukherjee"
__version__: str = "0.0.1"
__all__: tuple[str, ...] = ("Website",)


class Website(fastapi.FastAPI):
    client: aiohttp.ClientSession
    mail: Mail
    templates: Jinja2Templates = Jinja2Templates(directory=str(PATHS.TEMPLATES))
    _static: list[str] = [str(PATHS.STATIC), str(PATHS.ASSETS)]

    def __init__(
        self,
        *,
        title: str = __author__,
        description: str = DESCRIPTION,
        docs: str | None = None,
        debug: bool = False,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(
            title=title,
            description=description,
            on_startup=[self.on_startup],
            on_shutdown=[self.on_shutdown],
            docs_url=docs,
            redoc_url=docs,
            debug=debug,
            **kwargs,
        )
        self.logger = Logger(name=__name__)
        self.config = config

    def _mount_files(self) -> None:
        for path in self._static:
            tag = path.split("\\")[-1]
            self.routes.append(fastapi.routing.Mount(f"/{tag}", StaticFiles(directory=path), name=tag))
            self.logger.info(f"Mounted {tag} files")

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
        self.mail = Mail(website=self)
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
            "__main__:app",
            reload=True,
            reload_dirs=[str(PATHS.ROUTES), str(PATHS.TEMPLATES)],
            use_colors=True,
        )
