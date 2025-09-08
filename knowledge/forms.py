from django import forms
from django.contrib.auth import get_user_model
from .models import Knowledge
from common.models import Category

User = get_user_model()


class KnowledgeForm(forms.ModelForm):
    """ナレッジフォーム"""

    class Meta:
        model = Knowledge
        fields = ["title", "content", "category", "is_public", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "tags": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "カンマ区切りで入力"}
            ),
        }


class KnowledgeSearchForm(forms.Form):
    """ナレッジ検索フォーム"""

    q = forms.CharField(
        label="キーワード検索",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "タイトル、内容で検索"}
        ),
    )
    category = forms.ModelChoiceField(
        label="カテゴリ",
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    author = forms.ModelChoiceField(
        label="作成者",
        queryset=User.objects.filter(is_staff=True),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    is_public = forms.ChoiceField(
        label="公開状態",
        choices=[("", "すべて"), ("True", "公開"), ("False", "非公開")],
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
