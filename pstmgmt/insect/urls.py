from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dashboard', views.dashboard, name='insect_dashboard'),
    path('report', views.transaction_report, name='transaction_report'),
    path('add', views.add, name='add_insect'),
    path('view', views.view_insect, name='view_insect'),
    path('view_info/<int:id>', views.view_info, name='view_info'),
    path('show', views.show_insect, name='show_insect'),
    path('insert', views.insert, name='insert_ins'),
    path('insert_insect', views.insert_insect, name ='insert_insect'),
    path('add_new_insect', views.add_new_insect, name='add_new_insect'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('delete_insect/<int:id>', views.delete_insect, name='delete_insect'),
    path('update/<int:id>', views.update, name='update'),
    path('edit/<int:id>', views.edit_insect, name='edit_insect'),
    path('show_info_insect/<int:id>', views.show_info_insect, name='show_info_insect'),

]

app_name = 'insect'