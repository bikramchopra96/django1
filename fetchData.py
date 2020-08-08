import requests
import pymongo
from pymongo import MongoClient
import sys, json
import schedule
from datetime import datetime
import time

def fetchData():
    
    skip_num = 0
    
    while True:
        url = ("https://api.boardgameatlas.com/api/search?skip=" + str(skip_num))
        
        parameters = {"order_by": "popularity", "limit": 100, "skip": skip_num, "gt_price": 0.1, "client_id": "ieVACdbciW"}
        
        response = requests.get(url, params=parameters)
        
        # Get the response data as a python object. Verify that it's a dictionary.
        data = response.json()
    
        games = data["games"]
   
        client = pymongo.MongoClient("mongodb+srv://boardgames:boardgames@bdat1004.ashep.gcp.mongodb.net/boardgames?retryWrites=true&w=majority")
        db = client.boardGames
        BoardGames = db.boardGames
        
        BoardGames.insert_many(games)
    
        skip_num = skip_num + 100
        
        if skip_num > 10000:
            break

def updateData():
    
    client = pymongo.MongoClient("mongodb+srv://boardgames:boardgames@bdat1004.ashep.gcp.mongodb.net/boardgames?retryWrites=true&w=majority")
    db = client.boardGames
    BoardGames = db.boardGames
    
    BoardGames.remove( { } )
    
    fetchData()
    
    
def main():
    
    updateData()

if __name__ == "__main__":
       
    print("Start Time : "+str(datetime.now()))    
    schedule.every(1440).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)