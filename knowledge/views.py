from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import Knowledge
from .forms import KnowledgeForm, KnowledgeSearchForm


class KnowledgeListView(LoginRequiredMixin, ListView):
    """ナレッジ一覧"""

    model = Knowledge
    template_name = "knowledge/knowledge_list.html"
    context_object_name = "knowledge_list"
    paginate_by = 20

    def get_queryset(self):
        queryset = Knowledge.objects.select_related("category", "author")

        # 検索フォームの処理
        form = KnowledgeSearchForm(self.request.GET)
        if form.is_valid():
            q = form.cleaned_data.get("q")
            if q:
                queryset = queryset.filter(
                    Q(title__icontains=q)
                    | Q(content__icontains=q)
                    | Q(tags__icontains=q)
                )

            category = form.cleaned_data.get("category")
            if category:
                queryset = queryset.filter(category=category)

            author = form.cleaned_data.get("author")
            if author:
                queryset = queryset.filter(author=author)

            is_public = form.cleaned_data.get("is_public")
            if is_public:
                queryset = queryset.filter(is_public=is_public)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = KnowledgeSearchForm(self.request.GET)
        return context


class KnowledgeDetailView(LoginRequiredMixin, DetailView):
    """ナレッジ詳細"""

    model = Knowledge
    template_name = "knowledge/knowledge_detail.html"
    context_object_name = "knowledge"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increment_view_count()
        return obj


class KnowledgeCreateView(LoginRequiredMixin, CreateView):
    """ナレッジ作成"""

    model = Knowledge
    form_class = KnowledgeForm
    template_name = "knowledge/knowledge_form.html"
    success_url = reverse_lazy("knowledge:knowledge_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "ナレッジを作成しました。")
        return super().form_valid(form)


class KnowledgeUpdateView(LoginRequiredMixin, UpdateView):
    """ナレッジ更新"""

    model = Knowledge
    form_class = KnowledgeForm
    template_name = "knowledge/knowledge_form.html"

    def get_success_url(self):
        return reverse_lazy("knowledge:knowledge_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "ナレッジを更新しました。")
        return super().form_valid(form)


class KnowledgeDeleteView(LoginRequiredMixin, DeleteView):
    """ナレッジ削除"""

    model = Knowledge
    template_name = "knowledge/knowledge_confirm_delete.html"
    success_url = reverse_lazy("knowledge:knowledge_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "ナレッジを削除しました。")
        return super().delete(request, *args, **kwargs)
