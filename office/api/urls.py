from django.urls import path

from office.api.views.get_all_distribution_centers import get_all_distribution_centers

urlpatterns = [
    path('get-all-distribution-centers', get_all_distribution_centers, name='get_all_distribution_centers'),
]
