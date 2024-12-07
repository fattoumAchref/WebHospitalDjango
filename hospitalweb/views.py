from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def custom_dashboard(request):
    return render(request, 'admin/custom_dashboard.html')  # Template for the dashboard
