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

# Production-ready configuration
app.config['DEBUG'] = False  # Disable debug mode

@app.route('/api/filters', methods=['GET'])
def get_filters():
    sectors = mongo.db.TopicData.distinct("sector")
    regions = mongo.db.TopicData.distinct("region")
    end_years = mongo.db.TopicData.distinct("end_year")
    topics = mongo.db.TopicData.distinct("topic")
    pests = mongo.db.TopicData.distinct("pestle")
    sources = mongo.db.TopicData.distinct("source")
    countries = mongo.db.TopicData.distinct("country")
    
    # Filter out empty strings
    sectors = [sector for sector in sectors if sector]
    regions = [region for region in regions if region]
    end_years = [year for year in end_years if year]
    topics = [topic for topic in topics if topic]
    pests = [pest for pest in pests if pest]
    sources = [source for source in sources if source]
    countries = [country for country in countries if country]
    
    return jsonify({
        "sectors": sectors,
        "regions": regions,
        "end_years": end_years,
        "topics": topics,
        "pests": pests,
        "sources": sources,
        "countries": countries,
    })

@app.route('/api/data', methods=['GET'])
def get_data():
    sector = request.args.get('sector')
    region = request.args.get('region')
    end_year = request.args.get('end_year')
    topic = request.args.get('topic')
    pestle = request.args.get('pestle')
    source = request.args.get('source')
    country = request.args.get('country')
    
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
    if country:
        query['country'] = country
    
    data = list(mongo.db.TopicData.find(query))
    
    # Convert ObjectId to string and return necessary fields
    for item in data:
        item['_id'] = str(item['_id'])
    
    return jsonify(data)

# Use Gunicorn to serve the application
# Example command: gunicorn -w 4 -b 0.0.0.0:5000 app:app
if __name__ == '__main__':
    bind_address = '0.0.0.0:5000'
    workers = 4
    print(f"Running on {bind_address} with {workers} workers...")
    from gunicorn.app.base import BaseApplication

    class StandaloneApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            for key, value in self.options.items():
                self.cfg.set(key, value)

        def load(self):
            return self.application

    options = {
        'bind': bind_address,
        'workers': workers,
    }

    StandaloneApplication(app, options).run()
