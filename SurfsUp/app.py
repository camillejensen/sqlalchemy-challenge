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
    for date, prcp in results:
        prcp_dict= {}
        prcp_dict[date]= prcp
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data)

if __name__ == "__main__":
    app.run(debug=True, port= 8000)