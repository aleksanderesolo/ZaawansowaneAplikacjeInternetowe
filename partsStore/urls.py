from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import logout
from django.shortcuts import redirect
from graphene_django.views import GraphQLView

def custom_logout_view(request):
    logout(request)
    return redirect('wszystkie')  # lub '/' jeśli to Twoja strona główna

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('parts.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='parts/login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path("graphql/", GraphQLView.as_view(graphiql=True)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)