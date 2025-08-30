from django.urls import path
from . import views

app_name = 'equipe'

urlpatterns = [

    path('', views.index, name='equipe_index'),
    path('add/', views.add, name='equipe_add'),
    path('<int:id_equipe>/', views.detail, name='equipe_detail'),
    path('update/<int:id_equipe>/', views.update, name='equipe_update'),
    path('delete/<int:id_equipe>/', views.delete, name='equipe_delete'),

]
