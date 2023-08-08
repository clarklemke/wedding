from django.core.management import BaseCommand

from guests.reminder import send_all_reminders


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--send",
            action="store_true",
            dest="send",
            default=False,
            help="Actually send emails",
        )

    def handle(self, *args, **options):
        send_all_reminders(test_only=not options["send"])
