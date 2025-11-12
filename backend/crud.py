import subprocess
from datetime import datetime
from os_exe import get_ls_pid

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

def update_filter(data):
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
