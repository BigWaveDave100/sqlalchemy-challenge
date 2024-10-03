# Import the dependencies.

import numpy as np

import datetime as dt
from datetime import timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine, reflect = True)

# Save references to each table
measure = base.classes.measurement
Station = base.classes.station

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
    """Listing all api routes"""
    return(
        f"api routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start_date_alone><br/>"
        f"/api/v1.0/<start_date>/<end_date><br/>"
    )
#################################################
# Flask Route: showing precipitation values for all of Hawaii within the final year of measurement
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    final = session.query(measure.date, measure.prcp).filter(measure.date>='2016-08-23').group_by(measure.date).order_by(measure.date).all()
    session.close()

    pcrp_list = []
    for date, pcrp in final:
        pcrp_dict = {}
        pcrp_dict['date'] = date
        pcrp_dict['pcrp'] = pcrp
        pcrp_list.append(pcrp_dict)

    return jsonify(pcrp_list)

#################################################
# Flask Route: Showing all information on every station in the database
#################################################

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    finals = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()

    station_list = []
    for id, station, name, latitude, longitude, elevation in finals:
        station_dict = {}
        station_dict['id'] = id
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitude
        station_dict['elevation'] = elevation
        station_list.append(station_dict)
    return jsonify(station_list)

#################################################
# Flask Route: Temperature OBS readings for the last year of data from the most active station in the dataset which is WAIHEE 837.5, HI US
#################################################

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    finalss = session.query(measure.date, measure.tobs).filter(measure.date>='2016-08-23').filter(measure.station == Station.station).filter(Station.name == 'WAIHEE 837.5, HI US').all()
    session.close()

    tobs_list = []
    for date, tobs in finalss:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

#################################################
# Flask Route: Date and Temperature OBS calculations for the min, max and avg from a specified date to the last date
#################################################

@app.route("/api/v1.0/<start_date_alone>")
def Start(start_date_alone):
    session = Session(engine)
    finalsss = session.query(measure.date, func.min(measure.tobs), func.max(measure.tobs), func.avg(measure.tobs)).filter(measure.date >= start_date_alone).group_by(measure.date).all()
    session.close()

    start_list = []
    for date, tobs_min, tobs_max, tobs_avg in finalsss:
        start_dict = {}
        start_dict['date'] = date
        start_dict['tobs_min'] = tobs_min
        start_dict['tobs_max'] = tobs_max
        start_dict['tobs_avg'] = tobs_avg
        start_list.append(start_dict)
    return jsonify(start_list)

#################################################
# Flask Route: Date and Temperature OBS calculations for the min, max and avg from a specified date to another specified date
#################################################

@app.route("/api/v1.0/<start_date>/<end_date>")
def StartNEnd(start_date, end_date):
    session = Session(engine)
    finalssss = session.query(measure.date, func.min(measure.tobs), func.max(measure.tobs), func.avg(measure.tobs)).filter(measure.date >= start_date).filter(measure.date <= end_date).group_by(measure.date).all()
    session.close()

    start_n_end_list = []
    for date, Tobs_min, Tobs_max, Tobs_avg in finalssss:
        start_n_end_dict = {}
        start_n_end_dict['date'] = date
        start_n_end_dict['Tobs_min'] = Tobs_min
        start_n_end_dict['Tobs_max'] = Tobs_max
        start_n_end_dict['Tobs_avg'] = Tobs_avg
        start_n_end_list.append(start_n_end_dict)
    return jsonify(start_n_end_list)

if __name__ == '__main__':
    app.run(debug=True)

