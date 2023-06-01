from flask import Flask, request, render_template, session
from flask_session import Session
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        session.clear()
        file = request.files['file']
        df = pd.read_csv(file)
        session['df'] = df.to_dict()
        return render_template('select_axes.html', columns=list(df.columns))
    return render_template('upload.html')

@app.route('/plot', methods=['POST'])
def plot():
    x_axis = request.form['x_axis']
    y_axis = request.form['y_axis']
    df = pd.DataFrame(session['df'])
    plot = figure(title="Line Chart")
    plot.line(df[x_axis], df[y_axis], line_width=2)
    script, div = components(plot, INLINE)  # add INLINE here
    resources = INLINE.render()
    return render_template('plot.html', script=script, div=div, resources=resources)

if __name__ == '__main__':
    app.run(debug=True)
