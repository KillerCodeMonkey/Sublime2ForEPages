import sublime, sublime_plugin
import ep_action, ep_helper, ep_task, ep_cvs
import re
import os
import threading

helper = ep_helper.ep_helper(sublime.load_settings("Epages.sublime-settings"))
action = ep_action.ep_action(helper)
tasks = ep_task.ep_task(helper)
cvs = ep_cvs.ep_cvs(helper)

# class OpenFileOnCsVmCommand(sublime_plugin.WindowCommand):
#     def run(self):
#         vm_data = ep_helper.get_vm_data(self.view.file_name())
#         if vm_data["is_epages"]:
#             self.view.window().open_file("~/Entwicklung/epages6/cs-vm-lin2/" + vm_data["filename"])
#         else:
#             sublime.error_message("Not an epages6 folder")

class ep_on_post_save(sublime_plugin.EventListener):
    def on_post_save(self, view):
        # update ctags on vm
        action.update_ctags(view.file_name())

    def on_activated(self, view):
        self.view = view
        self.filename = view.file_name()
        if self.filename:
            t = threading.Thread(target=self.cvs_status())
            t.start()

    def cvs_status(self):
        status = cvs.status( self.filename )
        if status["status"]:
            self.view.set_status("cvs_a", "Status: " + status["status"])
        if status["branch"]:
            self.view.set_status("cvs_b", "Branch: " + status["branch"])

class OpenErrorLogCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = self.window.active_view().file_name()
        log = action.log(filename, "error")
        if log == "error":
            sublime.error_message("Not an epages6 folder")
        else:
            self.window.open_file(log)

class OpenDebugLogCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = self.window.active_view().file_name()
        log = action.log(filename, "dev")
        if log == "error":
            sublime.error_message("Not an epages6 folder")
        else:
            self.window.open_file(log)

class CheckSyntaxCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = self.window.active_view().file_name()
        result = action.check_syntax(filename)
        if result == "error":
            sublime.error_message("Not an epages6 folder")
        else:
            sublime.message_dialog(result)

class OpenCvsCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = self.window.active_view().file_name()
        cvs = action.cvs(filename)
        if cvs == "error":
            sublime.error_message("Not an epages6 folder")

class CorrectPermissionsCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = self.window.active_view().file_name()
        result = action.correct_permissions(filename)
        if result == "error":
            sublime.error_message("Not an epages6 folder")
        else:
            sublime.message_dialog("Permissions corrected!")

class RestartAppCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = self.window.active_view().file_name()
        result = action.restart_app(filename)
        if result == "error":
            sublime.error_message("Not an epages6 folder")
        else:
            sublime.message_dialog("AppServer restarted!")

class RestartPerlCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = self.window.active_view().file_name()
        result = action.restart_perl(filename)
        if result == "error":
            sublime.error_message("Not an epages6 folder")
        else:
            sublime.message_dialog("Perl restarted!")

class PerlCriticCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = self.window.active_view().file_name()
        result = action.perl_critic(filename)
        if result == "error":
            sublime.error_message("Not an epages6 folder")
        else:
            print(result)
            sublime.message_dialog(result)

class OrganizeImportsCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = self.window.active_view().file_name()
        result = action.organize_imports(filename)
        if result == "error":
            sublime.error_message("Not an epages6 folder")
        else:
            sublime.message_dialog("Imports organized")

class ImportCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = self.window.active_view().file_name()
        result = action.import_xml(filename)
        if result == "error":
            sublime.error_message("Not an epages6 folder")
        else:
            sublime.message_dialog("XML imported")

class DeleteCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = self.window.active_view().file_name()
        result = action.delete_xml(filename)
        if result == "error":
            sublime.error_message("Not an epages6 folder")
        else:
            sublime.message_dialog("XML deleted")

class ImportHookCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = self.window.active_view().file_name()
        result = action.import_hook(filename)
        if result == "error":
            sublime.error_message("Not an epages6 folder")
        else:
            sublime.message_dialog("Hook imported")

class DeleteHookCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = self.window.active_view().file_name()
        result = action.delete_hook(filename)
        if result == "error":
            sublime.error_message("Not an epages6 folder")
        else:
            sublime.message_dialog("Hook deleted")

class OpenTemplateCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Paste template here", "", self.on_done, None, None)

    def on_done(self, template_string):
        filename = self.window.active_view().file_name()
        template = action.template(filename, template_string)
        if template == "error":
            sublime.error_message("Not an epages6 folder")
        else:
            self.window.open_file(template)

class TaskChooseCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.tasklist = tasks.get_task_list()
        if len(self.tasklist) > 0:
            self.window.show_quick_panel ( ["Press ESC to create a new Task","Close current Task"]+self.tasklist, self.task_choose )
        else:
            self.window.run_command('task_create')

    def description(self):
        current_task = tasks.get_current_task()
        if current_task == None:
            return "No current Task"
        else:
            task = tasks.get_task(tasks.path+current_task+".task")
            return current_task + ' ('+ str(len(task["Files"])) + ')'

    def task_choose(self, i):
        # SKip the first Entry for info message for creation
        i = i - 2
        if i > -1:
            task = self.tasklist[i]
            tasks.set_current_task( task[0] )
        elif i == -1:
            tasks.set_current_task( None )
        else:
            self.window.run_command('task_create')

class TaskCreateCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel('Create a Task:', '', self.create_task, None, None)

    def create_task(self,input):
        self.taskname = input
        if input != '':
            self.window.show_input_panel('Description:', '', self.create_taskdescription, None, None)

    def create_taskdescription(self, description):
        if description != '':
            tasks.create_task(self.taskname, description)

class TaskFileAddCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = self.window.active_view().file_name()
        tasks.add_file(filename)

    def is_visible(self):
        filename = self.window.active_view().file_name()
        return tasks.get_current_task() != None and not tasks.contains_file(filename)

class TaskFileRemoveCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = self.window.active_view().file_name()
        tasks.remove_file(filename)

    def is_visible(self):
        filename = self.window.active_view().file_name()
        return tasks.get_current_task() != None and tasks.contains_file(filename)

class TaskOpenTaskFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        task = tasks.get_current_task()
        self.window.open_file(tasks.path+task+".task")

    def is_visible(self):
        return tasks.get_current_task() != None

class TaskListFilesCommand(sublime_plugin.WindowCommand):
    def run(self):
        files = tasks.list_files()
        self.filelist = []
        for f in files:
            head, tail = os.path.split(f)
            self.filelist.append([tail,f])
        if len(self.filelist) > 0:
            self.window.show_quick_panel ( self.filelist+["Open all"], self.open_file )

    def open_file(self, i):
        if i > -1 and i != len(self.filelist):
            self.window.open_file(self.filelist[i][1])
        elif i == len(self.filelist):
            for f in self.filelist:
                self.window.open_file(f[1])


    def is_visible(self):
        taskname = tasks.get_current_task()
        task = tasks.get_task(tasks.path+taskname+".task")
        return task != None and len(task["Files"]) > 0

# class CvsStatusCommand(sublime_plugin.WindowCommand):
#     def run(self):
#         self.filename = self.window.active_view().file_name()
#         #self.panel = self.window.new_file()
#         t = threading.Thread(target=self.cvs_status())
#         t.start()

#     def cvs_status(self):
#         relpath = os.path.relpath( self.filename ,'.')
#         path = os.path.dirname( relpath )
#         filename = os.path.basename( relpath )
#         cmd = "cd " + path + "&& cvs status " + filename
#         cvs_status = helper.system_exec( cmd )
#         m = re.compile(r".*?Status:\s*([a-zA-Z -]*)\s*.*?Sticky Tag:\s*(\S*).*", re.S).match(cvs_status)
#         if m:
#             self.window.active_view().set_status("cvs_status", "Status: " + m.group(1))
#             self.window.active_view().set_status("cvs_branch", "Branch: " + m.group(2))

#     def write_to_panel(self):
#         if len(self.textbuffer):
#             panel_edit = self.panel.begin_edit()
#             self.panel.insert(panel_edit, self.panel.size(), self.textbuffer)
#             self.panel.end_edit(panel_edit)
#             self.panel.show(self.panel.size())
#             self.textbuffer = ""
#             self.window.run_command("show_panel", {"panel": "output.test_panel"})
