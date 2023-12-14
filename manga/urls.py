from django.urls import path
from . import views

app_name = 'manga'
urlpatterns = [
    path('', views.manga, name='Index'),
    path('<int:manga_id>/', views.manga_id2, name='manga'),
    path('Prueba/', views.Prueba, name='Prueba')
]
