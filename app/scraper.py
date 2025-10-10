from bs4 import BeautifulSoup
import requests

# fetches all of the departments like 'Computer Science and Engineering (CSE)'
def getDepartments():

    ret = []
    # fetch page
    url = "https://catalog.uta.edu/coursedescriptions/"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        exit

    soup = BeautifulSoup(response.text, "html.parser")

    # all <li> elements
    li = soup.select("div.sitemap ul li")

    for list in li:
        ret.append(list.text)

    return ret

# returns all of the courses for a department like 'CSE 1310'
def getCourses(department: str):

    url = "https://catalog.uta.edu/coursedescriptions/" + department.lower()

    res = []
    
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        exit

    soup = BeautifulSoup(response.text, "html.parser")

    courseDivs = soup.select("div.courses div p.courseblocktitle")

    for course in courseDivs:
        # in the HTML non breaking space, so replace it with " "
        res.append(course.get_text().replace("\xa0", " ").strip())
    
    return res

