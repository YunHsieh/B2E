
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect

from app.models import *
from app.serializers import * 

# import base64
import random
from datetime import datetime, timedelta

# Create your views here.
class TinyUrl(APIView):
    permission_classes = [AllowAny ]
    def get(self, request, tinyurl):
        obj_url = store_tinyurl.objects.get(pk=tinyurl)
        return HttpResponseRedirect(obj_url.url)

    # if pk is already in db   so re-get again
    def reGetShortCode(self, keeplongtime = 0):
        digit_len = 6
        if keeplongtime:
            digit_len = 8
        get_shorten_url = ''.join([self.BASE62[random.randint(0,61)] for _ in range(digit_len)])

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
            obj_url = store_tinyurl.objects.get(url=request.POST.get('url',''), 
                iskeepforever = request.POST.get('iskeepforever',0))
        except store_tinyurl.DoesNotExist:
            obj_url = None

        if obj_url:
            return Response(settings.BASE_URL + obj_url.pk)

        # save data of format
        save_data = {}
        save_data['short_key'] = self.reGetShortCode(keeplongtime = request.POST.get('iskeepforever',0))
        save_data['url'] = request.POST.get('url')
        save_data['iskeepforever'] = request.POST.get('iskeepforever',0)

        # save data to DB
        url_serializers = StoreURLSerializers(data=save_data)
        if not url_serializers.is_valid():
            return Response(url_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        url_serializers.save()

        return Response(settings.BASE_URL + save_data['short_key'])


class TinyUrlMgr(APIView):
    permission_classes = [AllowAny ] # IsAdminUser
    def delete(self , request):
        expire_days = request.POST.get('expire_days', 30)
        deadline = datetime.now() - timedelta(days=30)
        obj_kill_item = store_tinyurl.objects.filter(create_time__lte=deadline, iskeepforever=0).delete()

        # todo  if your member will store for ever

        # using celery schedule clear anonymous data and more than one month

        return Response('Kill succeed')
