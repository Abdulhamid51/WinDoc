from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import *

class IndexView(View):
    def get(self, request):
        projects = Project.objects.all().order_by('-id')
        data = {
            "projects":projects
        }
        return render(request, 'index.html', data)

class DetailView(View):
    def get(self, request, id):
        projects = Project.objects.all()
        project = get_object_or_404(Project, id=id)
        urls = UrlDetail.objects.filter(project=project)
        data = {
            "project":project,
            "urls":urls,
            "projects":projects
        }
        return render(request, 'doc.html', data)