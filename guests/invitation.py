from datetime import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.http import Http404
from django.template.loader import render_to_string
from guests.models import Party

INVITATION_TEMPLATE = "email_templates/invitation.html"


def guess_party_by_invite_id_or_404(invite_id):
    try:
        return Party.objects.get(invitation_id=invite_id)
    except Party.DoesNotExist:
        if settings.DEBUG:
            # in debug mode allow access by ID
            return Party.objects.get(id=int(invite_id))
        else:
            raise Http404()


def get_invitation_context(party):
    return {
        "title": "Save The Date",
        "main_image": "save-the-date.svg",
        "main_color": "#ffefdb",
        "font_color": "#666666",
        "page_title": "Anna and Clark - You're Invited!",
        "preheader_text": "You are invited!",
        "invitation_id": party.invitation_id,
        "party": party,
    }


def send_invitation_email(party, recipient, test_only=False):
    if recipient is None:
        recipient = party.email
    if not recipient:
        print(
            "===== WARNING: no valid email addresses found for {} =====".format(party)
        )
        return

    context = get_invitation_context(party)
    context["email_mode"] = True
    context["site_url"] = settings.WEDDING_WEBSITE_URL
    context["couple"] = settings.BRIDE_AND_GROOM
    template_html = render_to_string(INVITATION_TEMPLATE, context=context)
    template_text = "You're invited to {}'s wedding. To view this invitation, visit {} in any browser.".format(
        settings.BRIDE_AND_GROOM, reverse("invitation", args=[context["invitation_id"]])
    )
    subject = "Anna and Clark Wedding Invitation"

    msg = EmailMultiAlternatives(
        subject,
        template_text,
        settings.DEFAULT_WEDDING_FROM_EMAIL,
        recipient,
        reply_to=[settings.DEFAULT_WEDDING_REPLY_EMAIL],
    )
    msg.attach_alternative(template_html, "text/html")

    print("sending invitation to {} ({})".format(party.name, ", ".join(recipient)))
    if not test_only:
        msg.send()


def send_all_invitations(test_only, mark_as_sent):
    to_send_to = Party.in_default_order().filter(invitation_sent=None)
    for party in to_send_to:
        send_invitation_email(party, test_only=test_only)
        if mark_as_sent:
            party.invitation_sent = datetime.now()
            party.save()
