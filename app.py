import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
app = Flask(__name__)
@app.route("/")
def main():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
  def precipitation():

  final_date = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
  end_date_string = final_date[0][0]
  end_date = dt.dt.strptime(end_date_string, "%Y-%m-%d")
  start_date = end_date - dt.timedelta(365)
  precipitation = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp).\
  filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date).all()
  results = {}
  for result in precipitation:
  results[result[0]] = result[1]
  return jsonify(results)

@app.route("/api/v1.0/stations")
  def stations():
  stations = session.query(Station).all()
  stations_list = []
      for station in stations:
          station_dictionary = {}
          station_dictionary["id"] = station.id
          station_dictionary["station"] = station.station
          station_dictionary["name"] = station.name
          station_dictionary["latitude"] = station.latitude
          station_dictionary["longitude"] = station.longitude
          station_dictionary["elevation"] = station.elevation
          stations_list.append(station_dictionary)

      return jsonify(stations)

@app.route("/api/v1.0/tobs")
  def tobs():
  final_date = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
  end_date_string = final_date[0][0]
  end_date = dt.dt.strptime(end_date_string, "%Y-%m-%d")
  start_date = end_date - dt.timedelta(365)
  results = session.query(Measurement).\ 
  filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date).all()

  tobs_list = []
  for result in results:
      tobs_dictionary = {}
      tobs_dictionary["date"] = result.date
      tobs_dictionary["station"] = result.station
      tobs_dictionary["tobs"] = result.tobs
      tobs_list.append(tobs_dictionary)

      return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
  def start(start):
      final_date = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
      end_date = final_date[0][0]
      temperatures = calc_temps(start, end_date)

      return_list = []
      date_dictionary = {'start_date': start, 'end_date': end_date}
      return_list.append(date_dictionary)
      return_list.append({'Observation': 'TMIN', 'Temperature': temperatures[0][0]})
      return_list.append({'Observation': 'TAVG', 'Temperature': temperatures[0][1]})
      return_list.append({'Observation': 'TMAX', 'Temperature': temperatures[0][2]})

      return jsonify(return_list)

@app.route("/api/v1.0/<start>/<end>")
  def start_end(start, end):
      temperatures = calc_temps(start, end)
      return_list = []
      date_dictionary = {'start_date': start, 'end_date': end}
      return_list.append(date_dictionary)
      return_list.append({'Observation': 'TMIN', 'Temperature': temperatures[0][0]})
      return_list.append({'Observation': 'TAVG', 'Temperature': temperatures[0][1]})
      return_list.append({'Observation': 'TMAX', 'Temperature': temperatures[0][2]})

      return jsonify(return_list)
