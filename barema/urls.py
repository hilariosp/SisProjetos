from django.urls import path
from . import views

app_name = 'barema'

urlpatterns = [

    path('', views.index, name='barema_index'),
    path('add/', views.add, name='barema_add'),
    path('<int:id_barema>/', views.detail, name='barema_detail'),
    path('update/<int:id_barema>/', views.update, name='barema_update'),
    path('delete/<int:id_barema>/', views.delete, name='barema_delete'),

]