from django.contrib.auth.models import User
import os
username = os.getenv('DJANGO_SU_NAME')
password = os.getenv('DJANGO_SU_PASSWORD')
email = os.getenv('DJANGO_SU_EMAIL')

if User.objects.filter(username=username).count()==0:
    User.objects.create_superuser(username, email, password)
    print('Superuser created.')
else:
    print('Superuser creation skipped.')

