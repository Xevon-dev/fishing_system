from PIL import Image, UnidentifiedImageError


def image_upload_error(uploaded_file):
    if not uploaded_file:
        return ""
    try:
        with Image.open(uploaded_file) as image:
            image.verify()
        uploaded_file.seek(0)
    except (UnidentifiedImageError, OSError, ValueError):
        return "Не вдалося прочитати файл як зображення."
    return ""
