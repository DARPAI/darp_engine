import functools
import inspect
import sys
import traceback
from collections.abc import Awaitable
from collections.abc import Callable
from collections.abc import Coroutine
from typing import Any
from typing import overload
from typing import ParamSpec
from typing import TypeVar

from mcp_server.src.logger import logger

X = TypeVar("X")
P = ParamSpec("P")


@overload
def log_errors(  # noqa
    func: Callable[P, Coroutine[Any, Any, X]]
) -> Callable[P, Coroutine[Any, Any, X]]: ...


@overload
def log_errors(func: Callable[P, X]) -> Callable[P, X]: ...  # noqa


def log_errors(func: Callable[P, Any]) -> Callable[P, Any]:

    def log_error(args: tuple, kwargs: dict) -> None:
        info = sys.exc_info()[2]
        assert (
            info is not None and info.tb_next is not None
        ), f"No traceback available {sys.exc_info()[2]=}"
        locals_vars = info.tb_frame.f_locals
        logger.error(f"{traceback.format_exc()} \n{locals_vars=} \n{args=} \n{kwargs=}")

    @functools.wraps(func)
    def sync_wrapped(*args: P.args, **kwargs: P.kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception:
            log_error(args, kwargs)
            raise

    @functools.wraps(func)
    async def async_wrapped(*args: P.args, **kwargs: P.kwargs) -> Awaitable[Any]:
        try:
            return await func(*args, **kwargs)
        except Exception:
            log_error(args, kwargs)
            raise

    if inspect.iscoroutinefunction(func):
        return async_wrapped

    return sync_wrapped
