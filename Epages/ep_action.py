import re

class ep_action(object):

    def __init__(helper):
        self.helper = helper


    #--- backend commands

    def update_ctags(self, filename):
        if self.helper.is_perl_module(filename):
            if self.helper.unix:
                vm = self.helper.vm_data(filename)["vm"]
                return self.helper.system_exec("ssh root@" + vm + " /bin/bash /srv/epages/eproot/maketags.sh &") if vm
            else:
                return self.helper.system_exec("restart epages")

    def check_syntax(self, filename):
        if self.helper.is_perl(filename):
            if self.helper.unix:
                vm = self.helper.vm_data(filename)["vm"]
                return self.helper.system_exec("ssh root@" + vm + " /srv/epages/eproot/Perl/bin/perl -c /srv/epages/eproot/" + filename) if vm
                return "error"
            else:
                return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + filename)
        # else if ep_helper.is_xml(filename):

    def perl_critic(self, filename):
        if self.helper.is_perl_module(filename):
            if self.helper.unix:
                vm = self.helper.vm_data(filename)["vm"]
                vm_filename = self.helper.vm_data(filename)["filename"]
                return self.helper.system_exec("ssh root@" + vm + "  /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Core/Scripts/critic.pl -verbose -profile /srv/epages/eproot/Cartridges/DE_EPAGES/Core/Scripts/perlcritic.conf /srv/epages/eproot/" + vm_filename) if vm
                return "error"
            else:
                return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + self.helper.working_path + "Cartridges\DE_EPAGES\Core\Scripts\critic.pl -verbose -profile " + self.helper.working_path + "Cartridges\DE_EPAGES\Core\Scripts\perlcritic.conf " + filename)

    def organize_imports(self, filename):
        if self.helper.is_perl_module(filename):
            if self.helper.unix:
                vm = self.helper.vm_data(filename)["vm"]
                vm_filename = self.helper.vm_data(filename)["filename"]
                return self.helper.system_exec("ssh root@" + vm + "  /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Core/Scripts/refactorCritic.pl -policy DE_EPAGES::Style::RequireCorrectImports -transform OrganizeImports -verbose /srv/epages/eproot/" + vm_filename) if vm
                return "error"
            else:
                return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + self.helper.working_path + "Cartridges\DE_EPAGES\Core\Scripts\\refactorCritic.pl -policy DE_EPAGES::Style::RequireCorrectImports -transform OrganizeImports -verbose " + filename)

    def correct_permissions(self, filename):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            return self.helper.system_exec("ssh root@" + vm + " /etc/init.d/epages6 perm cartridges") if vm
            return "error"

    # TODO
    def refresh_shared(self, filename):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            return self.helper.system_exec("ssh root@" + vm + " /etc/init.d/epages6 restart_perl") if vm
            return "error"
        else:
            return self.helper.system_exec("restart epages")

    def restart_perl(self, filename):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            return self.helper.system_exec("ssh root@" + vm + " /etc/init.d/epages6 restart_perl") if vm
            return "error"
        else:
            return self.helper.system_exec("restart epages")

    def restart_app(self, filename):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            return self.helper.system_exec("ssh root@" + vm + " /etc/init.d/epages6 start_service") if vm
            return "error"
        else:
            return self.helper.system_exec("restart epages")

    def import_xml(self, filename):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            vm_filename = self.helper.vm_data(filename)["filename"]
            return self.helper.system_exec("ssh root@" + vm + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Object/Scripts/import.pl -storename Store /srv/epages/eproot/" + vm_filename) if vm
            return "error"
        else:
            return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + self.helper.working_path + "Cartridges\DE_EPAGES\Object\Scripts\import.pl -storename Store " + filename)

    def import_hook(self, filename):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            vm_filename = self.helper.vm_data(filename)["filename"]
            return self.helper.system_exec("ssh root@" + vm + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Trigger/Scripts/import.pl -storename Store /srv/epages/eproot/" + vm_filename) if vm
            return "error"
        else:
            return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + self.helper.working_path + "Cartridges\DE_EPAGES\Trigger\Scripts\import.pl -storename Store " + filename)

    def delete_xml(self, filename):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            vm_filename = self.helper.vm_data(filename)["filename"]
            return self.helper.system_exec("ssh root@" + vm + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Object/Scripts/delete.pl -storename Store /srv/epages/eproot/" + vm_filename) if vm
            return "error"
        else:
            return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + self.helper.working_path + "Cartridges\DE_EPAGES\Object\Scripts\delete.pl -storename Store " + filename)

    def delete_hook(self, filename):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            vm_filename = self.helper.vm_data(filename)["filename"]
            return self.helper.system_exec("ssh root@" + vm + " /srv/epages/eproot/Perl/bin/perl /srv/epages/eproot/Cartridges/DE_EPAGES/Trigger/Scripts/delete.pl -storename Store /srv/epages/eproot/" + vm_filename) if vm
            return "error"
        else:
            return self.helper.system_exec(self.helper.working_path + "Perl/bin/perl.exe " + self.helper.working_path + "Cartridges\DE_EPAGES\Trigger\Scripts\delete.pl -storename Store " + filename)


    #--- filename manipulation

    def log(self, filename, logname):
        if self.helper.unix:
            vm = self.helper.vm_data(filename)["vm"]
            return self.helper.working_path + vm + "/Shared/Log/" + logname + ".log") if vm
            return "error"
        else:
            return self.helper.working_path + "Shared\Log\\" + logname + ".log")

    def template(self, filename, template):
        m = re.compile(r"^.*([\\|/]Cartridges.*?) .*$").match(template + ' ')
        if m:
            if self.helper.unix:
                vm = self.helper.vm_data(filename)["vm"]
                return self.helper.working_path + vm + m.group(1)) if vm
                return "error"
            else:
                return self.helper.working_path + m.group(1)


    #--- external GUI

    def cvs(self, filename):
        m = re.compile(r"(^.*)[/|\\](.*?)$").match(filename)
        if m:
            self.helper.system_exec(self.helper.cvs + " " + m.group(1) + " &")
        else:
            return "error"