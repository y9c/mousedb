#!/usr/bin/env python
# encoding: utf-8

from django import forms

from .models import Mouse
from .models import Breed

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


