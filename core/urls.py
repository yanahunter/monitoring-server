from django.urls import path

from core.views import ReportView, ComputersTemplateVew, HistogramsTemplateView

urlpatterns = [
    path('report/', ReportView.as_view()),
    path('computers/', ComputersTemplateVew.as_view()),
    path('computers/<str:computer_id>/', HistogramsTemplateView.as_view()),
]
