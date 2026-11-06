"""Read-only life stats for the dashboard, plus habit check-offs. Design: docs/stats-and-dashboard.md."""

from fastapi import APIRouter

from thea_agent.api.v1._not_implemented import not_implemented
from thea_agent.api.v1.schemas import HabitLogRequest, ListRequest

router = APIRouter(tags=["stats"])


@router.get("/today")
async def today() -> None:
    """Agenda, habits due, overnight changes, and THEA's one-line read of the day."""
    not_implemented("today")


@router.get("/stats/summary")
async def stats_summary(range: str = "7d") -> None:
    not_implemented("stats summary")


@router.get("/stats/series")
async def stats_series(area: str, range: str = "30d") -> None:
    """Time series for one area (sleep, steps, commits, ...) for a chart."""
    not_implemented("stats series")


@router.post("/habits/list")
async def list_habits(request: ListRequest) -> None:
    not_implemented("habit listing")


@router.post("/habits/log")
async def log_habit(request: HabitLogRequest) -> None:
    not_implemented("habit logging")


@router.post("/life/list")
async def list_life_log(request: ListRequest) -> None:
    """The documentation of life: a searchable timeline of events and memories."""
    not_implemented("life log")
