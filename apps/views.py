from django.db.models import F, Count, Q
from apps.models import attendancetable, datatable
from django.shortcuts import render,redirect
from django.db.models import Count, Q, Sum
from django.db.models import Case, When, IntegerField
from django.http import JsonResponse



def login(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')
        if (username == 'Grow' and password == '1234') or \
                (username == 'Lead@Control' and password == '1234') or \
                (username == 'Grow@Dev' and password == '1234'):
            request.session['username'] = username
            return redirect('index')
        else:
            error_message = "Invalid Login"
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


def index(request):
    dates = attendancetable.objects.order_by('-date').values_list('date', flat=True).distinct()
    return render(request,'index.html',{'dates': dates})



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
        hour_8_count=Count('email_id', filter=Q(date=date, hour_8=True)),
        total_hour_count=Sum(
            Case(
                When(date=date, then=1),
                default=0,
                output_field=IntegerField()
            )
        )
    ).order_by('email_id__batch')

    return render(request, 'table.html', {'attendance_data': attendance_data, 'selected_date': date})



def batch_attendance(request, batch, date):
    # Filter attendance records by batch and date
    attendance_records = attendancetable.objects.filter(email_id__batch=batch, date=date)

    # Count the number of students in the batch
    student_count = datatable.objects.filter(batch=batch).count()

    return render(request, 'batch_table.html', {'attendance_records': attendance_records, 'batch': batch, 'student_count': student_count, 'selected_date': date})


def student_detail(request, student_email):
    # Retrieve the student's details
    student = datatable.objects.get(email_id=student_email)

    # Retrieve the student's attendance records
    attendance_records = attendancetable.objects.filter(email_id=student)

    # Calculate the total count of True values for each hour across all dates
    total_hour_counts = {
        'hour_1': attendance_records.aggregate(total_hour_1=Sum(Case(When(hour_1=True, then=1), default=0, output_field=IntegerField())))['total_hour_1'],
        'hour_2': attendance_records.aggregate(total_hour_2=Sum(Case(When(hour_2=True, then=1), default=0, output_field=IntegerField())))['total_hour_2'],
        'hour_3': attendance_records.aggregate(total_hour_3=Sum(Case(When(hour_3=True, then=1), default=0, output_field=IntegerField())))['total_hour_3'],
        'hour_4': attendance_records.aggregate(total_hour_4=Sum(Case(When(hour_4=True, then=1), default=0, output_field=IntegerField())))['total_hour_4'],
        'hour_5': attendance_records.aggregate(total_hour_5=Sum(Case(When(hour_5=True, then=1), default=0, output_field=IntegerField())))['total_hour_5'],
        'hour_6': attendance_records.aggregate(total_hour_6=Sum(Case(When(hour_6=True, then=1), default=0, output_field=IntegerField())))['total_hour_6'],
        'hour_7': attendance_records.aggregate(total_hour_7=Sum(Case(When(hour_7=True, then=1), default=0, output_field=IntegerField())))['total_hour_7'],
        'hour_8': attendance_records.aggregate(total_hour_8=Sum(Case(When(hour_8=True, then=1), default=0, output_field=IntegerField())))['total_hour_8'],
    }


    # Calculate the total count of False values for each hour across all dates
    total_false_counts = {
        'hour_1': attendance_records.aggregate(total_hour_1=Sum(Case(When(hour_1=False, then=1), default=0, output_field=IntegerField())))['total_hour_1'],
        'hour_2': attendance_records.aggregate(total_hour_2=Sum(Case(When(hour_2=False, then=1), default=0, output_field=IntegerField())))['total_hour_2'],
        'hour_3': attendance_records.aggregate(total_hour_3=Sum(Case(When(hour_3=False, then=1), default=0, output_field=IntegerField())))['total_hour_3'],
        'hour_4': attendance_records.aggregate(total_hour_4=Sum(Case(When(hour_4=False, then=1), default=0, output_field=IntegerField())))['total_hour_4'],
        'hour_5': attendance_records.aggregate(total_hour_5=Sum(Case(When(hour_5=False, then=1), default=0, output_field=IntegerField())))['total_hour_5'],
        'hour_6': attendance_records.aggregate(total_hour_6=Sum(Case(When(hour_6=False, then=1), default=0, output_field=IntegerField())))['total_hour_6'],
        'hour_7': attendance_records.aggregate(total_hour_7=Sum(Case(When(hour_7=False, then=1), default=0, output_field=IntegerField())))['total_hour_7'],
        'hour_8': attendance_records.aggregate(total_hour_8=Sum(Case(When(hour_8=False, then=1), default=0, output_field=IntegerField())))['total_hour_8'],
    }

    #Total True Count
    total_true_count = sum(total_hour_counts.values())

    # Calculate the total count of False values across all eight hours
    total_false_count = sum(total_false_counts.values())
      # Calculate the percentage of True values out of the total of True and False values
    total_records = attendance_records.count()
    total_percentage = (total_true_count / (total_true_count + total_false_count)) * 100 if total_records > 0 else 0


    return render(request, 'student_table.html', {'student': student, 'attendance_records': attendance_records, 'total_hour_counts': total_hour_counts, 'total_true_count': total_true_count,'total_false_count': total_false_count, 'total_percentage': total_percentage,})

def search_attendance(request):
    date = request.GET.get('date')

    # Initialize a dictionary to store hour counts
    hour_counts = {}

    # Define the list of hours (adjust as needed)
    hours = ['hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8']

    # Iterate through the hours and calculate counts
    for hour in hours:
        count_key = f'{hour}_count'
        hour_counts[count_key] = Sum(Case(When(**{hour: True}, then=1), default=0, output_field=IntegerField()))

    # Query attendance data for the specified date
    attendance_data = attendancetable.objects.filter(date=date).values('email_id__batch').annotate(**hour_counts).order_by('email_id__batch')

    data = list(attendance_data)
    return JsonResponse(data, safe=False)