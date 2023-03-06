#!/usr/bin/python3

from models.Schedule import Create_Schedule
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

class Plot:
    def __init__(self):
        """
            creates an instance of the user database and queries 
            the Average column based on the date
        """
        self.schedule = Create_Schedule()
        self.data = self.schedule.View()
        self.Days = []
        self.average = []
        for key, value in self.data.items():
            if self.data[key]['Target'] == 1:
                         self.Days.append(datetime.strptime(self.data[key]\
                                            ["Date"], "%Y-%m-%d"))
                         self.average.append(self.data[key]['Average'])

    def show(self):
        """
            class method finds the mean average of a date and plots a graph
            of the queried user Average against date over a specified period 
        """
            
        date_average = defaultdict(list)
        for date, avg in zip(self.Days, self.average):
            date_average[date].append(avg)
        date_mean_avg = {date: sum(avgs) / len(avgs) for date, avgs
                            in date_average.items()}
        plt.bar(date_mean_avg.keys(), date_mean_avg.values(), width=0.4)
        plt.xlabel('Date')
        plt.ylabel('Average Score')
        plt.title('Daily Average Score')
        plt.xticks(rotation=25)
        plt.show()

    def Daily(self):
        plt.plot(self.Days, self.average)

        # Add labels
        plt.xlabel('Date')
        plt.ylabel('Average Score')
        plt.xticks(rotation=25)
        # Show the plot
        plt.show() 
