from __future__ import annotations

import enum
import pathlib
import random
import typing

import attrs

__all__: tuple[str, ...] = (
    "DESCRIPTION",
    "PATHS",
    "LINKS",
    "SKILLS",
    "VIDEOS",
)


@attrs.define
class Skill:
    name: str
    image: str


@attrs.define
class Video:
    title: str
    link: str
    description: str


class BaseEnum(enum.Enum):
    def __get__(self, instance: typing.Any, owner: typing.Any) -> typing.Any:
        return self.value


class SKILLS(BaseEnum):
    SOFTWARE_DEVELOPER = Skill("Software Developer", "https://i.imgur.com/9uHEMCX.jpg")
    ANIME_FAN = Skill("Anime Fan", "https://i.pinimg.com/736x/d4/5d/96/d45d966f6454fbc0151b8677cc4f7240.jpg")
    ROBOTICS = Skill("Robotics Enthusiast", "https://i.pinimg.com/564x/07/41/c5/0741c529edcc6105357f9b81d3e5c629.jpg")
    READING = Skill("Reading Novels", "https://i.pinimg.com/564x/f1/52/ae/f152ae10c08a43ca37beb24722b6f610.jpg")

    @classmethod
    def get_lucky_4(cls) -> list[Skill]:
        return [i.value for i in random.sample(list(cls), 4)]


class VIDEOS(BaseEnum):
    POKELORE = Video(
        title="PokéLore",
        link="https://www.youtube.com/embed/EMDFVsgAr0c",
        description="A new generation of Pokémon Bot.",
    )
    POKEMON = Video(
        title="Pokémon",
        link="https://www.youtube.com/embed/EMDFVsgAr0c",
        description="A new generation of Pokémon Bot.",
    )
    APPLE = Video(
        title="Apple", link="https://www.youtube.com/embed/EMDFVsgAr0c", description="A new generation of Pokémon Bot."
    )
    GOOGLE = Video(
        title="Google", link="https://www.youtube.com/embed/EMDFVsgAr0c", description="A new generation of Pokémon Bot."
    )

    @classmethod
    def get_as_list(cls) -> list[Video]:
        return [i.value for i in cls]


DESCRIPTION: str = """
                   Welcome to my personal website!
                   My name is Triyan Mukherjee and I am a 17 year old student from India.
                   Here, you'll find a collection of my academic work, personal projects, and a little bit about me.
                   I'm passionate about software development and almost anything tech related.
                   My hobbies include reading novels, anime and coding.
                   I'm always looking for new ways to challenge myself and learn something new.
                   Thank you for visiting and feel free to explore my website to learn more about me!
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
    WEBSITE = "https://website-1-j7943388.deta.app/"
