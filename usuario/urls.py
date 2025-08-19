from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    path('', views.index, name = "usuario_index"),
    path('add/', views.add, name = "usuario_add"),
    path('delete/<int:id_usuario>/', views.delete, name = "usuario_delete"),
    path('update/<int:id_usuario>/', views.update, name = "usuario_update"),
    path('<int:id_usuario>/', views.detail, name = "usuario_detail"),
]