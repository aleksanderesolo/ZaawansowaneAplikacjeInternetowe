from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from .views import PartViewSet, SamochodViewSet, OcenaViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'czesci', PartViewSet)
router.register(r'samochody', SamochodViewSet)
router.register(r'oceny', OcenaViewSet)

urlpatterns = [
    path('', views.wszystkie, name='wszystkie'),
    path('nowy/', views.nowy, name='nowy'),
    path('edytuj/<int:id>/', views.edytuj, name='edytuj'),
    path('usun/<int:id>/', views.usun, name='usun'),
    path('szczegoly/<int:id>/', views.szczegoly, name='szczegoly'),
    path('ocena/<int:id>/', views.dodaj_ocene, name='dodaj_ocene'),
    path('szczegoly_oceny/<int:id>/', views.szczegoly_z_ocenami, name='szczegoly_oceny'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('rejestracja/', views.rejestracja, name='rejestracja'),
    path('profil/', views.moj_profil, name='moj_profil'),
    path('dodaj_samochod/', views.dodaj_samochod, name='dodaj_samochod'),
    path('edytuj_samochod/<int:id>/', views.edytuj_samochod, name='edytuj_samochod'),
    path('usun_samochod/<int:id>/', views.usun_samochod, name='usun_samochod'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Dodaj router.urls na końcu
urlpatterns += router.urls
