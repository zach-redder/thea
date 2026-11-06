from typing import NoReturn

from fastapi import HTTPException, status


def not_implemented(feature: str) -> NoReturn:
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, f"{feature} is not implemented yet -- see docs/roadmap.md")
