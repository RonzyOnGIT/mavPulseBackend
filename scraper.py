from bs4 import BeautifulSoup
import requests
from supabase_client import supabase

# fetches all of the departments like 'Computer Science and Engineering (CSE)'
def getDepartments():
    ret = []
    url = "https://catalog.uta.edu/coursedescriptions/"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return ret

    soup = BeautifulSoup(response.text, "html.parser")
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
        return res

    soup = BeautifulSoup(response.text, "html.parser")
    courseDivs = soup.select("div.courses div p.courseblocktitle")
    
    for course in courseDivs:
        res.append(course.get_text().replace("\xa0", " ").strip())

    return res

# scrapes events from UTA Upcoming events calendar
def getUpcomingEvents():
    events = []
    url = "https://events.uta.edu/#tabs-46950015556440-46950015565660"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        eventsContainer = soup.find("div", {"id": "tabs-46950015556440-46950015565660"})
        
        if not eventsContainer:
            print("Warning: Could not find upcoming events container")
            return events
        
        upcomingEventsContainer = eventsContainer.find("div", class_="em-card-group")
        
        if not upcomingEventsContainer:
            print("Warning: Could not find upcoming events card group")
            return events

        # Process each event - only take first image per event to avoid duplicates
        for eventDiv in upcomingEventsContainer.find_all("div", recursive=False):
            try:
                titleContainer = eventDiv.select("h3 a")
                if not titleContainer:
                    continue
                    
                titleText = titleContainer[0].text.strip()

                dateElement = eventDiv.find("p", {"class": "em-card_event-text"})
                if not dateElement:
                    continue
                    
                dateText = dateElement.text.strip()

                # Get only the FIRST image to avoid duplicates
                img = eventDiv.find("img")
                imgSrc = img["src"] if img and img.get("src") else ""

                newEvent = {
                    "title": titleText,
                    "date": dateText,
                    "imgSrc": imgSrc
                }
                
                events.append(newEvent)
                
            except Exception as e:
                print(f"Error processing upcoming event: {e}")
                continue
    
    except Exception as e:
        print(f"Error fetching upcoming events: {e}")
    
    return events

# scrapes trending events from UTA events calendar
def getTrendingEvents():
    events = []
    url = "https://events.uta.edu/#tabs-46950015556440-46950015561563"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        eventsContainer = soup.find("div", {"id": "tabs-46950015556440-46950015561563"})
        
        if not eventsContainer:
            print("Warning: Could not find trending events container")
            print("The page structure may have changed. Returning empty list.")
            return events
        
        trendingEventsContainer = eventsContainer.find("div", class_="em-card-group")
        
        if not trendingEventsContainer:
            print("Warning: Could not find trending events card group")
            print("The page structure may have changed. Returning empty list.")
            return events

        # Process each event - only take first image per event to avoid duplicates
        for eventDiv in trendingEventsContainer.find_all("div", recursive=False):
            try:
                titleContainer = eventDiv.select("h3 a")
                if not titleContainer:
                    continue
                    
                titleText = titleContainer[0].text.strip()

                dateElement = eventDiv.find("p", {"class": "em-card_event-text"})
                if not dateElement:
                    continue
                    
                dateText = dateElement.text.strip()

                # Get only the FIRST image to avoid duplicates
                img = eventDiv.find("img")
                imgSrc = img["src"] if img and img.get("src") else ""

                newEvent = {
                    "title": titleText,
                    "date": dateText,
                    "imgSrc": imgSrc
                }
                
                events.append(newEvent)
                
            except Exception as e:
                print(f"Error processing trending event: {e}")
                continue
    
    except Exception as e:
        print(f"Error fetching trending events: {e}")
    
    return events


if __name__ == "__main__":
    print("Testing scraper...")
    print("\n=== Upcoming Events ===")
    upcoming = getUpcomingEvents()
    print(f"Found {len(upcoming)} upcoming events")
    for event in upcoming[:3]:  # Show first 3
        print(f"  - {event['title']} ({event['date']})")
    
    print("\n=== Trending Events ===")
    trending = getTrendingEvents()
    print(f"Found {len(trending)} trending events")
    for event in trending[:3]:  # Show first 3
        print(f"  - {event['title']} ({event['date']})")
