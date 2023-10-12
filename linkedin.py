import requests
from bs4 import BeautifulSoup
import csv
import cfscrape
import csv
import time
headers = {
    "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-encoding" : "gzip, deflate, sdch, br",
    "accept-language" : "en-US,en;q=0.8,ms;q=0.6",
    "user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}
def get_in_urls(input_file):
    csv_file_path = input_file

    # Open the CSV file for reading
    with open(csv_file_path, 'r', newline='') as csvfile:
        # Create a CSV reader
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            url = row['url']
            urls.append(url)
            print("URL:", url)


def login():
    print(f"Logging in with {email}...")
    session=CustomSession()
    login_url = 'https://www.linkedin.com/login'
    response = session.get(login_url,headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    csrf_token = soup.find('input', {'name': 'loginCsrfParam'}).get('value')
    login_data = {
    'session_key': email,
    'session_password': password,
    'loginCsrfParam': csrf_token,
    }
    login_submit_url = 'https://www.linkedin.com/checkpoint/lg/login-submit'
    response = session.post(login_submit_url, data=login_data)
    if response.status_code == 200:
        print("Login successful!")
    else:
        print("Login failed.")
    return session
# Create a custom session class using cfscrape
class CustomSession:
    def __init__(self):
        self.scraper = cfscrape.create_scraper()

    def get(self, url,headers):
        return self.scraper.get(url,headers=headers)
    def post(self, url, data=None, headers=None):
        return self.scraper.post(url, data=data, headers=headers)

def scrape(session):

    for url in urls:
        response=session.get(url,headers=headers)
        soup=BeautifulSoup(response.text,"lxml")
        print(response.status_code)
        while response.status_code!=200:
            print("Failed...Trying again in 10 seconds")
            time.sleep(10)
            response=session.get(url,headers=headers)
        section=soup.find("div",_class="inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp full-width")
        about=(section.find("span")["aria-hidden"==True]).get_text()
        data={
            "URL":url,
            "About":about
        }
        data_list.append(data)
        time.sleep(5)

def save_and_create_csv():
    with open("linkedin_about", mode='w', newline='') as csv_file:
        fieldnames = ["URL", "About"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()
    
    # Write the property data rows
    for data in data_list:
        writer.writerow(data)
    print(f"Data has been saved to linkedin_about")

if __name__=="__main__":
    
    input_file_link="in-urls.csv"
    email="youremail"
    password="yourpassword"
    urls=[]
    data_list=[]
    get_in_urls(input_file_link)
    s=login()
    time.sleep(10)
    scrape(s)
    save_and_create_csv()
    print("Done...")



