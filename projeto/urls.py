from django.urls import path
from . import views

app_name = 'projeto'

urlpatterns = [
    path('', views.index, name='projeto_index'),
    path('<int:id_projeto>/', views.detail, name='projeto_detail'),
    path('add/', views.add, name='projeto_add'),
    path('update/<int:id_projeto>/', views.update, name='projeto_update'),
    path('delete/<int:id_projeto>/', views.delete, name='projeto_delete'),
]