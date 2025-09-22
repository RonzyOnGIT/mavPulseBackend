from bs4 import BeautifulSoup
import requests

# fetches all of the departments

def getDepartments():

    ret = []
    # fetch page
    url = "https://catalog.uta.edu/coursedescriptions/"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        exit

    soup = BeautifulSoup(response.text, "html.parser")

    li = soup.select("div.sitemap ul li")

    for list in li:
        ret.append(list.text)

    return ret

# def getCourses():

