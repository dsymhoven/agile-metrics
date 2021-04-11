from jira import JIRA
import config
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt



PBI_finished = [6, 0, 6, 11, 5, 5, 6, 7, 11, 10, 10, 3, 5, 5, 13, 10, 14, 12, 10, 14, 4, 14, 11, 8, 13, 8]
PBI_cumulative = np.cumsum(PBI_finished)
PBI_average = np.average(PBI_finished)
PBI_stddeviation = np.std(PBI_finished)
dates = ['15/04/20', '21/04/20', '06/05/20', '19/05/20', '02/06/20', '16/06/20', '30/06/20', '14/07/20', '28/07/20',
         '11/08/20', '25/08/20', '09/09/20', '22/09/20', '08/10/20', '20/10/20', '03/11/20', '17/11/20', '01/12/20',
         '15/12/20', '12/01/21', '26/01/21', '09/02/21', '24/02/21', '10/03/21', '23/03/21', '06/04/21', '20/04/21',
         '04/05/21', '18/05/21', '01/06/21', '15/06/21', '29/06/21']


future_average_array = [PBI_average for x in range(6)]
future_min_array = [PBI_average - PBI_stddeviation for x in range(6)]
future_max_array = [PBI_average + PBI_stddeviation for x in range (6)]

future_average_array.insert(0, PBI_cumulative[-1])
future_min_array.insert(0, PBI_cumulative[-1])
future_max_array.insert(0, PBI_cumulative[-1])

forecast_average = np.cumsum(future_average_array)
forecast_min = np.cumsum(future_min_array)
forecast_max = np.cumsum(future_max_array)



plt.plot(dates[0:len(PBI_finished)], PBI_cumulative)
plt.plot(dates[len(PBI_finished)-1:], forecast_average)
plt.plot(dates[len(PBI_finished)-1:], forecast_min)
plt.plot(dates[len(PBI_finished)-1:], forecast_max)
#plt.plot(dates, forecast_average)
plt.gcf().autofmt_xdate()
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