#

from flask import Flask,render_template,request,url_for,redirect,make_response
from collections import defaultdict
import urllib
import os
import json
import pickle
import recommendation_engine

app = Flask(__name__, static_url_path='/static')

cache = defaultdict(list)
#specify your base directory
BASE_DIR = '/Users/john/Desktop/Demo'

with open('data/sample_items','r') as f:
	top_items = json.load(f)

with open('data/attribute_list.json','r') as f:
	attribute_list = json.load(f)

with open('data/item_info.pkl','r') as f:
	item_info = pickle.load(f)

with open('data/tag_name.pkl','r') as f:
	tag_name_dic = pickle.load(f)

with open('data/tag_pic_dic.pkl','r') as f:
	tag_pic_dic = pickle.load(f)

@app.route("/")
def home():
	response = make_response(render_template('frame.html'))
	response.set_cookie('user_id', "testhaha")

	#clear the cache, just for the sake of test
	cache['testhaha'] = list()
	return response

@app.route("/top/")
def top():
	return render_template('top.html',top_items=top_items[:20])


@app.route("/top/<count>/")
def top_load(count):
	c = int(count)
	x = "|".join([str(item) for item in top_items[20*c:(20*c+20)]])
	return x, 200, {'Content-Type': 'text/css; charset=utf-8'}

@app.route("/category/")
def category():
	print tag_pic_dic.keys()
	return render_template('category.html',attributes=attribute_list,dic=tag_name_dic,pic_dic=tag_pic_dic)

@app.route("/category/<attribute>/")
def one_category(attribute):
	attribute = int(attribute)
	items = item_info[item_info['attribute_id']==attribute]['item_id'].tolist()
	return render_template('one_category.html',attribute=attribute,items=items[:20],dic=tag_name_dic)

@app.route("/category/<attribute>/<count>/")
def one_category_load(attribute,count):
	attribute = int(attribute)
	c = int(count)
	items = item_info[item_info['attribute_id']==attribute]['item_id'].tolist()
	x = "|".join([str(item) for item in items[20*c:(20*c+20)]])
	return x, 200, {'Content-Type': 'text/css; charset=utf-8'}


@app.route("/purchase/<img_name>/")
def purchase(img_name):
	# return render_template('purchase.html')
	user_id = request.cookies.get('user_id')
	img_name = int(img_name)
	if user_id:
		if img_name in cache[user_id]:
			cache[user_id].remove(img_name)
			cache[user_id].append(img_name)
		else:
			cache[user_id].append(img_name)
	return render_template('purchase.html',purchased_items=cache[user_id][::-1])

@app.route("/recommendation/<img_name>/")
def recommendation(img_name):
	user_id = request.cookies.get('user_id')
	img_name = int(img_name)
	if user_id:
		if img_name in cache[user_id]:
			cache[user_id].remove(img_name)
			cache[user_id].append(img_name)
		else:
			cache[user_id].append(img_name)
	recommended_items = recommendation_engine.recommend(cache[user_id],30)
	return render_template('recommendation.html',recommendation_items=recommended_items)

@app.route("/purchaseremove/<img_name>/")
def purchase_remove(img_name):
	# return render_template('purchase.html')
	user_id = request.cookies.get('user_id')
	img_name = int(img_name)
	if user_id:
		if img_name in cache[user_id]:
			cache[user_id].remove(img_name)
	return render_template('purchase.html',purchased_items=cache[user_id][::-1])

@app.route("/recommendationremove/<img_name>/")
def recommendation_remove(img_name):
	user_id = request.cookies.get('user_id')
	img_name = int(img_name)
	if user_id:
		if img_name in cache[user_id]:
			cache[user_id].remove(img_name)
	recommended_items = recommendation_engine.recommend(cache[user_id],30)
	return render_template('recommendation.html',recommendation_items=recommended_items)

# @app.route("/scan/<file_path>/")
# def scan_html(file_path):

# 	frame = '''
# 	<html>
# 	<FRAMESET cols="80%%,20%%">
# 		<FRAME src="/rawhtml/%s">
# 		<FRAME src="/lable/%s">
# 	</FRAMESET>
# 	</html>
# 	'''

# 	frame = frame % (file_path,file_path)
# 	return frame

# @app.route("/rawhtml/<filename>/")
# def raw_html(filename):
# 	true_file = urllib.unquote(filename)
# 	return app.send_static_file(true_file)

# @app.route("/lable/<filename>/", methods=['GET', 'POST'])
# def lable_html(filename):
# 	#notice: unicode
# 	prof_html = urllib.unquote(filename)

# 	all_files =os.listdir(os.path.join(BASE_DIR,'static'))
# 	index = all_files.index(prof_html.encode('utf-8'))

# 	next_filehtml = None
# 	items = None

# 	#next file 
# 	if index+1 < len(all_files):
# 		next_filehtml = all_files[index+1]
# 	if request.method == 'POST':
# 		items = request.form.getlist('hello')
# 		if items:
# 			glo_dic[prof_html.encode('utf-8')] = items
# 			write_dic()
# 	prof = prof_html[:-5]
# 	if prof_html.encode('utf-8') in glo_dic:
# 		items = glo_dic[prof_html.encode('utf-8')]
# 	return render_template('lable.html',prof=prof, next=next_filehtml,items=items)
	
if __name__ == "__main__":
	# app.run(debug = True)
	app.run(host= '0.0.0.0', port=9000)