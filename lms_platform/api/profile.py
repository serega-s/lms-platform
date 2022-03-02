import shutil
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Body, Depends, File, UploadFile

from ..models.auth import User
from ..models.profile import Profile, ProfileCreate
from ..service.auth import get_current_user
from ..service.profile import ProfileService

router = APIRouter(
    prefix='/profiles',
    tags=['profiles']
)


@router.post('/', response_model=Profile)
def create_profile(
    full_name: str,
    bio: str,
    phone_number: str,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    service: ProfileService = Depends(),
):
    static_path = Path(f'static/{user.id}/profile/{full_name}/').absolute()
    if not static_path.exists():
        static_path.mkdir(parents=True, exist_ok=True)

    img_url = static_path / file.filename

    profile_obj = {
        'full_name': full_name,
        'bio': bio,
        'phone_number': phone_number,
        'url': str(img_url)
    }

    profile_data = ProfileCreate.parse_obj(profile_obj)

    return service.create_profile(user.id, profile_data, file.file)


@router.patch('/')
def edit_profile():
    ...