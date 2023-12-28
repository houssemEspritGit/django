
import os
from pdfminer.high_level import extract_text

from djangoProject1.settings import env


def extract_text_pdf(fileName):
    s = open(env('PROJECT_PATH')+"test_resumes.txt", "a", encoding='utf-8')
    directory = (env('MEDIA_PATH')+fileName)
    #for filename in os.listdir(directory):
    f = os.path.join(directory,"")
    chemin = os.path.abspath(f)
    print(chemin)
    print(type(chemin))
    m = extract_text(chemin)
    m += ". \n"
    m += "Chemin du fichier : " + chemin
    m += "  \n"
    s.write(m)
    s.write("/////")
    s.write("  ")
