# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytz
import datetime

from flask import Flask

# [START gae_python37_datastore_store_and_fetch_times]
from google.cloud import datastore

datastore_client = datastore.Client()
tz = pytz.timezone('Europe/London')
app = Flask(__name__)

def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


@app.route('/')
def root():
    return "hi"

@app.route('/tank', methods=['GET', 'POST'])
def tank():
    # The Cloud Datastore key for the new entity
    tank_key = datastore_client.key("tank")
    # Prepares the new entity
    tank = datastore.Entity(key=tank_key)

    # Saves the entity
    tank.update({'currentTemp': 50,'currentFeature': 5})
    datastore_client.put(tank)
    
    tank_keys = datastore_client.key('tank',tank.key.id)
    
    output = ('{}'.format(tank.key.id))
    
    currentTime = int((datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds())
    
    feature_key = datastore_client.key('feature')
    # Prepares the new entity
    feature = datastore.Entity(key=feature_key)
    # Saves the entity
    feature.update({'feature': 5,'time': currentTime,'tankKey': tank_keys})
    datastore_client.put(feature)
    
    temp_key = datastore_client.key('temp')
    # Prepares the new entity
    temp = datastore.Entity(key=temp_key)
    # Saves the entity
    temp.update({'temp': 50,'time': currentTime,'tankKey': tank_keys})
    datastore_client.put(temp)
    
    return output

@app.route('/reading/<tankId>/<float:sensor3>/<float:time>', methods=['GET', 'POST'])
def reading(tankId,sensor3,time):
    # The Cloud Datastore key for the new entity
    reading_key = datastore_client.key('reading')
    tank_key = datastore_client.key('tank',tankId)
    # Prepares the new entity
    reading = datastore.Entity(key=reading_key)
    # Saves the entity
    reading.update({'sensor3': sensor3,'time': time,'tankKey': tank_key})
    datastore_client.put(reading)
    output = ('{}'.format(reading.key.id))
    
    featureQuery = datastore_client.query(kind='feature')
    featureQuery.order = ['time']
    features = list(featureQuery.fetch())
    return str(features)



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
