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

def render_tekst(line, p_class=None):
    line = re.sub("\\[b\\]", "<strong>", line)
    line = re.sub("\\[/b\\]", "</strong>", line)
    line = re.sub("\\[i\\]", "<em>", line)
    line = re.sub("\\[/i\\]", "</em>", line)
    line = re.sub(r'\[url=&quot;(.*?)&quot;\]', r'<a href="\1">', line)
    line = re.sub(r'\[/url\]', r'</a>', line)
    line = re.sub(r'\[label=&quot;(.*?)&quot;\]', r'<a name="\1" />', line)
    line = re.sub(r'\[img=&quot;(.*?)&quot;\]', r'<img src="\1" border="0" />', line)
    line = re.sub(r'\n?\[li\]\n?', r'<li><span>', line)
    line = re.sub(r'\n?\[/li\]\n?', r'</span></li>', line)
    line = re.sub(r'\n', r'<br />', line)
    if p_class == None:
        line = re.sub(r'\n?\[ol\]\n?', r'</p><ol>', line)
        line = re.sub(r'\n?\[ul\]\n?', r'</p><ul>', line)
        line = re.sub(r'\n?\[/ol\]\n?', r'</ol><p>', line)
        line = re.sub(r'\n?\[/ul\]\n?', r'</ul><p>', line)
        line = "<p>"+line+"</p>"
        line = re.sub(r'<p></p>', r'', line)
        return line
    else:
        line = re.sub(r'\n?\[ol\]\n?', r'</p><ol class="%s">' % p_class, line)
        line = re.sub(r'\n?\[ul\]\n?', r'</p><ul class="%s">' % p_class, line)
        line = re.sub(r'\n?\[/ol\]\n?', r'</ol><p class="%s">' % p_class, line)
        line = re.sub(r'\n?\[/ul\]\n?', r'</ul><p class="%s">' % p_class, line)
        line = ("<p class=\"%s\">" % p_class) + line + "</p>"
        line = re.sub(r'<p class=\"%s\"></p>' % p_class, r'', line)
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
    text = "\n".join([s.strip() for s in text.strip().split("\n")])
    pieces = [render_tekst(s) for s in text.split("\n\n")]
    result = "".join([p for p in pieces])
    return mark_safe(result)

def render_programma_iter(pieces):
    for (lvl,idx,sup,title,pieces) in pieces:
        if title != None: title = conditional_escape(title)
        if idx != None:
            anchor = "_".join([z for z in idx.split(".")])
            yield "<a name=\"%s\"></a>" % (anchor,)
            if sup:
                yield "<div class=\"header-%d\"><a href=\"#%s\">%s</a></div>\n" % (lvl, anchor, title,)
            else:
                yield "<div class=\"header-%d\"><a href=\"#%s\">%s. %s</a></div>\n" % (lvl, anchor, idx, title,)
        for line in pieces:
            line = conditional_escape(line)
            yield render_tekst(line, "level-%d" % lvl)

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
    pieces = programma.parse_programma()
    pieces = select_hoofdstuk(pieces, hoofdstuk)
    return mark_safe("".join([s for s in render_programma_iter(pieces)]))

@register.simple_tag(name='hoofdstuk_link')
def get_hoofdstuk_link(hoofdstuk, base_url=None):
    (nr, title) = hoofdstuk
    if base_url != None: 
        base_url = reverse(base_url)
        return mark_safe(r'<a href="%s#%s">%s. %s</a>' % (base_url,nr,nr,title,))
    else:
        url = reverse('moties:default_hoofdstuk', kwargs={'hoofdstuk': nr,})
        return mark_safe(r'<a href="%s">%s. %s</a>' % (url,nr,title,))


