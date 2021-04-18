from jira import JIRA
import professional
import voice
import matplotlib.pyplot as plt
import numpy as np
import random

# functions
def calc_range_until_finsihed_with(number):
    PBI_finsished = PBI_cumulative[-1]
    sprints = 0
    while PBI_finsished < PBI_to_be_finished[-1]:
        PBI_finsished += number
        sprints += 1

    return sprints

def monte_carlo_simulation(trials: int):
    sprintdistribution = []
    for _ in range(trials):
        sprints = 0
        PBI_finsished = PBI_cumulative[-1]
        while PBI_finsished < PBI_to_be_finished[-1]:
            PBI_finsished += random.choice(PBI_finished_per_sprint)
            sprints += 1
        sprintdistribution.append(sprints)

    return sprintdistribution

# ==========================================================
# configuration
# ==========================================================


PBI_finished_per_sprint = professional.PBI_finished_per_sprint
PBI_to_be_finished = professional.PBI_to_be_finished
scope_changed_dates = professional.scope_changed_dates
dates = professional.dates
monte_carlo_trials = 10000
quantiles = [50, 80, 95]
plot_validation = False
plot_monte_carlo = False
plot_forecast = True


# ==========================================================
# Core Routine
# ==========================================================

# basic forecast calculations
PBI_cumulative = np.cumsum(PBI_finished_per_sprint)
PBI_average = np.average(PBI_finished_per_sprint)
PBI_stddeviation = np.std(PBI_finished_per_sprint)

# monte carlo simulation
distribution = monte_carlo_simulation(monte_carlo_trials)

# Calc percentiles and related dates
percentiles = np.percentile(distribution, quantiles)
date_quantile_1 = dates[len(PBI_finished_per_sprint) - 1 + int(percentiles[0])]
date_quantile_2 = dates[len(PBI_finished_per_sprint) - 1 + int(percentiles[1])]
date_quantile_3 = dates[len(PBI_finished_per_sprint) - 1 + int(percentiles[2])]

# forecast number of sprints based on std deviation
amount_sprints_average = calc_range_until_finsihed_with(PBI_average)
amount_sprints_worst_case = calc_range_until_finsihed_with(PBI_average - PBI_stddeviation)
amount_sprints_best_case = calc_range_until_finsihed_with(PBI_average + PBI_stddeviation)

# number of forecasted PBIs per sprint in the future stored in an array
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

# first element of forecasts is last element of cumulative.
# -2 because I want the beginning of the sprint when stories will be finished
date_best_case = dates[len(PBI_finished_per_sprint) - 1 + len(forecast_best_case) - 2]
date_average = dates[len(PBI_finished_per_sprint) - 1 + len(forecast_average) - 2]
date_worst_case = dates[len(PBI_finished_per_sprint) - 1 + len(forecast_worst_case) - 2]



# ==========================================================
# Plots
# ==========================================================

# validation of random numbers
if plot_validation:
    validationDistribution = random.choices(PBI_finished_per_sprint, k=10000)
    plt.figure(0)
    plt.hist(PBI_finished_per_sprint, density=True, label="sample Distribution")
    plt.hist(validationDistribution, density=True, alpha=0.3, label="validation")
    plt.title('Validation of random numbers distribution')
    plt.xlabel('PBIs finished per Sprint')
    plt.ylabel('density')
    plt.legend(loc='upper right')

# histogram monte carlo
if plot_monte_carlo:
    plt.figure(1)
    plt.hist(distribution, density=True)

    plt.axvline(percentiles[0], ymax=0.5, linestyle=':', color='green')
    plt.axvline(percentiles[1], ymax=0.6, linestyle=':', color='green')
    plt.axvline(percentiles[2], ymax=0.7, linestyle=':', color='green')
    plt.axis([0, max(distribution), 0, 1])

    plt.text(percentiles[0], 0.5, str(quantiles[0]) + str('%'))
    plt.text(percentiles[1], 0.6, str(quantiles[1]) + str('%'))
    plt.text(percentiles[2], 0.7, str(quantiles[2]) + str('%'))
    plt.title('MonteCarlo simulation with percentiles')

# forecast
if plot_forecast:
    plt.figure(2)

    plt.plot(dates[0:len(PBI_finished_per_sprint)], PBI_cumulative, label='PBI cumulative')
    plt.plot(dates[len(PBI_finished_per_sprint) - 1:len(PBI_finished_per_sprint) - 1 + len(forecast_average)], forecast_average, label='forecast average')
    plt.plot(dates[len(PBI_finished_per_sprint) - 1:len(PBI_finished_per_sprint) - 1 + len(forecast_worst_case)], forecast_worst_case, label='forecast worst case')
    plt.plot(dates[len(PBI_finished_per_sprint) - 1:len(PBI_finished_per_sprint) - 1 + len(forecast_best_case)], forecast_best_case, label='forecast best case')

    plt.axvline(x=date_quantile_1, color='b', linestyle='--')
    plt.axvline(x=date_quantile_2, color='b', linestyle='--')
    plt.axvline(x=date_quantile_3, color='b', linestyle='--')
    plt.text(x=date_quantile_2, y=plt.gca().get_ylim()[1], s=str(quantiles[1]) + str('%'))
    plt.plot(scope_changed_dates, PBI_to_be_finished)
    plt.legend(loc='upper left')
    plt.title('Forecast with std = ' + "{:.2f}".format(PBI_stddeviation))

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