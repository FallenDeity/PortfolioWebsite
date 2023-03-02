from __future__ import annotations

import asyncio
import time
import typing

__all__: tuple[str, ...] = (
    "ExpiringCache",
    "ExpiringEmailCache",
    "async_cache",
)


KT = typing.TypeVar("KT", bound=str)
VT = typing.TypeVar("VT", bound=tuple[typing.Any, float])
ASYNC_CACHE: typing.Dict[tuple[typing.Any, ...], typing.FrozenSet[typing.Any]] = {}


async def clean_cache() -> None:
    while True:
        await asyncio.sleep(3600)
        ASYNC_CACHE.clear()


def async_cache() -> typing.Callable[[typing.Callable[..., typing.Any]], typing.Callable[..., typing.Any]]:
    def decorator(func: typing.Callable[..., typing.Any]) -> typing.Callable[..., typing.Any]:
        async def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            key = (args, frozenset(kwargs.items()))
            if key in ASYNC_CACHE:
                return ASYNC_CACHE[key]
            if not ASYNC_CACHE:
                tasks = asyncio.all_tasks()
                for task in tasks:
                    if task.get_name() == "clean_cache":
                        break
                asyncio.create_task(clean_cache(), name="clean_cache")
            result = await func(*args, **kwargs)
            ASYNC_CACHE[key] = result
            return result

        return wrapper

    return decorator


class ExpiringCache(typing.Dict[KT, VT]):
    def __init__(self, seconds: float) -> None:
        self.__ttl: float = seconds
        super().__init__()

    def __verify_cache_integrity(self) -> None:
        current_time = time.monotonic()
        to_remove = [k for (k, (_, j)) in self.items() if current_time > (j + self.__ttl)]
        for k in to_remove:
            del self[k]

    def __contains__(self, key: str) -> bool:  # type: ignore
        self.__verify_cache_integrity()
        return super().__contains__(key)

    def __getitem__(self, key: str) -> typing.Any:
        self.__verify_cache_integrity()
        return super().__getitem__(key)[0]  # type: ignore

    def __setitem__(self, key: KT, value: typing.Sequence[typing.Any]) -> None:
        super().__setitem__(key, (value[0], time.monotonic()))  # type: ignore


class ExpiringEmailCache(ExpiringCache[str, typing.Tuple[str, float]]):
    ...
