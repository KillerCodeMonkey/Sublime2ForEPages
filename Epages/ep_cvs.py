import re
import os

class ep_cvs(object):
    def __init__(self, helper):
        self.helper = helper

    def status(self, abspath):
        relpath = os.path.relpath( abspath, os.getcwd() )

        pathname = os.path.dirname( relpath )
        filename = os.path.basename( relpath )

        status = {}

        cmd = "cd " + pathname + " && cvs status " + filename
        cvs_status = self.helper.system_exec( cmd )

        status_lines = cvs_status.split("\n")
        m = re.compile(r".*?Status:\s+([a-zA-Z -]*)").match( status_lines[1] )
        if m:
            status["status"] = m.group(1).strip()

        m = re.compile(r".*?Working revision:\s+([\d\.]*)").match( status_lines[3] )
        if m:
            status["working_revision"] = m.group(1).strip()

        m = re.compile(r".*?Repository revision:\s+([\d\.]*)\s*([^,]*)").match( status_lines[4] )
        if m:
            status["repository_revision"] = m.group(1).strip()
            status["repository_path"] = m.group(2).strip()

        m = re.compile(r".*?Sticky Tag:\s+(\S*)").match( status_lines[7] )
        if m:
            status["branch"] = m.group(1).strip()

        return status

    def update(self, abspath, version):
        relpath = os.path.relpath( abspath, os.getcwd() )

        pathname = os.path.dirname( relpath )
        filename = os.path.basename( relpath )

        cmd = "cd " + pathname + " && cvs update -r " + version + " " + filename
        cvs_status = self.helper.system_exec( cmd )
        return cvs_status

    def commit(self, abspath, message):
        elpath = os.path.relpath( abspath, os.getcwd() )

        pathname = os.path.dirname( relpath )
        filename = os.path.basename( relpath )

        cmd = "cd " + pathname + " && cvs commit -m \""+ message + "\" " + filename
        cvs_status = self.helper.system_exec( cmd )
        return cvs_status

    def add(self, abspath):
        relpath = os.path.relpath( abspath, os.getcwd() )

        pathname = os.path.dirname( relpath )
        filename = os.path.basename( relpath )

        cmd = "cd " + path + " && cvs add " + filename
        cvs_status = self.helper.system_exec( cmd )
        return cvs_status

    def remove(self, abspath):
        relpath = os.path.relpath( abspath, os.getcwd() )

        pathname = os.path.dirname( relpath )
        filename = os.path.basename( relpath )

        cmd = "cd " + pathname + " && cvs remove " + filename
        cvs_status = self.helper.system_exec( cmd )
        return cvs_status
