import glob
import os

class ep_task(object):

    def __init__(self, helper):
        self.helper = helper
        self.path = os.path.join(helper.working_path, ".ep_subl", "tasks")
        self.configfile = os.path.join(self.path, "config.json")

    def create_config(self):
        data = { "CurrentTask": None }
        self.helper.write_json_file( self.configfile, data )
        return data

    def get_current_task(self):
        try:
            data = self.helper.read_json_file( self.configfile )
        except IOError:
            data = self.create_config()

        return data["CurrentTask"]

    def set_current_task(self, task):
        data = self.helper.read_json_file( self.configfile )
        data["CurrentTask"] = task
        self.helper.write_json_file( self.configfile, data )

    def get_task(self, filename):
        try:
            data = self.helper.read_json_file( filename )
        except IOError:
            return None
        return data

    def get_task_list(self):
        tasks = [];
        for filename in glob.glob( os.path.join(self.path,'*.task') ):
            task = self.get_task( filename )
            taskname = os.path.basename(filename).split(".")[0]
            tasks.append([taskname, task["Description"]])
        return tasks

    def create_task(self, taskname, description=""):
        task = self.get_task( os.path.join(self.path, taskname + '.task') )
        if task == None:
            data = {"Description":description,"Files":[]}
            task = self.helper.write_json_file( os.path.join(self.path, taskname+".task"), data )
        self.set_current_task( taskname )
        return task

    def add_file(self, filename):
        taskname = self.get_current_task()
        task = self.get_task( os.path.join(self.path, taskname + '.task') )
        if not filename in task["Files"]:
            task["Files"].append(filename)
        self.helper.write_json_file( os.path.join(self.path, taskname + '.task'), task )

    def remove_file(self, filename):
        taskname = self.get_current_task()
        task = self.get_task( os.path.join(self.path, taskname + '.task') )
        if filename in task["Files"]:
            task["Files"].remove(filename)
        self.helper.write_json_file( os.path.join(self.path, taskname + '.task') , task )

    def list_files(self):
        taskname = self.get_current_task()
        task = self.get_task( os.path.join(self.path, taskname + '.task') )
        return task["Files"]

    def contains_file(self, filename):
        taskname = self.get_current_task()
        if taskname == None:
            return False
        task = self.get_task( os.path.join(self.path, taskname + '.task') )
        for f in task["Files"]:
            if filename == f:
                return True
        return False
