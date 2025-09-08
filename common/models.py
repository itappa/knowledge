from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Tag(models.Model):
    """タグ"""

    name = models.CharField("タグ名", max_length=50, unique=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    class Meta:
        verbose_name = "タグ"
        verbose_name_plural = "タグ"

    def __str__(self):
        return self.name


class Category(MPTTModel):
    """カテゴリ（階層構造）"""

    name = models.CharField("カテゴリ名", max_length=100)
    description = models.TextField("説明", blank=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = "カテゴリ"
        verbose_name_plural = "カテゴリ"

    def __str__(self):
        return self.name
