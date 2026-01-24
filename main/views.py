from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from .models import *

from django.contrib.auth import authenticate, login, logout

class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main:form')
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:form')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main:login')

class ApplicationDocumentView(LoginRequiredMixin, View):
    def get(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        return render(request, 'document.html', {'app': application})

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
    
class FormView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'form.html')

    def post(self, request):
        # Extract data from request.POST
        data = request.POST
        applicant_id = data.get('applicant_id')
        
        # Helper to convert 'True'/'False' strings to boolean
        def to_bool(val):
            return val == 'True'

        # Helper to handle empty date strings
        def to_date(val):
            return val if val else None

        try:
            fields = {
                # VISA PROCESS
                'oldin_otkaz': to_bool(data.get('oldin_otkaz', 'False')),
                'country': data.get('country'),
                'bankshot': data.get('bankshot'),
                
                # PASSPORT INFO
                'full_name': data.get('full_name'),
                'dob': to_date(data.get('dob')),
                'passport_number': data.get('passport_number'),
                'passport_issue': to_date(data.get('passport_issue')),
                'passport_expiry': to_date(data.get('passport_expiry')),
                'gender': data.get('gender'),
                
                # CONTACT
                'phone': data.get('phone'),
                'email': data.get('email'),
                'cell_phone': data.get('cell_phone', ''),
                'telegram': data.get('telegram', ''),
                'address': data.get('address'),
                'zipcode': data.get('zipcode'),
                
                # CERTIFICATE
                'test_type': data.get('test_type'),
                'score': data.get('score') if data.get('score') else 0,
                'test_date': to_date(data.get('test_date')),
                'expiry_date': to_date(data.get('expiry_date')),
                'test_report_number': data.get('test_report_number', ''),
                
                # UNIVERSITY INFO
                'education_level': data.get('education_level'),
                'uni_name': data.get('uni_name', ''),
                'uni_entry_date': to_date(data.get('uni_entry_date')),
                'uni_phone': data.get('uni_phone'),
                'uni_website': data.get('uni_website', ''),
                'uni_email': data.get('uni_email'),
                'uni_address': data.get('uni_address'),
                'diplom_number': data.get('diplom_number'),
                'gpa': data.get('gpa') if data.get('gpa') else 0,
                'grad_date': to_date(data.get('grad_date')),
                'prev_major1': data.get('prev_major1', ''),
                'prev_major1_entry': to_date(data.get('prev_major1_entry')),
                'prev_major1_grad': to_date(data.get('prev_major1_grad')),
                'prev_major2': data.get('prev_major2', ''),
                'prev_major2_entry': to_date(data.get('prev_major2_entry')),
                'prev_major2_grad': to_date(data.get('prev_major2_grad')),
                
                # FAMILY INFO - FATHER
                'father_name': data.get('father_name'),
                'father_passport': data.get('father_passport', ''),
                'father_dob': to_date(data.get('father_dob')),
                'father_phone': data.get('father_phone', ''),
                'father_job': data.get('father_job', ''),
                'father_position': data.get('father_position', ''),
                
                # FAMILY INFO - MOTHER
                'mother_name': data.get('mother_name'),
                'mother_passport': data.get('mother_passport', ''),
                'mother_dob': to_date(data.get('mother_dob')),
                'mother_phone': data.get('mother_phone', ''),
                'mother_job': data.get('mother_job', ''),
                'mother_position': data.get('mother_position', ''),

                # FINANCIAL SPONSOR INFO
                'sponsor_name': data.get('sponsor_name', ''),
                'sponsor_relation': data.get('sponsor_relation', ''),
                'sponsor_occupation': data.get('sponsor_occupation', ''),
                'sponsor_address': data.get('sponsor_address', ''),
                'sponsor_phone': data.get('sponsor_phone', ''),
                'sponsor_company': data.get('sponsor_company', ''),
                'sponsor_position': data.get('sponsor_position', ''),
                'sponsor_company_address': data.get('sponsor_company_address', ''),
                'sponsor_contact_no': data.get('sponsor_contact_no', ''),

                # EMERGENCY CONTACT INFO
                'emergency_name': data.get('emergency_name', ''),
                'emergency_relation': data.get('emergency_relation', ''),
                'emergency_occupation': data.get('emergency_occupation', ''),
                'emergency_address': data.get('emergency_address', ''),
                'emergency_phone': data.get('emergency_phone', '')
            }

            photo = request.FILES.get('photo')
            if photo:
                fields['photo'] = photo

            if applicant_id:
                # Update existing
                app_obj = get_object_or_404(Application, id=applicant_id)
                for key, value in fields.items():
                    setattr(app_obj, key, value)
                app_obj.save()
                pk = app_obj.id
                messages.success(request, 'Application updated successfully!')
            else:
                # Create new
                new_app = Application.objects.create(**fields)
                pk = new_app.id
                messages.success(request, 'Form submitted successfully!')
            
            return redirect('main:application_document', pk=pk)
        except Exception as e:
            import traceback
            print("ERROR IN FORM SUBMIT:")
            print(traceback.format_exc())
            messages.error(request, f'Error: {str(e)}')
            return redirect('main:form')

def delete_applicant(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        applicant = get_object_or_404(Application, pk=pk)
        applicant.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def get_universities(request):
    level = request.GET.get('level')
    universities = University.objects.filter(education_level=level, is_active=True).values('id', 'name')
    return JsonResponse(list(universities), safe=False)

def get_university_details(request):
    pk = request.GET.get('pk')
    uni = get_object_or_404(University, pk=pk)
    data = {
        'name': uni.name,
        'phone': uni.phone,
        'website': uni.website,
        'email': uni.email,
        'address': uni.address,
    }
    return JsonResponse(data)

def save_university(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        name = request.POST.get('name')
        education_level = request.POST.get('education_level')
        phone = request.POST.get('phone', '')
        website = request.POST.get('website', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        
        if pk:
            uni = get_object_or_404(University, pk=pk)
        else:
            uni = University()
            
        uni.name = name
        uni.education_level = education_level
        uni.phone = phone
        uni.website = website
        uni.email = email
        uni.address = address
        uni.save()
        
        return JsonResponse({'status': 'success', 'id': uni.id, 'name': uni.name})
    return JsonResponse({'status': 'error'}, status=400)

def get_applicants(request):
    applicants = Application.objects.all().values('id', 'full_name')
    return JsonResponse(list(applicants), safe=False)

def get_applicant_details(request):
    pk = request.GET.get('pk')
    app = get_object_or_404(Application, pk=pk)
    data = {
        'oldin_otkaz': app.oldin_otkaz,
        'country': app.country,
        'bankshot': app.bankshot,
        'full_name': app.full_name,
        'dob': app.dob.isoformat() if app.dob else '',
        'passport_number': app.passport_number,
        'passport_issue': app.passport_issue.isoformat() if app.passport_issue else '',
        'passport_expiry': app.passport_expiry.isoformat() if app.passport_expiry else '',
        'gender': app.gender,
        'phone': app.phone,
        'email': app.email,
        'cell_phone': app.cell_phone,
        'telegram': app.telegram,
        'address': app.address,
        'zipcode': app.zipcode,
        'test_type': app.test_type,
        'score': str(app.score),
        'test_date': app.test_date.isoformat() if app.test_date else '',
        'expiry_date': app.expiry_date.isoformat() if app.expiry_date else '',
        'test_report_number': app.test_report_number,
        'education_level': app.education_level,
        'uni_name': app.uni_name,
        'uni_entry_date': app.uni_entry_date.isoformat() if app.uni_entry_date else '',
        'uni_phone': app.uni_phone,
        'uni_website': app.uni_website,
        'uni_email': app.uni_email,
        'uni_address': app.uni_address,
        'diplom_number': app.diplom_number,
        'gpa': str(app.gpa),
        'grad_date': app.grad_date.isoformat() if app.grad_date else '',
        'prev_major1': app.prev_major1,
        'prev_major1_entry': app.prev_major1_entry.isoformat() if app.prev_major1_entry else '',
        'prev_major1_grad': app.prev_major1_grad.isoformat() if app.prev_major1_grad else '',
        'prev_major2': app.prev_major2,
        'prev_major2_entry': app.prev_major2_entry.isoformat() if app.prev_major2_entry else '',
        'prev_major2_grad': app.prev_major2_grad.isoformat() if app.prev_major2_grad else '',
        'father_name': app.father_name,
        'father_passport': app.father_passport,
        'father_dob': app.father_dob.isoformat() if app.father_dob else '',
        'father_phone': app.father_phone,
        'father_job': app.father_job,
        'father_position': app.father_position,
        'mother_name': app.mother_name,
        'mother_passport': app.mother_passport,
        'mother_dob': app.mother_dob.isoformat() if app.mother_dob else '',
        'mother_phone': app.mother_phone,
        'mother_job': app.mother_job,
        'mother_position': app.mother_position,

        'sponsor_name': app.sponsor_name,
        'sponsor_relation': app.sponsor_relation,
        'sponsor_occupation': app.sponsor_occupation,
        'sponsor_address': app.sponsor_address,
        'sponsor_phone': app.sponsor_phone,
        'sponsor_company': app.sponsor_company,
        'sponsor_position': app.sponsor_position,
        'sponsor_company_address': app.sponsor_company_address,
        'sponsor_contact_no': app.sponsor_contact_no,

        'emergency_name': app.emergency_name,
        'emergency_relation': app.emergency_relation,
        'emergency_occupation': app.emergency_occupation,
        'emergency_address': app.emergency_address,
        'emergency_phone': app.emergency_phone,

        'photo_url': app.photo.url if app.photo else None,
    }
    return JsonResponse(data)