import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

from flask import Flask

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23' ).\
            order_by(Measurement.date).all()

    df = pd.DataFrame(results, columns=['date', 'prcp'])
    d = dict(zip(df.date, df.prcp))
    return jsonify(d)

@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Station.station).all()
    station_names = list(np.ravel(station_list))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_result = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23' ).\
            order_by(Measurement.date).all()

    df2 = pd.DataFrame(tobs_result, columns=['date', 'tobs'])
    d2 = dict(zip(df2.date, df2.tobs))
    return jsonify(d2)

@app.route("/api/v1.0/start")
def start():
    results2 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= '2016-08-23').all()

    results3 = list(np.ravel(results2))
    return jsonify(results3)

@app.route("/api/v1.0/startend")
def startend():
    results4 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23').all()
    
    results5 = list(np.ravel(results4))
    return jsonify(results5)

if __name__ == '__main__':
    app.run(debug=True)