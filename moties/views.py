from wkhtmltopdf.views import PDFTemplateView
from moties.models import Motie
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

class MotieDetailView(DetailView):
    context_object_name = "motie"
    model = Motie

    def get_context_data(self, **kwargs):
        context = super(MotieDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        motie = context[self.context_object_name]
        if motie.status == Motie.INGEDIEND:
            context['status'] = "Deze motie is <strong>ingediend</strong>."
        elif motie.status == Motie.CONGRES:
            context['status'] = "Deze motie zal worden behandeld op het <strong>congres</strong>."
        elif motie.status == Motie.GOEDGEKEURD:
            context['status'] = "Deze motie is <strong>goedgekeurd</strong> om te worden behandeld."
        elif motie.status == Motie.VERWORPEN:
            context['status'] = "Deze motie is <strong>verworpen</strong>."
        elif motie.status == Motie.AANGENOMEN:
            context['status'] = "Deze motie is <strong>aangenomen</strong>."
        elif motie.status == Motie.UITGESTELD:
            context['status'] = "Deze motie is <strong>uitgesteld</strong>."
        return context


from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from moties.serializers import MotieSerializer

@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API
    """
    return Response({
        'moties': reverse('motie-list', request=request),
    })

class MotieList(generics.ListCreateAPIView):
    model = Motie
    serializer_class = MotieSerializer

class MotieDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Motie
    serializer_class = MotieSerializer


