from django.urls import path
from .views import DecoratedTokenObtainPairView, DecoratedTokenRefreshView
from . import views
urlpatterns = [
    path('', views.CreateRetrieveUpdateUserViewset.as_view({'post':'create'}), name='create-user'),
    path('<str:email>/', views.CreateRetrieveUpdateUserViewset.as_view({'get':'retrieve', 'put':'update'}), name='retrieve-update-user'),
    path('api/token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),



]
