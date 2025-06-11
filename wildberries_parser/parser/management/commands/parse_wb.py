import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from parser.services import parse_wildberries
from parser.models import Product

load_dotenv()


class Command(BaseCommand):
    help = 'Парсинг Wildberries и сохранение в базу'

    def handle(self, *args, **options):
        products = parse_wildberries(
            query=os.getenv("PRODUCT"),
            min_price=int(os.getenv("MIN_PRICE")),
            max_price=int(os.getenv("MAX_PRICE")),
            keyword=os.getenv("KEYWORD")
        )

        for product in products:
            Product.objects.create(
                name=product["name"],
                price=product["price"],
                url=product["url"],
            )

        self.stdout.write(self.style.SUCCESS(f"Сохранено {len(products)} товаров"))