from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', views.Verify.as_view(), name='token_verify'),
    path('Register/', views.Register.as_view()),
    path('ShowBars/', views.ShowBars.as_view()),
    path('ShowBarInfo/', views.ShowBarInfo.as_view()),
    path('UpdateUserInfo/', views.UpdateUserInfo.as_view()),
    path('AddBar/', views.AddBar.as_view()),
    path('UpdateBar/', views.UpdateBar.as_view()),
    path('ShowUserBarHistory/', views.ShowUserBarHistory.as_view()),
    path('RemoveBar/', views.RemoveBar.as_view()),
    path('AcceptBar/', views.AcceptBar.as_view()),
    path('SubmitPosition/', views.SubmitPosition.as_view()),
    path('GetDate/', views.GetDate.as_view()),
    # path('CancelBar/', views.RemoveBar.as_view()),
    # path('Authenticate/', views.Authenticate.as_view()),
    ]
