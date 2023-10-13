from django.urls import path
from . import views
from .views import indexView

urlpatterns = [
    path('', indexView.as_view() , name="index"),
    path('image/<int:id>', views.image, name="image"),
]