from django.urls import path,include

from user_application.views import created_user,login,update_user,created_post,singlepost,addlike,addcomment

urlpatterns = [ 
      path("",login.as_view(),name="login"),
      path("register",created_user.as_view(),name="register"),
      path("update_user/<int:id>",update_user.as_view(),name="update_user"),
      path("created_post",created_post.as_view(),name="created_post"),
      path("created_post/<int:pk>",singlepost.as_view(),name="singlepost"),
      path("like/<int:id>",addlike.as_view(),name="addlike"),
      path("addcomment/<int:id>",addcomment.as_view(),name="addcomment"),
]

