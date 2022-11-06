import os

from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


class Command(createsuperuser.Command):
    help = 'Create a superuser'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--password',
            dest='password',
            default=None,
            help='Specifies the password for the superuser.',
        )

    def handle(self, *args, **options):
        username = os.getenv(
            'DJANGO_SUPERUSER_USERNAME',
            options.get('username')
        )
        email = os.getenv(
            'DJANGO_SUPERUSER_EMAIL',
            options.get('email')
        )
        password = os.getenv(
            'DJANGO_SUPERUSER_PASSWORD',
            options.get('password')
        )
        database = options.get('database')

        if password and not username:
            raise CommandError(
                '--username is required if specifying --password'
            )

        options.update({
            'username': username,
            'password': password,
            'email': email
        })
        super(Command, self).handle(*args, **options)

        if password:
            user = self.UserModel._default_manager.db_manager(database).get(
                username=username
            )
            user.set_password(password)
            user.save()
