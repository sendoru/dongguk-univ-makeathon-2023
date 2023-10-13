from django.urls import path
from . import views
from .views import indexView

urlpatterns = [
    path('', indexView.as_view() , name="index"),
    path('image/<int:id>', views.image, name="image"),
    path('is_machine_ready', views.machine_ready, name="is_machine_ready"),
    path('ready_from_backend', views.ready_from_backend, name="ready_from_backend"),
    path('page_loaded', views.pageLoaded, name="page_loaded"),
]