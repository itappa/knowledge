from django.urls import path
from . import views

app_name = "inquiry"

urlpatterns = [
    path("", views.InquiryListView.as_view(), name="inquiry_list"),
    path("create/", views.InquiryCreateView.as_view(), name="inquiry_create"),
    path("<int:pk>/", views.InquiryDetailView.as_view(), name="inquiry_detail"),
    path(
        "<int:pk>/edit/",
        views.InquiryUpdateView.as_view(),
        name="inquiry_update",
    ),
    path(
        "<int:pk>/delete/",
        views.InquiryDeleteView.as_view(),
        name="inquiry_delete",
    ),
    # AJAX用
    path(
        "<int:pk>/status/",
        views.inquiry_status_update,
        name="inquiry_status_update",
    ),
    path("<int:pk>/assign/", views.inquiry_assign, name="inquiry_assign"),
]
