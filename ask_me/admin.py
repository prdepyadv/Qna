from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from .models import Answer, Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date", "view_answers")
    list_filter = ("pub_date", )
    search_fields = ("question_text__contains", )
    fields = ("question_text", "pub_date")

    def view_answers(self, obj):
        count = obj.answer_set.count()
        url = (
            reverse("admin:ask_me_answer_changelist")
            + "?"
            + urlencode({"answers__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Answers</a>', url, count)

    view_answers.short_description = "Answers"


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "answer", "approve", "disapprove")
    list_filter = ("approve", "disapprove")
    search_fields = ("answer__contains", )
