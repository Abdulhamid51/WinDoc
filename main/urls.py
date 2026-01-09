from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    # path("", IndexView.as_view(), name="index"),
    # path("doc/<int:id>", DetailView.as_view(), name="doc"),
    path('', FormView.as_view(), name='form'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('get-universities/', get_universities, name='get_universities'),
    path('get-university-details/', get_university_details, name='get_university_details'),
    path('save-university/', save_university, name='save_university'),
    path('get-applicants/', get_applicants, name='get_applicants'),
    path('get-applicant-details/', get_applicant_details, name='get_applicant_details'),
    path('delete-applicant/', delete_applicant, name='delete_applicant'),
    path('document/<int:pk>/', ApplicationDocumentView.as_view(), name='application_document'),
]
