import glob

class ep_task(object):

    def __init__(self, helper):
        self.helper = helper
        if helper.unix:
            self.path = helper.working_path + ".tasks/"
        else:
            self.path = helper.working_path + "tasks\\"
        self.configfile = self.path + "config.json"

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
        for filename in glob.glob(self.path+ '*.task'):
            task = self.get_task( filename )
            tasks.append([task["Name"], task["Description"]])
        return tasks

    def create_task(self, taskname, description=""):
        task = self.get_task(self.path + taskname + '.task')
        if task == None:
            data = {"Name":taskname,"Description":description,"Files":[]}
            task = self.helper.write_json_file( self.path+taskname+".task", data )
        self.set_current_task( task["Name"] )
        return task

    def add_file(self, filename):
        taskname = self.get_current_task()
        task = self.get_task(self.path + taskname + '.task')
        if not filename in task["Files"]:
            task["Files"].append(filename)
        self.helper.write_json_file( self.path + taskname + '.task', task )

    def remove_file(self, filename):
        taskname = self.get_current_task()
        task = self.get_task(self.path + taskname + '.task')
        if filename in task["Files"]:
            task["Files"].remove(filename)
        self.helper.write_json_file( self.path + taskname + '.task', task )

    def list_files(self):
        taskname = self.get_current_task()
        task = self.get_task(self.path + taskname + '.task')
        return task["Files"]

    def contains_file(self, filename):
        taskname = self.get_current_task()
        if taskname == None:
            return False
        task = self.get_task(self.path + taskname + '.task')
        for f in task["Files"]:
            if filename == f:
                return True
        return False
