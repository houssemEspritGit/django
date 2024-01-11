import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser

from base.models import User
from api.serializers import UserSerializer
from djangoProject1.settings import BASE_DIR, env
from ResumeAI_ import text_extraction
from ResumeAI_ import Elasticsearch
from ResumeAI_ import scrapping
from ResumeAI_ import scrapping2
import json


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
            filtred_data = Elasticsearch.convert_to_json("","")

            # # Specify the path to your JSON file
            # json_file_path = env('PROJECT_PATH')+"output.json"
            #
            # # Read the JSON file
            # with open(json_file_path, 'r',encoding="utf-8") as file:
            #     # Load JSON data
            #     output = json.load(file)
            scraping_result = scrapping.scrape(filtred_data[0])
            # 2nd web scrapper
            scraping_result2 = scrapping2.scrape2(filtred_data[0])
            scraping_result = scraping_result+scraping_result2
            # Convert each dictionary to a tuple of its items and use a set to track unique tuples
            unique_tuples = set(tuple(sorted(item.items())) for item in scraping_result)

            # Convert the tuples back to dictionaries to get the unique objects
            unique_objects = [dict(t) for t in unique_tuples]

            return Response(data=unique_objects)
        return Response(serializer.errors, status=400)
