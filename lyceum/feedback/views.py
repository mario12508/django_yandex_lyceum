from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import FeedbackForm


def feedback(request):
    template = "feedback/feedback.html"
    feedback_form = FeedbackForm(request.POST or None)
    if feedback_form.is_valid() and request.method == "POST":
        feedback_form.save()
        text = feedback_form.cleaned_data["text"]
        mail = feedback_form.cleaned_data["mail"]
        result = send_mail(
            "Обратная связь",
            text,
            settings.DJANGO_MAIL,
            [mail],
            fail_silently=False,
        )
        if result:
            messages.success(request, "Форма успешно заполнена")
        else:
            messages.error(request, "Не удалось отправить письмо.")

        return redirect("feedback:feedback")

    context = {"form": feedback_form}

    return render(request, template, context)


__all__ = ["feedback"]
