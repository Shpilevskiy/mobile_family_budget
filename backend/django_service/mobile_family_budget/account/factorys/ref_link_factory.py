from datetime import datetime, timedelta

from factory import (
    DjangoModelFactory,
    PostGenerationMethodCall
)

from account.models import RefLink


class RefLinkFactory(DjangoModelFactory):
    class Meta:
        model = RefLink
        django_get_or_create = ('creation_date', 'expire_date', 'activation_count')

    link = PostGenerationMethodCall('generate_new_link')
    creation_date = datetime.now()
    expire_date = datetime.now() + timedelta(days=10)
    activation_count = 3
