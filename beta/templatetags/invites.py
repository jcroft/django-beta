from django import template
from django.template import Library, Node
from django.template import resolve_variable

register = Library()

from beta.models import *
from beta.forms import *

class GetInvitesNode(template.Node):
  def __init__(self, user, varname):
    self.user = user
    self.varname = varname

  def render(self, context):
    user = resolve_variable(self.user, context)
    context[self.varname] = Invite.objects.filter(user=user, email="", activation_key="")
    return ''

@register.tag
def get_invites(parser, token):
  """
  Returns all invites available for the given user to send.

  Syntax::

      {% get_invites for [user] as [varname] %}

  Example::

      {% get_invites for user as invite_list %}

  """
  bits = token.contents.split()
  if len(bits) == 5:
    return GetInvitesNode(bits[2], bits[4])
  else:
    raise template.TemplateSyntaxError("'%s' tag takes four arguments" % bits[0])
    
    
class GetInviteFormNode(template.Node):
  def __init__(self, varname):
    self.varname = varname

  def render(self, context):
    user = context['request'].user
    invites = Invite.objects.filter(user=user, email="", activation_key="")
    if invites.count() > 0:
      invite = invites[0]
      context[self.varname] = InviteForm(instance=invite, prefix="invite")
    else:
      context[self.varname] = None
    return ''

@register.tag
def get_invite_form(parser, token):
  """
  Returns an invite form.

  Syntax::

      {% get_invite_form as [varname] %}

  Example::

      {% get_invite_form as invite_form %}

  """
  bits = token.contents.split()
  if len(bits) == 3:
    return GetInviteFormNode(bits[2])
  else:
    raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
