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

def render_tekst(line):
    line = re.sub("\\[b\\]", "<strong>", line)
    line = re.sub("\\[/b\\]", "</strong>", line)
    line = re.sub("\\[i\\]", "<em>", line)
    line = re.sub("\\[/i\\]", "</em>", line)
    line = re.sub(r'\[url=&quot;(.*?)&quot;\]', r'<a href="\1">', line)
    line = re.sub(r'\[/url\]', r'</a>', line)
    line = re.sub(r'\[label=&quot;(.*?)&quot;\]', r'<a name="\1" />', line)
    line = re.sub(r'\[img=&quot;(.*?)&quot;\]', r'<img src="\1" border="0" />', line)
    line = re.sub(r'\n?\[li\]\n?', r'<li>', line)
    line = re.sub(r'\n?\[/li\]\n?', r'</div></li>', line)
    line = re.sub(r'\n?\[ol\]\n?', r'<ol>', line)
    line = re.sub(r'\n?\[/ol\]\n?', r'</ol>', line)
    line = re.sub(r'\n?\[ul\]\n?', r'<ul>', line)
    line = re.sub(r'\n?\[/ul\]\n?', r'</ul>', line)
    line = re.sub(r'\n', r'<br />', line)
    return line

@register.filter(name='render_tekst', needs_autoescape=True)
@stringfilter
def render_tekst_filter(line, autoescape=True):
    if autoescape: line = conditional_escape(line)
    return mark_safe(render_tekst(line))


@register.filter(name='standpunt_tekst', needs_autoescape=True)
@stringfilter
def get_standpunt_tekst(text, autoescape=True):
    if autoescape: text = conditional_escape(text)
    pieces = [render_tekst(s.strip()) for s in text.strip().split("\n\n")]
    result = "".join(["<p" + p + "</p>" for p in pieces])
    return mark_safe(result)

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
            line = re.sub(r'\n?\[li\]\n?', r'<li><div class="li-level-%d">' % lvl, line)
            line = re.sub(r'\n?\[/li\]\n?', r'</div></li>', line)
            line = re.sub(r'\n?\[ol\]\n?', r'<ol>', line)
            line = re.sub(r'\n?\[/ol\]\n?', r'</ol>', line)
            line = re.sub(r'\n?\[ul\]\n?', r'<ul>', line)
            line = re.sub(r'\n?\[/ul\]\n?', r'</ul>', line)
            line = re.sub(r'\n', r'<br />', line)
            yield r'<p class="level-%d">' % lvl
            yield line
            yield "</p>\n"

@register.simple_tag(name='render_programma')
def render_programma(programma):
    return mark_safe(("".join([s for s in render_programma_iter(programma.parse_programma())])))

def select_hoofdstuk(pieces, hoofdstuk):
    good = False
    res = []
    for piece in pieces:
        if piece[0] == 1:
            good = piece[1] == str(hoofdstuk)
        if good:
            res += [piece,]
    return tuple(res)

@register.simple_tag(name='render_programma_hoofdstuk')
def render_programma_hoofdstuk(programma, hoofdstuk):
    return mark_safe(("".join([s for s in render_programma_iter(select_hoofdstuk(programma.parse_programma(), hoofdstuk))])))

@register.simple_tag(name='hoofdstuk_link')
def get_hoofdstuk_link(hoofdstuk, base_url=None):
    (nr, title) = hoofdstuk
    if base_url != None: 
        base_url = reverse(base_url)
        return mark_safe(r'<a href="%s#%s">%s. %s</a>' % (base_url,nr,nr,title,))
    else:
        url = reverse('moties:default_hoofdstuk', kwargs={'hoofdstuk': nr,})
        return mark_safe(r'<a href="%s">%s. %s</a>' % (url,nr,title,))


