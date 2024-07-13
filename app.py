from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)
CORS(app)

@app.route('/api/filters', methods=['GET'])
def get_filters():
    sectors = mongo.db.TopicData.distinct("sector")
    regions = mongo.db.TopicData.distinct("region")
    end_years = mongo.db.TopicData.distinct("end_year")
    topics = mongo.db.TopicData.distinct("topic")
    pests = mongo.db.TopicData.distinct("pestle")
    sources = mongo.db.TopicData.distinct("source")
    # swots = mongo.db.TopicData.distinct("swot")
    countries = mongo.db.TopicData.distinct("country")
    # cities = mongo.db.TopicData.distinct("city")
    
    # Filter out empty strings
    sectors = [sector for sector in sectors if sector]
    regions = [region for region in regions if region]
    end_years = [year for year in end_years if year]
    topics = [topic for topic in topics if topic]
    pests = [pest for pest in pests if pest]
    sources = [source for source in sources if source]
    # swots = [swot for swot in swots if swot]
    countries = [country for country in countries if country]
    # cities = [city for city in cities if city]
    
    return jsonify({
        "sectors": sectors,
        "regions": regions,
        "end_years": end_years,
        "topics": topics,
        "pests": pests,
        "sources": sources,
        # "swots": swots,
        "countries": countries,
        # "cities": cities
    })

@app.route('/api/data', methods=['GET'])
def get_data():
    sector = request.args.get('sector')
    region = request.args.get('region')
    end_year = request.args.get('end_year')
    topic = request.args.get('topic')
    pestle = request.args.get('pestle')
    source = request.args.get('source')
    swot = request.args.get('swot')
    country = request.args.get('country')
    city = request.args.get('city')
    
    query = {}
    
    if sector and sector != 'All':
        query['sector'] = sector
    if region and region != 'All':
        query['region'] = region
    if end_year:
        query['end_year'] = end_year
    if topic:
        query['topic'] = topic
    if pestle:
        query['pestle'] = pestle
    if source:
        query['source'] = source
    # if swot:
    #     query['swot'] = swot
    if country:
        query['country'] = country
    # if city:
    #     query['city'] = city
    
    data = list(mongo.db.TopicData.find(query))
    
    # Convert ObjectId to string and return necessary fields
    for item in data:
        item['_id'] = str(item['_id'])
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
