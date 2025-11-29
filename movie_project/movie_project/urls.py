from django.contrib import admin
from django.urls import path
import movie_app.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
    path('search/', views.search_page, name='search_movies'),
]
