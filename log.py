import logpy
from logpy import gitcmd, pageworks
import json

# Open and read the updates JSON file
with open('data/updates.json', 'r') as file:
    data = json.load(file)

# for date in data:
#     print(date)

# sess = gitcmd.Log()
# sess.add_remark('General update.')
# print('\n'*5)

pageworks.render_updates()

index = pageworks.Page('index')
index.replace_brics()
index.replace_brics(mode='publish')

dashboard = pageworks.Page('dashboard')
dashboard.replace_brics()
dashboard.replace_brics(mode='publish')

# print(ud1.render())

# test
# sess.close()