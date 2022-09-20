import uuid

from django.db import models


def _random_uuid():
    return uuid.uuid4().hex


class Party(models.Model):
    """
    A party consists of one or more guests.
    """

    name = models.TextField()
    email = models.EmailField(max_length=254, unique=True)
    invitation_id = models.CharField(
        max_length=32, db_index=True, default=_random_uuid, unique=True
    )
    save_the_date_sent = models.DateTimeField(null=True, blank=True, default=None)
    save_the_date_viewed = models.DateTimeField(null=True, blank=True, default=None)
    invite_sent = models.DateTimeField(null=True, blank=True, default=None)
    invite_viewed = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        """Return string representation."""
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def ordered_guests(self):
        return self.guest_set.order_by("pk")

    @property
    def any_guests_attending_canada(self):
        return any(self.guest_set.values_list("attending_canada", flat=True))

    @property
    def any_guests_attending_france(self):
        return any(self.guest_set.values_list("attending_france", flat=True))

    class Meta:
        db_table = "party"


class Guest(models.Model):
    """An event guest"""

    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    name = models.TextField()
    attending_canada = models.BooleanField(null=True, default=None)
    attending_france = models.BooleanField(null=True, default=None)
    dietary_restrictions = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        """Return string representation."""
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def unique_id(self):
        # convert to string so it can be used in the "add" templatetag
        return str(self.pk)

    class Meta:
        db_table = "guests"
