from pathlib import Path
from typing import Any


def static_image_url(path: str, file: Any):
    static_path = Path(path)
    if not static_path.exists():
        static_path.mkdir(parents=True, exist_ok=True)

    img_url = static_path / file.filename

    return str(img_url)
