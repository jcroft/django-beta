import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_utils.db.models import *

from beta.managers import *

class InviteRequest(CreationDateMixin):
  """
  An InviteRequest is a stored e-mail of a user who is interested in this site.
  """
  email = models.EmailField(_('Email address'), unique=True)
  invited = models.BooleanField(_('Invited'), default=False)

  def __unicode__(self):
    return u'Invite for %s' % self.email
    
class Invite(models.Model):
  """
  An invite is an invitation to use this site.
  """
  user            = models.ForeignKey(User, blank=True, null=True, related_name="invites")
  email           = models.EmailField(blank=True, help_text="E-mail address of the person being invited.")
  date_sent       = models.DateTimeField(blank=True, null=True)
  activation_key  = models.CharField(max_length=40, blank=True)
  redeemed        = models.BooleanField(default=False)
  objects         = InviteManager()

  def __unicode__(self):
    if self.user and self.email:
      return "%s invited %s" % (self.user, self.email)
    if self.user:
      return "%s (unsent)" % self.user
    if self.email:
      return "Admin invited %s" % self.email
    else:
      return "Invite"
      
  def send(self):
    if self.email and not self.activation_key:
      Invite.objects.send_invite(self)
    
  def save(self, *args, **kwargs):
    super(Invite, self).save(*args, **kwargs)
