from django.contrib import admin
from django.utils.translation import ugettext_lazy, ugettext as _

from beta.models import *

class InviteRequestAdmin(admin.ModelAdmin):
  date_hierarchy  = 'date_created'
  list_display    = ('email', 'date_created', 'invited',)
  list_filter     = ('date_created', 'invited',)
  actions         = ('send_invite',)
  search_fields   = ('email',)
  
  def send_invite(self, request, queryset):
    for invite_request in queryset:
      if not invite_request.invited:
        try:
          invite, created = Invite.objects.get_or_create(email=invite_request.email)
          Invite.objects.send_invite(invite)
          invite_request.invited = True
          invite_request.save()
        except:
          pass
    rows_updated = queryset.count()
    if rows_updated == 1: message_bit = "1 invite was"
    else: message_bit = "%s invites were" % rows_updated
    self.message_user(request, "%s successfully sent." % message_bit)
  send_invite.short_description = ugettext_lazy("Send invites to selected")
  
class InviteAdmin(admin.ModelAdmin):
  date_hierarchy  = 'date_sent'
  list_display    = ('__unicode__', 'email', 'user', 'date_sent','redeemed')
  list_filter     = ('date_sent', 'redeemed',)
  actions         = ('resend_invite',)
  search_fields   = ('email','user__username')
  
  def resend_invite(self, request, queryset):
    for invite in queryset:
      if invite.email:
        try:
          Invite.objects.send_invite(invite)
        except:
          pass
    rows_updated = queryset.count()
    if rows_updated == 1: message_bit = "1 invite was"
    else: message_bit = "%s invites were" % rows_updated
    self.message_user(request, "%s successfully resent." % message_bit)
  resend_invite.short_description = ugettext_lazy("Re-send invites to selected")

admin.site.register(InviteRequest, InviteRequestAdmin)
admin.site.register(Invite, InviteAdmin)
