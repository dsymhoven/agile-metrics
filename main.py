from jira import JIRA
import config
import matplotlib.pyplot as plt
import numpy as np
import random

# functions
def get_intersect(a1, a2, b1, b2):
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack([a1,a2,b1,b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return (float('inf'), float('inf'))
    return (x/z, y/z)

def calc_range_until_finsihed_with(number):
    PBI_finsished = PBI_cumulative[-1]
    sprints = 0
    while PBI_finsished < number_PBI_to_be_finished:
        PBI_finsished += number
        sprints += 1

    return sprints

def monte_carlo_simulation(trials: int):
    sprintdistribution = []
    for _ in range(trials):
        sprints = 0
        PBI_finsished = PBI_cumulative[-1]
        while PBI_finsished < number_PBI_to_be_finished:
            PBI_finsished += random.choice(PBI_finished_per_sprint)
            sprints += 1
        sprintdistribution.append(sprints)

    return sprintdistribution

def plot_histogram(distribution: [int]):
    plt.figure(0)
    plt.hist(distribution, density=True)
    percentiles = np.percentile(distribution, [25, 50, 75, 95])

    plt.axvline(percentiles[0], ymax = 0.5, linestyle = ':', color = 'green')
    plt.axvline(percentiles[1], ymax = 0.6, linestyle = ':', color = 'green')
    plt.axvline(percentiles[2], ymax = 0.7, linestyle = ':', color = 'green')
    plt.axvline(percentiles[3], ymax = 0.8, linestyle = ':', color = 'green')
    plt.axis([0, 10, 0, 1])

    plt.text(percentiles[0], 0.5, '25%')
    plt.text(percentiles[1], 0.6, '50%')
    plt.text(percentiles[2], 0.7, '70%')
    plt.text(percentiles[3], 0.8, '95%')
    plt.title('MonteCarlo simulation with percentiles')
    plt.show()

def plot_mc_validation(sampleDistribution: [int]):
    validationDistribution = random.choices(sampleDistribution, k=10000)

    plt.figure(1)
    plt.hist(sampleDistribution, density=True, label="sample Distribution")
    plt.hist(validationDistribution, density=True, alpha=0.3, label="validation")
    plt.legend(loc='upper right')
    plt.show()



# config
PBI_finished_per_sprint = [6, 0, 6, 11, 5, 5, 6, 7, 11, 10, 10, 3, 5, 5, 13, 10, 14, 12, 10, 14, 4, 14, 11, 8, 13, 8]
number_PBI_to_be_finished = 260
dates = ['15/04/20', '21/04/20', '06/05/20', '19/05/20', '02/06/20', '16/06/20', '30/06/20', '14/07/20', '28/07/20',
         '11/08/20', '25/08/20', '09/09/20', '22/09/20', '08/10/20', '20/10/20', '03/11/20', '17/11/20', '01/12/20',
         '15/12/20', '12/01/21', '26/01/21', '09/02/21', '24/02/21', '10/03/21', '23/03/21', '06/04/21', '20/04/21',
         '04/05/21', '18/05/21', '01/06/21', '15/06/21', '29/06/21', '13/07/21', '27/07/21', '10/08/21', '24/08/21',
         '07/09/21']

# basic forecast calculations
PBI_cumulative = np.cumsum(PBI_finished_per_sprint)
PBI_average = np.average(PBI_finished_per_sprint)
PBI_stddeviation = np.std(PBI_finished_per_sprint)


# simulations
distribution = monte_carlo_simulation(10000)
plot_mc_validation(distribution)
plot_histogram(distribution)

# forecast number of sprints based on std deviation
amount_sprints_average = calc_range_until_finsihed_with(PBI_average)
amount_sprints_worst_case = calc_range_until_finsihed_with(PBI_average - PBI_stddeviation)
amount_sprints_best_case = calc_range_until_finsihed_with(PBI_average + PBI_stddeviation)

# number of forecasted PBIs per sprint in the future stores in an array
future_average_array = [PBI_average for x in range(amount_sprints_average)]
future_worst_case_array = [PBI_average - PBI_stddeviation for x in range(amount_sprints_worst_case)]
future_best_case_array = [PBI_average + PBI_stddeviation for x in range (amount_sprints_best_case)]

# insert number of currently finished PBIs in order to be able to calculate cumulative
future_average_array.insert(0, PBI_cumulative[-1])
future_worst_case_array.insert(0, PBI_cumulative[-1])
future_best_case_array.insert(0, PBI_cumulative[-1])

# calculate cumulative PBIs
forecast_average = np.cumsum(future_average_array)
forecast_worst_case = np.cumsum(future_worst_case_array)
forecast_best_case = np.cumsum(future_best_case_array)


scope_to_be_finished_line = np.array([number_PBI_to_be_finished for x in range(len(dates))])

# first element of forecasts is last element of cumulative.
# -2 because I want the beginning of the sprint when stories will be finished
date_best_case = dates[len(PBI_finished_per_sprint) - 1 + len(forecast_best_case) - 2]
date_average = dates[len(PBI_finished_per_sprint) - 1 + len(forecast_average) - 2]
date_worst_case = dates[len(PBI_finished_per_sprint) - 1 + len(forecast_worst_case) - 2]


plt.figure(2)
plt.plot(dates[0:len(PBI_finished_per_sprint)], PBI_cumulative, label='PBI cumulative')
plt.plot(dates[len(PBI_finished_per_sprint) - 1:len(PBI_finished_per_sprint) - 1 + len(forecast_average)], forecast_average, label='forecast average')
plt.plot(dates[len(PBI_finished_per_sprint) - 1:len(PBI_finished_per_sprint) - 1 + len(forecast_worst_case)], forecast_worst_case, label='forecast worst case')
plt.plot(dates[len(PBI_finished_per_sprint) - 1:len(PBI_finished_per_sprint) - 1 + len(forecast_best_case)], forecast_best_case, label='forecast best case')
plt.axvline(x=date_best_case, color='b', linestyle='--')
plt.axvline(x=date_average, color='b', linestyle='--')
plt.axvline(x=date_worst_case, color='b', linestyle='--')
plt.plot(dates, scope_to_be_finished_line)
plt.legend(loc='upper left')
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