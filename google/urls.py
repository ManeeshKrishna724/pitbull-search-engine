from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('register',views.register_page,name="register-page"),
    path('login',views.login_page,name="login-page"),
    path('settings/<str:obj>/conform',views.conformation_page,name="conformation-page"),
    path('settings/history',views.search_history,name="search-history"),
    path('change-password',views.password_reset,name="change-password"),
    path('settings',views.settings_page,name='settings-page'),
    path('search/<str:q>',views.search_result,name="search-result"),
    path('search/<str:q>/image/<int:page>',views.search_result_image,name="search-result-img"),
    path('search/<str:q>/image/view/',views.view_image,name="image-view"),
    path('search/<str:q>/news',views.search_result_news,name="search-result-news"),
    path('search/<str:q>/video/<int:page>',views.search_result_videos,name="search-result-videos"),
]