from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from classes.models import ClassTeacher, SchoolClass
from school_sessions.models import SchoolSession
from students.models import StudentEnrollment

from .forms import SchoolClassForm


@login_required
def class_list(request):
    current_session = SchoolSession.objects.filter(is_current=True).first()

    classes = []
    for school_class in SchoolClass.objects.all().order_by("name"):
        student_count = StudentEnrollment.objects.filter(
            school_class=school_class,
            **({"session": current_session} if current_session else {}),
        ).count()

        teacher_link = ClassTeacher.objects.filter(school_class=school_class)
        if current_session:
            teacher_link = teacher_link.filter(session=current_session)
        teacher_link = teacher_link.select_related("teacher").first()

        classes.append(
            {
                "school_class": school_class,
                "student_count": student_count,
                "teacher_name": (
                    teacher_link.teacher.get_full_name() or teacher_link.teacher.username
                )
                if teacher_link
                else None,
            }
        )

    return render(request, "classes/class_list.html", {"classes": classes})


@login_required
def class_detail(request, pk):
    school_class = get_object_or_404(SchoolClass, pk=pk)
    current_session = SchoolSession.objects.filter(is_current=True).first()

    enrollments = StudentEnrollment.objects.filter(
        school_class=school_class,
        **({"session": current_session} if current_session else {}),
    ).select_related("student").order_by("student__first_name", "student__last_name")

    class_teacher = ClassTeacher.objects.filter(school_class=school_class)
    if current_session:
        class_teacher = class_teacher.filter(session=current_session)
    class_teacher = class_teacher.select_related("teacher").first()

    context = {
        "school_class": school_class,
        "enrollments": enrollments,
        "class_teacher": class_teacher,
    }
    return render(request, "classes/class_detail.html", context)


@login_required
def class_add(request):
    if request.method == "POST":
        form = SchoolClassForm(request.POST)
        if form.is_valid():
            school_class = form.save()
            return redirect("class_detail", pk=school_class.pk)
    else:
        form = SchoolClassForm()

    return render(request, "classes/class_form.html", {"form": form})
