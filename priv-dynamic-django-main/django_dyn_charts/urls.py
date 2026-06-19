from django.urls import path
from django_dyn_charts import views 

urlpatterns = [
    path('dynamic-charts/', views.index, name="dynamic_charts"),
    path('dynamic-charts/<str:aPath>/', views.model_charts, name="model_charts"),
    path('dynamic-charts/embed/<int:aId>/', views.embed, name="chart_embed"),
    path('add-chart/', views.add_chart, name="add_chart"),
    path('delete-chart/', views.delete_chart, name="delete_chart"),
]
