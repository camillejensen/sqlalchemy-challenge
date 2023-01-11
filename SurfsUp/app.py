import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)
@app.route("/")
def index():
    """Welcome to the Hawaii Climate Homepage. Find the available routes below."""
    return(
        f"Welcome to the Hawaii Climate Homepage. Find the available routes below.<br/>"
        f"<br/>"
        f"Precipitation Data for 2017<br/>"  
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"List of Active Weather Stations<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Data for the Most Active Station for One Year<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"The Average, Minimum, and Maximum Temperature for a specified Start Date<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"The Average, Minimum, and Maximum Temperature for a specified Start and End Date<br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session= Session(engine)
    one_year= dt.date(2017,8,23) - dt.timedelta(days=365)
    data=session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year).all()
    session.close()

    prcp_data=[]
    for date, prcp in data:
        prcp_dict= {}
        prcp_dict[date]= prcp
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data)
@app.route("/api/v1.0/stations")
def stations():
    session= Session(engine)
    sations= session.query(Station.name, Station.station, Station.elevation, Station.latitude, Station.longitude).all()
    session.close()
    station_data=[]
    for name, station, elevation, latitude, longitude in stations:
        station_dict={}
        station_dict["Name"]=name
        station_dict["Station ID"]=station
        station_dict["Elevation"]=elevation
        station_dict["latitude"]=latitude
        station_dict["Longitude"]=longitude
        station_data.append(station_dict)
    return jsonify(station_data)
@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    one_year= dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs= session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year).all()
    session.close()

    active_station=[]
    for date, temp in active_station:
        active_dict={}
        active_dict[date]= temp
        active_station.append(active_dict)
    return jsonify(active_station)
@app.route("/api/v1.0/<start>")
def start(start):
    session=Session(engine)
    results= session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    start_date=[]
    for min, max, avg in results:
        start_dict={}
        start_dict["Minimum Temperature"]= min
        start_dict["Maximum Temperature"]= max
        start_dict["Average Temperature"]= avg
        start_date.append(start_dict)
    return jsonify(start_date)
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session= Session(engine)
    results= session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <=end).all()
    session.close()
    start_end_date=[]
    for min, max, avg in results:
        start_end_dict={}
        start_end_dict["Minimum Temperature"]= min
        start_end_dict["Maximum Temperature"]= max
        start_end_dict["Average Temperature"]= avg
        start_end_date.append(start_end_dict)
    return jsonify(start_end_date)


if __name__ == "__main__":
    app.run(debug=True)