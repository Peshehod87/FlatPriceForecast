from flask import  redirect, render_template, request, url_for, Flask, json
import re

app = Flask(__name__)
from MapService import MapService
from global_constants import ShowOnMap
mapService = MapService()
selectedTypes = [] 
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/moscowMapFrame/', defaults={'currentTypes': None})
@app.route('/moscowMapFrame/<currentTypes>')
def map(currentTypes):
    print("selectedTypes:")
    print(currentTypes)
    convertedTypes = getConvertedTypes(currentTypes)
    Map = mapService.get_map(convertedTypes)
    return Map.get_root().render()

@app.route('/moscowMapIndex', defaults={'currentTypes': None})
@app.route('/moscowMapIndex/', defaults={'currentTypes': None})
@app.route('/moscowMapIndex/<currentTypes>',)
def index(currentTypes):
    print(getChecks(currentTypes))
    return render_template('index.html', checks = getChecks(currentTypes), currentTypes = currentTypes)

@app.route('/get_selected_types', methods=['POST'])
def getSelectedTypes():
    if request.method == 'POST':
        currentTypes = request.form.getlist('selectedTypes')

    return redirect(url_for('index', currentTypes = { "types" :  currentTypes }))

def getConvertedTypes(currentTypes):
    if currentTypes is None:
        return None
    currentTypesDict = json.loads(re.sub('\'','"',currentTypes))

    return [int(s) for s in currentTypesDict["types"]]

def getChecks(currentTypes):

    convertedTypes = getConvertedTypes(currentTypes)
    checks = [
        { "type": ShowOnMap.HOUSE.value, "display": "Дома", "isChecked": (currentTypes is not None and ShowOnMap.HOUSE.value in convertedTypes) },
        { "type": ShowOnMap.MALL.value, "display": "Магазины", "isChecked": currentTypes is not None and ShowOnMap.MALL.value in convertedTypes },
        { "type": ShowOnMap.SCHOOL.value, "display": "Школы", "isChecked": currentTypes is not None and ShowOnMap.SCHOOL.value in convertedTypes },
        { "type": ShowOnMap.CHILD_CLINIC.value, "display": "Детские поликлиники", "isChecked": currentTypes is not None and ShowOnMap.CHILD_CLINIC.value in convertedTypes },
        { "type": ShowOnMap.ADULT_CLINIC.value, "display": "Поликлиники", "isChecked": currentTypes is not None and ShowOnMap.ADULT_CLINIC.value in convertedTypes },
       # { "type": ShowOnMap.SUBWAY.value, "display": "Метро", "isChecked": currentTypes is not None and ShowOnMap.SUBWAY.value in convertedTypes }
    ]
    return checks

if __name__ == '__main__':
    app.run()