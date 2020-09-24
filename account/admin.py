from django.contrib import admin
from account.models import User,Teacher,Student,McqExam,Question,Student_Response,Results
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name","username","email")
    list_filter = ("is_admin","is_teacher","is_student")
    search_fields = ("first_name","last_name")
    ordering = ("first_name",)
    readonly_fields=["password"]

    def save_model(self, request, obj, form, change):
        user_database = User.objects.get(pk=obj.pk)
    # Check firs the case in which the password is not encoded, then check in the case that the password is encode
        if not (check_password(form.data['password'], user_database.password) or user_database.password == form.data['password']):
            obj.password = make_password(obj.password)
        else:
            obj.password = user_database.password
        super().save_model(request, obj, form, change)

@admin.register(Teacher)
class TeacherAdmin(UserAdmin):
    list_display = ("name","username","email")
    list_filter = ("department","subject",)
    search_fields = ("first_name","last_name")
    ordering = ("first_name",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("sap_id","name","email")
    list_filter = ("department","division")
    search_fields = ("sap_id",)
    ordering = ("sap_id",)


admin.site.register(McqExam)
admin.site.register(Question)
admin.site.register(Student_Response)
admin.site.register(Results)
