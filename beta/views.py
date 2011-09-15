from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from beta.forms import *
from beta.models import *

def invite_request(request, template_name="beta/invite_request_form.html", extra_context=None):
    """
    Allow a user to request an invite at a later date by entering their email address.
    
    **Arguments:**
    
    ``template_name``
        The name of the tempalte to render.  Optional, defaults to
        privatebeta/invite.html.

    ``extra_context``
        A dictionary to add to the context of the view.  Keys will become
        variable names and values will be accessible via those variables.
        Optional.
    
    **Context:**
    
    The context will contain an ``InviteRequestForm`` that represents a
    :model:`invitemelater.InviteRequest` accessible via the variable ``form``.
    If ``extra_context`` is provided, those variables will also be accessible.
    
    **Template:**
    
    :template:`privatebeta/invite.html` or the template name specified by
    ``template_name``.
    """
    messages = None
    if request.POST:
        form = InviteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages = ["Thanks! We'll let you know when the site launches.",]
    else:
        form = InviteRequestForm()

    context = {'form': form, 'messages': messages }

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template_name, context,
        context_instance=RequestContext(request))

def invite_request_complete(request, template_name="beta/invite_request_complete.html", extra_context=None):
    """
    Display a message to the user after the invite request is completed
    successfully.
    
    **Arguments:**
    
    ``template_name``
        The name of the template to render.  Optional, defaults to
        beta/invite_sent.html.

    ``extra_context``
        A dictionary to add to the context of the view.  Keys will become
        variable names and values will be accessible via those variables.
        Optional.
    
    **Context:**
    
    There will be nothing in the context unless a dictionary is passed to
    ``extra_context``.
    
    **Template:**
    
    :template:`privatebeta/sent.html` or the template name specified by
    ``template_name``.
    """
    return direct_to_template(request, template=template_name, extra_context=extra_context)




@login_required
def send_invite(request):
  try:
    invite = Invite.objects.filter(user=request.user, email="", activation_key="")[0]
  except IndexError:
    return render_to_response("beta/invites_depleted.html", {}, context_instance=RequestContext(request))
  if request.method == "POST":
    form = InviteForm(request.POST, instance=invite, prefix="invite")
    if form.is_valid():
      invite = form.save(commit=False)
      invite.user = request.user
      invite.save()
      invite.send()
      context = { 'invite': invite, }
      return render_to_response('beta/invite_sent.html', context, context_instance=RequestContext(request))
    else:
      context = { 'invite_form': form, }
      return render_to_response('beta/invite_form.html', context, context_instance=RequestContext(request))
  else:
    form = InviteForm(instance=invite, prefix="invite")
    context = { 'invite_form': form, }
    return render_to_response('beta/invite_form.html', context, context_instance=RequestContext(request))
