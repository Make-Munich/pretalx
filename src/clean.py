from pretalx.event.utils import create_organiser_with_user
from pretalx.person.models import User
from os import getenv

password = getenv('DJANGO_SU_PASSWORD')
email = getenv('DJANGO_SU_EMAIL')

if User.objects.filter(email=email).count()==0:
    User.objects.create_superuser(email, password)
    print('Superuser created.')
else:
    print('Superuser creation skipped.')

user = User.objects.order_by('-id').filter(is_administrator=True).first()
organiser_name = 'Make Munich Organiser'
organiser_slug = 'mmorg'

create_organiser_with_user(name=organiser_name, slug=organiser_slug, user=user)