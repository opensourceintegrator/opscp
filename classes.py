from subprocess import PIPE, Popen
import shlex


class BashCommand:
    def __init__(self, command):
        self.command = shlex.split(command)
        self.process = Popen(self.command, stdout=PIPE, stderr=PIPE)

    def run_command(self):
        while True:
            output = self.process.stdout.readline().decode()
            if output == '' and self.process.poll() is not None:  # Process finished.
                break
            if output:
                print(output.strip())
        rc = self.process.poll()
        return rc


class ListPackages:
    def __init__(self, *args):
        self.command = shlex.split('apt list ' + ''.join(args))
        self.process = Popen(self.command, stdout=PIPE, stderr=PIPE)

    def run_command(self):
        packages = {}
        self.process.stdout.readline()  # skip the first line
        while True:
            output = self.process.stdout.readline().decode()
            if output == '' and self.process.poll() is not None:  # Process finished.
                break
            splitted_output = output.split("/")
            package_name = splitted_output[0]
            package_version = splitted_output[1].split()[1].split(":")[-1].split("-")[0]
            packages[package_name] = package_version
        return packages
