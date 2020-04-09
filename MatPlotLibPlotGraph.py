from matplotlib import pyplot as plt
import matplotlib
import pandas as pd
import numpy as np


plt.style.use('seaborn')

DATA = pd.read_csv('Covid19Result.csv')


labels = DATA['Date'] #x-values


confirm = DATA['Confirmed']
death = DATA['Deaths']
recover = DATA['Recovered']
act = DATA['Active']


x = np.arange(len(labels))
width = 0.4


fig, ax = plt.subplots()


rects1 = ax.barh(x+width/2,confirm, width, color='#204051', label='Confirmed')
rects2 = ax.barh(x-width/2, act, width, color='#1eb2a6', label='Active')
rects3 = ax.barh(x+width/4, recover, width, color='#ffb0cd', label='Recovered')
rects4 = ax.barh(x-width/4, death, width, color='#dd2c00', label='Deaths') #3b6978

ax.set_title('Covid19 in India')
ax.set_xlabel('Number of People')
ax.set_yticks(x)
ax.set_yticklabels(labels)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), shadow=True, ncol=4)


def autolabel(rects):
	"""Attach a text label above each bar in *rects*, displaying its height."""
	for rect in rects:
		height = rect.get_height()
		ax.annotate('{}'.format(height),
			xy=(rect.get_x() + rect.get_width() / 2, height),
			xytext=(0, 1),  # 3 points vertical offset
			textcoords="offset points", ha='center', va='top')



fig.tight_layout()

plt.show()
