import requests
from bs4 import BeautifulSoup

def scrape2(keyWords):
    keyWords = keyWords["technologies"]
    keysParsed  = ''
    #pagination
    for key in keyWords:
        keysParsed += key
    url = 'https://www.emploitunisie.com/recherche-jobs-tunisie/'+keysParsed
    response = requests.get(url)
    job_info = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        job_listings = soup.find_all('div', class_='job-description-wrapper')
        for job_listing in job_listings:
            job_data = {}
            job_data['Type de poste'] = job_listing.find('h5').text.strip()
            recruiter_info = job_listing.find('p', class_='job-recruiter').text.strip().split('|')
            job_data['Entreprise'] = recruiter_info[1].strip()
            job_data['Publiée le'] = recruiter_info[0].strip()
            job_data['Lieu de travail'] = job_listing.find('p').text.strip()

            # Check if the 'job-tags' element is present
            job_tags = job_listing.find('div', class_='job-tags')
            if job_tags:
                # Extract key skills
                skills = job_tags.find_all('div', class_='badge')
                job_data['skills'] = [skill.text.strip() for skill in skills]
            else:
                job_data['skills'] = []

            job_info.append(job_data)

    else:
        print(f"Failed to retrieve the page. Status Code: {response.status_code}")

    return (job_info)
