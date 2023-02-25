from __future__ import annotations

import typing
from abc import ABC

import attrs
from pydantic import BaseModel

__all__: tuple[str, ...] = (
    "Model",
    "User",
    "Email",
)


@attrs.define
class Model(ABC):
    """Base class for all models."""

    def to_payload(self) -> dict[typing.Any, typing.Any]:
        """Convert the model to a payload."""
        return attrs.asdict(self)


@attrs.define
class User(Model):
    ip: str
    time: float
    feedback: str


class Email(BaseModel):
    email: str
    message: str
    subject: str = "Feedback"
