from django.shortcuts import render
from django.http import HttpResponse
from Trustagain_App.models import User

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the Trustagain_App index.")

def users(request):
    user_list = User.objects.order_by('first_name')
    user_dict = {'users': user_list}
    return render(request, 'appTwo/users.html', context = user_dict) # with this render returns we can grap stuff from the database

# this is used to import my forms
def form_name_view(request):
    forms_instance = forms.Formname()
    if request.method == "POST": # if there is a request or someone hit the submit button do below
        forms_instance = forms.Formname(request.POST)

        if forms_instance.is_valid():
            print("VALIDATION SUCCESS")
            print("NAME: " + forms_instance.cleaned_data['name'])   
            print("EMAIL: " + forms_instance.cleaned_data['email'])
            print("TEXT: " + forms_instance.cleaned_data['text'])

    return render(request, 'appTwo/form_page.html' , {'form': forms_instance})  