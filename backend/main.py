from flask import Flask, render_template, request
from datetime import datetime
import time
import psutil
import subprocess

app = Flask(__name__,
        template_folder='/app/LogsParser/frontend-Shaitan',
        static_folder='/app/LogsParser/frontend-Shaitan/css')

@app.route('/')
def entry_page() -> 'html':
    return render_template('index.html')

def get_ls_pid():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'logstash' in proc.info['name'].lower() or \
            any('logstash' in arg.lower() for arg in proc.info['cmdline'] or []):
                return proc.info['pid']

def create_input(data):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    INPUT_FILE = f'/app/data/logstash/input_data/data.{timestamp}'
    with open(INPUT_FILE, "w") as f:
        f.write(data)

def read_output():
    OUTPUT_FILE = '/app/data/logstash/output_data/data'
    with open(OUTPUT_FILE, "r") as f:
        data = f.read()
    return data

def create_filter(data):
    PID = str(get_ls_pid())
    LS_CONF = '/app/logstash/config/conf.d/logsparser.conf'
    CONFIG = f'''
input {{
  file {{
    path => "/app/data/logstash/input_data/data.*"
    mode => "read"
    codec => plain {{
      charset => "UTF-8"
    }}
    start_position => "beginning"
    sincedb_path => "/dev/null"
  }}
}}

filter {{
  {data}
}}

output {{
  file {{
    path => "/app/data/logstash/output_data/data"
    flush_interval => 0
    write_behavior => "overwrite"
  }}
}}
'''
    with open(LS_CONF, 'w') as f:
        f.write(CONFIG)
    subprocess.call(["kill","-1",PID])

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


if __name__ == "__main__":
    app.run()
