import re
import os
import shutil

class ep_cvs(object):
    def __init__(self, helper):
        self.helper = helper

        if helper.unix:
            self.path = helper.working_path + ".ep_subl/cvs/"
        else:
            self.path = helper.working_path + "ep_subl\\cvs\\"

    def status(self, abspath, callback):
        relpath = os.path.relpath( abspath, os.getcwd() )

        pathname = os.path.dirname( relpath )
        filename = os.path.basename( relpath )

        status = {"file": abspath}

        cmd = "cd " + pathname + " && cvs status " + filename
        cvs_status = self.helper.system_exec( cmd )

        m = re.compile(r".*No CVSROOT specified.*", re.S).match(cvs_status)
        if m:
            status["error"] = cvs_status
            callback( status )
            return

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
            branch = m.group(1).strip()
            if branch == "(none)":
                branch = "HEAD"
            status["branch"] = branch

        callback( status )

    def update(self, abspath, version, callback):
        relpath = os.path.relpath( abspath, os.getcwd() )

        pathname = os.path.abspath( os.path.dirname( relpath ) )
        filename = os.path.basename( relpath )

        cmd = "cd " + pathname + " && cvs update -r " + version + " " + filename
        cvs_status = self.helper.system_exec( cmd )

        print cvs_status
        m = re.compile(r"C [\S]+", re.S).search(cvs_status)

        # File is in conflict
        if m:
            m1 = re.compile(r"^retrieving revision (.*)").search(cvs_status)
            if m1:
                oldfile = ".#" + filename + "." + m1.group(1)
                cmd = "cd " + pathname + " && rm -rf " + filename + " && cp " + oldfile +" " + filename + " && cvs update -C -r " + version + " " + filename
                print cmd
                cvs_status = self.helper.system_exec( cmd )
                print cvs_status
                status = {"status" : "conflict", "localfile" : os.path.join(self.path, filename), "remotefile" : os.path.join(self.path, oldfile) }
                callback( status )
                return

        m = re.compile(r"M [\S]+", re.S).search(cvs_status)
        if m:
            status = {"status" : "merged"}
            callback( status )
            return

        status = {"status" : "updated"}
        callback( status )

    def commit(self, abspath, message, callback):
        elpath = os.path.relpath( abspath, os.getcwd() )

        pathname = os.path.dirname( relpath )
        filename = os.path.basename( relpath )

        cmd = "cd " + pathname + " && cvs commit -m \""+ message + "\" " + filename
        cvs_status = self.helper.system_exec( cmd )

        needs_add = re.compile(r"cvs add").search(cvs_status)
        if needs_add:
            self.add(abspath)
            self.commit(abspath, message, callback)
            return
        callback({"status": "success"})

    def add(self, abspath):
        relpath = os.path.relpath( abspath, os.getcwd() )

        pathname = os.path.dirname( relpath )
        filename = os.path.basename( relpath )

        cmd = "cd " + path + " && cvs add " + filename
        cvs_status = self.helper.system_exec( cmd )
        return cvs_status


    def is_cvs_dir(self, abspath):
        pathname = os.path.dirname( abspath )
        return os.path.exists( os.path.join(pathname, "CVS" ))

    def open_diff_tool(self, file1, file2):
        cmd = "meld " + file1 + " " + file2 + " &"
        self.helper.system_call( cmd )
