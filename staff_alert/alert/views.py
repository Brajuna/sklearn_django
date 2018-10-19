from django.shortcuts import render,HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from . import form
from .models import FileData
from .form import Signup
import pandas as pd


class Index(TemplateView):

    template_name = 'index.html'



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
            file = request.FILES['myfile']
            if(file.name[-4:] != ".csv"):
                return HttpResponse(" upsupported file format ")
            fs = FileSystemStorage()
            f_data = fs.save(file.name[:-4]+str(n)+file.name[-4:],file)
            k = FileData.objects.create(file_title =file.name[:-4]+str(n)+file.name[-4:],file = f_data)
            k.save()


    return render(request,'form.html',{'form':Form})


def output(request):

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

class details(DetailView):

    model = FileData
    template_name = ''


def analy_list(request):

    j = FileData.objects.all()

    return render(request,'list_view.html',{'j':j})

def algorithms(request):

    return HttpResponse('welcome to algarithms')

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


