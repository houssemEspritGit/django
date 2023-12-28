import requests
from bs4 import BeautifulSoup
import json
import re
import csv

def scrape(keyWords):
    keyWords = keyWords["technologies"]
    keysParsed  = ''

    #pagination
    for key in keyWords:
        keysParsed += key

    i = 0
    reqFailed = False
    #liste of Req
    reqList = []
    array_result = []
    while not reqFailed:
        i += 1
        x = requests.get('https://www.keejob.com/offres-emploi/?keywords='+ keysParsed  + '&page=' + str(i))
        #pagination req by job
        if x.status_code != 200:
          reqFailed = not reqFailed
          print("intoError")
          break
        soup = BeautifulSoup(x.text, 'html.parser')

        links=soup.find_all('div',class_='span8')
        real_links=[]
        for link in links:
            if len(link["class"])== 1:
                real_links.append(link.h6.a['href'])
        for link in real_links :
            x= requests.get('https://www.keejob.com'+link)
            soup = BeautifulSoup(x.text, 'html.parser')
            data=soup.find('div',class_='text').find_all('div',class_='meta')
            print("----")
            person = {}
            # person['id'] = "ee"
            # print(person)
            for d in data:
                # Parse HTML content
                soup2 = BeautifulSoup(str(d), 'html.parser')

    # Extract all information
                job_info = {}
                job_info["link"] = 'https://www.keejob.com'+link
                for meta_div in soup.find_all('div', {'class': 'meta'}):
                    key_element = meta_div.find('b')
                    if key_element:
                        key = key_element.text.strip()

                        # Find the <br/> tag
                        br_tag = meta_div.find('br')

                        # If <br/> is found, get the text of the next sibling, considering possible whitespace nodes
                        if br_tag:
                            value = br_tag.find_next_sibling(text=True)
                            if value is not None:
                                # Remove extra spaces and beautify the value
                                beautified_value = re.sub(r'\s+', ' ', value.strip())
                                job_info[key] = beautified_value.strip()

                json_data = json.dumps(job_info, ensure_ascii=False, indent=2)

                # Load the JSON string into a dictionary
                job_info = json.loads(json_data)
                array_result.append(job_info)
                # Specify the CSV file path
        #         csv_file_path = "output.csv"
        #
        #         # Write data to CSV file
        #         with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        #             writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #
        #             # Write header
        #             writer.writerow(['Key', 'Value'])
        #
        #             # Write data
        #             for key, value in job_info.items():
        #                 writer.writerow([key, value])
        #   # files.download(csv_file_path)
        # print(array_result)
        return array_result
