from django.shortcuts import render
from django.http import HttpResponse
#from rest_framework.decorators import api_view
#from rest_framework.response import Response
from django.views.generic import TemplateView
from django.http import FileResponse

global ready
ready = False


class indexView(TemplateView):
    template_name = 'index.html'

def pageLoaded(res):
    res = HttpResponse("?")
    global ready
    ready = False

    return res

def image(res, id):
    img_url = 'app/img/' + str(id) + '.jpg'
    img = open(img_url, 'rb')
    res = FileResponse(img)

    return res

def machine_ready(res):
    global ready
    print(ready)
    if(ready):
        res = HttpResponse("yes")
    else:
        res = HttpResponse("no!")
    
    return res

def ready_from_backend(res):
    res = HttpResponse("?")

    global ready
    ready = True
    return res