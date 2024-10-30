print('\n'*5)

import logpy
from logpy import gitcmd, pageworks

print('\n'*5)

# sess = gitcmd.Log()
# sess.add_remark('General update.')
# print('\n'*5)

page = pageworks.Page('dashboard_template.html')
brics = page.read_brics()
# for bric in brics:
#     print(bric)
# print('\n'*5)


page.replace_brics()
# for chunk in page.bric_split():
#     print(chunk)
print('\n'*5)


# sess.close()