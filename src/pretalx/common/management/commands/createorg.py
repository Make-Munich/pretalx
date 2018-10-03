from urllib.parse import urljoin

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from django.urls import reverse
from django.utils.translation import ugettext as _

from pretalx.event.utils import create_organiser_with_user
from pretalx.person.models import User


def get_nonempty(prompt):
    result = input(prompt).strip()
    while not result:
        result = input(
            _('This value is required, please enter some value to proceed: ')
        )
    return result


class Command(BaseCommand):
    help = 'Initializes your pretalx instance. Only to be used once.'

    @transaction.atomic
    def handle(self, *args, **options):
        user = User.objects.order_by('-id').filter(is_administrator=True).first()
        organiser_name = 'Make Munich Organiser'
        organiser_slug = 'mmorg'

        organiser, team = create_organiser_with_user(
            name=organiser_name, slug=organiser_slug, user=user
        )

        event_url = urljoin(settings.SITE_URL, reverse('orga:event.create'))
        team_url = urljoin(
            settings.SITE_URL,
            reverse(
                'orga:organiser.teams.view',
                kwargs={'organiser': organiser.slug, 'pk': team.pk},
            ),
        )
        self.stdout.write(self.style.SUCCESS(_('\nNow that this is done, you can:')))
        self.stdout.write(
            _(' - Create your first event at {event_url}').format(event_url=event_url)
        )
        self.stdout.write(
            _(
                ' - Invite somebody to the organiser team at {team_url} and let them create the event'
            ).format(team_url=team_url)
        )
        self.stdout.write(
            _(
                ' - Use the command "import_schedule /path/to/schedule.xml" if you want to import an event."'
            )
        )
