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


class Application(models.Model):
    # VISA PROCESS
    oldin_otkaz = models.BooleanField(default=False, verbose_name="Oldin Otkaz")
    country = models.CharField(max_length=255, verbose_name="Country")
    bankshot = models.CharField(max_length=255, verbose_name="Bankshot")
    
    # PASSPORT INFO
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    dob = models.DateField(verbose_name="Date of Birth")
    passport_number = models.CharField(max_length=50, verbose_name="Passport Number")
    passport_issue = models.DateField(verbose_name="Passport Issue Date")
    passport_expiry = models.DateField(verbose_name="Passport Expiry Date")
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Gender")
    
    # CONTACT
    phone = models.CharField(max_length=20, verbose_name="Phone")
    email = models.EmailField(verbose_name="Email")
    address = models.TextField(verbose_name="Address")
    zipcode = models.CharField(max_length=20, verbose_name="Zipcode")
    
    # CERTIFICATE
    TEST_TYPE_CHOICES = [
        ('IELTS', 'IELTS'),
        ('TOPIK', 'TOPIK'),
        ('TOEFL', 'TOEFL'),
    ]
    test_type = models.CharField(max_length=10, choices=TEST_TYPE_CHOICES, verbose_name="Test Type")
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Score")
    test_date = models.DateField(verbose_name="Test Date")
    expiry_date = models.DateField(verbose_name="Expiry Date")
    
    # UNIVERSITY INFO
    EDUCATION_LEVEL_CHOICES = [
        ('bachelor', 'Bakalavr'),
        ('master', 'Magistr'),
        ('college', 'College'),
    ]
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, verbose_name="Education Level")
    uni_phone = models.CharField(max_length=20, verbose_name="University Phone")
    uni_website = models.URLField(verbose_name="University Website", blank=True)
    uni_email = models.EmailField(verbose_name="University Email")
    uni_address = models.TextField(verbose_name="University Address")
    diplom_number = models.CharField(max_length=100, verbose_name="Diploma Number")
    gpa = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="GPA")
    grad_date = models.DateField(verbose_name="Graduation Date")
    prev_major = models.CharField(max_length=255, verbose_name="Previous Major")
    
    # FAMILY INFO - FATHER
    father_name = models.CharField(max_length=255, verbose_name="Father Name")
    father_passport = models.CharField(max_length=50, verbose_name="Father Passport", blank=True)
    father_dob = models.DateField(verbose_name="Father DOB", null=True, blank=True)
    father_phone = models.CharField(max_length=20, verbose_name="Father Phone", blank=True)
    father_job = models.CharField(max_length=255, verbose_name="Father Occupation", blank=True)
    
    # FAMILY INFO - MOTHER
    mother_name = models.CharField(max_length=255, verbose_name="Mother Name")
    mother_passport = models.CharField(max_length=50, verbose_name="Mother Passport", blank=True)
    mother_dob = models.DateField(verbose_name="Mother DOB", null=True, blank=True)
    mother_phone = models.CharField(max_length=20, verbose_name="Mother Phone", blank=True)
    mother_job = models.CharField(max_length=255, verbose_name="Mother Occupation", blank=True)
    
    photo = models.ImageField(upload_to='applicant_photos/', null=True, blank=True, verbose_name="Photo")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.passport_number}"
    
    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"


class University(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ('bachelor', 'Bakalavr'),
        ('master', 'Magistr'),
        ('college', 'College'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="University Name")
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, verbose_name="Education Level")
    phone = models.CharField(max_length=20, verbose_name="Phone", blank=True)
    website = models.URLField(verbose_name="Website", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)
    address = models.TextField(verbose_name="Address", blank=True)
    country = models.CharField(max_length=100, verbose_name="Country", default="Uzbekistan")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    def __str__(self):
        return f"{self.name} ({self.get_education_level_display()})"
    
    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"
        ordering = ['name']