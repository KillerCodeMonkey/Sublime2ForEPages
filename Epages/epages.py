import sublime, sublime_plugin
import ep_action, ep_helper

helper = ep_helper.ep_helper(sublime.load_settings("Epages.sublime-settings"))
action = ep_action.ep_action(helper)

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
        log = action.log(filename, "debug")
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
