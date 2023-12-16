import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser

from base.models import User
from api.serializers import UserSerializer
from djangoProject1.settings import BASE_DIR
from ResumeAI import text_extraction
from ResumeAI import Elasticsearch


@api_view(['GET'])
def getData(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def createData(request):
    if request.method == "POST":
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            article = serializer.save()
            data = serializer.data
            text_extraction.extract_text_pdf(data["pdf"])
            Elasticsearch.convert_to_json("","")
            #open(r"C:\Users\Houssem Zerai\PycharmProjects\djangoProject1\ResumeAI\test_resumes.txt", 'w').close()
            #open(r"C:\Users\Houssem Zerai\PycharmProjects\djangoProject1\ResumeAI\output.json", 'w').close()
            return Response(data=data)
        return Response(serializer.errors, status=400)
