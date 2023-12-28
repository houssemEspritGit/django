import spacy
import re
import json

from djangoProject1.settings import env


def convert_to_json(model, txt_file):
    model = env('PROJECT_PATH')+"LAST2_CUSTOM_NER_XX"
    txt_file = env('PROJECT_PATH')+"test_resumes.txt"
    nlp = spacy.load(model)
    with open(txt_file,encoding="utf8") as f:
        contents = f.read()
    resumes = re.split("/////", contents)
    master_entities = []
    i=0

    for resume in resumes:
        i=i+1

        #tab = re.split("$$", resume)

        entities = {'id':'' ,'loc': [], 'technologies': [], 'certif': [], 'date': [], 'education': [], 'experience': [],
                    'formation': [], 'languages': [], 'org': []
            , 'per': [], 'school': [], 'university': [], 'email': [], 'phone_number': '','path':''}
        #-----------------------------------------------------------------------------------------------------------------
        # Recherche de la phrase "Chemin du fichier :" et extraction du chemin
        match = re.search(r"Chemin du fichier :(.+)", resume)

        #print(f'this is match:{match}')
        if match:

            chemin_fichier = match.group(1)
            entities['path'] = chemin_fichier
        # -------------------------------------------------------------------------------------------
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", resume)



        entities['email']=emails
        entities['email'] = list(set(entities['email']))

        # -------------------------------------------------------------------------------------------


        phone = " \n ".join(re.findall(r'[\+\(\+216]?[1-9][0-9 .\(\)]{8,}[0-9]', resume))




        # phone=re.findall(r'(\+216)?[1-9][0-9 .\(\)]{8,}[0-9]', resume)
        for ph in phone :
            entities['phone_number']+= ph.replace(')','')
        # entities['phone_number']= list(set(entities['phone_number']))
        #print("---------")
        #print(type(phone))
        # -------------------------------------------------------------------------------------------
        entities['id']=i
        doc = nlp(resume)

        for ent in doc.ents:
            if ent.label_ == 'PER':
                entities['per'].append((ent.text).replace('\n', ' '))
                entities['per'] = list(set(entities['per']))
            if ent.label_ == 'LOC':
                entities['loc'].append((ent.text).replace('\n', ' '))
                entities['loc'] = list(set(entities['loc']))
            if ent.label_ == 'TECHNOLOGIES':
                entities['technologies'].append((ent.text).replace('\n', ' '))
            if ent.label_ == 'CERTIF':
                entities['certif'].append((ent.text).replace('\n', ' '))
            if ent.label_ == 'DATE':
                entities['date'].append((ent.text).replace('\n', ' '))
            if ent.label_ == 'EDUCATION':
                entities['education'].append((ent.text).replace('\n', ' '))
            if ent.label_ == 'EXPERIENCE':
                entities['experience'].append((ent.text).replace('\n', ' '))
            if ent.label_ == 'FORMATION':
                entities['formation'].append((ent.text).replace('\n', ' '))
            if ent.label_ == 'LANGUAGES':
                entities['languages'].append((ent.text).replace('\n', ' '))
            if ent.label_ == 'ORG':
                entities['org'].append((ent.text).replace('\n', ' '))
            if ent.label_ == 'SCHOOL':
                entities['school'].append((ent.text).replace('\n', ' '))
            if ent.label_ == 'UNIVERSITY':
                entities['university'].append((ent.text).replace('\n', ' '))
        master_entities.append(entities)
    # ------------------------------------------------------------------------------------------------
        #print(type(entities['technologies'][1]))
        if any(tech == entities["path"] for tech in entities["technologies"]):
            # Remove the similar element from "technologies"
            entities["technologies"] = [tech for tech in entities["technologies"] if tech != entities["path"]]
        if entities['technologies'] :
            # print(f"this is -1 : {entities['technologies'][-1]}")
            # print(f"this is path : {entities['path']}")
            if  entities['technologies'][-1] in entities['path']:
                entities['technologies'].pop()


    with open(env('PROJECT_PATH')+"output.json", 'w', encoding='utf-8') as outfile:
        json.dump(master_entities, outfile, ensure_ascii=False)
    with open(env('PROJECT_PATH')+"output.json", 'r', encoding='utf-8') as outfile:
        return json.load(outfile)
####################

#
## apply model and convert results to json
#convert_to_json(r"C:\Users\Houssem\Desktop\Esprit\Data science\ResumeAI_\LAST2_CUSTOM_NER_XX", "test_resumes.txt")