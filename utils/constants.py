import enum
import pathlib
import typing

__all__: tuple[str, ...] = (
    "DESCRIPTION",
    "PATHS",
    "LINKS",
)


class BaseEnum(enum.Enum):
    def __get__(self, instance: typing.Any, owner: typing.Any) -> typing.Any:
        return self.value


DESCRIPTION: str = """
                   A personal website for Triyan Mukherjee.
                   """


class PATHS(BaseEnum):
    UTILS = pathlib.Path(__file__).parent.parent / "utils"
    ROUTES = pathlib.Path(__file__).parent.parent / "routes"
    CLIENT = pathlib.Path(__file__).parent.parent / "client"
    STATIC = pathlib.Path(__file__).parent.parent / "templates" / "static"
    TEMPLATES = pathlib.Path(__file__).parent.parent / "templates"
    ASSETS = pathlib.Path(__file__).parent.parent / "templates" / "static" / "assets"

    def __str__(self) -> str:
        return str(self.value.as_posix())


class LINKS(str, BaseEnum):
    SOURCE = "https://github.com/FallenDeity/PersonalWebsite"
    GITHUB = "https://github.com/FallenDeity"
    DISCORD = "https://discord.com/users/656838010532265994"
    GMAIL = "mailto:triyanmukherjee@gmail.com"
    LINKEDIN = "https://www.linkedin.com/in/triyan-mukherjee-1a46b8247/"
