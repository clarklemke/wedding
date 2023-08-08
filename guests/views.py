from collections import namedtuple
from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView

from .invitation import (
    INVITATION_TEMPLATE,
    get_invitation_context,
    guess_party_by_invite_id_or_404,
    send_invitation_email,
)
from .models import Guest
from .reminder import REMINDER_TEMPLATE, get_reminder_context, send_reminder_email
from .save_the_date import (
    SAVE_THE_DATE_CONTEXT,
    SAVE_THE_DATE_TEMPLATE,
    get_save_the_date_context,
    send_save_the_date_email,
)
from .update_france import send_update_email


class GuestListView(ListView):
    model = Guest


def home_page(request: HttpRequest) -> HttpResponse:
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
            "wedding_time_canada": settings.WEDDING_TIME_CANADA,
            "wedding_time_france": settings.WEDDING_TIME_FRANCE,
        },
    )


def save_the_date_preview(request: HttpRequest) -> HttpResponse:
    context = get_save_the_date_context()
    context["email_mode"] = False
    return render(request, SAVE_THE_DATE_TEMPLATE, context=context)


@login_required
def test_email(request: HttpRequest) -> HttpResponse:
    context = get_save_the_date_context()
    send_save_the_date_email(context, [settings.DEFAULT_WEDDING_TEST_EMAIL])
    return HttpResponse("sent!")


def invitation(request: HttpRequest, invite_id: str) -> HttpResponse:
    party = guess_party_by_invite_id_or_404(invite_id)
    if party.invite_viewed is None:
        # update if this is the first time the invitation was opened
        party.invite_viewed = datetime.utcnow()
        party.save()
    if request.method == "POST":
        for response in _parse_invite_params(request.POST):
            guest = Guest.objects.get(pk=response.guest_pk)
            assert guest.party == party
            guest.attending_canada = response.attending_canada
            guest.attending_france = response.attending_france
            guest.dietary_restrictions = response.dietary_restrictions
            guest.save()
        return HttpResponseRedirect(reverse("rsvp-confirm", args=[invite_id]))
    return render(
        request,
        template_name="home.html",
        context={
            "party": party,
            "save_the_dates": SAVE_THE_DATE_CONTEXT,
            "support_email": settings.DEFAULT_WEDDING_REPLY_EMAIL,
            "website_url": settings.WEDDING_WEBSITE_URL,
            "couple_name": settings.BRIDE_AND_GROOM,
            "wedding_location_canada": settings.WEDDING_LOCATION_CANADA,
            "wedding_location_france": settings.WEDDING_LOCATION_FRANCE,
            "wedding_date_canada": settings.WEDDING_DATE_CANADA,
            "wedding_date_france": settings.WEDDING_DATE_FRANCE,
            "wedding_time_canada": settings.WEDDING_TIME_CANADA,
            "wedding_time_france": settings.WEDDING_TIME_FRANCE,
        },
    )


InviteResponse = namedtuple(
    "InviteResponse",
    ["guest_pk", "attending_canada", "attending_france", "dietary_restrictions"],
)


def _parse_invite_params(params):
    responses = {}
    for param, value in params.items():
        if param.startswith("attending-canada"):
            pk = int(param.split("-")[-1])
            response = responses.get(pk, {})
            response["attending_canada"] = True if value == "yes" else False
            responses[pk] = response
        elif param.startswith("attending-france"):
            pk = int(param.split("-")[-1])
            response = responses.get(pk, {})
            response["attending_france"] = True if value == "yes" else False
            responses[pk] = response
        elif param.startswith("dietary"):
            pk = int(param.split("-")[-1])
            response = responses.get(pk, {})
            response["dietary_restrictions"] = value
            responses[pk] = response

    for pk, response in responses.items():
        yield InviteResponse(
            pk,
            response["attending_canada"],
            response["attending_france"],
            response.get("dietary_restrictions", None),
        )


def rsvp_confirm(request: HttpRequest, invite_id: str = None) -> HttpResponse:
    party = guess_party_by_invite_id_or_404(invite_id)
    return render(
        request,
        template_name="rsvp_confirmation.html",
        context={
            "party": party,
            "support_email": settings.DEFAULT_WEDDING_REPLY_EMAIL,
            "couple_name": settings.BRIDE_AND_GROOM,
            "website_url": settings.WEDDING_WEBSITE_URL,
        },
    )


@login_required
def invitation_email_preview(request: HttpRequest, invite_id: str) -> HttpResponse:
    party = guess_party_by_invite_id_or_404(invite_id)
    context = get_invitation_context(party)
    return render(request, INVITATION_TEMPLATE, context=context)


@login_required
def invitation_email_test(request: HttpRequest, invite_id: str) -> HttpResponse:
    party = guess_party_by_invite_id_or_404(invite_id)
    print(party)
    send_invitation_email(party, [party.email])
    return HttpResponse("sent!")


@login_required
def reminder_email_preview(request: HttpRequest, invite_id: str) -> HttpResponse:
    party = guess_party_by_invite_id_or_404(invite_id)
    context = get_reminder_context(party)
    return render(request, REMINDER_TEMPLATE, context=context)


@login_required
def reminder_email_test(request: HttpRequest, invite_id: str) -> HttpResponse:
    party = guess_party_by_invite_id_or_404(invite_id)
    print(party)
    send_reminder_email(party, [party.email])
    return HttpResponse("sent!")


@login_required
def update_email_test(request: HttpRequest, invite_id: str) -> HttpResponse:
    party = guess_party_by_invite_id_or_404(invite_id)
    print(party)
    send_update_email(party, [party.email])
    return HttpResponse("sent!")
