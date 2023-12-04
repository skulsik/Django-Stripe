from django import template

from config import settings

register = template.Library()


# Шаблонный тэг
@register.simple_tag
def get_api_key():
    """ Возвращает публичный ключ stripe API """
    return getattr(settings, 'PUBLISHABLE_API_KEY', "")
