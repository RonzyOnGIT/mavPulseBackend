from scraper import getDepartments

depts = getDepartments()


for dept in depts:
    arr = dept.split()
    deptNum = arr[-1]
    deptNumTrimmed = deptNum[1:-1]
    print(deptNumTrimmed)


# print(depts)