from django.views.generic import ListView
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from .models import Guest


from .save_the_date import (
    get_save_the_date_context,
    send_save_the_date_email,
    SAVE_THE_DATE_TEMPLATE,
)


class GuestListView(ListView):
    model = Guest


def save_the_date_preview(request):
    context = get_save_the_date_context()
    context["email_mode"] = False
    return render(request, SAVE_THE_DATE_TEMPLATE, context=context)


def test_email(request):
    context = get_save_the_date_context()
    send_save_the_date_email(context, [settings.DEFAULT_WEDDING_TEST_EMAIL])
    return HttpResponse("sent!")
