from threading import Timer
from py_localtunnel.tunnel import Tunnel
import os
import sys

from pymongo import MongoClient
def run_localtunnel(sever_id:int, port: int, subdomain: str):
    t = Tunnel()
    url = t.get_url(subdomain)
    sys.stdout.write(f"Your url is: {url}\n")
    sys.stdout.flush()

    ngrok_address = url

    client = MongoClient("mongodb+srv://johnnyjana730:DEcbw3EIB0CIjciD@cluster0.wxhtomw.mongodb.net/?retryWrites=true&w=majority")
    db = client['search']  # Replace 'your_database_name' with your actual database name
    ngrok_urls_collection = db['ngrok_urls']
    ngrok_url = ngrok_address

    # Data to be saved
    data = {
        "_id": "search_" + str(sever_id),  # Set your custom _id here
        "url": ngrok_url,
        # Add other fields as needed
    }
    try:
        # Insert data into MongoDB
        ngrok_urls_collection.delete_one({"_id": "search_" + str(sever_id)})
    except:
        pass
    ngrok_urls_collection.insert_one(data)
    # ngrok_urls_collection.insert_one({'url' + str(sever_id): ngrok_url})

    sys.stdout.write(f"writed url to mango: {url}\n")
    sys.stdout.flush()
    
    try:
        t.create_tunnel(port)
    except KeyboardInterrupt:
        sys.stdout.write("\nKeyboardInterrupt: Stopping tunnel...\n")
        sys.stdout.flush()

    t.stop_tunnel()
    os._exit(0)

def run_lt(sever_id:int, port: int, subdomain: str = None):
    run_localtunnel(sever_id, port, subdomain)

def start_lt(sever_id:int, port: int, subdomain: str = None):
    lt_adress = run_lt(sever_id, port, subdomain)
    print(lt_adress)


def run_with_lt(sever_id, app, subdomain: str = None):
    old_run = app.run

    def new_run(*args, **kwargs):
        port = kwargs.get('port', 5000)
        thread = Timer(1, start_lt, args=(sever_id, port, subdomain))
        thread.setDaemon(True)
        thread.start()
        old_run(*args, **kwargs)
    app.run = new_run
