from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.settings import settings

router = APIRouter()
templates = Jinja2Templates(directory=Path(settings.root_dir, 'templates'))


@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    """
    Display the input field and submit button
    :param request: N/A
    :return: Renders a page
    """
    return templates.TemplateResponse('index.html', {'request': request})
