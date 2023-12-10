# app1/templatetags/custom_tags.py
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_stars(rating):
    stars = range(1, 6)
    html = ""
    if rating:
        for star in stars:
            if rating >= star:
                html += '<div><i class="icon-star text-10 text-yellow-2"></i></div>'
        return mark_safe(html)
    return mark_safe('<div><i class="icon-star text-10 text-yellow-2"></i></div><div><i class="icon-star text-10 text-yellow-2"></i></div><div><i class="icon-star text-10 text-yellow-2"></i></div><div><i class="icon-star text-10 text-yellow-2"></i></div>')
