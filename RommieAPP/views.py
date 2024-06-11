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

@api_view(['POST'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def UserInsert_f(request):
    try:
        serializer = InsertUserSerializer(data=request.data)
        if serializer.is_valid():
            import uuid
            user_uuid = str(uuid.uuid4())
            Data = {
                "user_uuid":user_uuid,
                "user_type":serializer.data["user_type"],
                "phone_number":serializer.data["phone_number"],
                "profile_picture":serializer.data["profile_picture"],
                "IsDeleted": "0",
                "CreatedBy": "system",
                "CreatedAt": datetime.now(),
                "UpdatedBy": "system",
                "UpdatedAt": datetime.now()
            }
            serializer.save(Data)
            
           
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
            json_data = {
                'status_code': 300,
                'status': 'Fail',
                'Reason': serializer.errors,
                'Remark': 'Send valid data'
            }
            return Response(json_data, status=stus.HTTP_300_MULTIPLE_CHOICES)
    except Exception as e:
        print("Error --------:", e)
        json_data = {
            'status_code': 400,
            'status': 'Fail',
            'Reason': e,
            'Remark': 'landed in exception',
        }
        raise APIException(json_data) 
    
