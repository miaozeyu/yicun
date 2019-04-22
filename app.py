from flask import Flask

from routes import init_api_routes
from Data_Ingestor.twitter_streaming_producer import startStreaming

app = Flask(__name__)

init_api_routes(app)
startStreaming()

if __name__ == '__main__':
    app.run(debug=True)