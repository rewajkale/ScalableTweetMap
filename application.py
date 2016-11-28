from flask import Flask, render_template,json, request
import requests
from flask.ext.googlemaps import GoogleMaps

ES_addr = 'http://ec2-35-160-188-74.us-west-2.compute.amazonaws.com:9200'

application = Flask(__name__)
GoogleMaps(application)

res_count = requests.get(ES_addr + '/twitter/tweets/_count')

count_json = json.loads(res_count.text)

@application.route('/',methods=['POST'])
def run2():
    

    dp_res = request.form['dropdown']
    selected = dp_res

    query = json.dumps({
        "size":5000,
        "query": {
            "match": {
                "text": dp_res
            }
        }
    })
    res_query = requests.get(ES_addr + '/twitter/tweets/_search?', data=query)


    query_json = json.loads(res_query.text)


    coord_list = []
    for i in range(len(query_json['hits']['hits'])):
        coord_list.append([query_json['hits']['hits'][i]['_source']['text']] + query_json['hits']['hits'][i]['_source']['coordinates'])



    return render_template('tweet-map-home.html', count = count_json['count'], coord_list = coord_list, selected = selected)

@application.route('/', methods=['GET','POST'])
def home():


    return render_template('tweetmap.html', count = count_json['count'], coord_list = [])


if __name__ == '__main__':
    application.debug = True
    application.run()
