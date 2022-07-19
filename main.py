from pickle import NONE
from flask import Flask, render_template, make_response, jsonify, request
import requests
import json

app = Flask(__name__)

@app.route("/")
def instruccion():
    return render_template('index.html')

@app.route("/searchComics")
def buscador():
    if request.args:
        req = request.args
        type = req.get('type')
        if req.get('name') == "":
            name = ""
            data = requests.get(noNameURL(type))
        else:
            name = req.get('name')
            data = requests.get(nameURL(type,name))
    if data.status_code == 200:
        data_json = json.loads(data.text)
        return insertJson(type,data_json)
    res = make_response(jsonify({"error": "No Query String"}), 404)
    return res

def nameURL(type,name):
    ts=1
    public_key= "0a2df6dcc3bc1b03fe1c3166a69c8399"
    my_hash = 'd1bda4b72582e6f299e744c5489962c5'
    limit=100
    if type == "personaje":
        url = f"https://gateway.marvel.com:443/v1/public/characters?nameStartsWith={name}&limit={limit}&ts={ts}&apikey={public_key}&hash={my_hash}"
    elif type == "comic":
        url = f"https://gateway.marvel.com:443/v1/public/comics?format=comic&formatType=comic&titleStartsWith={name}&limit={limit}&ts={ts}&apikey={public_key}&hash={my_hash}"
    return url

def noNameURL(type):
    ts=1
    public_key= "0a2df6dcc3bc1b03fe1c3166a69c8399"
    my_hash = 'd1bda4b72582e6f299e744c5489962c5'
    limit=100
    if type == "personaje":
        url = f"https://gateway.marvel.com:443/v1/public/characters?limit={limit}&ts={ts}&apikey={public_key}&hash={my_hash}"
    elif type == "comic":
        url = f"https://gateway.marvel.com:443/v1/public/comics?format=comic&formatType=comic&limit={limit}&ts={ts}&apikey={public_key}&hash={my_hash}"
    return url

def insertJson(type,data_json):
    collection={}
    collection.clear()
    collection["collection"]=[]
    if type == "personaje":
        for i in data_json["data"]["results"]:
            id=i["id"]
            name=i["name"]
            image=i["thumbnail"]["path"]
            extension=i["thumbnail"]["extension"]
            appearances=i["comics"]["available"]
            imageExtension=image+"."+extension
            dic={"id":id,
                "name":name,
                "image":imageExtension,
                "appearances":appearances}
            collection["collection"].append(dic)        
    elif type == "comic":
        for i in data_json["data"]["results"]:
            id=i["id"]
            title=i["title"]
            image=i["thumbnail"]["path"]
            extension=i["thumbnail"]["extension"]
            dates=i["dates"][0]["date"]
            imageExtension=image+"."+extension
#            fecha = dateutil.parser.parse(dates)
#            fecha = fecha.strftime('%Y-%m-%d')
            dic={"id":id,
                "title":title,
                "image":imageExtension,
                "appearances":dates}
            collection["collection"].append(dic)
    return collection

app.run(host="0.0.0.0")