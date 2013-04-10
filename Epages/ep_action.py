import re
import threading
import os

class ep_action(object):

    def __init__(self, helper):
        self.helper = helper


    #--- backend commands

    def update_ctags(self, filename):
        if self.helper.is_perl_module(filename):
            if self.helper.unix:
                vm = self.helper.vm_data(filename)["vm"]
                if vm: self.helper.system_call("ssh root@" + vm + " /bin/bash /srv/epages/eproot/maketags.sh &")
            else:
                return self.helper.system_exec("restart epages")

    def check_syntax(self, filename):
        if self.helper.is_perl(filename):
            if self.helper.unix:
                vm = self.helper.vm_data(filename)["vm"]
                vm_filename = self.helper.vm_data(filename)["filename"]
                if vm: return self.helper.system_exec("ssh root@" + vm + " /srv/epages/eproot/Perl/bin/perl -c /srv/epages/eproot/" + vm_filename)
                return "error"
            else:
                return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + filename)
        elif self.helper.is_js(filename):
            if self.helper.unix:
                vm = self.helper.vm_data(filename)["vm"]
                vm_filename = self.helper.vm_data(filename)["filename"]
                if vm: return self.helper.system_exec("ssh root@" + vm + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Presentation/Scripts/checkJSSyntax.pl -type Store -warnings -file " + "/srv/epages/eproot/" + vm_filename)
                return "error"
            else:
                return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + self.helper.working_path + "Cartridges\DE_EPAGES\Presentation\Scripts\checkJSSyntax.pl -type Store -warnings -file " + filename)
        # else if ep_helper.is_xml(filename):

    def perl_critic(self, filename):
        if self.helper.is_perl_module(filename):
            if self.helper.unix:
                vm = self.helper.vm_data(filename)["vm"]
                vm_filename = self.helper.vm_data(filename)["filename"]
                if vm: return self.helper.system_exec("ssh root@" + vm + "  /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Core/Scripts/critic.pl -verbose -profile /srv/epages/eproot/Cartridges/DE_EPAGES/Core/Scripts/perlcritic.conf /srv/epages/eproot/" + vm_filename)
                return "error"
            else:
                return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + self.helper.working_path + "Cartridges\DE_EPAGES\Core\Scripts\critic.pl -verbose -profile " + self.helper.working_path + "Cartridges\DE_EPAGES\Core\Scripts\perlcritic.conf " + filename)

    def organize_imports(self, filename):
        if self.helper.is_perl_module(filename):
            if self.helper.unix:
                vm = self.helper.vm_data(filename)["vm"]
                vm_filename = self.helper.vm_data(filename)["filename"]
                if vm: return self.helper.system_exec("ssh root@" + vm + "  /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Core/Scripts/refactorCritic.pl -policy DE_EPAGES::Style::RequireCorrectImports -transform OrganizeImports -verbose /srv/epages/eproot/" + vm_filename)
                return "error"
            else:
                return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + self.helper.working_path + "Cartridges\DE_EPAGES\Core\Scripts\\refactorCritic.pl -policy DE_EPAGES::Style::RequireCorrectImports -transform OrganizeImports -verbose " + filename)

    def correct_permissions(self, filename):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            if vm: return self.helper.system_exec("ssh root@" + vm + " /etc/init.d/epages6 perm cartridges")
            return "error"

    # TODO
    def refresh_shared(self, filename):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            if vm: return self.helper.system_exec("ssh root@" + vm + " /etc/init.d/epages6 restart_perl")
            return "error"
        else:
            self.helper.system_exec("net stop epages")
            return self.helper.system_exec("net start epages")

    def restart_perl(self, filename, callback):
        class restart_thread(threading.Thread):
            def __init__(self, helper, callback):
                threading.Thread.__init__(self)
                self.helper = helper
                self.callback = callback

            def run(self):
                if self.helper.unix:
                    vm = self.helper.vm_data(filename)["vm"]
                    if vm:
                        callback( self.helper.system_exec("ssh root@" + vm + " /etc/init.d/epages6 restart_perl") )
                        return  callback("error")
                else:
                    self.helper.system_exec("net stop epages")
                    callback( self.helper.system_exec("net start epages") )

        thread = restart_thread(self.helper, callback)
        thread.start()

    def set_debug(self, filename, lvl):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            if vm: return self.helper.system_exec("ssh root@" + vm + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Object/Scripts/set.pl -storename Store -path \"/\" JSDebugLevel=" + lvl)
            return "error"
        else:
            return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + self.helper.working_path + "Cartridges\DE_EPAGES\Object\Scripts\set.pl -storename Store -path \"/\" JSDebugLevel=" + lvl)

    def restart_app(self, filename):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            if vm: return self.helper.system_exec("ssh root@" + vm + " /etc/init.d/epages6 start_service")
            return "error"
        else:
            self.helper.system_exec("net stop epages")
            return self.helper.system_exec("net start epages")

    def import_xml(self, filename):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            vm_filename = self.helper.vm_data(filename)["filename"]
            if vm: return self.helper.system_exec("ssh root@" + vm + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Object/Scripts/import.pl -storename Store /srv/epages/eproot/" + vm_filename)
            return "error"
        else:
            return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + self.helper.working_path + "Cartridges\DE_EPAGES\Object\Scripts\import.pl -storename Store " + filename)

    def import_hook(self, filename):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            vm_filename = self.helper.vm_data(filename)["filename"]
            if vm: return self.helper.system_exec("ssh root@" + vm + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Trigger/Scripts/import.pl -storename Store /srv/epages/eproot/" + vm_filename)
            return "error"
        else:
            return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + self.helper.working_path + "Cartridges\DE_EPAGES\Trigger\Scripts\import.pl -storename Store " + filename)

    def delete_xml(self, filename):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            vm_filename = self.helper.vm_data(filename)["filename"]
            if vm: return self.helper.system_exec("ssh root@" + vm + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Object/Scripts/delete.pl -storename Store /srv/epages/eproot/" + vm_filename)
            return "error"
        else:
            return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + self.helper.working_path + "Cartridges\DE_EPAGES\Object\Scripts\delete.pl -storename Store " + filename)

    def delete_hook(self, filename):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            vm_filename = self.helper.vm_data(filename)["filename"]
            if vm: return self.helper.system_exec("ssh root@" + vm + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Trigger/Scripts/delete.pl -storename Store /srv/epages/eproot/" + vm_filename)
            return "error"
        else:
            return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + self.helper.working_path + "Cartridges\DE_EPAGES\Trigger\Scripts\delete.pl -storename Store " + filename)


    #--- filename manipulation

    def log(self, filename, logname):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            if vm: return self.helper.working_path + vm + "/Shared/Log/" + logname + ".log"
            return "error"
        else:
            return self.helper.working_path + "Shared\Log\\" + logname + ".log"

    def template(self, filename, template):
        m = re.compile(r"^.*([\\|/]Cartridges.*?) .*$").match(template + ' ')
        if m:
            if self.helper.unix:
                vm = self.helper.vm_data(filename)["vm"]
                if vm: return self.helper.working_path + vm + m.group(1)
                return "error"
            else:
                return self.helper.working_path + m.group(1)


    #--- external GUI

    def cvs(self, filename):
        if os.path.isdir(filename):
            self.helper.system_call(self.helper.cvs + " " + filename + " &")
        else:
            self.helper.system_call(self.helper.cvs + " " + os.path.dirname(filename) + " &")
