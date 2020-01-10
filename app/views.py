
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect

from app.models import *
from app.serializers import * 

# import base64
import random
from datetime import datetime

# Create your views here.
class TinyUrl(APIView):
    
    def get(self, request, tinyurl):
        obj_url = store_tinyurl.objects.get(pk=tinyurl)
        return HttpResponseRedirect(obj_url.url)

    # if pk is already in db   so re-get again
    def reGetShortCode(self):
        get_shorten_url = ''.join([self.BASE62[random.randint(0,61)] for _ in range(6)])
        try:
            obj_url = store_tinyurl.objects.get(pk=get_shorten_url)
        except store_tinyurl.DoesNotExist:
            obj_url = None
        if obj_url:
            return self.reGetShortCode()
        else:
            return get_shorten_url

    # register user
    def post(self , request):
        self.BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # check parameters
        if not request.POST.get('url',''):
            return Response( "Don't have got any parameters : url",status = status.HTTP_400_BAD_REQUEST)

        # get the url whether in db
        try:
            obj_url = store_tinyurl.objects.get(url=request.POST.get('url',''))
        except store_tinyurl.DoesNotExist:
            obj_url = None

        if obj_url:
            return Response(settings.BASE_URL + obj_url.pk)

        save_data = {}
        save_data['short_key'] = self.reGetShortCode()
        save_data['url'] = request.POST.get('url')
        url_serializers = StoreURLSerializers(data=save_data)
        if not url_serializers.is_valid():
            return Response(url_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        url_serializers.save()

        return Response(settings.BASE_URL + save_data['short_key'])



    
    