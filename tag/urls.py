from django.urls import path
from . import views

app_name = 'tag'

urlpatterns = [

    path('', views.index, name='tag_index'),
    path('add/', views.add, name='tag_add'),
    path('<int:id_tag>/', views.detail, name='tag_detail'),
    path('update/<int:id_tag>/', views.update, name='tag_update'),
    path('delete/<int:id_tag>/', views.delete, name='tag_delete'),

]

