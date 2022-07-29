from fastapi import APIRouter

from app.settings import settings

router = APIRouter()


@router.get('/status')
async def status():
    return {
        'status': 'OK'
    }


@router.get('/status/version')
async def status_version():
    return {
        'version': settings.ci_commit_id,
        'branch': settings.ci_branch
    }
