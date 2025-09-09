from django.urls import path
from . import views

app_name = 'avaliacao'

urlpatterns = [

    path('', views.index, name='avaliacao_index'),
    path('add/', views.add, name='avaliacao_add'),
    path('<int:id_avaliacao>/', views.detail, name='avaliacao_detail'),
    path('update/<int:id_avaliacao>/', views.update, name='avaliacao_update'),
    path('delete/<int:id_avaliacao>/', views.delete, name='avaliacao_delete'),
    path('carregar-criterios/<int:id_barema>/', views.carregar_criterios_barema, name='carregar_criterios_barema'),

]