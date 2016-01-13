'''This example demonstrates embedding a standalone Bokeh document
into a simple Flask application, with a basic HTML web form.

To view the example, run:

    python simple.py

in this directory, and navigate to:

    http://localhost:5000

'''
from __future__ import print_function

import flask
import datetime
from datetime import datetime, date, time
from therm.app import app

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.resources import CDN
from bokeh.templates import CSS_RESOURCES, JS_RESOURCES
from bokeh.util.string import encode_utf8
from bokeh.models import Range1d

import math

colors = {
    'Black': '#000000',
    'Red':   '#FF0000',
    'Green': '#00FF00',
    'Blue':  '#0000FF',
}

def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

def temp_model(t, t_sunrise, t_sunset, T_max, T_min):
    """
        At sunrise, the temperature starts to increase again T = T_min
        At sunset, the temperature started the decrease already: T = (T_max+T_min)/2
        

    """
    #t_sunrise = 5.0
    #t_sunset = 22.0
    len_day = (t_sunset - t_sunrise)
    len_night = 24-len_day
    #T_max = 35.0
    #T_min = 20.0
    T0 = (T_max + T_min) / 2.0 #27.0 # mean temperature
    TA = (T_max - T_min) / 2.0 #5.0 # temperature variance
    #tm = 14.0 # time when Max temp is reached
    t = t % 24.0
    if t < t_sunrise:
        y = T0 - TA * (24-(t_sunset-t))/len_night
    elif t > t_sunset:
        y = T0 - TA * (t-t_sunset)/len_night
    else:
        y = T0 + TA*math.cos(math.pi * (1.5*(t-t_sunrise)/len_day-1))
    return y

# all time arguments should be in datetime.time
def temp_model3(t, t_sunrise, t_sunset, T_max, T_min):
    """
        At sunrise, the temperature starts to increase again T = T_min
        At sunset, the temperature started the decrease already: T = (T_max+T_min)/2
        

    """
    len_day = (t_sunset - t_sunrise).total_seconds()
    len_night = datetime.deltatime(24).total_seconds-len_day
    # time of maximum temperature, for now noon + 3h
    t_max = (t_sunset + t_sunrise)/2 + datetime.deltatime(3).total_seconds()
    TA = (T_max-T_min)/(1-math.cos(math.pi*(t_sunrise-t_max)/len_day))
    T0 = T_max - TA
    T_sunrise = T_min
    T_sunset = T0 + TA*math.cos(math.pi*(t_sunset-t_max)/len_day)
    T_delta = T_sunset - T_sunrise
    #tm = 14.0 # time when Max temp is reached
    t = t % 24.0
    if t < t_sunrise:
        y = T_sunrise + T_delta * (t_sunrise-t)/len_night
    elif t > t_sunset:
        y = T_sunset - T_delta * (t-t_sunset)/len_night
    else:
        y = T0 + TA*math.cos(math.pi*(t-t_max)/len_day)
    return y

def hoursToSeconds(hours):
    return hours * 60 * 60

def timeToSeconds(t):
    return (t.hour*60 + t.minute)*60 + t.second

def timeToMinutes(t):
    # round to nearest minute
    return int(timeToSeconds(t)/60)

@app.route("/plot")
def polynomial():
    """ Very simple embedding of a polynomial chart

    """

    # Grab the inputs arguments from the URL
    # This is automated by the button
    args = flask.request.args

    # Get all the form arguments in the url with defaults
    color = colors[getitem(args, 'color', 'Black')]

    today = date.today()
    t_start = time(int(getitem(args, 'start', 0)))
    t_end = time(int(getitem(args, 'end', 24)))
    T_min = int(getitem(args, 'T_min', 25))
    T_max = int(getitem(args, 'T_max', 32))
    t_sunrise = time(int(getitem(args, 'sunrise', 5)))
    t_sunset = time(int(getitem(args, 'sunset', 22)))

    # Create a polynomial line graph
    minutes = list(range(timeToMinutes(t_start), timeToMinutes(t_end) + 1))
    x = [time(hour=i/60, minute=i%60) for i in minutes]
    fig = figure(title="Temperature Model",
                 x_axis_type = "datetime")
    fig.line(x,
             [temp_model3(i, t_sunrise, t_sunset, T_max, T_min) for i in minutes],
             color=color,
             line_width=2)
    fig.yaxis.axis_label = 'Temperature'
    fig.y_range = Range1d(start=0, end=35)
    fig.xaxis.axis_label = 'Time'

    # Configure resources to include BokehJS inline in the document.
    # For more details see:
    #   http://bokeh.pydata.org/en/latest/docs/reference/resources_embedding.html#bokeh-embed
    resource = CDN
    js_resources = JS_RESOURCES.render(js_raw=resource.js_raw,
                                       js_files=resource.js_files)
    css_resources = CSS_RESOURCES.render(css_raw=resource.css_raw,
                                         css_files=resource.css_files)
    
    # For more details see:
    #   http://bokeh.pydata.org/en/latest/docs/user_guide/embedding.html#components
    script, div = components(fig, resource)
    html = flask.render_template(
        'embed2.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        color=color,
        start=t_start,
        end=t_end,
        T_min=T_min,
        T_max=T_max,
        sunrise=sunrise,
        sunset=sunset
    )
    return encode_utf8(html)


@app.route("/plot2")
def polynomial2():
    """ Very simple embedding of a polynomial chart

    """

    # Grab the inputs arguments from the URL
    # This is automated by the button
    args = flask.request.args

    # Get all the form arguments in the url with defaults
    color = colors[getitem(args, 'color', 'Black')]

    start = datetime.time(int(getitem(args, 'start', 0)))
    end = datetime.time(int(getitem(args, 'end', 24)))
    T_min = int(getitem(args, 'T_min', 25))
    T_max = int(getitem(args, 'T_max', 32))
    sunrise = datetime.time(int(getitem(args, 'sunrise', 5)))
    sunset = dateimte.time(int(getitem(args, 'sunset', 22)))

    # Create a polynomial line graph
    x = list(range(start, end + 1))
    fig = figure(title="Temperature Model")
    fig.line(x, [temp_model3(i, sunrise, sunset, T_max, T_min) for i in x], color=color, line_width=2)
    fig.yaxis.axis_label = 'Temperature'
    fig.y_range = Range1d(start=0, end=35)
    fig.xaxis.axis_label = 'Time'

    # Configure resources to include BokehJS inline in the document.
    # For more details see:
    #   http://bokeh.pydata.org/en/latest/docs/reference/resources_embedding.html#bokeh-embed
    resource = CDN
    js_resources = JS_RESOURCES.render(js_raw=resource.js_raw,
                                       js_files=resource.js_files)
    css_resources = CSS_RESOURCES.render(css_raw=resource.css_raw,
                                         css_files=resource.css_files)
    
    # For more details see:
    #   http://bokeh.pydata.org/en/latest/docs/user_guide/embedding.html#components
    script, div = components(fig, resource)
    html = flask.render_template(
        'embed2.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        color=color,
        start=start,
        end=end,
        T_min=T_min,
        T_max=T_max,
        sunrise=sunrise,
        sunset=sunset
    )
    return encode_utf8(html)

