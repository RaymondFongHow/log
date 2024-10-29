import subprocess
from pexpect import popen_spawn
from datetime import datetime

with open('/Users/raymondfonghow/Credentials/github.txt','r') as cred:
    username = cred.readline().strip()
    password = cred.readline().strip()

class Log(object):

    def __init__(self):
        print('Initializing Log')
        with open('gitcmd_hist.txt','a') as hist:
            hist.write(str(datetime.now()))

    def add_remark(self,remark=''):
        self.remark = remark

    def disp_hist(self):
        with open('gitcmd_hist.txt','r') as hist:
            lines = hist.readlines()
            for line in lines:
                print(line,end='')

    def close(self):
        with open('gitcmd_hist.txt','a') as hist:
            hist.write(' ')
            hist.write(self.remark)
            hist.write('\n')
        self.disp_hist()
        print('Logging session closed.\n')

# cmd = "cd C:\\Users\Dropbox\git-test"
# returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix

# cmd = "git add ." 
# subprocess.call(cmd, shell=True)

# cmd = 'git commit -m "python project update"'
# subprocess.call(cmd, shell=True)

# cmd = "git remote set-url origin https://github.com/Tehsurfer/git-test.git"
# subprocess.call(cmd, shell=True)

# cmd = "git push "
# child_process = popen_spawn.PopenSpawn(cmd)
# child_process.expect('User')
# child_process.sendline(user)
# child_process.expect('Password')
# child_process.sendline(password)
# print('returned value:', returned_value)

# print('end of commands')