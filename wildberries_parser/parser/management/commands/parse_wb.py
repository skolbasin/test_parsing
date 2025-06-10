from django.core.management.base import BaseCommand
from parser.services import parse_wildberries
from parser.models import Product


class Command(BaseCommand):
    help = 'Парсинг Wildberries и сохранение в базу'

    def handle(self, *args, **options):
        products = parse_wildberries(
            query="очки",
            min_price=1000,
            max_price=5000,
            color="черный"
        )

        for product in products:
            Product.objects.create(
                name=product["name"],
                price=product["price"],
                url=product["url"],
            )

        self.stdout.write(self.style.SUCCESS(f"Сохранено {len(products)} товаров"))