from django.contrib.admin import AdminSite
from django.urls import path
from .models import Course
from django.shortcuts import render, redirect
class MyAdminSite(AdminSite):
    site_header = "LearnFreee Admin"
    site_title = "LearnFreee Admin Portal"
    index_title = "Welcome to LearnFreee Admin Dashboard"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('custom-admin/', self.admin_view(self.custom_admin_view), name="custom_admin"),
        ]
        return custom_urls + urls

    def custom_admin_view(self, request):
        if request.method == "POST":
            title = request.POST['title']
            description = request.POST['description']
            instructor = request.POST['instructor']
            price = request.POST['price']
            duration = request.POST['duration']
            Course.objects.create(title=title, description=description, instructor=instructor, price=price, duration=duration)
            return redirect('/myadmin/custom-admin/')
        
        courses = Course.objects.all()
        return render(request, 'admin/custom_admin.html', {'courses': courses})

admin_site = MyAdminSite(name='myadmin')
