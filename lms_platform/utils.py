import shutil
from pathlib import Path
from typing import Any


def build_image_url(path: str, file: Any) -> str:
    """
        Build image url from static files
    """
    static_path = Path(path)
    if not static_path.exists():
        static_path.mkdir(parents=True, exist_ok=True)

    img_url = static_path / file.filename

    return str(img_url)


def copy_fileobj(image: Any, file: Any):
    """
        Write image into Pydantic model
    """
    with open(image, 'wb+') as file_obj:
        shutil.copyfileobj(file, file_obj)
