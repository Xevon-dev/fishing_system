from django import template

register = template.Library()


@register.simple_tag
def catch_display_name(catch):
    return catch.custom_fish_name or (catch.fish.name if catch.fish_id else "Риба")
