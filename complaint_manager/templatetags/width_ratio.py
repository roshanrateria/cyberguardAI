from django.template.defaulttags import register

@register.filter
def width_ratio(value, max_value=0.8, mid_value=0.5, min_value=0.2):
    if value >= max_value:
        return 100
    elif value >= mid_value:
        return (value - mid_value) / (max_value - mid_value) * 100
    else:
        return (value - min_value) / (mid_value - min_value) * 100# -*- coding: utf-8 -*-

