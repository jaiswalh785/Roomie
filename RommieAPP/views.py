from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view , authentication_classes , permission_classes
from rest_framework import status as stus
from datetime import datetime
from .serializer import *
from .queries import *
from models import User

@api_view(['POST'])
def UserInsert_f(request):
    try:
        print("Request received.")
        print(f"Request data: {request.data}")

        serializer = InsertUserSerializer(data=request.data)
        print(f"Serializer data: {serializer}")

        if serializer.is_valid():
            print("Serializer is valid.")
            # import uuid
            # user_uuid = str(uuid.uuid4())
            Data = {
                # "user_uuid": user_uuid,
                "user_type": serializer.validated_data["user_type"],
                "phone_number": serializer.validated_data["phone_number"],
                "IsDeleted": "0"
            }
            print(Data)
            # serializer.save(**Data)
            User.save(**Data)
            
            if 1:
                json_data = {
                    'status_code': 200 ,
                    'status':'Success',
                    'data':Data,
                    'message': 'Data Inserted successfully',
                }
                return Response(json_data,status=stus.HTTP_200_OK)
            else:
                json_data = {
                    'status_code': 200,
                    'status': 'Failed',
                    'data':'',
                    'message': 'Data Insertion Failed',
                }
                return Response(json_data,status=stus.HTTP_200_OK)
        else:
            print("Serializer is invalid.")
            print(f"Errors: {serializer.errors}")
            json_data = {
                'status_code': 400,
                'status': 'Fail',
                'Reason': serializer.errors,
                'Remark': 'Send valid data'
            }
            return Response(json_data, status=stus.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error: {e}")
        json_data = {
            'status_code': 500,
            'status': 'Fail',
            'Reason': f'{e}',
            'Remark': 'An exception occurred',
        }
        raise APIException(json_data)