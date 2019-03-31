from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homeview),
    path('post/<int:pk>', views.blogPageView),
    path('login/',views.signin),
    path('signup/',views.signup),
    path('create/',views.create_post),
    path('logout/',views.logout_user),
    path('delete/<int:pk>/', views.delete_post),
    path('post/<int:pk>/edit/', views.edit_post),
]