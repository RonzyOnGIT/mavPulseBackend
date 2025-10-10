# This file is responsible for making calls to the scraper, and clean up data so that the server can get data to server to database and client

from scraper import getDepartments
from scraper import getCourses


depts = {}

# deptartments is like 'Accounting (ACCT)'
departments = getDepartments()

# create dictionary with key values for departments and values of empty arrays
# the values will be an array of all classes for department
counter = 0
for dept in departments:
    depts[dept] = None
    counter += 1


# loop through each department and add every class for each department to the corresponding department
for dept in departments:

    print(f"fetching courses for {dept}...")
    # split the string into array of strings with delim of " "
    arr = dept.split()

    # remove the '()' 
    deptNum = arr[-1]
    deptNumTrimmed = deptNum[1:-1]

    # one of the courses has a '/' instead of '-' so just return BSAD for which is actual course number used
    if "/" in deptNumTrimmed:
        deptNumTrimmed = "BSAD"

    # deptCourses is the array of every course for a department like CSE department
    deptCourses = getCourses(deptNumTrimmed) 

    # this will hold the courses without the extra fluff so its only '(Department and Number) (Class name)'
    deptCoursesTrimmed = []

    # go through each course from the department
    for course in deptCourses:

        # split up each course with the delimeter of '.'
        deptCourseArr = course.split('.')

        # glue back into one string the trimmed version removing fluff
        courseTrimmed = deptCourseArr[0] + deptCourseArr[1]

        deptCoursesTrimmed.append(courseTrimmed)

    depts[dept] = deptCoursesTrimmed


for key, value in depts.items():
    print(f"{key}: {value}\n")

# We would return 'depts' back to the server at which point the server would populate database so we dont have to keep scraping cause its slow
