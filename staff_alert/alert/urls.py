from django.urls import path
from . import views

urlpatterns =[

    path('input',views.input,name='input'),
    path('',views.Index.as_view(),name='home'),
    path('output',views.output,name='output'),
    path('analy/<int:pk1>',views.analy,name='output'),
    path('analy',views.analy_list,name='output'),
    path('algorithms',views.algorithms,name='algorithms'),
]


