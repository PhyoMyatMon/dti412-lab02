"""Page handlers for the CoursePortal catalog app."""

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import Http404
from django.shortcuts import render

from .data import COURSES_DATA


def home_view(request):
    """Render the homepage with a course count and featured course."""
    context = {
        "total_courses": len(COURSES_DATA),
        "featured_course": COURSES_DATA[0],
    }
    return render(request, "catalog/home.html", context)


def course_list_view(request):
    """Render courses, optionally filtered by the q search parameter."""
    query = request.GET.get("q", "").strip()
    normalized_query = query.casefold()
    courses = [
        course
        for course in COURSES_DATA
        if not normalized_query
        or normalized_query in course["title"].casefold()
        or normalized_query in course["code"].casefold()
    ]
    return render(
        request,
        "catalog/course_list.html",
        {"courses": courses, "query": query},
    )


def course_detail_view(request, course_id):
    """Render the requested syllabus or return a 404 for an unknown ID."""
    course = next(
        (item for item in COURSES_DATA if item["id"] == course_id),
        None,
    )
    if course is None:
        raise Http404("Course with specified ID was not found.")
    return render(request, "catalog/course_detail.html", {"course": course})


def inquiry_view(request):
    """Validate an inquiry POST and render the form or its result."""
    form_data = {
        "student_name": "",
        "email": "",
        "course_code": "",
        "message": "",
    }
    errors = []
    submitted_data = None

    if request.method == "POST":
        form_data = {
            field: request.POST.get(field, "").strip()
            for field in form_data
        }

        if not form_data["student_name"]:
            errors.append("Student Name is required.")

        if not form_data["email"]:
            errors.append("A valid Email address is required.")
        else:
            try:
                validate_email(form_data["email"])
            except ValidationError:
                errors.append("A valid Email address is required.")

        if not form_data["message"]:
            errors.append("Inquiry message cannot be empty.")

        valid_course_codes = {course["code"] for course in COURSES_DATA}
        if form_data["course_code"] and form_data["course_code"] not in valid_course_codes:
            errors.append("Select a course from the available list.")

        if not errors:
            submitted_data = form_data.copy()

    context = {
        "courses": COURSES_DATA,
        "form_data": form_data,
        "submitted_data": submitted_data,
        "errors": errors,
    }
    return render(request, "catalog/inquiry.html", context)
