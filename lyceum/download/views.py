import mimetypes
import os
from urllib.parse import unquote

from django.conf import settings
from django.http import FileResponse, Http404


def download_image(request, file_path):
    file_path = unquote(file_path)
    absolute_path = os.path.join(settings.MEDIA_ROOT, str(file_path))

    if not os.path.exists(absolute_path):
        raise Http404("Файл не найден")

    content_type, _ = mimetypes.guess_type(absolute_path)
    content_type = content_type or "application/octet-stream"

    response = FileResponse(
        open(absolute_path, "rb"),
        as_attachment=True,
        content_type=content_type,
    )
    response["Content-Disposition"] = (
        f'attachment; filename="{os.path.basename(file_path)}"'
    )
    return response
