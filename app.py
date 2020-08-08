from flask import Flask
from flask import render_template
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
from flask import jsonify

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://boardgames:boardgames@bdat1004.ashep.gcp.mongodb.net/boardgames?retryWrites=true&w=majority")
db = client.boardGames
col = db.boardGames


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/boardgames/all", methods=['GET'])
def allBoardGames():
    client = pymongo.MongoClient("mongodb+srv://boardgames:boardgames@bdat1004.ashep.gcp.mongodb.net/boardgames?retryWrites=true&w=majority")
    db = client.boardGames
    col = db.boardGames
    games = col.find({},{'_id': 0})
    allGames = []
    for game in games:
        allGames.append(game)
    return jsonify({"allGames" : allGames})

@app.route('/boardgames/', methods=['GET'])
def getGameByName(name):
  client = pymongo.MongoClient("mongodb+srv://boardgames:boardgames@bdat1004.ashep.gcp.mongodb.net/boardgames?retryWrites=true&w=majority")
  db = client.boardGames
  col = db.boardGames
  game = col.find_one({"name" : name})
  if game:
    output = {{"game": game}}
  else:
    output = "No such name"
  return jsonify({'result' : output})


if __name__ == "__main__":
    app.run(debug=True)