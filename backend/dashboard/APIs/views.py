from django.shortcuts import render
from rest_framework.response import Response
from io import BytesIO
import pandas as pd
# Create your views here.

def UploadFunction(request):
    
    df=pd.read_excel(BytesIO(((request.FILES['file']).open()).read()))
    return Response(200)
 