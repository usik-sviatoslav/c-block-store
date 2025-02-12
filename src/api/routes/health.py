from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def healthcheck(request: Request) -> dict[str, str]:  # noqa: F841
    return {"status": "ok"}
