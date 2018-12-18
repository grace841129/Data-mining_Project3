import sys
import math
import time
import copy
from copy import deepcopy
import numpy
import itertools
from math import sin, asin, cos, radians, fabs, sqrt 

def readfile(filename) :

	inputfile = str(filename)
	dataReadIn = []

	with open (inputfile, 'r') as f :
		for line in f :
			dataReadIn.append ([row for row in line.strip().split(',')])

	return dataReadIn

def nodeset(datalist):

	temp=[]
	node_set=[]
	for i in range(len(datalist)):
		for j in range(len(datalist[0])):
			temp.append(datalist[i][j])
			node_set=sorted(set(temp))#set去掉重複
	return node_set

def HITS(node,data):
	t1=time.time()

	iter_max=sys.argv[1]
	threshold=sys.argv[2]

	hub={}
	authority={}
	for i in range(len(node)): #皆先初始化為1
		hub[node[i]]=1
		authority[node[i]]=1

	#計算所有node的hub authority
	is_stop=False
	count=False
	for i in range(int(iter_max)):
		para=0 #標準化
		change=0 #每次變化量

		#compute authority
		auth_temp=authority.copy()
		for x in range(len(node)):
			authority[node[x]]=0 #先歸零
			for y in range(len(data)):
				if(data[y][1] == node[x]):
					authority[node[x]]+=hub[data[y][0]]
			para+=pow(authority[node[x]],2)

		#標準化
		para=sqrt(para)
		for x in range(len(node)):
			authority[node[x]] /= para
			change+=abs(auth_temp[node[x]]-authority[node[x]]) #差值的絕對值

		#compute hub
		para=0
		hub_temp=hub.copy()
		for x in range(len(node)):
			hub[node[x]]=0
			for y in range(len(data)):
				if(data[y][0] == node[x]):
					hub[node[x]]+=authority[data[y][1]]
			para+=pow(hub[node[x]],2)

		#標準化
		para=sqrt(para)
		for x in range(len(node)):
			hub[node[x]]/=para
			change+=abs(hub_temp[node[x]]-hub[node[x]])

		if(change < float(threshold)):
			is_stop=True
			break
		
		t=time.time()
		#超過三小時則停止
		if(t-t1 == 10800): 
			count=True
			break

	t2=time.time()

	print("HITS Result:")
	#print("Hub:"+str(hub))
	#print("Authority:"+str(authority))
	if is_stop:
		print("Converge after "+str(i+1)+" times of iterations.")
	else:
		print("Cannot converge in "+str(sys.argv[1])+" times.")

	print("Best authority node : ", max(authority.items(), key=lambda x: x[1]))
	print("Best hub node : ", max(hub.items(), key=lambda x: x[1]))
	if count:
		print("HITS computing time : More than THREE hours!")
	else:
		print("HITS computing time : "+str(t2-t1)+" sec")
	print("------------------------------------------------------------")

def PageRank(node,data):
	t1=time.time()

	iter_max=sys.argv[1]
	threshold=sys.argv[2]
	damping=0.15
	node_count=len(node)

	outdegree={}
	for i in range(node_count):
		outdegree[node[i]]=0

	#compute each node's outdegree
	for i in range(node_count):
		for j in range(len(data)):
			if(data[j][0] == node[i]):
				outdegree[node[i]]+=1

	#沒有outdegree的點皆預設為->對其他所有點都有edge
	data_len=len(data)
	for x in range(node_count):
		if(outdegree[node[x]]==0):
			for y in range(node_count):
				if(node[x] != node[y]):
					data.append([node[x],node[y]])
					outdegree[node[x]]+=1
	data_len=len(data)

	#compute pagerank
	PR={}
	for x in range(node_count):
		PR[node[x]]=1
	d_value=damping/node_count #d/N

	is_stop=False
	count=False
	for i in range(int(iter_max)):
		change=0
		for x in range(node_count):
			rank=0
			for y in range(data_len):
				if(data[y][1] == node[x]):
					rank+=((1-damping) * ((PR[data[y][0]]) / (outdegree[data[y][0]])))
			rank+=d_value
			change+=abs(PR[node[x]]-rank)
			PR[node[x]]=rank

		if(change < float(threshold)):
			is_stop=True
			break

		t=time.time()
		#超過三小時則停止
		if(t-t1 == 10800): 
			count=True
			break

	t2=time.time()

	print("PageRank Result:")
	#print("PageRank:"+str(PR))
	if is_stop:
		print("Converge after "+str(i+1)+" times of iterations.")
	else:
		print("Cannot converge in "+str(sys.argv[1])+" times.")

	print("Best PageRank node : ", max(PR.items(), key=lambda x: x[1]))
	if count:
		print("PageRank computing time : More than THREE hours!")
	else:
		print("PageRank computing time : "+str(t2-t1)+" sec")
	print("------------------------------------------------------------")

def indegree_fun(node,data):
	inde=[]
	for i in range(len(data)):
		if(data[i][1] == node):
			inde.append(data[i][0])
	return inde

def SimRank(node,data):
	t1=time.time()

	C=sys.argv[3] #default 0.8
	iter_max=sys.argv[1]
	threshold=sys.argv[2]
	node_count=len(node)

	indegree={}
	for x in range(node_count):
		indegree[node[x]]=0

	#compute indegree
	for x in range(node_count):
		for y in range(len(data)):
			if(data[y][1]==node[x]):
				indegree[node[x]]+=1

	sim_before=[]
	simrank=[]

	for x in range(node_count):
		sim_before.append(0)
		simrank.append([])

	for x in range(node_count):
		for y in range(node_count):
			if(y == x):
				simrank[x].append(1)
			else:
				simrank[x].append(0)

	is_stop=False
	count=False
	for i in range(int(iter_max)):
		sim_before=copy.deepcopy(simrank)	#copy.deepcopy不會跟著list改變
		change=0

		for x in range(node_count):
			for y in range(node_count):
				start_node=indegree_fun(node[x],data)
				end_node=indegree_fun(node[y],data)

				if(indegree[node[x]] == 0) or (indegree[node[y]] == 0):
					simrank[int(node[x])-1][int(node[y])-1]=0
				else:
					s=0
					for z in range(len(start_node)):
						for w in range(len(end_node)):
							s+=sim_before[int(start_node[z])-1][int(end_node[w])-1]
					simrank[int(node[x])-1][int(node[y])-1] = (float(C)*s)/(indegree[node[x]]*indegree[node[y]])

		for x in range(len(simrank)):
			for y in range(len(simrank[0])):
				change+=abs(simrank[x][y]-sim_before[x][y])

		if(change < float(threshold)):
			is_stop=True
			break

		t=time.time()
		#超過三小時則停止
		if(t-t1 == 10800): 
			count=True
			break
	t2=time.time()

	print("SimRank Result:")
	if is_stop:
		print("Converge after "+str(i+1)+" times of iterations.")
	else:
		print("Cannot converge in "+str(sys.argv[1])+" times.")

	print("SimRank :",end=" ")
	print(simrank)
	if count:
		print("SimRank computing time : More than THREE hours!")
	else:
		print("SimRank computing time : "+str(t2-t1)+" sec")
	print("------------------------------------------------------------")

if __name__ == '__main__':
	
	for i in range(8):
		a=readfile("graph_"+str(i+1)+".txt")
		b=nodeset(a)
		print("graph_"+str(i+1)+".txt")
		HITS(b , a )
		PageRank(b,a)

		if(i <= 3):
			SimRank(b,a)
	'''
	i=2
	a=readfile("graph_"+str(i+1)+".txt")
	b=nodeset(a)
	print("graph_"+str(i+1)+".txt")
	HITS(b , a )
	PageRank(b,a)
	'''
	print()