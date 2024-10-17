from django import template

register = template.Library()

@register.filter
def get_query_param(params, field_name):
    """
    Returns the value for the custom field from the query params, if available.
    """
    return params.get(field_name, "")

@register.filter
def option_names(options_queryset):
    return ', '.join([option.option_name for option in options_queryset])

register.filter('get_query_param', get_query_param)
register.filter('option_names', option_names)