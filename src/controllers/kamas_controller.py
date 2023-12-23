import datetime

from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from src.models.kamas_model import Kamas, Kamas_Pydantic

router = APIRouter()


@router.post("/kamas", responses={404: {"model": HTTPNotFoundError}})
async def create_kamas_value(message: Kamas_Pydantic):
    await Kamas.create(**message.dict(exclude_unset=True))


@router.get("/today", responses={404: {"model": HTTPNotFoundError}})
async def get_today_kamas(server: str):
    today_start = datetime.datetime.now(datetime.timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    today_end = today_start + datetime.timedelta(days=1)
    return (
        await Kamas.filter(
            timestamp__gte=today_start, timestamp__lt=today_end, server=server
        )
        .order_by("-timestamp")
        .first()
    )


@router.get("/yesterday", responses={404: {"model": HTTPNotFoundError}})
async def get_yesterday_kamas(server: str):
    today_start = datetime.datetime.now(datetime.timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    yesterday_start = today_start - datetime.timedelta(days=1)
    return (
        await Kamas.filter(
            timestamp__gte=yesterday_start, timestamp__lt=today_start, server=server
        )
        .order_by("-timestamp")
        .first()
    )


@router.get("/kamas", responses={404: {"model": HTTPNotFoundError}})
async def get_kamas(server: str, scope: str):
    today_start = datetime.datetime.now(datetime.timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    if scope == "day":
        today_end = today_start + datetime.timedelta(days=1)
        return await Kamas.filter(
            timestamp__gte=today_start, timestamp__lt=today_end, server=server
        ).order_by("timestamp")
    elif scope == "week":
        week_start = today_start - datetime.timedelta(days=today_start.weekday())
        week_end = week_start + datetime.timedelta(days=7)
        return await Kamas.filter(
            timestamp__gte=week_start, timestamp__lt=week_end, server=server
        ).order_by("timestamp")
    else:
        month_start = today_start.replace(day=1)
        month_end = month_start + datetime.timedelta(days=32)
        return await Kamas.filter(
            timestamp__gte=month_start, timestamp__lt=month_end, server=server
        ).order_by("timestamp")
