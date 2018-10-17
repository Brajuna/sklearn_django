from django.shortcuts import render,HttpResponse
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from . import form
from .models import FileData
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


    return render(request,'home.html',{'form':Form})


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


def analy_list(request):

    j = FileData.objects.all()

    return render(request,'list_view.html',{'j':j})



# Create your views here.
