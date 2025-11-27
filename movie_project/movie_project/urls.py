from django.contrib import admin
from django.urls import path
import movie_app.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', views.search_population, name='search_movies'),
]
