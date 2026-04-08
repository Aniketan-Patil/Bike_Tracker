from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import ServiceRecord
from .forms import ServiceRecordForm, UnderServiceForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from .sms_notifications import send_sms  # Import the send_sms function

# Login Choice View
def login_choice(request):
    return render(request, 'serviceapp/login_choice.html')

# Admin/Manager Login View
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = AuthenticationForm(request, data=request.POST or None)
    next_url = request.GET.get('next') or request.POST.get('next') or settings.LOGIN_REDIRECT_URL

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        if user.groups.filter(name='AdminManager').exists():
            login(request, user)
            return redirect(next_url)
        else:
            form.add_error(None, 'You are not authorized as Admin/Manager')

    return render(request, 'serviceapp/login.html', {'form': form, 'next': next_url, 'role': 'Admin/Manager Login'})

# Associate Login View
def associate_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = AuthenticationForm(request, data=request.POST or None)
    next_url = request.GET.get('next') or request.POST.get('next') or settings.LOGIN_REDIRECT_URL

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        if user.groups.filter(name='Associate').exists():
            login(request, user)
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            else:
                return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            form.add_error(None, 'You are not authorized as Associate')

    return render(request, 'serviceapp/login.html', {'form': form, 'next': next_url, 'role': 'Associate Login'})

# Service Incharge Login View
def service_incharge_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        if user.groups.filter(name='ServiceIncharge').exists():
            login(request, user)
            return redirect('dashboard')
        else:
            form.add_error(None, 'You are not authorized as Service Incharge')

    return render(request, 'serviceapp/login.html', {'form': form, 'role': 'Service Incharge Login'})

# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('login_choice')

# Dashboard View (Role-Based)
@login_required
def dashboard(request):
    print("DASHBOARD VIEW CALLED")
    user = request.user

    if user.groups.filter(name='AdminManager').exists():
        print("Rendering admin_dashboard.html")
        records = ServiceRecord.objects.all().order_by('id')
        return render(request, 'serviceapp/admin_dashboard.html', {'records': records})

    elif user.groups.filter(name='Associate').exists():
        print("Rendering associate_dashboard.html")
        cutoff_date = timezone.now().date() - timedelta(days=90)
        records = ServiceRecord.objects.filter(last_serviced_date__lte=cutoff_date).order_by('id')

        for record in records:
            record.days_exceeded = (timezone.now().date() - record.last_serviced_date).days - 90

        return render(request, 'serviceapp/associate_dashboard.html', {'records': records})

    elif user.groups.filter(name='ServiceIncharge').exists():
        print("Rendering service_incharge_dashboard.html")
        under_service_records = ServiceRecord.objects.filter(progress__icontains='under').order_by('id')
        completed_records = ServiceRecord.objects.filter(progress__iexact='completed').order_by('-last_serviced_date')
        return render(request, 'serviceapp/service_incharge_dashboard.html', {
            'under_service_records': under_service_records,
            'completed_records': completed_records
        })

    else:
        print("Rendering unauthorized.html")
        return render(request, 'serviceapp/unauthorized.html')

# Service Records (Admin/Manager)
@login_required
def service_records(request):
    records = ServiceRecord.objects.all().order_by('id')
    return render(request, 'serviceapp/service_records.html', {'records': records})

# Add Service Record
@login_required
def add_record(request):
    if request.method == 'POST':
        form = ServiceRecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            # SMS Notification Logic
            cutoff_date = timezone.now().date() - timedelta(days=90)
            if record.last_serviced_date <= cutoff_date:
                message = f"Reminder: Your bike model {record.bike_model} (Reg No: {record.reg_no}) is due for service."
                send_sms(record.contact, message)
            return redirect('service_records')
    else:
        form = ServiceRecordForm()
    return render(request, 'serviceapp/record_form.html', {'form': form})

# Edit Service Record
@login_required
def edit_record(request, pk):
    record = get_object_or_404(ServiceRecord, pk=pk)
    if request.method == 'POST':
        form = ServiceRecordForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save()
            # SMS Notification Logic
            cutoff_date = timezone.now().date() - timedelta(days=90)
            if record.last_serviced_date <= cutoff_date:
                message = f"Reminder: Your bike model {record.bike_model} (Reg No: {record.reg_no}) is due for service."
                send_sms(record.contact, message)
            return redirect('dashboard')
    else:
        form = ServiceRecordForm(instance=record)
    return render(request, 'serviceapp/record_form.html', {'form': form})

# Delete Service Record
@login_required
def delete_record(request, pk):
    record = get_object_or_404(ServiceRecord, pk=pk)
    record.delete()
    return redirect('dashboard')

# Service Due (Associate)
@login_required
def service_due(request):
    cutoff_date = timezone.now().date() - timedelta(days=90)
    records = ServiceRecord.objects.filter(last_serviced_date__lte=cutoff_date).order_by('id')

    for record in records:
        record.days_exceeded = (timezone.now().date() - record.last_serviced_date).days - 90

    return render(request, 'serviceapp/service_due.html', {'records': records})

# Under Maintenance View
@login_required
def under_service(request):
    records = ServiceRecord.objects.filter(progress__icontains='under').order_by('id')
    return render(request, 'serviceapp/under_service.html', {'records': records})

# Add to Under Maintenance
@login_required
def add_under_service(request):
    if request.method == 'POST':
        form = UnderServiceForm(request.POST)
        if form.is_valid():
            under_service = form.save(commit=False)
            if under_service.progress.lower() == 'completed':
                under_service.service_record.last_serviced_date = timezone.now().date()
                under_service.service_record.progress = 'Completed'
                under_service.service_record.save()
            else:
                under_service.service_record.progress = 'Under Maintenance'
                under_service.service_record.save()
            under_service.save()
            return redirect('under_service')
    else:
        form = UnderServiceForm()
    return render(request, 'serviceapp/add_under_service.html', {'form': form})

# ✅ NEW: Edit Under Service with date update logic and SMS notification
@login_required
def edit_under_service(request, pk):
    # Fetch the service record directly, not UnderServiceRecord
    record = get_object_or_404(ServiceRecord, pk=pk)

    if request.method == 'POST':
        # Use the UnderServiceForm to update the ServiceRecord
        form = UnderServiceForm(request.POST, instance=record)
        
        if form.is_valid():
            updated_record = form.save(commit=False)

            # Check if the progress is completed, and update last_serviced_date
            if updated_record.progress.lower() == 'completed':
                updated_record.last_serviced_date = timezone.now().date()

            updated_record.save()  # Save the ServiceRecord object

            # SMS Notification Logic
            cutoff_date = timezone.now().date() - timedelta(days=90)
            if updated_record.last_serviced_date <= cutoff_date:
                message = f"Reminder: Your bike model {updated_record.bike_model} (Reg No: {updated_record.reg_no}) is due for service."
                send_sms(updated_record.contact, message)

            return redirect('under_service')  # Redirect to the under_service list

    else:
        form = UnderServiceForm(instance=record)  # Use the same form for editing

    return render(request, 'serviceapp/add_under_service.html', {'form': form})

@login_required
def service_incharge_dashboard(request):
    user = request.user

    # Fetch the records that are under maintenance and completed
    under_service_records = ServiceRecord.objects.filter(progress__icontains='under').order_by('id')
    completed_records = ServiceRecord.objects.filter(progress__iexact='completed').order_by('-last_serviced_date')

    return render(request, 'serviceapp/service_incharge_dashboard.html', {
        'under_service_records': under_service_records,
        'completed_records': completed_records
    })

