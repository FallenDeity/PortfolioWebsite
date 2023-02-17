import typing

import nox

T = typing.TypeVar("T", bound=typing.Callable[..., None])


def with_poetry(work_flow: str) -> typing.Callable[[T], T]:
    def decorator(func: T) -> T:
        @nox.session(name=func.__name__)
        def wrapper(session: nox.Session) -> None:
            session.install("poetry")
            session.run("poetry", "install", external=True, silent=True)
            session.log(f"Running {work_flow}...")
            func(session, "poetry", "run", work_flow)
            session.log(f"Finished {work_flow}.")

        return typing.cast(T, wrapper)

    return decorator


@with_poetry("black")
def black(session: nox.Session, *args: str) -> None:
    session.run(*args, ".")


@with_poetry("isort")
def isort(session: nox.Session, *args: str) -> None:
    session.run(*args, ".")


@with_poetry("ruff")
def ruff(session: nox.Session, *args: str) -> None:
    session.run(*args, ".")


@with_poetry("pyright")
def pyright(session: nox.Session, *args: str) -> None:
    session.run(*args, ".")
