from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from moties.models import Motie
from re import sub

register = template.Library()

@register.filter(name='motie_status_list')
def get_motie_status_list(motie):
    if motie.status == Motie.VERWORPEN:
        return "(verworpen)"
    if motie.status == Motie.UITGESTELD:
        return "(aangehouden)"
    if motie.status == Motie.CONGRES:
        return "(in congresboek)"
    if motie.status == Motie.GOEDGEKEURD:
        return "(goedgekeurd)"
    if motie.status == Motie.INGEDIEND:
        return "(ingediend)"
    return ""

@register.filter(name='motie_has_comments')
def get_has_comments(motie):
    return ""

@register.filter(name='standpunt_tekst', needs_autoescape=True)
@stringfilter
def get_standpunt_tekst(text, autoescape=True):
    if autoescape:
        text = conditional_escape(text)
    text = text.strip()
    text = "\n".join([s.strip() for s in text.split("\n")])
    text = sub("(?<!\n)(\n)(?!\n)", "<br />", text)
    text = [s for s in text.split("\n") if len(s)]
    if len(text) > 0: text = "<p>" + "</p><p>".join(text) + "</p>"
    else: text = ""
    return mark_safe(text)


