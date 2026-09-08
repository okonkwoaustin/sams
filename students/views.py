from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from attendances.models import AttendanceRecord
from school_sessions.models import SchoolSession
from students.models import Student, StudentEnrollment

from .forms import StudentForm


@login_required
def student_list(request):
    query = request.GET.get("q", "").strip()
    students = Student.objects.all().order_by("first_name", "last_name")

    if query:
        students = students.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(admission_number__icontains=query)
        )

    current_session = SchoolSession.objects.filter(is_current=True).first()
    enrollments_by_student = {}
    if current_session:
        enrollments = StudentEnrollment.objects.filter(
            session=current_session
        ).select_related("school_class")
        enrollments_by_student = {e.student_id: e.school_class for e in enrollments}

    paginator = Paginator(students, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    for student in page_obj:
        student.current_class = enrollments_by_student.get(student.id)

    return render(request, "students/student_list.html", {"students": page_obj})


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    enrollments = student.enrollments.select_related("school_class", "session").order_by(
        "-session__start_year"
    )
    attendance_records = (
        AttendanceRecord.objects.filter(student_enrollment__student=student)
        .select_related("attendance")
        .order_by("-attendance__date")[:15]
    )

    context = {
        "student": student,
        "enrollments": enrollments,
        "attendance_records": attendance_records,
    }
    return render(request, "students/student_detail.html", context)


@login_required
def student_add(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect("student_detail", pk=student.pk)
    else:
        form = StudentForm()

    return render(request, "students/student_form.html", {"form": form})


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_detail", pk=student.pk)
    else:
        form = StudentForm(instance=student)

    return render(request, "students/student_form.html", {"form": form, "student": student})
