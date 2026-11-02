from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/hotels")
async def get_hotels_page(
    request: Request
):
    return templates.TemplateResponse(request, "hotels.html",)