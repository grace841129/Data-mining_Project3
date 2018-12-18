# -*- coding: utf-8 -*-

import sys
import itertools
from itertools import permutations



if __name__ == "__main__" :


	
	inputFile1 = ("IBM_FPtransaction")

	dataReadIn1 = []

	with open (inputFile1, 'r') as f :
		for line in f :
			dataReadIn1.append ([row for row in line.strip().split(' ')])
	f.close ()
	
	ans_list=[]
	ans_list = [[] for x in range(90)]
	
	ans_list2=[]
	ans_list2 = [[] for x in range(1000)]
	
	cnt=0
	for cnt2 in range(10):
		for cnt3 in range(10):
			if(cnt2 != cnt3):
				ans_list[cnt].append(str(cnt2))
				ans_list[cnt].append(str(cnt3))
				cnt+=1

	fw = open ("graph_7.txt", 'w') 
 
	for cnt1 in range (len(ans_list)) :  
		for cnt2 in range(len(ans_list[0])-1):
			fw.write ("%s," % ans_list[cnt1][cnt2])
		fw.write ("%s\n" % ans_list[cnt1][len(ans_list[0])-1])
	