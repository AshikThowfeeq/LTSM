from django.db.models import F, Count, Q
from apps.models import attendancetable, datatable
from django.shortcuts import render


def datelist(request):
    dates = attendancetable.objects.order_by('-date').values_list('date', flat=True).distinct()
    return render(request, 'date_list.html', {'dates': dates})


def attendance_dashboard(request, date):
    # Query the database to get attendance data for the specified date
    attendance_data = attendancetable.objects.filter(date=date).values('email_id__batch').annotate(
        hour_1_count=Count('email_id', filter=Q(date=date, hour_1=True)),
        hour_2_count=Count('email_id', filter=Q(date=date, hour_2=True)),
        hour_3_count=Count('email_id', filter=Q(date=date, hour_3=True)),
        hour_4_count=Count('email_id', filter=Q(date=date, hour_4=True)),
        hour_5_count=Count('email_id', filter=Q(date=date, hour_5=True)),
        hour_6_count=Count('email_id', filter=Q(date=date, hour_6=True)),
        hour_7_count=Count('email_id', filter=Q(date=date, hour_7=True)),
        hour_8_count=Count('email_id', filter=Q(date=date, hour_8=True))
    ).order_by('email_id__batch')

    return render(request, 'attendance_dashboard.html', {'attendance_data': attendance_data, 'selected_date': date})


def batch_attendance(request, batch, date):
    # Filter attendance records by batch and date
    attendance_records = attendancetable.objects.filter(email_id__batch=batch, date=date)

    # Count the number of students in the batch
    student_count = datatable.objects.filter(batch=batch).count()

    return render(request, 'batch_attendance.html', {'attendance_records': attendance_records, 'batch': batch, 'student_count': student_count, 'selected_date': date})


def student_detail(request, student_email):
    # Retrieve the student's details
    student = datatable.objects.get(email_id=student_email)

    # Retrieve the student's attendance records
    attendance_records = attendancetable.objects.filter(email_id=student)

    return render(request, 'student_detail.html', {'student': student, 'attendance_records': attendance_records})

