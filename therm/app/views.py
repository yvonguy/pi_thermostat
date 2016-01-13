from flask import render_template, redirect, flash, request
from therm.app import app
from therm.database.db import DB
from therm.model.thermometer import Thermometer
from therm.model.temperature import Temperature
from forms import ThermometerRenameForm
from bokeh.plotting import figure, output_file, show


@app.route('/')
@app.route('/index')
@app.route('/therms')
def index():
    user = {'nickname': 'Yvon'}
    theDb = app.get_db() #DB('therm.db')
    therms = theDb.readThermometers()
    thermReadings = []
    for therm in therms:
        (rawTemp, ident, created_at) = theDb.getLastTemperatureReading(therm.getIdentifier())
        thermReadings.append({
                'celcius': Temperature(rawTemp).getCelciusString(),
                'ident': ident,
                'name': therm.getName(),
                'date': created_at
                })
        
    return render_template('index.html',
                           title='Home',
                           user=user,
                           readings=thermReadings)

@app.route('/therm/<identifier>')
def therm(identifier):
    theDb = app.get_db() #DB('therm.db')
    therm = theDb.getThermometer(identifier)
    rawReadings = theDb.getTemperatureReadings(identifier)
    count = len(rawReadings)
    #convert milliCs into human Cs
    readings = []
    for reading in rawReadings:
        readings.append({
            'celcius':Temperature(reading[0]).getCelciusString(),
            'datetime':reading[2]
            })
    return render_template('therm.html',
                           identifier=identifier,
                           name=therm.getName(),
                           readings=readings,
                           count=count)

@app.route('/therm/<identifier>/rename', methods=['GET', 'POST'])
def therm_rename(identifier):
    theDb = app.get_db() #DB('therm.db')
    therm = theDb.getThermometer(identifier)
    form = ThermometerRenameForm()
    if form.validate_on_submit():
        flash('Thermometer renamed to %s' % form.name.data)
        therm.setName(form.name.data)
        theDb.saveThermometers([therm])
        return redirect('/therm/' + identifier)
    return render_template('therm_rename.html',
                           title='Rename Thermostat',
                           identifier=identifier,
                           name=therm.getName(),
                           form=form)
        

@app.route('/plot-off')
def plot():
    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    # output to static HTML file
    output_file("lines.html", title="line plot example")

    # create a new plot with a title and axis labels
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness
    p.line(x, y, legend="Temp.", line_width=2)

    # show the results
    show(p)
