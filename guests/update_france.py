from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from guests.models import Party

UPDATE_TEMPLATE = "email_templates/update.html"


def get_update_context(party: Party) -> dict:
    return {
        "title": "Viella Wedding Update",
        "main_color": "#ffefdb",
        "font_color": "#666666",
        "page_title": "Anna and Clark's Viella Wedding Update",
        "preheader_text": "Can't wait to party!",
        "invitation_id": party.invitation_id,
        "party": party,
    }


def send_update_email(party: Party, test_only: bool = False) -> None:
    recipient = party.email
    if not recipient:
        print(f"===== WARNING: no valid email addresses found for {party} =====")
    context = get_update_context(party)
    context["email_mode"] = True
    context["site_url"] = settings.WEDDING_WEBSITE_URL
    context["couple"] = settings.BRIDE_AND_GROOM
    template_html = render_to_string(UPDATE_TEMPLATE, context=context)
    template_text = (
        f"Update to this weekend's Viella wedding {settings.BRIDE_AND_GROOM}."
    )
    subject = "Updated Timeline for Anna and Clark's France Wedding"

    msg = EmailMultiAlternatives(
        subject,
        template_text,
        settings.DEFAULT_WEDDING_FROM_EMAIL,
        [recipient],
        reply_to=[settings.DEFAULT_WEDDING_REPLY_EMAIL],
    )
    msg.attach_alternative(template_html, "text/html")

    print(f"sending update to {party.name} ({recipient})")
    if not test_only:
        msg.send()


def send_all_updates(test_only: bool) -> None:
    to_send_to = Party.objects.filter()
    for party in to_send_to:
        if party.any_guests_attending_france:
            send_update_email(party, test_only=test_only)
