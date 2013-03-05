import sys
import re
import subprocess

class ep_helper(object):

    def __init__(self):
        settings = sublime.load_settings("Epages.sublime-settings")
        self.working_path = settings.get("working_path")
        self.cvs = settings.get("cvs")
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

        return {'stdout' : print_stdout, 'stderr' : print_stderr}

    def match_shared(self, filename):
        if self.unix:

        else:

    def is_perl(self, filename):
        return re.match(r".*\.(pm|pl|t)$", filename.lowercase)

    def is_perl_module(self, filename):
        return re.match(r".*\.pm$",  filename.lowercase)

    def is_xml(self, filename):
        return re.match(r".*\.xml$",  filename.lowercase)

    def is_js(self, filename):
        return re.match(r".*\.js$",  filename.lowercase)

    def is_json(self, filename):
        return re.match(r".*\.json$",  filename.lowercase)
