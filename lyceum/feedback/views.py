from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import FeedbackFileForm, FeedbackForm, UserProfileForm
from feedback.models import FeedbackFile


def feedback(request):
    template = "feedback/feedback.html"
    author = UserProfileForm(request.POST or None)
    content = FeedbackForm(request.POST or None)
    files = FeedbackFileForm(request.POST, request.FILES)
    if author.is_valid() and content.is_valid() and request.method == "POST":
        feedback_item = content.save()
        author_feedback = author.save()
        author_feedback.author = feedback_item
        author_feedback.save()

        files = request.FILES.getlist("file")
        for f in files:
            FeedbackFile.objects.create(feedback=feedback_item, file=f)

        text = content.cleaned_data["text"]
        mail = author.cleaned_data["mail"]
        send_mail(
            "Обратная связь",
            text,
            settings.EMAIL_HOST,
            [mail],
            fail_silently=False,
        )
        messages.success(request, "Форма успешно заполнена")

        return redirect("feedback:feedback")

    context = {
        "author": author,
        "content": content,
        "files": files,
    }

    return render(request, template, context)


__all__ = ["feedback"]
