from flask import render_template, request
from crud import update_filter, create_input, read_output
from main import app

@app.route('/')
def entry_page() -> 'html':
    return render_template('index.html')

@app.route('/', methods=["POST"])
def result_page() -> 'html':
    input_data = request.form['samples']
    filter_pattern = request.form['filter']
    create_filter(data=filter_pattern)
    create_input(data=input_data)
    result_data = read_output()
    return render_template('index.html',
            samples=input_data,
            filter=filter_pattern,
            result=result_data,)
