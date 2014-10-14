# Run as $ python rec.py

from math import sqrt
import random
import operator

def loadMovieLens(path='./data'):
	# Get movie titles
	movies={}
	for line in open(path+'/movies.dat'):
		(id,title)=line.split('|')[0:2]
		movies[id]=title
	# Load data
	prefs={}
	for line in open(path+'/ratings.dat'):
		(user,movieid,rating)=line.split('\t')[0:3]
		prefs.setdefault(user,{})
		prefs[user][movies[movieid]]=float(rating)
	return prefs

# Pearson co-relation formula
def sim_pearson(prefs,p1,p2):
	# Get the list of mutually rated items                      
	si={}                                                       
	for item in prefs[p1]:                                      
		if item in prefs[p2]: 
			si[item]=1                          
	# Find the number of elements                               
	n=len(si)                                                   
	# if they are no ratings in common, return 0                
	if n==0:
		 return 0                                           
	# Add up all the preferences                                
	sum1=sum([prefs[p1][it] for it in si])                      
	sum2=sum([prefs[p2][it] for it in si])                      
	# Sum up the squares                                        
	sum1Sq=sum([pow(prefs[p1][it],2) for it in si])             
	sum2Sq=sum([pow(prefs[p2][it],2) for it in si])             
	# Sum up the products                                       
	pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])        
	# Calculate Pearson score                                   
	num=pSum-(sum1*sum2/n)                                      
	den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))     
	if den==0:
		return 0                                         
	r=num/den
	# print 'the r is: ', r
	return r

# Returns a distance-based similarity score for person1 and person2
# Euclidean distance score
def sim_distance(prefs,person1,person2):                                  
	# Get the list of shared_items                                          
	si={}                                                                   
	for item in prefs[person1]:                                             
		if item in prefs[person2]:                                            
			si[item]=1                                                        
	# if they have no ratings in common, return 0                           
	if len(si)==0: 
		return 0                                                 
	# Add up the squares of all the differences                             
	sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])
	return 1/(1+sum_of_squares)

# Adjusted cosine formula
def sim_cosine(prefs, p1, p2):
	  si={}
	  for item in prefs[p1]:
	    if item in prefs[p2]:  si[item]=1
	  n = len(si)
	  if n == 0 : return 0
	  # calculate the averge rationg made by both users
	  sum1 = sum([prefs[p1][it] for it in prefs[p1]]) 
	  sum2 = sum([prefs[p2][it] for it in prefs[p2]])
	  ave_1 = sum1/len(prefs[p1])
	  ave_2 = sum2/len(prefs[p2])

	  pSum = sum([(prefs[p1][it]-ave_1) * (prefs[p2][it]-ave_2) for it in si])
	  #

	  sum1Sq = sum([pow(prefs[p1][it]-ave_1, 2) for it in si])
	  sum2Sq = sum([pow(prefs[p2][it]-ave_2, 2) for it in si])
	  #
	  den = sqrt(sum1Sq) * sqrt(sum2Sq)
	  if den == 0 : return 0
	  r = pSum/den
	  #print 'the r is : ', r
	  return r


def calculateSimilarItems(prefs,n=30):
	# Create a dictionary of items showing which other items they
	# are most similar to.
	result={}
	# Invert the preference matrix to be item-centric
	itemPrefs = transformPrefs(prefs)
	c=0
	for item in itemPrefs:
		# Status updates for large datasets
		c+=1
		if (c % 100 == 0): 
			print "%d / %d" % (c,len(itemPrefs))
		# Find the most similar items to this one
		scores=topMatches(itemPrefs,item,n=n,similarity=sim_pearson)
		result[item]=scores
	return result

def transformPrefs(prefs):
	result={}                                        
	for person in prefs:                             
		# print 'person is',person
		for item in prefs[person]:                     
			# print 'item in prefs[person]: ', item
			result.setdefault(item,{})                   
			# Flip item and person                       
			result[item][person]=prefs[person][item]     
	return result
	
def topMatches(prefs,person,n=5,similarity=sim_pearson):
	scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]
	# Sort the list so the highest scores appear at the top 
	scores.sort( )
	scores.reverse( )
	return scores

# User based CF recommendations
def getRecommendations(prefs,person,similarity=sim_pearson):
	totals={}                                                       
	simSums={}                                                      
	for other in prefs:                                             
		# don't compare me to myself                                  
		if other==person: 
			continue                                    
		sim=similarity(prefs,person,other)                            
		# ignore scores of zero or lower                              
		if sim<=0: 
			continue                                           
		for item in prefs[other]:                                     
			# only score movies I haven't seen yet                      
			if item not in prefs[person] or prefs[person][item]==0:     
				# Similarity * Score 
				totals.setdefault(item,0) 
				totals[item]+=prefs[other][item]*sim 
				# Sum of similarities 
				simSums.setdefault(item,0) 
				simSums[item]+=sim
	# Create the normalized list
	rankings=[(total/simSums[item],item) for item,total in totals.items()]
	# Return the sorted list 
	rankings.sort( ) 
	rankings.reverse( ) 
	return rankings

# Item based CF recommendations
def getRecommendedItems(prefs,itemMatch,user):
	count = 0
	userRatings=prefs[user]
	scores={}
	totalSim={}
	# Loop over items rated by this user
	# print 'user ratings items',userRatings.items()
	for (item,rating) in userRatings.items():
		#print userRatings.items()
		# Loop over items similar to this one

		print item
		# print len(itemMatch['Mr. Saturday Night (1992)'])
		t2 = open('b.txt', 'w+')
		t2.write(str(itemMatch))
		t2.close()
		# print itemMatch
		if not itemMatch.has_key(item):
			count += 1
			print 'not found'
			continue
		print 'found'
		# print 'item match for one item: ',itemMatch[item]
		for (similarity,item2) in itemMatch[item]:
			# Ignore if this user has already rated this item
			if item2 in userRatings: 
				continue
			if similarity == 0: 
				continue
			# Weighted sum of rating times similarity
			scores.setdefault(item2,0)
			scores[item2]+=(similarity)*rating
			# Sum of all the similarities
			totalSim.setdefault(item2,0)
			totalSim[item2] = totalSim[item2]+abs(similarity)
	print 'the # of movies only watched by this user is: ',count
	# Divide each total score by total weighting to get an average 
	# print 'what is this: ',totalSim[item]
	# print 'the total sim for one item is: ', totalSim[item2]
	rankings=[(score/totalSim[item],item) for item,score in scores.items()]
	# Return the rankings from highest to lowest 
	rankings.sort( )
	rankings.reverse( )
	return rankings

# Calculate RMSE values
def getRMSE(real_list, evaluate_list):
	result = []
	# find all the squares
	for real_movie in real_list:
		for eval_movie in evaluate_list:
			if real_movie[0] == eval_movie[1]:
				print 'find same movie'
				result.append(pow(real_movie[1]-eval_movie[0], 2))
				break
	# sum up all the squares
	sum1 = sum([it for it in result])
	# Calculate the rmse
	rmse = sqrt(sum1/len(real_list))
	return rmse

total = []
for this in range(0, 2):
	r = []
	rmse = []
	for i in range(0,1):
		b  = random.randint(1,941)
		r.append(b)

	#uid = '925'
	for one in r:
		uid = str(one)
		prefs = loadMovieLens()
		out1 = str(prefs)
		copy = prefs.copy()
		del copy[uid]
		# prune the prefs dataset
		removed_list = []
		x = prefs[uid]
		userLength = len(x)
		print 'original user movie size is: ', userLength
		sorted_x = sorted(x.iteritems(), key=operator.itemgetter(1))
		sorted_x.reverse()
		pruned_list = sorted_x[:userLength/2]
		pruned_user = {}
		for item in pruned_list:
			pruned_user[item[0]] = item[1]
		removed_list = sorted_x[userLength/2:]
		print 'removed list b size is:', len(removed_list)
		prefs[uid] = pruned_user
		
		itemsim = calculateSimilarItems(copy)
		#print itemsim
		evaluate_list = getRecommendedItems(prefs,itemsim,uid)
		#evaluate_list = getRecommendations(prefs,uid,similarity=sim_pearson)
		result = getRMSE(removed_list , evaluate_list)
		####print 'removed list b is: ', removed_list
		####print 'evaluate_list is: ', evaluate_list[:100]
		print 'user movie size is: ',len(prefs[uid]) 
		#print 'itemsim size is:', len(itemsim)
		print 'evaluate list size is: ', len(evaluate_list)
		print 'rmse is: ', result  
		rmse.append((one, result))
		
	print rmse
	sum_r = sum([item[1] for item in rmse])
	average_r = sum_r/len(rmse)
	#print 'the smaples users are: ', r 
	#print 'the average rmse of 10 samples is : ', average_r
	total.append(average_r)
	
sum_final = sum([one for one in total])
print 'the average rmse is: ', sum_final/len(total)
