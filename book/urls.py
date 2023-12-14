from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.index, name='Index'),
    path('<int:book_id>/', views.book_index, name='book'),
    path('<int:book_id>/<str:chapter>/', views.book_id, name='book_show')
]
