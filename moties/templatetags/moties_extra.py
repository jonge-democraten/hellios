from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.core.urlresolvers import reverse
from moties.models import Motie
import re

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
    text = re.sub("(?<!\n)(\n)(?!\n)", "<br />", text)
    text = [s for s in text.split("\n") if len(s)]
    if len(text) > 0: text = "<p>" + "</p><p>".join(text) + "</p>"
    else: text = ""
    return mark_safe(text)

def render_programma_iter(pieces):
    for (lvl,idx,title,pieces) in pieces:
        if title != None: title = conditional_escape(title)
        if idx != None:
            anchor = "_".join([z for z in idx.split(".")])
            yield "<a name=\"%s\"></a>" % (anchor,)
            yield "<div class=\"header-%d\"><a href=\"#%s\">%s. %s</a></div>\n" % (lvl, anchor, idx, title,)
        for line in pieces:
            line = conditional_escape(line)
            line = re.sub("\\[b\\]", "<strong>", line)
            line = re.sub("\\[/b\\]", "</strong>", line)
            line = re.sub("\\[i\\]", "<em>", line)
            line = re.sub("\\[/i\\]", "</em>", line)
            line = re.sub(r'\[url=&quot;(.*?)&quot;\]', r'<a href="\1">', line)
            line = re.sub(r'\[/url\]', r'</a>', line)
            line = re.sub(r'\[label=&quot;(.*?)&quot;\]', r'<a name="\1" />', line)
            line = re.sub(r'\[img=&quot;(.*?)&quot;\]', r'<img src="\1" border="0" />', line)
            line = re.sub(r'\[li\]', r'<li><div class="level-%d">' % lvl, line)
            line = re.sub(r'\[/li\]', r'</div></li>', line)
            line = re.sub(r'\[ol\]', r'<ol>', line)
            line = re.sub(r'\[/ol\]', r'</ol>', line)
            line = re.sub(r'\[ul\]', r'<ul>', line)
            line = re.sub(r'\[/ul\]', r'</ul>', line)
            line = re.sub(r'\n', r'<br />', line)
            yield r'<p class="level-%d">' % lvl
            yield line
            yield "</p>\n"

@register.simple_tag(name='render_programma')
def render_programma(programma):
    return mark_safe(("".join([s for s in render_programma_iter(programma.parse_programma())])))

@register.simple_tag(name='hoofdstuk_link')
def get_hoofdstuk_link(hoofdstuk, base_url=""):
    if base_url != None: base_url = reverse(base_url)
    else: base_url = ""
    (nr, title) = hoofdstuk
    return mark_safe(r'<a href="%s#%s">%s. %s</a>' % (base_url,nr,nr,title,))
