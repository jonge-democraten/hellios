from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

class CommentForm(forms.Form):
    author = forms.CharField(max_length=250)
    email = forms.EmailField()
    tekst = forms.CharField(widget=forms.Textarea)
    controleveld = forms.CharField(max_length=250)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['author'].label = "Naam:"
        self.fields['email'].label = "Email:"
        self.fields['tekst'].label = "Opmerking:"
        self.fields['controleveld'].label = "JD oprichtingsjaar:"

    def is_valid(self):
        if not super(CommentForm, self).is_valid(): return False
        if not self.cleaned_data['controleveld'] == "1984": return False
        return True
