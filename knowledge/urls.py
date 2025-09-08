from django.urls import path
from . import views

app_name = "knowledge"

urlpatterns = [
    path("", views.KnowledgeListView.as_view(), name="knowledge_list"),
    path(
        "create/",
        views.KnowledgeCreateView.as_view(),
        name="knowledge_create",
    ),
    path(
        "<int:pk>/",
        views.KnowledgeDetailView.as_view(),
        name="knowledge_detail",
    ),
    path(
        "<int:pk>/edit/",
        views.KnowledgeUpdateView.as_view(),
        name="knowledge_update",
    ),
    path(
        "<int:pk>/delete/",
        views.KnowledgeDeleteView.as_view(),
        name="knowledge_delete",
    ),
]
