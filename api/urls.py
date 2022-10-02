from django.urls import path

from .views import Enrollment, EnrollmentView, MarkView
from .views import CompanyView
from .views import EmployeeView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('companies/', CompanyView.as_view(), name='companies_list'),
    path('employee/', EmployeeView.as_view(), name='Employee_list'),
    path('enrollment/', EnrollmentView.as_view(), name='Enrollment_list'),
    path('mark/', MarkView.as_view(), name='Mark_list') 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)