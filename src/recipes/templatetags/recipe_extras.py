from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def is_hero_page(context):
    """
    Check if the current page is a hero page (home, login, logout).
    Returns True if the current URL name is one of the hero pages.
    """
    request = context['request']
    hero_pages = ['home', 'login', 'logout']
    return request.resolver_match.url_name in hero_pages

@register.simple_tag(takes_context=True)
def get_nav_classes(context, hero_class, default_class):
    """
    Return the appropriate CSS classes based on whether it's a hero page.
    """
    if is_hero_page(context):
        return hero_class
    return default_class

@register.simple_tag(takes_context=True)
def get_footer_classes(context):
    """
    Return the appropriate footer CSS classes based on whether it's a hero page.
    """
    if is_hero_page(context):
        return "fixed right-0 z-50 bottom-0 left-0 bg-alternate_a-800/70 backdrop-blur-sm text-accent-300"
    return "bg-alternate_a-100 border-t border-gray-200 text-accent-800"
