from __future__ import annotations

import time
import typing


__all__: tuple[str, ...] = (
    "ExpiringCache",
    "ExpiringEmailCache",
)


KT = typing.TypeVar("KT", bound=str)
VT = typing.TypeVar("VT", bound=tuple[typing.Any, float])


class ExpiringCache(dict[KT, VT]):
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


class ExpiringEmailCache(ExpiringCache[str, str]):
    ...
