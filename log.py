import logpy
from logpy import gitcmd, pageworks
import json

# Open and read the updates JSON file
# with open('updates.json', 'r') as file:
#     data = json.load(file)


sess = gitcmd.Log()
sess.add_remark('General update.')
print('\n'*5)

index = pageworks.Page('index')
index.replace_brics()
index.replace_brics(mode='publish')

dashboard = pageworks.Page('dashboard')
dashboard.replace_brics()
dashboard.replace_brics(mode='publish')

cat,title,desc = 'CATEGORY','TITLE','DESCRIPTION'
ud1 = pageworks.Update(cat,title,desc)
print(ud1.render())

# test
# sess.close()