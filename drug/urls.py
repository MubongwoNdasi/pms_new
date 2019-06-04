from django.urls import path, include
from drug import views


app_name = "drug"

urlpatterns = [
    path('', views.DrugList.as_view(), name='list'),
    path('<pharmacy>/drugs/', views.DrugsPharmacy.as_view(), name='pharmacy_drugs'),

    # adding drug to cart
    path('add_to_cart/<slug>/', views.add_to_cart, name='add_to_cart'),

    # remove drug from cart
    path('remove_from_cart/<slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove_single_drug_from_cart/<slug>/', views.remove_single_drug_from_cart, name='remove_single_drug_from_cart'),

    # view cart
    path('order-summary/', views.OrderSummary.as_view(), name='order_summary'),

    # CRUD urls
    path('register/', views.DrugRegister.as_view(), name='register'),
    path('<slug>/', views.DrugDetail.as_view(), name='detail'),
    path('<slug>/edit/', views.DrugEdit.as_view(), name='edit'),
    path('<slug>/delete/', views.DrugDelete.as_view(), name='delete'),

    # list of expired drugs
    path('<pharmacy>/expired_drugs/', views.DrugsExpired.as_view(), name='expired_drugs'),
]


