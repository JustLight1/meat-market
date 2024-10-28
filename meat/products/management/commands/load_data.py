import time

import requests
from django.conf import settings
from django.core.management import BaseCommand

from products.models import Category, Product


categories_id = {
    67903: 'Баранина',
    67902: 'Говядина',
    67905: 'Курица',
    67837: 'Свинина',
    68199: 'Фарш',
    68161: 'Маринады',
    68163: 'Полуфабрикаты',
    68178: 'Горячка гриль',
    68173: 'Горячка копчения',
    68182: 'Горячка мангал',
    67845: 'Молочка',
}


def get_data(group_id):

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9,zh;q=0.8,uk;q=0.7',
        'authorization': f'Bearer {settings.API_TOKEN}',
        'dnt': '1',
        'origin': settings.MAIN_URL,
        'priority': 'u=1, i',
        'referer': settings.MAIN_URL,
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': settings.USER_AGENT,
    }

    params = {
        'page': '0',
        'size': '50',
        'menuId': settings.MENU_ID,
        'groupId': group_id,
        'sort': 'createdDate,desc',
    }
    try:
        response = requests.get(
            settings.API_URL,
            params=params,
            headers=headers,
        )
        response.raise_for_status()
        return response.json().get('rows')
    except requests.RequestException as e:
        print(f'Ошибка при запросе данных с API: {e}')
        return []


class Command(BaseCommand):
    help = ('Запуск: python manage.py load_data.')

    def handle(self, *args, **options):
        print('Старт')
        try:
            for group_id, group_name in categories_id.items():
                time.sleep(2)

                products_list = get_data(group_id)
                if not products_list:
                    continue

                category, _ = Category.objects.get_or_create(
                    name=group_name
                )

                existing_products = {
                    product.name: product for product in
                    Product.objects.filter(category=category)
                }

                new_products = []
                updated_products = []

                for product_data in products_list:
                    product_name = product_data.get('name')
                    product_price = product_data.get(
                        'variations', [{}]
                    )[0].get('price')

                    existing_product = existing_products.get(product_name)

                    if existing_product:
                        if existing_product.price != product_price:
                            existing_product.price = product_price
                            updated_products.append(existing_product)
                    else:
                        new_products.append(
                            Product(name=product_name, category=category,
                                    price=product_price))

                if new_products:
                    Product.objects.bulk_create(new_products)
                    print(
                        f'Добавлено #{len(new_products)} новых продуктов в '
                        f'категорию *{group_name}*'
                    )
                else:
                    print(
                        f'Новых товаров в категории *{group_name}*, не '
                        'появилось'
                    )

                if updated_products:
                    Product.objects.bulk_update(updated_products, ['price'])
                    print(
                        f'Обновлено #{len(updated_products)} продуктов в '
                        f'категории *{group_name}*'
                    )
                else:
                    print(
                        f'Цены в категории *{group_name}* на товары, остались '
                        'прежними'
                    )

        except Exception as e:
            print(f'Ошибка при выполнении: {e}')
        finally:
            print('Работа завершена успешно!')
