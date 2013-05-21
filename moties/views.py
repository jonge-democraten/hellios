from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic import DetailView, ListView, FormView, View
from django.views.generic.detail import SingleObjectMixin
from moties.forms import CommentForm
from moties.models import Motie, Tag, Comment
from re import sub

def has_notulen(motie):
    if motie.congres == None:
        return False
    if motie.congres.notulen == None:
        return False
    return len(motie.congres.notulen.strip()) > 0

def get_congres(motie):
    congres = motie.congres
    if congres != None:
        return congres.naam
    else:
        return "--"

def get_congres_inleiding(motie):
    congres = motie.congres
    if congres != None:
        return congres.inleiding
    else:
        return "De JD,"

def get_status(motie):
    if motie.status == Motie.INGEDIEND:
        return "<strong>ingediend</strong>"
    elif motie.status == Motie.GOEDGEKEURD:
        return "<strong>goedgekeurd ter behandeling</strong>"
    elif motie.status == Motie.CONGRES:
        return "<strong>in congresboek</strong>: %s" % get_congres(motie)
    elif motie.status == Motie.VERWORPEN:
        return "<strong>verworpen</strong>: %s" % get_congres(motie)
    elif motie.status == Motie.AANGENOMEN:
        return "<strong>aangenomen</strong>: %s" % get_congres(motie)
    elif motie.status == Motie.UITGESTELD:
        return "<strong>aangehouden</strong>: %s" % get_congres(motie)

def to_br_list(str):
    if str == None: return []
    # strip whole block
    str = str.strip()
    # strip all lines
    str = "\n".join([s.strip() for s in str.split("\n")])
    # replace single newlines by <br />
    str = sub("(?<!\n)(\n)(?!\n)", "<br />", str)
    # convert to list and remove empty lines
    str = [s for s in str.split("\n") if len(s)]
    return str

def to_p(str):
    if str == None: return ""
    str = str.strip()
    str = "\n".join([s.strip() for s in str.split("\n")])
    str = sub("(?<!\n)(\n)(?!\n)", "<br />", str)
    str = [s for s in str.split("\n") if len(s)]
    if len(str) == 0: return ""
    return "<p>" + "</p><p>".join(str) + "</p>"

def get_content(motie):
    if len(motie.content.strip()) > 0:
        return motie.content.strip()

    inleiding = get_congres_inleiding(motie)
    con = to_br_list(motie.constateringen)
    over = to_br_list(motie.overwegingen)
    uit = to_br_list(motie.uitspraken)
    toe = to_p(motie.toelichting)

    inleiding = "<p><em>" + inleiding + "</em></p>"
    con = len(con) and ("<p><strong>constaterende dat</strong></p><ul><li>" + "</li><li>".join(con) + "</li></ul>") or ""
    over = len(over) and ("<p><strong>overwegende dat</strong></p><ul><li>" + "</li><li>".join(over) + "</li></ul>") or ""
    uit = len(uit) and ("<p><strong>spreekt uit dat</strong></p><ul><li>" + "</li><li>".join(uit) + "</li></ul>") or ""
    toe = len(toe) and ("<p><strong>Toelichting:</strong></p>" + toe) or ""
    orde = "<p><em>en gaat over tot de orde van de dag.</em></p>"

    return inleiding + con + over + uit + orde + toe

class MotieFullView(DetailView):
    template_name = 'moties/motie.html'
    context_object_name = "motie"
    model = Motie

    def get_context_data(self, **kwargs):
        context = super(MotieFullView, self).get_context_data(**kwargs)
        motie = context['motie']
        context['status'] = get_status(motie)
        context['content'] = get_content(motie)
        context['tags'] = Tag.objects.annotate(num_moties=Count('motie')).order_by('-num_moties', 'kort').filter(motie__id__exact=motie.id)
        context['has_notulen'] = has_notulen(motie)
        context['has_comments'] = motie.comments.count() > 0
        context['comment_form'] = CommentForm()
        return context

class CommentView(SingleObjectMixin, FormView):
    template_name = 'moties/motie.html'
    context_object_name = "motie"
    form_class = CommentForm
    model = Motie

    def get_context_data(self, **kwargs):
        context = super(CommentView, self).get_context_data(**kwargs)
        motie = context['motie']
        context['status'] = get_status(motie)
        context['content'] = get_content(motie)
        context['tags'] = Tag.objects.annotate(num_moties=Count('motie')).order_by('-num_moties', 'kort').filter(motie__id__exact=motie.id)
        context['has_notulen'] = has_notulen(motie)
        context['has_comments'] = motie.comments.count() > 0
        context['comment_form'] = self.form
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_invalid(self, form):
        self.object = self.get_object()
        self.form = form
        return super(CommentView, self).form_invalid(form)

    def form_valid(self, form):
        self.object = self.get_object()
        comment = Comment(motie=self.object, tekst=form.cleaned_data['tekst'], auteur=form.cleaned_data['author'], email=form.cleaned_data['email'])
        comment.save()
        return super(CommentView, self).form_valid(form)

class MotieView(View):
    def get(self, request, *args, **kwargs):
        view = MotieFullView.as_view()
        return view(request, *args, **kwargs);

    def post(self, request, *args, **kwargs):
        view = CommentView.as_view()
        return view(request, *args, **kwargs);

class FilterMixin(object):
    def get_queryset_filters(self):
        filters = {}
        for item in self.allowed_filters:
            if item in self.request.GET:
                 filters[self.allowed_filters[item]] = self.request.GET[item]
        return filters

    def get_queryset(self):
        return super(FilterMixin, self).get_queryset()\
              .filter(**self.get_queryset_filters())

class MotieListView(FilterMixin, ListView):
    queryset = Motie.objects.all()
    context_object_name = 'moties'
    template_name = 'moties/list.html'
    paginate_by = 50000
    allowed_filters = {'tag': 'tags__kort',}
    allowed_sorts = {'motie': ('-datum','titel',), 'congres': ('-congres__datum','titel',), 'titel': ('titel',)}

    def get_queryset(self):
        qs = super(MotieListView, self).get_queryset()
        if not self.request.user.is_authenticated():
            qs = qs.exclude(status__exact=Motie.INGEDIEND)
        if "order" in self.request.GET:
            if self.request.GET['order'] in self.allowed_sorts:
                return qs.order_by(*self.allowed_sorts[self.request.GET['order']])
                
        return qs.order_by('-datum')

    def get_context_data(self, **kwargs):
        context = super(MotieListView, self).get_context_data(**kwargs)
        context['base_url'] = self.request.path
        context['request'] = self.request
        return context

class TagView(MotieListView):
    template_name = 'moties/tag.html'

    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        return context

    def get_queryset(self):
        return super(TagView, self).get_queryset().filter(tags__kort=self.kwargs['tag'])

class TagListView(ListView):
    queryset = Tag.objects\
                .annotate(num_moties=Count('motie'))\
                .filter(num_moties__gt=0)\
                .order_by('-num_moties')
    context_object_name = 'tags'
    template_name = 'moties/tags.html'

def view_home(request):
    tags = Tag.objects.annotate(num_moties=Count('motie')).filter(num_moties__gt=0).order_by('-num_moties')[:12]
    return render_to_response("moties/home.html", {'tags': tags})


# from rest_framework import viewsets
# from moties.serializers import MotieSerializer

# class MotieViewSet(viewsets.ModelViewSet):
#     queryset = Motie.objects.all()
#     serializer_class = MotieSerializer
