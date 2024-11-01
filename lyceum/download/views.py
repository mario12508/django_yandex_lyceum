import mimetypes
from pathlib import Path
from urllib.parse import unquote

from django.conf import settings
from django.http import FileResponse, Http404


def download_image(request, file_path):
    file_path = unquote(file_path)
    absolute_path = Path(settings.MEDIA_ROOT) / file_path

    if not absolute_path.exists():
        raise Http404("Файл не найден")

    content_type, _ = mimetypes.guess_type(str(absolute_path))
    content_type = content_type or "application/octet-stream"

    response = FileResponse(
        open(absolute_path, "rb"),
        as_attachment=True,
        content_type=content_type,
    )
    response["Content-Disposition"] = (
        f'attachment; filename="{absolute_path.name}"'
    )
    return response


__all__ = ["download_image"]
