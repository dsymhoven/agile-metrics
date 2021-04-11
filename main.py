from jira import JIRA
import config
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import random
import datetime as dt



PBI_finished_per_sprint = [6, 0, 6, 11, 5, 5, 6, 7, 11, 10, 10, 3, 5, 5, 13, 10, 14, 12, 10, 14, 4, 14, 11, 8, 13, 8]
number_PBI_to_be_finished = 260
PBI_cumulative = np.cumsum(PBI_finished_per_sprint)
PBI_average = np.average(PBI_finished_per_sprint)
PBI_stddeviation = np.std(PBI_finished_per_sprint)
dates = ['15/04/20', '21/04/20', '06/05/20', '19/05/20', '02/06/20', '16/06/20', '30/06/20', '14/07/20', '28/07/20',
         '11/08/20', '25/08/20', '09/09/20', '22/09/20', '08/10/20', '20/10/20', '03/11/20', '17/11/20', '01/12/20',
         '15/12/20', '12/01/21', '26/01/21', '09/02/21', '24/02/21', '10/03/21', '23/03/21', '06/04/21', '20/04/21',
         '04/05/21', '18/05/21', '01/06/21', '15/06/21', '29/06/21', '13/07/21', '27/07/21', '10/08/21', '24/08/21',
         '07/09/21']

def calc_range_until_finsihed_with(number):
    PBI_finsished = PBI_cumulative[-1]
    number_of_sprints = 1
    while PBI_finsished < number_PBI_to_be_finished:
        PBI_finsished += number
        number_of_sprints += 1

    return number_of_sprints - 1

def monte_carlo_simulation(trials: int):
    sprintdistribution = []
    for _ in range(trials):
        sprints = 0
        PBI_finsished = PBI_cumulative[-1]
        while PBI_finsished < number_PBI_to_be_finished:
            PBI_finsished += random.choice(PBI_finished_per_sprint)
            sprints += 1
        sprintdistribution.append(sprints-1)

    return sprintdistribution

distribution = monte_carlo_simulation(10000)
check = random.choices(PBI_finished_per_sprint, k=1000)

result_average = calc_range_until_finsihed_with(PBI_average)
result_min = calc_range_until_finsihed_with(PBI_average - PBI_stddeviation)
result_max = calc_range_until_finsihed_with(PBI_average + PBI_stddeviation)

future_average_array = [PBI_average for x in range(result_average)]
future_min_array = [PBI_average - PBI_stddeviation for x in range(result_min)]
future_max_array = [PBI_average + PBI_stddeviation for x in range (result_max)]

future_average_array.insert(0, PBI_cumulative[-1])
future_min_array.insert(0, PBI_cumulative[-1])
future_max_array.insert(0, PBI_cumulative[-1])

forecast_average = np.cumsum(future_average_array)
forecast_min = np.cumsum(future_min_array)
forecast_max = np.cumsum(future_max_array)

perc = np.percentile(distribution, [70, 80, 85, 95])
y = np.array([number_PBI_to_be_finished for x in range(len(dates))])

plt.figure(0)
plt.hist(distribution)
plt.title('MC distribution')

plt.figure(1)
plt.plot(dates[0:len(PBI_finished_per_sprint)], PBI_cumulative)
plt.plot(dates[len(PBI_finished_per_sprint) - 1:len(PBI_finished_per_sprint) - 1 + len(forecast_average)], forecast_average)
plt.plot(dates[len(PBI_finished_per_sprint) - 1:len(PBI_finished_per_sprint) - 1 + len(forecast_min)], forecast_min)
plt.plot(dates[len(PBI_finished_per_sprint) - 1:len(PBI_finished_per_sprint) - 1 + len(forecast_max)], forecast_max)
plt.plot(dates, y)
plt.gcf().autofmt_xdate()

plt.figure(2)
plt.title('PBI finsished distribution')
plt.hist(PBI_finished_per_sprint)

plt.figure(3)
plt.hist(check)
plt.title('check')

plt.show()



# jira = JIRA(basic_auth=(config.username, config.password), options={'server': config.server})
#
# firstSprint = 96
# lastSprint = 100
# finishedItemsPerSprint = []
#
# for sprint in range(firstSprint, lastSprint + 1):
#     finishedItems = []
#     for issue in jira.search_issues('project = MIELCLD3 AND component = Professional AND Sprint = "Team Professional Sprint ' + str(sprint) + '"'):
#         print(issue.fields.issuetype)
#         if (issue.fields.issuetype.name == 'Story' or issue.fields.issuetype.name == 'Aufgabe') and issue.fields.status.name == 'Abgenommen':
#             finishedItems.append(issue)
#     finishedItemsPerSprint.append(len(finishedItems))
#
#
# print(finishedItemsPerSprint)
#
# plt.plot(list(range(firstSprint, lastSprint+1)), np.cumsum(finishedItemsPerSprint))
# plt.show()