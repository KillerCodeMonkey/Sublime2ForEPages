import sys
import re
import subprocess
import json
import os
import threading

class ep_helper(object):

    def __init__(self, settings):
        self.settings = settings
        self.working_path = self.settings.get("working_path")
        self.cvs = self.settings.get("cvs")
        self.unix = False if sys.platform == "win32" else True

    def vm_data(self, filename):
        m = re.compile(self.working_path + r"(.*?)/(Cartridges.*)$").match(filename)
        if m:
            return {"vm": m.group(1), "filename": m.group(2), "is_epages": True}
        return {"vm": "", "filename": "", "is_epages": False}

    def system_exec(self, command):
        result = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        print_stdout = result.stdout.read()
        print_stderr = result.stderr.read()
        try:
            print_stdout = print_stdout.decode("utf-8")
        except UnicodeDecodeError:
            print_stdout = print_stdout.decode("iso8859-1")
        try:
            print_stderr = print_stderr.decode("utf-8")
        except UnicodeDecodeError:
            print_stderr = print_stderr.decode("iso8859-1")

        return print_stdout + '\n\n' + print_stderr

    def system_call(self, command):
        subprocess.call(command, shell=True)

    def is_perl(self, filename):
        return re.match(r".*\.(pm|pl|t)$", filename.lower())

    def is_perl_module(self, filename):
        return re.match(r".*\.pm$",  filename.lower())

    def is_xml(self, filename):
        return re.match(r".*\.xml$",  filename.lower())

    def is_js(self, filename):
        return re.match(r".*\.js$",  filename.lower())

    def is_json(self, filename):
        return re.match(r".*\.json$",  filename.lower())

    def ensure_dir(self, f):
        d = os.path.dirname(f)
        if not os.path.exists(d):
            os.makedirs(d)

    def write_json_file(self, filename, jsondata):
        self.ensure_dir(filename)
        with open(filename, 'w+') as outfile:
            json.dump(jsondata, outfile, sort_keys=False, indent=4, separators=(',', ': '))
            outfile.close()
            return jsondata
        return None

    def read_json_file(self, filename):
        self.ensure_dir(filename)
        with open(filename, 'r') as infile:
            data = json.load(infile)
            infile.close()
            return data
        return None
