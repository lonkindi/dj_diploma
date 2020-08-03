from django import template

register = template.Library()


@register.filter
def get_stars(Value):
    stars = ''
    for i in range(Value):
        stars += "★"
    return stars
