import psutil

def get_ls_pid():
	for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
		if 'logstash' in proc.info['name'].lower() or \
			any('logstash' in arg.lower() for arg in proc.info['cmdline'] or []):
				return proc.info['pid']
