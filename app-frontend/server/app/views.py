from django.shortcuts import render
from django.http import HttpResponse
#from rest_framework.decorators import api_view
#from rest_framework.response import Response
from django.views.generic import TemplateView
from django.http import FileResponse


class indexView(TemplateView):
    template_name = 'index.html'

def image(res, id):
    img_url = 'app/img/' + str(id) + '.jpg'
    img = open(img_url, 'rb')
    res = FileResponse(img)

    return res