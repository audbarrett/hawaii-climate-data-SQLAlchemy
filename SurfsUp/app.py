# Import the dependencies.
import numpy as np
import flask 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    all_precipitation = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["precip"] = prcp
        all_precipitation.append(precip_dict)
    
    return jsonify(all_precipitation)
    session.close()

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)
    return jsonify(all_stations)
    session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date > '2016-08-23').all()

    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)
session.close()

@app.route("/api/v1.0/<start>")
def temperatures_start(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    all_temperatures = []
    for tmin, tavg, tmax in results:
        temp_dict = {}
        temp_dict["min_temp"] = tmin
        temp_dict["avg_temp"] = tavg
        temp_dict["max_temp"] = tmax
        all_temperatures.append(temp_dict)
    return jsonify(all_temperatures)
session.close()

@app.route("/api/v1.0/<start>/<end>")
def temps_start_end(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    all_temperatures = []
    for tmin, tavg, tmax in results:
        temp_dict = {}
        temp_dict["min_temp"] = tmin
        temp_dict["avg_temp"] = tavg
        temp_dict["max_temp"] = tmax
        all_temperatures.append(temp_dict)
    return jsonify(all_temperatures)
session.close()
if __name__ == '__main__':
    app.run(debug=True)