from django.contrib import admin

from feedback.models import Feedback, FeedbackFile, StatusLog, UserProfile


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        Feedback.user_profile.field.name,
        Feedback.status.field.name,
    )
    readonly_fields = (Feedback.created_on.field.name,)
    list_editable = (Feedback.status.field.name,)

    def save_model(self, request, obj, form, change):
        field = Feedback.status.field.name
        if field in form.changed_data:
            StatusLog(
                user=request.user,
                feedback=obj,
                status_from=form.initial["status"],
                status_to=form.cleaned_data["status"],
            ).save()

        super().save_model(request, obj, form, change)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        UserProfile.name.field.name,
        UserProfile.mail.field.name,
    )


@admin.register(FeedbackFile)
class FeedbackFileAdmin(admin.ModelAdmin):
    list_display = (
        FeedbackFile.feedback.field.name,
        FeedbackFile.file.field.name,
    )


@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = (
        StatusLog.user.field.name,
        StatusLog.timestamp.field.name,
        StatusLog.status_from.field.name,
        StatusLog.status_to.field.name,
    )


__all__ = ["FeedbackAdmin", "StatusLogAdmin"]
