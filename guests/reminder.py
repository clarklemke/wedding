from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from guests.models import Party

REMINDER_TEMPLATE = "email_templates/reminder.html"


def get_reminder_context(party: Party) -> dict:
    return {
        "title": "Reminder",
        "main_color": "#ffefdb",
        "font_color": "#666666",
        "page_title": "Anna and Clark - You're Invited!",
        "preheader_text": "You are invited!",
        "invitation_id": party.invitation_id,
        "party": party,
    }


def send_reminder_email(party: Party, test_only: bool = False) -> None:
    recipient = party.email
    if not recipient:
        print(
            "===== WARNING: no valid email addresses found for {} =====".format(party)
        )
    context = get_reminder_context(party)
    context["email_mode"] = True
    context["site_url"] = settings.WEDDING_WEBSITE_URL
    context["couple"] = settings.BRIDE_AND_GROOM
    template_html = render_to_string(REMINDER_TEMPLATE, context=context)
    template_text = "You're invited to {}'s wedding. To view this invitation, visit {} in any browser.".format(
        settings.BRIDE_AND_GROOM, reverse("invitation", args=[context["invitation_id"]])
    )
    subject = "Anna and Clark Wedding Invitation Reminder"

    msg = EmailMultiAlternatives(
        subject,
        template_text,
        settings.DEFAULT_WEDDING_FROM_EMAIL,
        [recipient],
        reply_to=[settings.DEFAULT_WEDDING_REPLY_EMAIL],
    )
    msg.attach_alternative(template_html, "text/html")

    print(f"sending invitation to {party.name} ({recipient})")
    if not test_only:
        msg.send()


def send_all_reminders(test_only: bool) -> None:
    to_send_to = Party.objects.filter()
    for party in to_send_to:
        send_reminder_email(party, test_only=test_only)
