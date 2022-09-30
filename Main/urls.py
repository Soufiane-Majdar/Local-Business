from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.home, name='home'), 
    path('detail/<int:id>', views.detail, name='detail'),
    path('favorite/<int:id>',views.favorite,name='favorite'),
    path('upload_csv',views.upload_csv, name='upload_csv'),
    # static change by form and busines id
    path('status/<int:id>',views.status,name='status'),
    # login
    path('login',views.login_user,name='login'),
    # logoout
    path('logout',views.logout_user,name='logout'),
]