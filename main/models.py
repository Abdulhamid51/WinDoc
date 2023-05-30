from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200)
    info = models.TextField()

    def __str__(self):
        return self.title


class UrlDetail(models.Model):
    project = models.ForeignKey(Project, related_name="urldetails", on_delete=models.CASCADE)
    
    URLTYPES = (
        ("POST","POST"),
        ("GET","GET"),
        ("PUT","PUT"),
        ("PATCH","PATCH"),
        ("DELETE","DELETE"),
    )

    title = models.CharField(max_length=200)
    info = models.TextField()
    method_type = models.CharField(choices=URLTYPES, max_length=10)
    url = models.CharField(max_length=400)
    request = models.TextField()
    request_type = models.CharField(max_length=100)
    response = models.TextField()

    def __str__(self):
        return self.title
