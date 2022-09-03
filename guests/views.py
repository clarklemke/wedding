from django.views.generic import ListView
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Guest
from .save_the_date import SAVE_THE_DATE_CONTEXT


from .save_the_date import (
    get_save_the_date_context,
    send_save_the_date_email,
    SAVE_THE_DATE_TEMPLATE,
)


class GuestListView(ListView):
    model = Guest


def home_page(request):
    return render(
        request,
        "home.html",
        context={
            "save_the_dates": SAVE_THE_DATE_CONTEXT,
            "support_email": settings.DEFAULT_WEDDING_REPLY_EMAIL,
            "website_url": settings.WEDDING_WEBSITE_URL,
            "couple_name": settings.BRIDE_AND_GROOM,
            "wedding_location_canada": settings.WEDDING_LOCATION_CANADA,
            "wedding_location_france": settings.WEDDING_LOCATION_FRANCE,
            "wedding_date_canada": settings.WEDDING_DATE_CANADA,
            "wedding_date_france": settings.WEDDING_DATE_FRANCE,
        },
    )


def save_the_date_preview(request):
    context = get_save_the_date_context()
    context["email_mode"] = False
    return render(request, SAVE_THE_DATE_TEMPLATE, context=context)


@login_required
def test_email(request):
    context = get_save_the_date_context()
    send_save_the_date_email(context, [settings.DEFAULT_WEDDING_TEST_EMAIL])
    return HttpResponse("sent!")
