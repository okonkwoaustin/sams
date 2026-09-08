from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from classes.models import SchoolClass
from school_sessions.models import SchoolSession, Term
from students.models import StudentEnrollment

from .models import Attendance, AttendanceRecord


@login_required
def attendance_take(request, class_id):
    school_class = get_object_or_404(SchoolClass, pk=class_id)
    current_session = SchoolSession.objects.filter(is_current=True).first()
    current_term = Term.objects.filter(is_current=True).first()
    today = timezone.now().date()

    enrollments = StudentEnrollment.objects.filter(
        school_class=school_class,
        **({"session": current_session} if current_session else {}),
    ).select_related("student").order_by("student__first_name", "student__last_name")

    # Find (but don't create yet) today's register for this class, if one exists.
    attendance = Attendance.objects.filter(
        school_class=school_class, date__date=today
    ).first()

    existing_status = {}
    if attendance:
        existing_status = {
            r.student_enrollment_id: r.status
            for r in attendance.records.all()
        }

    if request.method == "POST":
        if not current_term:
            return render(
                request,
                "attendances/attendance_take.html",
                {
                    "school_class": school_class,
                    "term": None,
                    "today": today,
                    "enrollments": [],
                    "error": "No current term is set up — ask an admin to mark one active.",
                },
            )

        if attendance is None:
            attendance = Attendance.objects.create(
                school_class=school_class,
                term=current_term,
                date=timezone.now(),
                teacher=request.user,
            )

        for enrollment in enrollments:
            status = request.POST.get(f"status_{enrollment.id}")
            if not status:
                continue
            AttendanceRecord.objects.update_or_create(
                attendance=attendance,
                student_enrollment=enrollment,
                defaults={"status": status},
            )

        return redirect("attendance_detail", pk=attendance.pk)

    for enrollment in enrollments:
        enrollment.current_status = existing_status.get(enrollment.id)

    context = {
        "school_class": school_class,
        "term": current_term,
        "today": today,
        "enrollments": enrollments,
    }
    return render(request, "attendances/attendance_take.html", context)


@login_required
def attendance_history(request):
    class_filter = request.GET.get("class")

    attendances = Attendance.objects.select_related("school_class", "term").order_by(
        "-date"
    )
    if class_filter:
        attendances = attendances.filter(school_class_id=class_filter)

    for attendance in attendances:
        total = attendance.records.count()
        present = attendance.records.filter(status="Present").count()
        attendance.present_rate = round((present / total) * 100) if total else 0

    context = {
        "attendances": attendances[:100],
        "all_classes": SchoolClass.objects.all().order_by("name"),
    }
    return render(request, "attendances/attendance_history.html", context)


@login_required
def attendance_detail(request, pk):
    attendance = get_object_or_404(
        Attendance.objects.select_related("school_class", "term", "teacher"), pk=pk
    )
    records = attendance.records.select_related(
        "student_enrollment__student"
    ).order_by("student_enrollment__student__first_name")

    context = {"attendance": attendance, "records": records}
    return render(request, "attendances/attendance_detail.html", context)
