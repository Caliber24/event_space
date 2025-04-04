from django.urls import path
from . import views
urlpatterns = [
    path('', views.CreateRetrieveUpdateUserViewset.as_view({'post':'create'}), name='create-user'),
    path('<str:email>/', views.CreateRetrieveUpdateUserViewset.as_view({'get':'retrieve', 'put':'update'}), name='retrieve-update-user')

]
