from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from allauth.account.views import LoginView, SignupView
from attendances.models import Attendance
from classes.models import ClassTeacher, SchoolClass
from school_sessions.models import SchoolSession, Term
from students.models import Student, StudentEnrollment


class CustomLoginView(LoginView):
    """
    Renders our own chalkboard/ledger-styled template instead of allauth's
    default, while reusing all of allauth's login logic (email-based login,
    rate limiting, "remember me", etc.)
    """
    template_name = "signin_signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mode"] = "signin"
        return context


class CustomSignupView(SignupView):
    """
    Renders our own template for signup, while reusing allauth's signup
    logic (password validation, mandatory email verification code, etc.)
    """
    template_name = "signin_signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mode"] = "signup"
        return context


@login_required
def dashboard(request):
    current_session = SchoolSession.objects.filter(is_current=True).first()
    current_term = Term.objects.filter(is_current=True).first()

    total_students = Student.objects.count()
    total_classes = SchoolClass.objects.count()

    today = timezone.now().date()
    today_attendance = Attendance.objects.filter(date__date=today)
    today_records_count = sum(a.records.count() for a in today_attendance)
    today_present_count = sum(
        a.records.filter(status="Present").count() for a in today_attendance
    )
    today_attendance_rate = (
        round((today_present_count / today_records_count) * 100)
        if today_records_count
        else None
    )

    my_classes = []
    class_teacher_links = ClassTeacher.objects.filter(teacher=request.user)
    if current_session:
        class_teacher_links = class_teacher_links.filter(session=current_session)

    for link in class_teacher_links.select_related("school_class"):
        student_count = StudentEnrollment.objects.filter(
            school_class=link.school_class
        ).count()
        my_classes.append(
            {"school_class": link.school_class, "student_count": student_count}
        )

    recent_attendance = (
        Attendance.objects.select_related("school_class")
        .filter(teacher=request.user)
        .order_by("-date")[:6]
    )

    context = {
        "total_students": total_students,
        "total_classes": total_classes,
        "today_attendance_rate": today_attendance_rate,
        "current_term": current_term,
        "my_classes": my_classes,
        "recent_attendance": recent_attendance,
    }
    return render(request, "dashboard.html", context)
