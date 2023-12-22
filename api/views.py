import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser

from base.models import User
from api.serializers import UserSerializer
from djangoProject1.settings import BASE_DIR, env
from ResumeAI import text_extraction
from ResumeAI import Elasticsearch
from ResumeAI import scrapping
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
            Elasticsearch.convert_to_json("","")

            # Specify the path to your JSON file
            json_file_path = env('PROJECT_PATH')+"output.json"

            # Read the JSON file
            with open(json_file_path, 'r',encoding="utf-8") as file:
                # Load JSON data
                output = json.load(file)

            # Print the parsed data
            #open(r"C:\Users\Houssem Zerai\PycharmProjects\djangoProject1\ResumeAI\test_resumes.txt", 'w').close()
            #open(r"C:\Users\Houssem Zerai\PycharmProjects\djangoProject1\ResumeAI\output.json", 'w').close()
            scraping_result = scrapping.scrape(output[0])
            # Convert each dictionary to a tuple of its items and use a set to track unique tuples
            unique_tuples = set(tuple(sorted(item.items())) for item in scraping_result)

            # Convert the tuples back to dictionaries to get the unique objects
            unique_objects = [dict(t) for t in unique_tuples]

            return Response(data=unique_objects)
        return Response(serializer.errors, status=400)
