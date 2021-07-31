from django.urls import path, include
from . import views
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
# router.register(r'insectdata', views.InsectDataViewSet)
# router.register(r'transaction', views.TransactionViewSet)
# router.register(r'transactionmedia', views.TransactionMediaViewSet)


urlpatterns = [
    path('listen/', views.incoming_message, name='webhook_message'),
    path('', include(router.urls)),
    path('login_api/', views.LoginUserApi.as_view(), name='login_api'),
    path('registration_api/', views.RegistrationApi.as_view(), name='registration_api'),
    path('userprofile_api/', views.UserProfileApi.as_view(), name='userprofile_api'),
    path('transaction_api/', views.CreateTransaction.as_view(), name='transaction_api'),
    path('transactionbyuuid_api/', views.GetTransactionByUUID.as_view(), name='transactionbyuuid_api'),
]

app_name = 'api'








