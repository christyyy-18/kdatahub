"""Filters that partially hide contact details on publicly reachable pages."""

from django import template

register = template.Library()


@register.filter
def mask_email(value):
    """j***@gmail.com -- enough for the owner to recognise, not to harvest."""
    value = (value or '').strip()
    if '@' not in value:
        return value
    local, _, domain = value.partition('@')
    if len(local) <= 1:
        return f'{local}***@{domain}'
    return f'{local[0]}***{local[-1] if len(local) > 2 else ""}@{domain}'


@register.filter
def mask_phone(value):
    """024****103 -- first three and last three digits only."""
    digits = ''.join(ch for ch in str(value or '') if ch.isdigit())
    if len(digits) < 7:
        return '*' * len(digits)
    return f'{digits[:3]}{"*" * (len(digits) - 6)}{digits[-3:]}'


@register.filter
def first_name_only(value):
    """Ama Mensah -> Ama. Enough for the owner to recognise their own order."""
    return (str(value or '').strip().split(' ') or [''])[0]
