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
from .models import User
import pymongo
@api_view(['POST'])
def UserInsert_f(request):
    try:
        connect_string='mongodb+srv://User_369:TonyStark007@cluster0.37ajaix.mongodb.net/roomie?retryWrites=true&w=majority'

        serializer = InsertUserSerializer(data=request.data)

        if serializer.is_valid():
            print('====================================11')
            # print("Serializer is valid.")
            # import uuid
            # user_uuid = str(uuid.uuid4())
            Data = {
                # "user_uuid": user_uuid,
                "user_type": serializer.validated_data["user_type"],
                "phone_number": serializer.validated_data["phone_number"],
                "IsDeleted": "0"
            }
            print(Data)
            # saved=serializer.save(**Data)
            my_client = pymongo.MongoClient(connect_string)

            # First define the database name
            dbname = my_client['roomie']

            # Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection
            collection_name = dbname["user"]
            # user = User()
            # print('========= user',user)
            collection_name.save(**Data)
            # User.save(**Data)
            print('==================================== after')
            
        
            json_data = {
                'status_code': 200 ,
                'status':'Success',
                'data':'',
                'message': 'Data Inserted successfully',
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