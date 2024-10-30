import logpy
from logpy import gitcmd, pageworks

# sess = gitcmd.Log()
# sess.add_remark('General update.')
# print('\n'*5)

index = pageworks.Page('index')
index.replace_brics()
index.replace_brics(mode='publish')

dashboard = pageworks.Page('dashboard')
dashboard.replace_brics()
dashboard.replace_brics(mode='publish')

# test
# sess.close()