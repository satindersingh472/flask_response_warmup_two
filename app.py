
from dbhelpers import conn_exe_close
from apihelpers import get_display_results, verify_endpoints_info
from flask import Flask, request, make_response
import json
import dbcreds

app = Flask(__name__)

@app.post('/api/pokemon')
def add_pokemon():
    invalid = verify_endpoints_info(request.json, ['name','description','image_url'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    results = get_display_results('call add_pokemon(?,?,?)',
    [request.json.get('name'),request.json.get('description'),request.json.get('image_url')])
    if(len(results) == 1):
        return make_response(json.dumps(results[0][0],default=str),200)
    elif(len(results) == 0):
        return make_response(json.dumps('No Pokemon added',default=str),500)

@app.get('/api/pokemon')
def all_pokemons():
    results = get_display_results('call all_pokemons()',[])
    results_json = make_response(json.dumps(results,default=str),200)
    return results_json


if(dbcreds.production_mode == True):
    print('Running in PRODUCTION MODE')
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print('Running in TESTING MODE')
    app.run(debug=True)


