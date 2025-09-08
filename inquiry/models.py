from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from common.models import Category, Tag

User = get_user_model()


class Inquiry(models.Model):
    """問い合わせ"""

    STATUS_CHOICES = [
        ("new", "新規"),
        ("in_progress", "対応中"),
        ("waiting", "保留"),
        ("resolved", "解決済み"),
        ("closed", "完了"),
    ]

    PRIORITY_CHOICES = [
        ("low", "低"),
        ("medium", "中"),
        ("high", "高"),
        ("urgent", "緊急"),
    ]

    title = models.CharField("件名", max_length=200)
    content = models.TextField("内容")
    customer_name = models.CharField("顧客名", max_length=100)
    customer_email = models.EmailField("顧客メールアドレス")
    customer_phone = models.CharField("顧客電話番号", max_length=20, blank=True)

    status = models.CharField(
        "ステータス", max_length=20, choices=STATUS_CHOICES, default="new"
    )
    priority = models.CharField(
        "優先度", max_length=20, choices=PRIORITY_CHOICES, default="medium"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="カテゴリ",
    )
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="担当者"
    )

    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)
    resolved_at = models.DateTimeField("解決日時", null=True, blank=True)

    tags = models.ManyToManyField(Tag, blank=True, verbose_name="タグ")

    class Meta:
        verbose_name = "問い合わせ"
        verbose_name_plural = "問い合わせ"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.customer_name}"

    def save(self, *args, **kwargs):
        if self.status == "resolved" and not self.resolved_at:
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)


class Response(models.Model):
    """対応履歴"""

    inquiry = models.ForeignKey(
        Inquiry,
        on_delete=models.CASCADE,
        related_name="responses",
        verbose_name="問い合わせ",
    )
    responder = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="対応者")
    content = models.TextField("対応内容")
    is_internal = models.BooleanField(
        "内部メモ", default=False, help_text="顧客には表示されない内部メモ"
    )
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    class Meta:
        verbose_name = "対応履歴"
        verbose_name_plural = "対応履歴"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.inquiry.title} - {self.responder}"


class Attachment(models.Model):
    """添付ファイル"""

    inquiry = models.ForeignKey(
        Inquiry,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name="問い合わせ",
    )
    file = models.FileField("ファイル", upload_to="inquiry_attachments/")
    filename = models.CharField("ファイル名", max_length=255)
    uploaded_at = models.DateTimeField("アップロード日時", auto_now_add=True)

    class Meta:
        verbose_name = "添付ファイル"
        verbose_name_plural = "添付ファイル"

    def __str__(self):
        return self.filename
