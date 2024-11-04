from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import FeedbackFileForm, FeedbackForm, UserProfileForm
from feedback.models import FeedbackFile


def feedback(request):
    template = "feedback/feedback.html"
    user_profile_form = UserProfileForm(request.POST or None)
    feedback_form = FeedbackForm(request.POST or None)
    feedback_file_form = FeedbackFileForm(request.POST, request.FILES)
    if (
        user_profile_form.is_valid()
        and feedback_form.is_valid()
        and request.method == "POST"
    ):
        user_profile = user_profile_form.save()
        feedbac = feedback_form.save(commit=False)
        feedbac.user_profile = user_profile
        feedbac.save()

        files = request.FILES.getlist("file")
        for f in files:
            FeedbackFile.objects.create(feedback=feedbac, file=f)

        text = feedback_form.cleaned_data["text"]
        mail = user_profile_form.cleaned_data["mail"]
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
        "user_profile_form": user_profile_form,
        "feedback_form": feedback_form,
        "feedback_file_form": feedback_file_form,
    }

    return render(request, template, context)


__all__ = ["feedback"]
