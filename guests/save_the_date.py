from copy import copy
from email.mime.image import MIMEImage
import os
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Party


SAVE_THE_DATE_TEMPLATE = "email_templates/save_the_date.html"
SAVE_THE_DATE_CONTEXT = {
    "title": "Save The Date",
    "header_filename": "save-the-date.png",
    "main_image": "save-the-date.png",
    "main_color": "#ffffff",
    "font_color": "#ff5c3e",
}


def send_all_save_the_dates(test_only=False, mark_as_sent=False):
    to_send_to = Party.filter(save_the_date_sent=None)
    for party in to_send_to:
        send_save_the_date_to_party(party, test_only=test_only)
        if mark_as_sent:
            party.save_the_date_sent = datetime.now()
            party.save()


def send_save_the_date_to_party(party, test_only=False):
    context = SAVE_THE_DATE_CONTEXT
    recipient = party.email
    if not recipient:
        print(
            "===== WARNING: no valid email addresses found for {} =====".format(party)
        )
    else:
        send_save_the_date_email(context, recipient, test_only=test_only)


def get_save_the_date_context():
    context = copy(SAVE_THE_DATE_CONTEXT)
    context["name"] = "Save The Date"
    context["rsvp_address"] = settings.DEFAULT_WEDDING_REPLY_EMAIL
    context["site_url"] = settings.WEDDING_WEBSITE_URL
    context["couple"] = settings.BRIDE_AND_GROOM
    context["location_canada"] = settings.WEDDING_LOCATION_CANADA
    context["location_france"] = settings.WEDDING_LOCATION_FRANCE
    context["date_canada"] = settings.WEDDING_DATE_CANADA
    context["date_france"] = settings.WEDDING_DATE_FRANCE
    context["page_title"] = settings.BRIDE_AND_GROOM + " - Save the Date!"
    context["preheader_text"] = (
        "The date that you've eagerly been waiting for is finally here. "
        + settings.BRIDE_AND_GROOM
        + " are getting married! Save the date!"
    )
    return context


def send_save_the_date_email(context, recipient, test_only=False):
    context["email_mode"] = True
    context["rsvp_address"] = settings.DEFAULT_WEDDING_REPLY_EMAIL
    context["site_url"] = settings.WEDDING_WEBSITE_URL
    context["couple"] = settings.BRIDE_AND_GROOM
    template_html = render_to_string(SAVE_THE_DATE_TEMPLATE, context=context)
    template_text = f"""Save the date(s) for {settings.BRIDE_AND_GROOM}'s wedding! 
    {settings.WEDDING_DATE_CANADA} {settings.WEDDING_LOCATION_CANADA} and
    {settings.WEDDING_DATE_FRANCE} {settings.WEDDING_LOCATION_FRANCE}"""

    subject = "Save the Date!"
    # https://www.vlent.nl/weblog/2014/01/15/sending-emails-with-embedded-images-in-django/
    msg = EmailMultiAlternatives(
        subject,
        template_text,
        settings.DEFAULT_WEDDING_FROM_EMAIL,
        recipient,
        reply_to=[settings.DEFAULT_WEDDING_REPLY_EMAIL],
    )
    msg.attach_alternative(template_html, "text/html")
    # for filename in (context["header_filename"], context["main_image"]):
    #     attachment_path = os.path.join(
    #         os.path.dirname(__file__), "static", "save-the-date", "images", filename
    #     )
    #     with open(attachment_path, "rb") as image_file:
    #         msg_img = MIMEImage(image_file.read())
    #         msg_img.add_header("Content-ID", "<{}>".format(filename))
    #         msg.attach(msg_img)

    print("sending {} to {}".format(context["name"], ", ".join(recipient)))
    if not test_only:
        msg.send()


def clear_all_save_the_dates():
    print("clear")
    for party in Party.objects.exclude(save_the_date_sent=None):
        party.save_the_date_sent = None
        print("resetting {}".format(party))
        party.save()
