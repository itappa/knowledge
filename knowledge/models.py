from django.db import models
from common.models import Category
from inquiry.models import Inquiry
from django.contrib.auth import get_user_model

User = get_user_model()


class Knowledge(models.Model):
    """ナレッジベース"""

    title = models.CharField("タイトル", max_length=200)
    content = models.TextField("内容")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="カテゴリ",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作成者")

    is_public = models.BooleanField("公開", default=True)
    view_count = models.PositiveIntegerField("閲覧回数", default=0)

    related_inquiries = models.ManyToManyField(
        Inquiry, blank=True, verbose_name="関連問い合わせ"
    )

    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    tags = models.CharField(
        "タグ", max_length=500, blank=True, help_text="カンマ区切りで入力"
    )

    class Meta:
        verbose_name = "ナレッジ"
        verbose_name_plural = "ナレッジ"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=["view_count"])
