import arxivscraper
import pandas as pd
import networkx as nx

#STEP 1 Scrape
###################################################
print('starting scraper')
scraper = arxivscraper.Scraper(category='cs', date_from='2017-05-29',date_until='2017-06-01')
output = scraper.scrape()
cols = ('title', 'authors')
df = pd.DataFrame(output,columns=cols)

#df.to_csv('out.csv', sep=',')
#df = pd.read_csv('out.csv')

#STEP 2 Social Network Creation and Visualization
###################################################

##convert col to list of authors per book
#indexs for 2 things combins while making combos
import numpy as np
from itertools import combinations

#authors = df['authors']
authors = df.authors.astype(str)
title = df['title']

#print (type(authors)) #nparray
authors = authors.str.replace('[', '')
authors = authors.str.replace("'", "")
authors = authors.str.replace(']', '')

count = 0
authorFirst = np.array([])
authorSecond = np.array([])
authorTitle = np.array([])	


print('generating Edgelist combos from data')
for i in authors:
	#for every title
	#print(count)
	coAuthors = authors[count].split(",")
	#we have a list of co authors 
	#find every combination
	r=2
	coAuthorcombos = list(combinations(coAuthors, r)) 
	#print(coAuthorcombo)
	#print(type(coAuthorcombo))#list
	
	try:
		#print(coAuthorcombos[0])
		#print(type(coAuthorcombos[0]))#tuple
		#print(coAuthorcombos[0][0])
		#print(type(coAuthorcombos[0][0]))#str
		ccc = 0
		for j in coAuthorcombos:
				authors1 = coAuthorcombos[ccc][0]
				authors2 = coAuthorcombos[ccc][1]
				authorT = title[count]
				ccc = ccc+1
				authorFirst= np.append(authorFirst,authors1)
				authorSecond= np.append(authorSecond,authors2)
				authorTitle = np.append(authorTitle,authorT)
	except IndexError:
		print('sorry, no [0]')

	
	count = count+1


#make new dataframe 	
#print(authorFirst)
inputData = {'author1':authorFirst, 'author2':authorSecond, 'title':authorTitle}
ddf = pd.DataFrame(data=inputData)
print('Edgelist generated')

G = nx.from_pandas_edgelist(ddf, source='author1', target='author2', edge_attr='title', create_using=nx.DiGraph())
print('Graph G created')

import matplotlib.pyplot as plt
import networkx as nx

print ('Draw/Plot Visualization starting')
print ('close figure to continue...')
pos = nx.spring_layout(G)
colors = range(G.number_of_edges())
nx.draw(G, pos, node_color='#A0CBE2', edge_color=colors, width=3, edge_cmap=plt.cm.Blues, with_labels=True)
plt.show()
print ('Draw/Plot Visualization done')

#STEP 3: Calculate network measures
##################################################

import matplotlib.pyplot as plt
import collections

#DEGREE DISTRIBUTION
print ('Degree Distribution Histogram starting')
print ('close figure to continue...')
GG = nx.from_pandas_edgelist(ddf, source='author1', target='author2', edge_attr='title')
degree_sequence = sorted([d for n, d in GG.degree()], reverse=True)  # degree sequence
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())
fig, ax = plt.subplots()
plt.bar(deg, cnt, width=0.80, color='b')
plt.title("Degree Histogram")
plt.ylabel("Count")
plt.xlabel("Degree")
ax.set_xticks([d + 0.4 for d in deg])
ax.set_xticklabels(deg)
plt.axes([0.4, 0.4, 0.5, 0.5])
Gcc = sorted(nx.connected_component_subgraphs(GG), key=len, reverse=True)[0]
pos = nx.spring_layout(GG)
plt.axis('off')
nx.draw_networkx_nodes(GG, pos, node_size=20)
nx.draw_networkx_edges(GG, pos, alpha=0.4)
plt.show()
print ('Degree Distribution Histogram done')

#CHOOSE TWO:
#centrality: degree, eigenvector, katz, pagerank, betweenness, closeness, group
#transitivity, reciprocity, similarity (structural, regular)

#FIRST NETWORK MEASURE
print("first network measure")
print("transitivity:")
print(nx.transitivity(G))

#SECOND NETOWRK MEASURE
print("second network measure")
print("reciprocity:")
print(nx.reciprocity(G))
