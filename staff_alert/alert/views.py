from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseRedirect,JsonResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import logout as Logout
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from . import form
from django.contrib.auth.decorators import login_required
from .models import FileData
from .form import Signup
import pandas as pd
from django.contrib import sessions



class Index(TemplateView):

    template_name = 'index.html'


@login_required(login_url='/accounts/login/')

def input(request):
    Form = form.FileUpload(request.POST,request.FILES)

    if 'upload' in request.POST :

        if(Form.is_valid()):
            j = FileData.objects.all()
            query_list = []
            for k in j:
                query_list.append(k.id)

            if  len(query_list)>0:
                j = FileData.objects.all().last()
                n = j.id
            else:
                n = 1

            title = request.POST['file_title']
            request.session['name'] = 'monika'
            file = request.FILES['myfile']
            if(file.name[-4:] != ".csv"):
                return HttpResponse(" upsupported file format ")
            fs = FileSystemStorage()
            f_data = fs.save(file.name[:-4]+str(n)+file.name[-4:],file)
            k = FileData.objects.create(file_title =file.name[:-4]+str(n)+file.name[-4:],file = f_data)
            k.save()


    return render(request,'form.html',{'form':Form,'name':'upload'})


def output(request): #not used


    j = FileData.objects.all()
    l = []
    for jk in j:
        l.append(jk)
    # mm = open(settings.MEDIA_ROOT)
    print(len(l))
    fs = FileSystemStorage()
    mm = fs.open(l[len(l)-1].file_title)
    print(mm)
    df = pd.read_csv(mm)
    #print(df.values.tolist())
    i = df.plot().get_figure()
    i.savefig('media//a.png')
    fs = FileSystemStorage()

    return HttpResponse(fs.open('a.png').file,content_type='image/png')
    #response = HttpResponse(file,content_type='application')
    #return response
    #return  HttpResponse("<a href = 'input/'>output</a>")


def analy(request,pk1):

    j = FileData.objects.get(id=pk1)

    fs = FileSystemStorage()
    mm = fs.open(j.file_title)

    print(mm)
    df = pd.read_csv(mm)

    i = df.plot().get_figure()
    i.savefig('alert/static/media/files/a.png')
    fs = FileSystemStorage()

    return render(request,'img.html',)

   # return HttpResponse(fs.open('a.png').file,content_type='image/png')

class lists(ListView):

    model = FileData
    template_name = 'list_view.html'

class details(DetailView): #not used

    model = FileData
    template_name = ''


def analy_list(request):

    j = FileData.objects.all()

    return render(request,'list_view.html',{'j':j})

@login_required(login_url='/accounts/login/')
def algorithms(request):

    objs = FileData.objects.all()
    return render(request,'dashboard.html',{'objs':objs})

@login_required(login_url='/accounts/login/')
def dash(request,pk):

    objs = FileData.objects.all()

    csv = FileData.objects.get(pk = pk)

    fs = FileSystemStorage()
    f = fs.open(csv.file_title)
    f_title = csv.file_title
    b_path = fs.base_location

    df = pd.read_csv(f)
    v = df.values.tolist()
    h = list(df)



    m_df = []
    if 'add' in request.POST:

        for k in range(len(h)):
            m_df.append(request.POST[h[k]])
        fs = FileSystemStorage()
        df = pd.DataFrame()
        df.append(pd.DataFrame([v], columns=h), ignore_index=True)
        df.append(pd.DataFrame([m_df],columns=h),ignore_index=True)
        fs.delete(csv.file_title)
        df.to_csv(fs.base_location+"\\"+ csv.file_title)





    return render(request,'dashboard.html',{'objs':objs,'h':h,'v':v})

class Signup(FormView):

    template_name = 'form.html'
    form_class = Signup
    success_url = '/success/'

    def form_valid(self, form):

        print('success')

        user = User.objects.create_user(username=form.cleaned_data['user_name'],password=form.cleaned_data['password'],email=form.cleaned_data['email'])
        user.firstname = form.cleaned_data['first_name']
        user.lastname = form.cleaned_data['last_name']
        user.save()
        return super().form_valid(form)


def logout(request):
    print(request.session['name'])
    Logout(request)

    return HttpResponseRedirect('/')

def csv_json(request,pk):
    obj = FileData.objects.get(pk=pk)
    fs = FileSystemStorage()
    csv = fs.open(obj.file_title)
    df = pd.read_csv(csv)
    print(type(df))
    return JsonResponse({'lables':list(df),'data':df.values.tolist()})



