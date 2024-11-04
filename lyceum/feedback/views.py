from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import FeedbackFileForm, FeedbackForm, UserProfileForm
from feedback.models import FeedbackFile


def feedback(request):
    template = "feedback/feedback.html"
    author_form = UserProfileForm(request.POST or None)
    content_form = FeedbackForm(request.POST or None)
    files_form = FeedbackFileForm(request.POST, request.FILES)
    if (
        author_form.is_valid()
        and content_form.is_valid()
        and request.method == "POST"
    ):
        feedback_item = content_form.save()
        author_profile = author_form.save(commit=False)
        author_profile.author = feedback_item
        author_profile.save()

        files_form = request.FILES.getlist("file")
        for f in files_form:
            FeedbackFile.objects.create(feedback=feedback_item, file=f)

        text = content_form.cleaned_data["text"]
        mail = author_form.cleaned_data["mail"]
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
        "author_form": author_form,
        "content_form": content_form,
        "files_form": files_form,
    }

    return render(request, template, context)


__all__ = ["feedback"]
