from jira import JIRA
import config
import matplotlib.pyplot as plt

jira = JIRA(basic_auth=(config.username, config.password), options={'server': config.server})

firstSprint = 96
lastSprint = 100
finishedItemsPerSprint = []

for sprint in range(firstSprint, lastSprint + 1):
    finishedItems = []
    for issue in jira.search_issues('project = MIELCLD3 AND component = Voice AND Sprint = "Team Voice Sprint ' + str(sprint) + '"'):
        print(issue.fields.issuetype)
        if (issue.fields.issuetype.name == 'Story' or issue.fields.issuetype.name == 'Aufgabe') and issue.fields.status.name == 'Abgenommen':
            finishedItems.append(issue)
    finishedItemsPerSprint.append(len(finishedItems))


print(finishedItemsPerSprint)

plt.plot(range(firstSprint, lastSprint+1), finishedItemsPerSprint)
plt.show()