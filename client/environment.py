import os
import typing as t

import attrs
from dotenv import load_dotenv

__all__: tuple[str, ...] = ("config",)
load_dotenv()
MISSING = object()


@attrs.define(kw_only=True, slots=True)
class EnvironmentVariable:
    name: str
    default: t.Any = MISSING
    cast: type = str
    required: bool = True

    def __attrs_post_init__(self) -> None:
        self.default = os.getenv(self.name, self.default)
        if self.required and self.default is MISSING:
            raise ValueError(f"Missing required environment variable {self.name}")
        try:
            self.default = self.cast(self.default)
        except Exception as e:
            raise ValueError(f"Failed to cast {self.name} to {self.cast.__name__}") from e

    def __str__(self) -> str:
        return self.default if isinstance(self.default, str) else str(super())


class ENVIRONMENT:
    _instance: t.Optional["ENVIRONMENT"] = None

    def __new__(cls, *args: t.Any, **kwargs: t.Any) -> "ENVIRONMENT":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


config = ENVIRONMENT()
