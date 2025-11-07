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

# scrapes events from UTA events calendar
# it should return array of objects? 
def getUpcomingEvents():

    events = []
    url = "https://events.uta.edu/#tabs-46950015556440-46950015565660"

    # this one is for trending, but I think u can still use the same url as above and just change the id on soup.
    # url = "https://events.uta.edu/#tabs-46950015556440-46950015561563" 

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # gets container that has upcoming events and other random stuff
    eventsContainer = soup.find("div", {"id": "tabs-46950015556440-46950015565660"})

    # actually gets upcoming events container
    upcomingEventsContainer = eventsContainer.find("div", class_="em-card-group")

    # set recursive to false because it was returning duplicate images for events
    for eventDiv in upcomingEventsContainer.find_all("div", recursive=False):
        titleContainer = eventDiv.select("h3 a")
        titleText = titleContainer[0].text

        dateText = eventDiv.find("p", {"class": "em-card_event-text"}).text

        images = eventDiv.find_all("img")

        for img in images:
            newEvent = {
                "title": titleText,
                "date": dateText.strip(),
                "imgSrc": img["src"]
            }
            
            events.append(newEvent)
    
    return events


if __name__ == "__main__":
    res = getUpcomingEvents()

    print(res)

