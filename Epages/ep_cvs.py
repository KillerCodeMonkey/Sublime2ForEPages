import re
import os
import shutil
import threading
import time
class ep_cvs(object):
    def __init__(self, helper):
        self.helper = helper

        if helper.unix:
            self.path = helper.working_path + ".ep_subl/cvs/"
        else:
            self.path = helper.working_path + "ep_subl\\cvs\\"

    def status(self, abspath, callback):
        class status_thread(threading.Thread):
            def __init__(self, abspath, callback, helper, path):
                threading.Thread.__init__(self)
                self.abspath = abspath
                self.callback = callback
                self.helper = helper
                self.path = path

            def run(self):
                relpath = os.path.relpath( self.abspath, os.getcwd() )

                pathname = os.path.dirname( relpath )
                filename = os.path.basename( relpath )

                status = {"file": self.abspath}

                cmd = "cd " + pathname + " && cvs status " + filename
                cvs_status = self.helper.system_exec( cmd )

                m = re.compile(r".*No CVSROOT specified.*", re.S).match(cvs_status)
                if m:
                    status["error"] = cvs_status
                    self.callback( status )
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

                self.callback( status )

        thread = status_thread(abspath, callback, self.helper, self.path)
        thread.start()

    def update(self, abspath, version, callback):
        class update_thread(threading.Thread):
            def __init__(self, abspath, version, helper, path, callback):
                threading.Thread.__init__(self)
                self.callback = callback
                self.abspath = abspath
                self.version = version
                self.helper = helper
                self.path = path

            def run(self):
                relpath = os.path.relpath( self.abspath, os.getcwd() )

                pathname = os.path.abspath( os.path.dirname( relpath ) )
                filename = os.path.basename( relpath )

                cmd = "cd " + pathname + " && cvs update -r " + self.version + " " + filename
                cvs_status = self.helper.system_exec( cmd )

                print cvs_status
                m = re.compile(r"C \S+", re.S).search(cvs_status)

                # File is in conflict
                if m:
                    m1 = re.compile(r"^retrieving revision (.*)").search(cvs_status)
                    if m1:
                        oldfile = ".#" + filename + "." + m1.group(1)
                        cmd = "cd " + pathname + " && rm -rf " + filename + " && cp " + oldfile +" " + filename + " && cvs update -C -r " + self.version + " " + filename
                        print cmd
                        cvs_status = self.helper.system_exec( cmd )
                        print cvs_status
                        status = {"status" : "conflict", "localfile" : os.path.join(self.path, filename), "remotefile" : os.path.join(self.path, oldfile) }
                        self.callback( status )
                        return

                m = re.compile(r"M \S+", re.S).search(cvs_status)
                if m:
                    status = {"status" : "merged"}
                    self.callback( status )
                    return

                status = {"status" : "updated"}
                self.callback( status )

        thread = update_thread(abspath, version, self.helper, self.path, callback)
        thread.start()

    def commit(self, abspath, message, callback):
        class commit_thread(threading.Thread):
            def __init__(self, abspath, message, helper, path, add, commit, callback):
                threading.Thread.__init__(self)
                self.callback = callback
                self.abspath = abspath
                self.message = message
                self.helper = helper
                self.path = path
                self.add = add
                self.commit = commit

            def run(self):
                relpath = os.path.relpath( self.abspath, os.getcwd() )

                pathname = os.path.dirname( relpath )
                filename = os.path.basename( relpath )

                cmd = "cd " + pathname + " && cvs commit -m \""+ self.message + "\" " + filename
                cvs_status = self.helper.system_exec( cmd )

                needs_add = re.compile(r"cvs add").search(cvs_status)
                if needs_add:
                    self.add(self.abspath)
                    self.commit(self.abspath, self.message, self.callback)
                    return
                self.callback({"status": "success"})

        thread = commit_thread(abspath, message, self.helper, self.path, self.add, self.commit, callback)
        thread.start()

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
