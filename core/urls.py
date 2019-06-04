from django.urls import path, include
from core import views

app_name = 'core'

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    # path('signup/', SignUpView.as_view(), name='register'),
    # path('login/', login_view, name='login')
    path('<name>/profile/', views.UserProfile.as_view(), name='profile'),
    path('profile/update/', views.profile, name='profile_update'),

    # pharmacy create
    path('pharmacy_create/', views.PharmacyRegister.as_view(), name='pharmacy_create'),

    # list of pharmacy users in my pharmacy
    path('<pharmacy>/pharmacists/', views.PharmacistList.as_view(), name='pharmacist_list'),
    path('is_pharmacist/', views.pharmacist_add, name='pharmacist_add')
]
