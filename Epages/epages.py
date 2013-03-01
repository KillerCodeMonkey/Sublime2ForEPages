
import sublime, sublime_plugin

import subprocess
import re


class OpenFileOnCsVmCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        vm_data = ep_helper.get_vm_data(self.view.file_name())
        if vm_data["is_epages"]:
            self.view.window().open_file("~/Entwicklung/epages6/cs-vm-lin2/" + vm_data["filename"])
        else:
            sublime.error_message("Not an epages6 folder")

class OpenErrorLogCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        vm_data = ep_helper.get_vm_data(self.view.file_name())
        if vm_data["is_epages"]:
            self.view.window().open_file("~/Entwicklung/epages6/" + vm_data["vm"] + "/Shared/Log/error.log")
        else:
            sublime.error_message("Not an epages6 folder")

class OpenDebugLogCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        vm_data = ep_helper.get_vm_data(self.view.file_name())
        if vm_data["is_epages"]:
            self.view.window().open_file("~/Entwicklung/epages6/" + vm_data["vm"] + "/Shared/Log/debug.log")
        else:
            sublime.error_message("Not an epages6 folder")

class CheckSyntaxCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        vm_data = ep_helper.get_vm_data(self.view.file_name())
        if vm_data["is_epages"]:
            ep_action.check_syntax(vm_data["filename"], vm_data["vm"])
        else:
            sublime.error_message("Not an epages6 folder")

class OpenCervisiaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        local_filename = self.view.file_name()
        vm_data = ep_helper.get_vm_data(local_filename)
        if vm_data["is_epages"]:
            m = re.compile(r"(^.*)/(.*?)$").match(local_filename)
            if m:
                subprocess.call("cervisia " + m.group(1) + " &", shell = True)
                # subprocess.call("cervisia --log " + local_filename + " &", shell = True)
        else:
            sublime.error_message("Not an epages6 folder")

class CorrectPermissionsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        local_filename = self.view.file_name()
        vm_data = ep_helper.get_vm_data(local_filename)
        if vm_data["is_epages"]:
            print "Correct permissions on " + vm_data["vm"]
            subprocess.call("ssh root\@" + vm_data["vm"] + " /etc/init.d/epages6 perm cartridges", shell = True)
            sublime.message_dialog("Correct permissions finished")
        else:
            sublime.error_message("Not an epages6 folder")

class RestartCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        local_filename = self.view.file_name()
        vm_data = ep_helper.get_vm_data(local_filename)
        if vm_data["is_epages"]:
            print "Restart application server on " + vm_data["vm"]
            result = subprocess.Popen("ssh root\@" + vm_data["vm"] + " /etc/init.d/epages6 start_service", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            print result.stdout.read()
            sublime.message_dialog("Restart application server finished")
        else:
            sublime.error_message("Not an epages6 folder")

class PerlCriticCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        local_filename = self.view.file_name()
        vm_data = ep_helper.get_vm_data(local_filename)
        if vm_data["is_epages"] and ep_helper.is_perl(local_filename):
            print "Do perl::critic on " + vm_data["vm"]
            result = subprocess.Popen("ssh root\@" + vm_data["vm"] + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Core/Scripts/critic.pl -verbose -profile /srv/epages/eproot/Cartridges/DE_EPAGES/Core/Scripts/perlcritic.conf /srv/epages/eproot/" + vm_data["filename"], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            print_stdout = result.stdout.read()
            print_stderr = result.stderr.read()
            try:
                sublime.message_dialog(print_stdout.decode("utf-8") + "\n\n" + print_stderr.decode("utf-8"))
            except UnicodeDecodeError:
                print "return perl::critic result with encoding iso8859-1"
                sublime.message_dialog(print_stdout.decode("iso8859-1") + "\n\n" + print_stderr.decode("iso8859-1"))
        else:
            sublime.message_dialog("Not an epages6 folder")

class OrganizeImportsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        local_filename = self.view.file_name()
        vm_data = ep_helper.get_vm_data(local_filename)
        if vm_data["is_epages"] and ep_helper.is_perl(local_filename):
            print "Organize imports on " + vm_data["vm"]
            result = subprocess.Popen("ssh root\@" + vm_data["vm"] + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Core/Scripts/refactorCritic.pl -policy DE_EPAGES::Style::RequireCorrectImports -transform OrganizeImports -verbose /srv/epages/eproot/" + vm_data["filename"], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            sublime.message_dialog(result.stdout.read())
        else:
            sublime.error_message("Not an epages6 folder")

class ImportCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        local_filename = self.view.file_name()
        vm_data = ep_helper.get_vm_data(local_filename)
        if vm_data["is_epages"] and ep_helper.is_xml(local_filename):
            print "Import on " + vm_data["vm"]
            result = subprocess.Popen("ssh root\@" + vm_data["vm"] + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Object/Scripts/import.pl -storename Store /srv/epages/eproot/" + vm_data["filename"], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            sublime.message_dialog("Import finished\n\n" + result.stdout.read())
        else:
            sublime.error_message("Not an epages6 folder")

class DeleteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        local_filename = self.view.file_name()
        vm_data = ep_helper.get_vm_data(local_filename)
        if vm_data["is_epages"] and ep_helper.is_xml(local_filename):
            print "Delete on " + vm_data["vm"]
            result = subprocess.Popen("ssh root\@" + vm_data["vm"] + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Object/Scripts/delete.pl -storename Store /srv/epages/eproot/" + vm_data["filename"], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            sublime.message_dialog("Delete finished\n\n" + result.stdout.read())
        else:
            sublime.error_message("Not an epages6 folder")

class ImportHookCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        local_filename = self.view.file_name()
        vm_data = ep_helper.get_vm_data(local_filename)
        if vm_data["is_epages"] and ep_helper.is_xml(local_filename):
            print "Import hook on " + vm_data["vm"]
            result = subprocess.Popen("ssh root\@" + vm_data["vm"] + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Trigger/Scripts/import.pl -storename Store /srv/epages/eproot/" + vm_data["filename"], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            sublime.message_dialog("Import hook finished\n\n" + result.stdout.read())
        else:
            sublime.error_message("Not an epages6 folder")

class DeleteHookCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        local_filename = self.view.file_name()
        vm_data = ep_helper.get_vm_data(local_filename)
        if vm_data["is_epages"] and ep_helper.is_xml(local_filename):
            print "Delete hook on " + vm_data["vm"]
            result = subprocess.Popen("ssh root\@" + vm_data["vm"] + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Trigger/Scripts/delete.pl -storename Store /srv/epages/eproot/" + vm_data["filename"], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            sublime.message_dialog("Delete hook finished\n\n" + result.stdout.read())
        else:
            sublime.error_message("Not an epages6 folder")

class OpenTemplateCommand(sublime_plugin.WindowCommand):
    def run(self):
        local_filename = self.window.active_view().file_name()
        self.vm_data = ep_helper.get_vm_data(local_filename)
        if self.vm_data["vm"]:
            self.window.show_input_panel("Paste template here", "", self.on_done, None, None)
        else:
            sublime.error_message("Not an epages6 folder")

    def on_done(self, template_string):
        m = re.compile(r"^.*(/Cartridges.*?) .*$").match(template_string + ' ')
        if m:
            self.window.open_file("~/Entwicklung/epages6/" + self.vm_data["vm"] + m.group(1))





class ep_on_post_save(sublime_plugin.EventListener):
    def on_post_save(self, view):

        vm_data = ep_helper.get_vm_data(view.file_name())

        if vm_data["is_epages"]:
            filename = vm_data["filename"]
            vm = vm_data["vm"]
            print filename + " on " + vm

            # update ctags on vm
            ep_action.update_ctags(filename, vm)




class ep_action(object):
    @staticmethod
    def update_ctags(filename, vm):
        if ep_helper.is_perl_module(filename):
            print "Updating tags for Cartridges"
            subprocess.call("ssh root@" + vm + " /bin/bash /srv/epages/eproot/maketags.sh &", shell = True)

    @staticmethod
    def check_syntax(filename, vm):
        syntax_result = ''
        if ep_helper.is_perl(filename):
            print "Check perl syntax"
            result = subprocess.Popen("ssh root\@" + vm + " /srv/epages/eproot/Perl/bin/perl -c /srv/epages/eproot/" + filename + " &", shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            syntax_result = result.stderr.read()
            sublime.message_dialog(syntax_result)
        # else if ep_helper.is_xml(filename):




class ep_helper(object):
    settings = sublime.load_settings("Epages.sublime-settings")
    working_path = settings.get("working_path")

    @staticmethod
    def get_vm_data(filename):
        m = re.compile(r"/home/jonas/Entwicklung/epages6/(.*?)/(Cartridges.*)$").match(filename)
        if m:
            return {"vm": m.group(1), "filename": m.group(2), "is_epages": True}
        return {"vm": "", "filename": "", "is_epages": False}

    @staticmethod
    def is_perl(filename):
        return re.match(r".*\.(pm|pl|t)$", filename)

    @staticmethod
    def is_perl_module(filename):
        return re.match(r".*\.pm$", filename)

    @staticmethod
    def is_xml(filename):
        return re.match(r".*\.xml$", filename)
