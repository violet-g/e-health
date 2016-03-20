from django.conf.urls import patterns, url
from ehealth import views

urlpatterns = patterns('',
        url(r"^$", views.index, name="index"),
        #url(r'register/', views.register, name='register'),
        #url(r"login/",views.user_login,name="login"),
        url(r"logout/",views.user_logout,name="logout"),
        url(r"^dashboard/$",views.dashboard,name="dashboard"),
        # url(r"^updateProfile/$",views.update_profile,name="profile update"),
        url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
        url(r'^test_ajax/$', views.test_ajax, name='test_ajax'),
        url(r"^search_ajax/$",views.search_ajax,name="search_ajax"),
        url(r"^add_page_ajax/$",views.add_page_ajax,name="add_page_ajax"),
        url(r'^new_folder_ajax/$', views.new_folder_ajax, name='new_folder_ajax'),
        url(r'^delete_folder_ajax/$', views.delete_folder_ajax, name='delete_folder_ajax'),
        url(r'^delete_page_ajax/$', views.delete_page_ajax, name='delete_page_ajax'),
        url(r'^checkout_folder_ajax/$', views.checkout_folder_ajax, name='checkout_folder_ajax'),
        )
