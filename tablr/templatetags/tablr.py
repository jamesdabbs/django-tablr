import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def parse(s):
    """ Parses and formats the (pre-escaped) text returned from reddit's 
        JSON API 
    """
    try:
        s = s.replace('&amp;', '&')
        s = s.replace('&gt;', '>')
        s = s.replace('&lt;', '<')
        s = s.replace('/r', '<br/>')
        s = s[s.find('<p>'): s.find('</p>')+4].strip()
        return mark_safe(s)
    except:
        return ''
        

@register.filter
def condense(s):
    """ Removes newlines and returns from a string, making it suitable for 
        display in a reddit comment table cell
    """
    s = s.replace('\n', '  ')
    return s
