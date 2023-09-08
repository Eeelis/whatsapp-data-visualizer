#https://towardsdatascience.com/analyzing-whatsapp-chats-with-python-20d62ce7fe2d
#https://whatstk.readthedocs.io/en/stable/source/about.html

from whatstk import WhatsAppChat, FigureBuilder
from whatstk.graph import plot
import matplotlib.pyplot as plt
import numpy
import re
import os
from collections import Counter

chat = WhatsAppChat.from_source(os.path.dirname(os.path.realpath(__file__)) + "\\Log.txt")
chat = chat.rename_users({"NameToDisplay": ["NameInChat"]})
fb = FigureBuilder(chat=chat)

def main():

	show_graphs = False

	messages = []
	words = []
	non_words = ["media", "omitted"]

	for row in chat.df.message:
		messages.append(row)

	for row in messages:

		row = re.sub('[^A-Öa-ö0-9]+', " ", row)
		querywords = row.split()
		resultwords  = [word for word in querywords if word.lower() not in non_words and len(word) > 1]

		for word in resultwords:
			words.append(word)

	if show_graphs:
		plot_total_messages_sent()
		plot_total_messages_sent_by_user()
		plot_total_characters_sent()
		plot_characters_sent_by_user()
		plot_messages_sent_by_hour()
		plot_interaction_flow()
	
	find_most_common_words(words)

def plot_total_messages_sent():
	figure = fb.user_interventions_count_linechart(cumulative=True, all_users=True, title="Messages Sent", xlabel="Time", legend_label="Messages Sent")
	plot(figure)

def plot_total_messages_sent_by_user():
	figure = fb.user_interventions_count_linechart(cumulative=True, all_users=False, title="Messages Sent", xlabel="Time")
	plot(figure)

def plot_total_characters_sent():
	fig = fb.user_interventions_count_linechart(msg_length=True, cumulative=True, all_users=True, title="Characters Sent", legend_label="Characters Sent")
	plot(fig)

def plot_characters_sent_by_user():
	fig = fb.user_interventions_count_linechart(msg_length=True, cumulative=True, title="Characters sent by User")
	plot(fig)

def plot_messages_sent_by_hour():
	fig = fb.user_interventions_count_linechart(date_mode='hour', title='Messages Sent', xlabel='Hour')
	plot(fig)

def plot_interaction_flow():
	fig = FigureBuilder(chat=chat).user_message_responses_flow()
	plot(fig)

def find_most_common_words(words):
	words = Counter(words)
	res = words.most_common(20)
	names, values = zip(*res)
	ind = numpy.arange(len(res))

	width = 0.2
	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, values, width, color='r')
	ax.set_ylabel('Count')
	ax.set_xticks(ind+width)
	ax.set_xticklabels(names, rotation=45)

	plt.show()

if __name__ == "__main__":
    main()

