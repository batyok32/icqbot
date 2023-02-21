from typing import OrderedDict
from django.core.management.base import BaseCommand
from faker import Faker

# import faker.providers
from django.utils.text import slugify
from main.models import VpnKey


def run():
    vpns = VpnKey.objects.all()
    for vpn in vpns:
        print(vpn.name)

    # letters = ["b", "d", "e"]
    # for letter in letters:
    #     print(f"Start Creating {letter}")
    #     for i in range(60):
    #         i += 1
    #         text = f"{letter}{i}"
    #         vpnket = VpnKey.objects.create(name=text)
    #         vpnket.save()
    #     print(f"Created {letter}")
