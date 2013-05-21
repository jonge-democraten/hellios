from django import template
from moties.models import Motie

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
