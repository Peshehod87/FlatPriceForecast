from flask import Flask
app = Flask(__name__)
from MapService import MapService

mapService = MapService()

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/map')
def map():
    Map = mapService.get_map()
    print(Map)
    return Map.get_root().render()

if __name__ == '__main__':
    app.run()