"""
- Views should be free from logical detailing
"""
import traceback

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import JSONRenderer

import json

from django.apps import apps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from logging_essar import init_logging
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import GallaryImages
from .serializers import GallaryImagesSerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json"
        super(JSONResponse, self).__init__(content, **kwargs)


class GallaryListView(APIView):
    parser_classes = (MultiPartParser,)

    def get(self, request, format=None):
        """ Fetch the all gallaryimages from the GallaryImages Models

        > GET: http://{{ip}}/gallary/gallaryhome/ """
        try:
            gallary_obj =  GallaryImages.objects.filter(is_deleted=False)
            if not gallary_obj:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            gallary_obj = GallaryImagesSerializer(gallary_obj, many=True).data
            return Response({"data":gallary_obj},status=status.HTTP_200_OK)
        except ObjectDoesNotExist as objNE:
            # Model object does not exist
            return Response(objNE.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"error get all images > uncaught exception > %s " % str(traceback.format_exc()))
            return Response(e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        """
        Add the send/request gallaryimages to the GallaryImages Models

        > POST: http://{{ip}}/gallary/gallaryhome/

         jsonbody ====>
        {
           "images":[ ' '],

        }"""
        images_objs = []
        try:
            images = dict((request.data).lists())['file[]']
            # if not images or isinstance(images, (int, list)):
            #     return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

            for image in images:
                gallary_img_obj = GallaryImagesSerializer(data={'file':image})
                if gallary_img_obj.is_valid():
                    gallary_img_obj.save()
                images_objs.append(gallary_img_obj.data)

            return Response(images_objs, status=status.HTTP_200_OK)

        except KeyError as e:
            # checking here require keys in the request body
            return Response(data={"message": str(e) + ' required'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except AttributeError as attr:
            # attribute missing while stroing the data
            return Response({"details": "attribute missing"}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist as objNE:
            # Model object does not exist
            return Response(objNE.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as exc:
            # if serializer is not valid or missing of the key
            return Response(exc.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # if serializer is not valid or missing of the key
            return Response(e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GallaryDetailView(APIView):

    def get(self, request, format=None):
        """ Fetch the all gallaryimages from the GallaryImages Models

        > GET: http://{{ip}}/gallary/gallaryhome/ """
        print("request.GET.get('image_id')---------",request.GET.get('image_id'))
        try:
            gallary_obj = GallaryImages.objects.filter(id=request.GET.get('image_id'),is_deleted=False)
            print("gallary_obj------------",gallary_obj)
            if not gallary_obj:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            gallary_obj = GallaryImagesSerializer(gallary_obj,many=True).data
            return Response({"data": gallary_obj}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist as objNE:
            # Model object does not exist
            return Response(objNE.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"error get images> uncaught exception > %s " % str(traceback.format_exc()))
            return Response(e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, format=None):
        """Add the send/request gallaryimages to the GallaryImages Models

        > patch: http://{{ip}}/gallary/gallaryhome/

         jsonbody ====>
        {
           "images":[ ' '],

        }"""
        try:
            self.image_id = request.GET.get('image_id')
            jsondata = request.FILES
            print('GallaryImages.objects.get(id=self.image_id)',jsondata)
            gallary_img_obj = GallaryImagesSerializer(GallaryImages.objects.get(id=self.image_id), data=jsondata, partial=True)
            if gallary_img_obj.is_valid():
                gallary_img_obj.save()
                return Response(gallary_img_obj.data,status=status.HTTP_200_OK)

        except KeyError as KeyEr:
            return Response(data=KeyEr.__dict__, status=status.HTTP_406_NOT_ACCEPTABLE)

        except AttributeError as attr:
            return Response({"details": "attribute missing"}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist as objNE:
            return Response(objNE.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as exc:
            return Response(exc.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)