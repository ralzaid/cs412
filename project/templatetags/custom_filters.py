from django import template

register = template.Library()

@register.filter
def dict_key(dictionary, key):
    """Returns the value for a given key in a dictionary."""
    return dictionary.get(key, [])
