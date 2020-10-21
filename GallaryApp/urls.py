from django.urls import path

from . import views


urlpatterns = [
    # get all and post the gallary images
    path('gallaryhome/', views.GallaryListView.as_view()),
    # edit & update the images
    path("gallaryimagedetail/", views.GallaryDetailView.as_view()),
    path("gallaryimagedetail/(?p<image_id>[\w-]+)/", views.GallaryDetailView.as_view()),

]