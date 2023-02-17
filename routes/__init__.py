import functools
import inspect
import time
import typing as t

import attrs
import fastapi

if t.TYPE_CHECKING:
    from client import Website


__all__: tuple[str, ...] = (
    "Extension",
    "route",
)
T = t.TypeVar("T", bound=t.Callable[[fastapi.Request], t.Coroutine[t.Any, t.Any, fastapi.Response]])


@attrs.define(slots=True, frozen=True, kw_only=True)
class Route:
    path: str
    method: str
    response_class: t.Any
    name: str


class LoggedRoute(fastapi.routing.APIRoute):
    def get_route_handler(
        self,
    ) -> t.Callable[[fastapi.Request], t.Coroutine[t.Any, t.Any, fastapi.Response]]:
        original_route_handler = super().get_route_handler()

        @functools.wraps(original_route_handler)
        async def route_handler(request: fastapi.Request) -> fastapi.Response:
            ip = request.client.host if request.client else ""
            start_time = time.time()
            response = await original_route_handler(request)
            process_time = time.time() - start_time
            message = f"{ip} {request.method} {request.url} {response.status_code} {process_time:.2f}s"
            request.app.logger.info(message)
            return response

        return route_handler


class Extension(fastapi.APIRouter):
    def __init__(self, *, app: "Website", **kwargs: t.Any) -> None:
        self.app = app
        super().__init__(**kwargs, tags=[self.__class__.__name__], route_class=LoggedRoute)
        self._setup()

    def _setup(self) -> None:
        for name, obj in inspect.getmembers(self):
            if isinstance(_route := getattr(obj, "_route", None), Route):
                self.add_api_route(
                    _route.path,
                    obj,
                    name=_route.name,
                    methods=[_route.method],
                    response_class=_route.response_class,
                )
                self.app.logger.info(f"Loaded {name} route")


def route(
    path: str | None = None, *, method: str = "GET", response_class: t.Any = None
) -> t.Callable[..., t.Callable[[t.Any], t.Any]]:
    @functools.wraps(route)
    def wrapper(func: T) -> T:
        first_arg = inspect.signature(func).parameters.values().__iter__().__next__()
        if first_arg.name != "self":
            raise TypeError("Route must be a class method")
        path_ = path or f"/{func.__name__}"
        response_model = response_class or inspect.signature(func).return_annotation or fastapi.Response
        custom = Route(path=path_, method=method, response_class=response_model, name=func.__name__)
        setattr(func, "_route", custom)
        return func

    return wrapper  # type: ignore