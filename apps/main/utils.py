# разпределить правильный путь для сохранение картинок
def category_image_path(instance, filename):
    extension = filename.strip(".")[-1]
    return f"categories/{instance.slug}.{extension}"