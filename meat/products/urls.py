from django.urls import path

from . import views


app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.product_list,
         name='product_list'),
    path('contacts/', views.feedback, name='contacts'),
    path('success/', views.success_view, name='success'),

]
