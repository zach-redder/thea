from importlib.metadata import version

from fastapi import APIRouter

from thea_agent.api.v1.schemas import DependencyStatus, DetailedHealthResponse, HealthResponse

router = APIRouter(tags=["health"])
SERVICE = "thea-agent"


@router.get("/health")
async def health() -> HealthResponse:
    """Liveness: unauthenticated, so Docker/compose and uptime checks can call it."""
    return HealthResponse(service=SERVICE, version=version(SERVICE))


@router.get("/health/detailed")
async def health_detailed() -> DetailedHealthResponse:
    """Readiness per dependency. Real probes for Postgres, Redis, voice and home come with the runtime."""
    deps = [DependencyStatus(name=name, ok=False, detail="probe not implemented") for name in ("postgres", "redis")]
    return DetailedHealthResponse(service=SERVICE, version=version(SERVICE), dependencies=deps)
