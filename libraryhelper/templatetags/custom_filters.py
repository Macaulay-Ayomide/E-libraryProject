from ..models import  Defaulters
from django import template
register = template.Library()


#custom filters
@register.filter()
def stars(value):
    value = Defaulters.objects.filter(matric = value).count()
    print(value)
    return value