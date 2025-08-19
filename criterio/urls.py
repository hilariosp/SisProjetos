from django.urls import path
from . import views

app_name = 'criterio'

urlpatterns = [

    path('', views.index, name='criterio_index'),
    path('add/', views.add, name='criterio_add'),
    path('<int:id_criterio>/', views.detail, name='criterio_detail'),
    path('update/<int:id_criterio>/', views.update, name='criterio_update'),
    path('delete/<int:id_criterio>/', views.delete, name='criterio_delete'),

]