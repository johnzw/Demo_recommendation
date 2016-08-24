import numpy
import json
import pickle

with open('data/top_items.json','r') as f:
	all_items = json.load(f)
with open('data/user_cart.json','r') as f:
	all_user_cart = json.load(f)

raw_to_index_map = {}
index_to_raw_map = {}

for index, item in enumerate(all_items):
	raw_to_index_map[item] = index
	index_to_raw_map[index] = item

with open('data/backup_indicator_matrix.pkl') as f:
	indicator_matrix = pickle.load(f)

def construct_indicator():
	#initialize the matrix
	indicator_matrix = numpy.zeros((len(all_items),len(all_items)))
	#fill in the matrix
	for i in range(len(all_items)):
		print "processing i",i
		for j in range(len(all_items)):
			#it has been processed
			if indicator_matrix[j][i] != 0:
				indicator_matrix[i][j] = indicator_matrix[j][i]
				continue
			if i!=j:
				#get the raw index of i and j
				raw_i = index_to_raw_map[i]
				raw_j = index_to_raw_map[j]
				#initialize the hit
				hit_i = 0
				hit_j = 0
				hit_together = 0
				hit_i_flag = False
				hit_j_flag = False
				#loop the user cart
				for user_cart in all_user_cart:
					if raw_i in user_cart:
						hit_i += 1
						hit_i_flag = True
					if raw_j in user_cart:
						hit_j += 1
						hit_j_flag = True
					if hit_i_flag and hit_j_flag:
						hit_together += 1
					hit_i_flag,hit_j_flag = False, False

				#caculate the score
				indicator_matrix[i][j] = hit_together*1.0/(hit_i+hit_j-hit_together)

	#write the file
	with open('data/indicator_matrix.pkl','w') as f:
		pickle.dump(indicator_matrix, f)

	return indicator_matrix

def recommend(items,num):
	#map the index
	mapped_items = [raw_to_index_map[int(item)] for item in items]
	#initialzie the purchase vector
	purchase_vector = numpy.zeros(len(all_items))
	for item in mapped_items:
		purchase_vector[item] = 1

	#get the score result
	result_vector = numpy.dot(indicator_matrix,purchase_vector)

	#get the max 10 items
	recommended_items = [index_to_raw_map[item] for item in numpy.argsort(result_vector)[::-1][:num]]
	return recommended_items

