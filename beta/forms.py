from django import forms

from beta.models import *

class InviteRequestForm(forms.ModelForm):
  class Meta:
    model = InviteRequest
    fields = ['email']

class InviteForm(forms.ModelForm):
  class Meta:
    model = Invite
    fields = ['email']
