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
    "GITHUB_USERNAME",
    "BADGES",
    "CERTIFICATES",
)


@attrs.define
class Certificate:
    name: str
    image: str
    link: str


@attrs.define
class Badge:
    name: str
    image: str
    completion: float
    category: str
    color: str = "bg-blue-500"


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
                   """
GITHUB_USERNAME: str = "FallenDeity"


class PATHS(BaseEnum):
    UTILS = pathlib.Path(__file__).parent.parent / "utils"
    ROUTES = pathlib.Path(__file__).parent.parent / "routes"
    CLIENT = pathlib.Path(__file__).parent.parent / "client"
    STATIC = pathlib.Path(__file__).parent.parent / "templates" / "static"
    TEMPLATES = pathlib.Path(__file__).parent.parent / "templates"
    ASSETS = pathlib.Path(__file__).parent.parent / "templates" / "static" / "assets"
    SCREENSHOTS = pathlib.Path(__file__).parent.parent / "templates" / "static" / "assets" / "screenshots"

    def __str__(self) -> str:
        return str(self.value.as_posix())


class LINKS(str, BaseEnum):
    SOURCE = "https://github.com/FallenDeity/PersonalWebsite"
    GITHUB = "https://github.com/FallenDeity"
    DISCORD = "https://discord.com/users/656838010532265994"
    GMAIL = "mailto:triyanmukherjee@gmail.com"
    LINKEDIN = "https://www.linkedin.com/in/triyan-mukherjee-1a46b8247/"
    WEBSITE = "https://website-1-j7943388.deta.app/"


class BADGES:
    PYTHON = Badge(
        name="Python",
        image="static/assets/badges/Python.png",
        completion=0.9,
        category="Programming Languages",
        color="bg-yellow-500",
    )
    TYPESCRIPT = Badge(
        name="TypeScript",
        image="static/assets/badges/TypeScript.png",
        completion=0.9,
        category="Programming Languages",
    )
    MARKDOWN = Badge(
        name="Markdown",
        image="static/assets/badges/Markdown.png",
        completion=0.9,
        category="Programming Languages",
        color="bg-black",
    )
    JAVASCRIPT = Badge(
        name="JavaScript",
        image="static/assets/badges/JavaScript.png",
        completion=0.8,
        category="Programming Languages",
        color="bg-yellow-600",
    )
    HTML = Badge(
        name="HTML",
        image="static/assets/badges/HTML.png",
        completion=0.8,
        category="Programming Languages",
        color="bg-red-500",
    )
    CSS = Badge(
        name="CSS",
        image="static/assets/badges/CSS.png",
        completion=0.8,
        category="Programming Languages",
        color="bg-green-500",
    )
    C = Badge(
        name="C",
        image="static/assets/badges/C.png",
        completion=0.7,
        category="Programming Languages",
        color="bg-indigo-500",
    )
    C_PLUS_PLUS = Badge(
        name="C++",
        image="static/assets/badges/C++.png",
        completion=0.7,
        category="Programming Languages",
        color="bg-purple-500",
    )
    RUST = Badge(
        name="Rust",
        image="static/assets/badges/Rust.png",
        completion=0.7,
        category="Programming Languages",
        color="bg-red-700",
    )
    ArchLinux = Badge(
        name="Arch Linux",
        image="static/assets/badges/frameworks/ArchLinux.png",
        completion=0.0,
        category="Frameworks",
    )
    Arduino = Badge(
        name="Arduino",
        image="static/assets/badges/frameworks/Arduino.png",
        completion=0.0,
        category="Frameworks",
    )
    Bootstrap = Badge(
        name="Bootstrap",
        image="static/assets/badges/frameworks/Bootstrap.png",
        completion=0.0,
        category="Frameworks",
    )
    Debian = Badge(
        name="Debian",
        image="static/assets/badges/frameworks/Debian.png",
        completion=0.0,
        category="Frameworks",
    )
    FastApi = Badge(
        name="FastApi",
        image="static/assets/badges/frameworks/FastApi.png",
        completion=0.0,
        category="Frameworks",
    )
    Flask = Badge(
        name="Flask",
        image="static/assets/badges/frameworks/Flask.png",
        completion=0.0,
        category="Frameworks",
    )
    Flutter = Badge(
        name="Flutter",
        image="static/assets/badges/frameworks/Flutter.png",
        completion=0.0,
        category="Frameworks",
    )
    Git = Badge(
        name="Git",
        image="static/assets/badges/frameworks/Git.png",
        completion=0.0,
        category="Frameworks",
    )
    Jinja = Badge(
        name="Jinja",
        image="static/assets/badges/frameworks/Jinja.png",
        completion=0.0,
        category="Frameworks",
    )
    MongoDB = Badge(
        name="MongoDB",
        image="static/assets/badges/frameworks/MongoDB.png",
        completion=0.0,
        category="Frameworks",
    )
    MySql = Badge(
        name="My SQL",
        image="static/assets/badges/frameworks/MySql.png",
        completion=0.0,
        category="Frameworks",
    )
    Postgres = Badge(
        name="Postgres",
        image="static/assets/badges/frameworks/Postgres.png",
        completion=0.0,
        category="Frameworks",
    )
    ROS = Badge(
        name="ROS",
        image="static/assets/badges/frameworks/ROS.png",
        completion=0.0,
        category="Frameworks",
    )
    RPI = Badge(
        name="Raspberry Pi",
        image="static/assets/badges/frameworks/RPI.png",
        completion=0.0,
        category="Frameworks",
    )
    Tailwind = Badge(
        name="Tailwind CSS",
        image="static/assets/badges/frameworks/TailwindCSS.png",
        completion=0.0,
        category="Frameworks",
    )

    @classmethod
    def get_all(cls) -> dict[str, list[Badge]]:
        data: dict[str, list[Badge]] = {}
        for i in cls.__dict__.values():
            if isinstance(i, Badge):
                data.setdefault(i.category, []).append(i)
        return data


class CERTIFICATES(BaseEnum):
    INTRODUCTION_TO_SOFTWARE_ENGINEERING = Certificate(
        name="Introduction to Software Engineering",
        image="static/assets/certificates/IntroductionToSoftwareEngineering.jpeg",
        link="https://www.coursera.org/account/accomplishments/verify/7JMJCZ4Y939Y",
    )
    INTRODUCTION_TO_DATA_SCIENCE_IN_PYTHON = Certificate(
        name="Introduction to Data Science in Python",
        image="static/assets/certificates/IntroductionToDataScienceInPython.jpeg",
        link="https://www.coursera.org/account/accomplishments/verify/4NG522XGC23G",
    )
    INTRODUCTION_TO_HTML5 = Certificate(
        name="Introduction to HTML5",
        image="static/assets/certificates/IntroductionToHTML5.jpeg",
        link="https://www.coursera.org/account/accomplishments/verify/GHVFUFMTLZ6J",
    )
    CRASH_COURSE_ON_PYTHON = Certificate(
        name="Crash Course on Python",
        image="static/assets/certificates/CrashCourseOnPython.jpeg",
        link="https://www.coursera.org/account/accomplishments/verify/GGU5NFGFD8A4",
    )
    WHAT_IS_DATA_SCIENCE = Certificate(
        name="What is Data Science?",
        image="static/assets/certificates/WhatIsDataScience.jpeg",
        link="https://www.coursera.org/account/accomplishments/verify/NXWF8FYAMVW5",
    )
    FOUNDATIONS_OF_USER_EXPERIENCE_UX_DESIGN = Certificate(
        name="Foundations of User Experience (UX) Design",
        image="static/assets/certificates/FoundationsOfUserExperienceUxDesign.jpeg",
        link="https://www.coursera.org/account/accomplishments/verify/3HDQWUBMU46X",
    )
    PYTHON_FOR_DATA_SCIENCE_AI_DEVELOPMENT = Certificate(
        name="Python for Data Science, AI & Development",
        image="static/assets/certificates/PythonForDataScienceAiDevelopment.jpeg",
        link="https://www.coursera.org/account/accomplishments/verify/2ZVJS2GPGN65",
    )
    FOUNDATIONS_DATA_DATA_EVERYWHERE = Certificate(
        name="Foundations: Data, Data, Everywhere",
        image="static/assets/certificates/FoundationsDataDataEverywhere.jpeg",
        link="https://www.coursera.org/account/accomplishments/verify/LJBUCJYCPXHJ",
    )
    PROGRAMMING_FOR_EVERYBODY_GETTING_STARTED_WITH_PYTHON = Certificate(
        name="Programming for Everybody (Getting Started with Python)",
        image="static/assets/certificates/ProgrammingForEverybodyGettingStartedWithPython.jpeg",
        link="https://www.coursera.org/account/accomplishments/verify/V4FEKD8UJHAZ",
    )
    TOOLS_FOR_DATA_SCIENCE = Certificate(
        name="Tools for Data Science",
        image="static/assets/certificates/ToolsForDataScience.jpeg",
        link="https://www.coursera.org/account/accomplishments/verify/H58JA5XG4GAT",
    )

    @classmethod
    def get_random(cls, n: int = 5) -> list[Certificate]:
        return [i.value for i in random.sample(list(cls), n)]
