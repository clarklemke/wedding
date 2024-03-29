from django.urls import path, re_path

from .views import (
    GuestListView,
    home_page,
    invitation,
    invitation_email_preview,
    invitation_email_test,
    reminder_email_preview,
    reminder_email_test,
    rsvp_confirm,
    save_the_date_preview,
    test_email,
    update_email_test,
    update_preview,
)

urlpatterns = [
    path("", home_page, name="home"),
    re_path(r"^guests/$", GuestListView.as_view(), name="guest-list"),
    re_path(r"^invite/(?P<invite_id>[\w-]+)/$", invitation, name="invitation"),
    re_path(
        r"^invite-email/(?P<invite_id>[\w-]+)/$",
        invitation_email_preview,
        name="invitation-email",
    ),
    re_path(
        r"^invite-email-test/(?P<invite_id>[\w-]+)/$",
        invitation_email_test,
        name="invitation-email-test",
    ),
    re_path(
        r"^save-the-date/$",
        save_the_date_preview,
        name="save-the-date",
    ),
    re_path(
        r"^update-preview/$",
        update_preview,
        name="update",
    ),
    re_path(r"^email-test/$", test_email, name="test-email"),
    re_path(
        r"^rsvp/confirm/(?P<invite_id>[\w-]+)/$", rsvp_confirm, name="rsvp-confirm"
    ),
    re_path(
        r"^reminder-email-test/(?P<invite_id>[\w-]+)/$",
        reminder_email_test,
        name="reminder-email-test",
    ),
    re_path(
        r"^reminder-email-preview/(?P<invite_id>[\w-]+)/$",
        reminder_email_preview,
        name="reminder-email-preview",
    ),
    re_path(
        r"^update-email-test/(?P<invite_id>[\w-]+)/$",
        update_email_test,
        name="update-email-test",
    ),
]
