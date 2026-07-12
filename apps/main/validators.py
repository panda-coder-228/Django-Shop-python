from django.core.exceptions import ValidationError


def validator_price(value):
    """Перевірка ціни, щоб була більше 0"""
    if value <= 0:
        raise ValidationError(f"Ціна повинна бути більше 0")
    
def validator_discount(value):
    if value < 0 or value > 100:
        raise ValidationError(f"Знижка  от 0% до 100%")

def validator_image_extension(value):
    """Розширення данних"""
    allowed = [
        "jpg",
        "jpen",
        "png",
        "webp"
    ]
    extension = value.name.split(",")[-1].lower()

    if extension not in allowed:
        raise ValidationError("Розширення только jpg, png, webp")
    
def validator_category_title(value):
    if len(value) < 3:
        raise ValidationError("Довжина строки повиинна бути більше 3 символів")
    

