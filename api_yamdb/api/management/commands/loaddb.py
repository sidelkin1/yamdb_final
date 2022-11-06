import datetime
from pathlib import Path

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from sqlalchemy import create_engine


class Command(BaseCommand):
    help = 'Load YaMDB database'

    DB_URI = (
        'postgresql://'
        f'{settings.DATABASES["default"]["USER"]}'
        f':{settings.DATABASES["default"]["PASSWORD"]}'
        f'@{settings.DATABASES["default"]["HOST"]}'
        f':{settings.DATABASES["default"]["PORT"]}'
        f'/{settings.DATABASES["default"]["NAME"]}'
    )

    TABLES_PATH = Path(settings.STATIC_ROOT).joinpath('data')

    DB_TABLES = {
        'users.csv': 'users_user',
        'category.csv': 'titles_category',
        'genre.csv': 'titles_genre',
        'titles.csv': 'titles_title',
        'genre_title.csv': 'titles_title_genre',
        'review.csv': 'reviews_review',
        'comments.csv': 'reviews_comment',
    }

    CONVERTERS = {
        'pub_date': lambda x: pd.to_datetime(x).tz_localize(None),
        'bio': str,
        'first_name': str,
        'last_name': str,
    }

    COLUMNS = {
        'author': 'author_id',
        'review': 'review_id',
        'title': 'title_id',
        'genre': 'genre_id',
        'category': 'category_id',
    }

    def handle(self, *args, **options):
        try:
            engine = create_engine(self.DB_URI)

            with engine.connect().execution_options(autocommit=True) as conn:
                self.stdout.write(
                    self.style.SUCCESS('Успешное подключение к БД')
                )

                for file_name, table_name in self.DB_TABLES.items():
                    self.stdout.write(
                        self.style.NOTICE(
                            f'Обработка таблицы {table_name}... '
                        ),
                        ending='',
                    )

                    path = self.TABLES_PATH.joinpath(file_name)
                    df = pd.read_csv(path, converters=self.CONVERTERS)
                    df.rename(columns=self.COLUMNS, inplace=True)

                    if table_name == 'users_user':
                        df = df.assign(
                            password='12345',
                            last_login=pd.NaT,
                            is_superuser=False,
                            is_staff=False,
                            is_active=True,
                            date_joined=datetime.datetime.now(),
                        )
                    elif table_name == 'titles_title':
                        df = df.assign(description=None)

                    df.to_sql(
                        name=table_name,
                        con=conn,
                        if_exists='append',
                        index=False,
                        index_label='id'
                    )

                    self.stdout.write(
                        self.style.SUCCESS('OK')
                    )

        except Exception as error:
            raise CommandError(error) from error
        finally:
            engine.dispose()
