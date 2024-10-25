from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from products.forms import FeedbackForm
from products.models import Category, Product

SMILES = {
    settings.SHEEPMEAT: '🐑',
    settings.BEEF: '🥩',
    settings.CHICKEN: '🍗',
    settings.PORK: '🐷',
    settings.MINCED_MEAT: '🥩',
    settings.MARINADES: '🥩',
    settings.POLUFABRIKATY: '🥟',
    settings.GRILL: '🍖',
    settings.KOPCHENIYA: '🍖',
    settings.MANGAL: '🍢',
    settings.MILK: '🥛',
    settings.WATER: '🥤'
}


def index(request):
    return render(request, 'base.html')


@cache_page(60 * 15)
def category_list(request):
    categories = Category.objects.prefetch_related('products').all()
    categories_with_products = []

    for category in categories:
        products = category.products.all()[:5]
        categories_with_products.append({
            'category': category,
            'products': products,
            'smile': SMILES.get(category.id)
        })

    context = {
        'categories_with_products': categories_with_products,
        'categories': categories,
        'active_category_id': None,
    }
    return render(request, 'products/index.html', context)


@cache_page(60 * 15)
def product_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    context = {
        'categories_with_products': [{'category': category,
                                      'products': products,
                                      'smile': SMILES.get(category.id)}],
        'categories': Category.objects.all(),
        'active_category_id': category.id,
    }
    return render(request, 'products/index.html', context)


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']

            subject = 'Новый отзыв'
            email_message = f'Имя: {name}\nEmail: {email}\nСообщение: {text}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.DEFAULT_FROM_EMAIL]
            send_mail(subject, email_message, from_email, recipient_list)
            return redirect('products:success')
    else:
        form = FeedbackForm()

    return render(request, 'products/contacts.html', {'form': form})


def success_view(request):
    form = FeedbackForm()
    return render(request, 'products/success.html', {'form': form})
