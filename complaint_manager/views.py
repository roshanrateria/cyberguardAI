from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
def index_view(request):
    if request.user.is_authenticated:
        # Get complaints submitted by the logged-in user
        complaints = Complain.objects.filter(user=request.user)
        return render(request, 'hello_world.html', {'complaints': complaints})
    else:
        return redirect('login')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('upload_complain')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form,'errors': form.errors})

from django.views import View
from .models import Complain
from .forms import ComplainForm
from .utils import classify_complaint,categorize,parse_response
import json
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile



class UploadComplainView(View):
    def post(self, request):
        if request.user.is_authenticated:
            if 'upload_choice' in request.POST:
                upload_choice = request.POST['upload_choice']
                print("Request received")
                if upload_choice == 'video':
                    form = ComplainForm(request.POST, request.FILES)
                    if form.is_valid():
                        print('valid')
                        video_file = request.FILES['video']
                        temp_file = default_storage.save(str(settings.MEDIA_ROOT) + '/temp/' + video_file.name, ContentFile(video_file.read()))
                        video_path = str(settings.MEDIA_ROOT) + '/temp/' + video_file.name

                        response,des = classify_complaint(video_path)
                        data = parse_response(response)
                        complain = Complain(**data)
                        complain.user = request.user
                        complain.addon = request.POST.get('addon', '')
                        complain.video = request.FILES['video']
                        complain.issue_description=des
                        # Add other fields from the form
                        complain.incident_datetime = form.cleaned_data['incident_datetime']
                        
                        complain.national_id = form.cleaned_data['national_id']
                        complain.bank_name = form.cleaned_data['bank_name']
                        complain.transaction_id = form.cleaned_data['transaction_id']
                        complain.transaction_date = form.cleaned_data['transaction_date']
                        complain.fraud_amount = form.cleaned_data['fraud_amount']
                        complain.evidence = form.cleaned_data['evidence']
                        complain.suspect_website_urls = form.cleaned_data['suspect_website_urls']
                        complain.suspect_mobile_no = form.cleaned_data['suspect_mobile_no']
                        complain.suspect_email = form.cleaned_data['suspect_email']
                        complain.suspect_bank_account_no = form.cleaned_data['suspect_bank_account_no']
                        complain.suspect_address = form.cleaned_data['suspect_address']
                        complain.suspect_photo = form.cleaned_data['suspect_photo']
                        complain.suspect_other_document = form.cleaned_data['suspect_other_document']

                        complain.save()

                        return render(request, 'Uploaded.html', {'id': complain.id})

                elif upload_choice == 'manual':
                    form = ComplainForm(request.POST, request.FILES)
                    if form.is_valid():
                        # Call categorize function for manual input
                        text_input = f"{form.cleaned_data['issue_description']}"
                        cat=categorize(text_input)
                        print(cat)
                        category_data = parse_response(cat)
                        # Update form with categorized datata
                        print(category_data)
                        # Save the complaint with all fields
                        complain = form.save(commit=False)
                        complain.category=category_data['category']
                        complain.subcategory=category_data['subcategory']
                        complain.priority=category_data['priority']
                        complain.confidence_score=category_data['confidence_score']
                        complain.user = request.user
                        complain.save()
                        return render(request, 'Uploaded.html', {'id': complain.id})
                    else:
                        return render(request, 'upload_complain.html', {'form': form})

            else:
                return render(request, 'upload_complain.html', {'form': ComplainForm()})
        else:
            return redirect('login')

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'upload_complain.html', {'form': ComplainForm()})
        else:
            return redirect('login')


from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class ComplainListView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        complains = Complain.objects.all()
        return render(request, 'complain_list.html', {'complains': complains})

    def test_func(self):
        return self.request.user.is_superuser


class ComplainDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            complain = Complain.objects.get(pk=pk)
        except Complain.DoesNotExist:
            return redirect('complain_list')  # Redirect if the complaint doesn't exist or the user isn't authorized
        
        return render(request, 'complain_details.html', {'complain': complain})
    def test_func(self):
        return self.request.user.is_superuser

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

@login_required
def user_complaints_view(request):
    complaints = Complain.objects.filter(user=request.user)
    return render(request, 'hello_world.html', {'complaints': complaints})

class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        complaints = Complain.objects.filter(user=user)
        return render(request, 'user_detail.html', {'user': user, 'complaints': complaints})

    def test_func(self):
        return self.request.user.is_superuser