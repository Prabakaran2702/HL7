from django.urls import path
from . import views
from django.views.generic import TemplateView
app_name = 'hl7'

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html') , name='index'),
    path('errors/', views.ListError.as_view(), name='error_cards'),
]