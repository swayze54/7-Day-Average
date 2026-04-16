import csv
import requests


def main():
    # Read NYTimes Covid Database
    download = requests.get(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
    )
    decoded_content = download.content.decode("utf-8")
    file = decoded_content.splitlines()
    reader = csv.DictReader(file)

    # Construct 14 day lists of new cases for each states
    new_cases = calculate(reader)

    # Create a list to store selected states
    states = []
    print("Choose one or more states to view average COVID cases.")
    print("Press enter when done.\n")

    while True:
        state = input("State: ")
        if state in new_cases:
            states.append(state)
        if len(state) == 0:
            break

    print(f"\nSeven-Day Averages")

    # Print out 7-day averages for this week vs last week
    comparative_averages(new_cases, states)


def calculate(reader):
    new_cases = {}
    previous_cases = {}
    for row in reader:
        state = row["state"]
        cases = int(row["cases"])

        if state not in previous_cases:
            previous_cases[state] = cases
            new_cases[state] = []

        new = cases - previous_cases[state]
        previous_cases[state] = cases

        new_cases[state].append(new)
        if len(new_cases[state]) > 14:
            new_cases[state].pop(0)

    return new_cases

def comparative_averages(new_cases, states):

    this_week = {}
    last_week = {}
    for state in states:
        this_week[state] = []
        last_week[state] = []
        index = 13

        while True:
            if 0 <= index < 7:
                case = new_cases[state].pop(index)
                this_week[state].append(case)
                index -= 1
            elif index >= 7:
                case = new_cases[state].pop(index)
                last_week[state].append(case)
                index -= 1
            else:
                break

    for state in this_week:
        try:
            this_week_average = round(sum(this_week[state]) / 7)
            last_week_average = round(sum(last_week[state]) / 7)
        except: ZeroDivisionError

        try:
            biweekly_percent = round((this_week_average - last_week_average) / ((this_week_average + last_week_average) / 2) * 100)
            if biweekly_percent > 0:
                direction = "an increase"
            else:
                direction = "a decrease"
        except: ZeroDivisionError

        print(f"{state} had a 7-day-average of {this_week_average} and {direction} of {abs(biweekly_percent)}%")


main()

