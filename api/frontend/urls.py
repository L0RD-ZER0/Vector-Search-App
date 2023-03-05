from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('add', views.add, name='add-report'),
    path('result', views.result, name='result'),
    path('report', views.report, name='report'),
    path('report/<int:report_id>/', views.view_report, name='homepage'),
]
