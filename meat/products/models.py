from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        verbose_name='Категория'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(
        'Изображение',
        upload_to='products/',
        blank=True
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self) -> str:
        return self.name
