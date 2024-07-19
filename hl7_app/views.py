from django.shortcuts import render
from hl7_app.models import ErrorCharges
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, View, TemplateView
# Create your views here.

class ListError(ListView):
    template_name = 'error_cards.html'
    model = ErrorCharges
    context_object_name = 'errors'

    def get_context_data(self, **kwargs):
        # Get the default context from the superclass
        context = super().get_context_data(**kwargs)
        
        # Add custom context for error counts
        context['error_counts'] = {
            'patient_name_not_found': ErrorCharges.objects.filter(error_type='Patient name not found').count(),
            'dob_not_found': ErrorCharges.objects.filter(error_type='DOB not found').count(),
            'other_error': ErrorCharges.objects.filter(error_type='Other error').count(),  
        }
        
        return context