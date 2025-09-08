from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category
from knowledge.models import Knowledge
from inquiry.models import Inquiry
from django.db.models import Count


@login_required
def dashboard(request):
    """ダッシュボード"""
    # 統計情報
    total_inquiries = Inquiry.objects.count()
    new_inquiries = Inquiry.objects.filter(status="new").count()
    in_progress_inquiries = Inquiry.objects.filter(status="in_progress").count()
    urgent_inquiries = Inquiry.objects.filter(priority="urgent").count()

    # 最近の問い合わせ
    recent_inquiries = Inquiry.objects.select_related("category", "assigned_to")[:10]

    # 最近のナレッジ
    recent_knowledge = Knowledge.objects.select_related("category", "author")[:5]

    # カテゴリ別統計
    category_stats = Category.objects.annotate(inquiry_count=Count("inquiry")).order_by(
        "-inquiry_count"
    )[:10]

    # 担当者別統計
    from django.contrib.auth import get_user_model

    User = get_user_model()
    assignee_stats = (
        User.objects.filter(is_staff=True)
        .annotate(assigned_count=Count("inquiry"))
        .order_by("-assigned_count")[:10]
    )

    context = {
        "total_inquiries": total_inquiries,
        "new_inquiries": new_inquiries,
        "in_progress_inquiries": in_progress_inquiries,
        "urgent_inquiries": urgent_inquiries,
        "recent_inquiries": recent_inquiries,
        "recent_knowledge": recent_knowledge,
        "category_stats": category_stats,
        "assignee_stats": assignee_stats,
    }

    return render(request, "common/dashboard.html", context)
