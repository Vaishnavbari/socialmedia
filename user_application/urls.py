from django.urls import path,include
from user_application.views import created_user,login,update_user
urlpatterns = [
   path("",login.as_view(),name="login"),
   path("register",created_user.as_view(),name="register"),
   path("update_user/<int:id>",update_user.as_view(),name="update_user"),
   # path("auth/",include("rest_framework.urls")),
]
