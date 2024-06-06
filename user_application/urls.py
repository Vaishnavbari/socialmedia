from django.urls import path,include
from user_application.views import created_user,userlogin,update_user,created_post,addlike,addcomment,singlepost,Logout_user,forgot_password, password_confirm_mail
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [ 
    
      path("",userlogin.as_view(),name="login"),
      path("register",created_user.as_view(),name="register"),
      path("update_user/<int:id>",update_user.as_view(),name="update_user"),
      path("created_post",created_post.as_view(),name="created_post"),
      path("single_post",singlepost.as_view(),name="singlepost"),
      path("single_post/<int:pk>",singlepost.as_view(),name="singlepost"),
      path("like/<int:id>",addlike.as_view(),name="addlike"),
      path("addcomment/<int:id>",addcomment.as_view(),name="addcomment"),
      path("delete_comment/<int:id>",addcomment.as_view(),name="deltecomment"),
      path("edit_comment/<int:id>",addcomment.as_view(),name="edit_comment"),
      path("Logout_user",Logout_user.as_view(),name="Logout_user"),
      path("forgot_password",forgot_password.as_view(),name="forgot password"),
      path("password_request_confirm/<uidb64>/<token>/",password_confirm_mail.as_view(),name="password_reset_confirm"),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)