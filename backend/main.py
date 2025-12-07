from flask import Flask, render_template, request
from crud import update_filter, create_input, read_output
import time

app = Flask(__name__,
        template_folder='/app/LogsParser/frontend-Shaitan',
        static_folder='/app/LogsParser/frontend-Shaitan/css')

@app.route('/')
def entry_page() -> 'html':
    return render_template('index.html')

@app.route('/', methods=["POST"])
def result_page() -> 'html':
    input_data = request.form['samples']
    filter_pattern = request.form['filter']
    update_filter(data=filter_pattern)
    create_input(data=input_data)
    result_data = read_output()
    return render_template('index.html',
            samples=input_data,
            filter=filter_pattern,
            result=result_data,)

if __name__ == "__main__":
    app.run(host="192.168.1.8")
