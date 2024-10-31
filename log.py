import logpy
from logpy import gitcmd, pageworks
import json
from datetime import datetime

# sess = gitcmd.Log()
# sess.add_remark('General update.')
# print('\n'*5)

class Update(object):

    def __init__(self,cat,title,desc):
        self.cat = cat
        self.title = title
        self.desc = desc

    def render(self,addr='static/brics/update.html'):
        with open(addr) as ud_templ:
            ud_txt = ud_templ.read()
        repl_dict = {
            '{%category%}':self.cat,
            '{%title%}':self.title,
            '{%description%}':self.desc
        }
        for repl in repl_dict:
            ud_lst = ud_txt.split(repl)
            ud_txt = ud_lst[0]+repl_dict[repl]+ud_lst[1]
        return ud_txt+'\n' # there's a new line here!!!


def render_updates(category='Dashboard',data_addr='data/updates.json',cal_day_addr='static/brics/cal_day.html',target_dir='static/brics/'):
    with open(data_addr, 'r') as file:
        data = json.load(file)
    ud_html = ''
    with open(cal_day_addr) as file:
        cal_day_str = file.read()
        cal_day_lst = cal_day_str.split('{%updates%}')
    # finding the proper indent in cal_day.html
    indent = 0
    i = -1
    while cal_day_lst[0][i] == ' ':
        indent += 1
        i -= 1
    # insert lines for days irritatively
    for year in data:
        for cal_date in data[year]:
            entry = 0
            cal_day_str_dup = cal_day_str
            month,date = cal_date.split(' ')[0],cal_date.split(' ')[1]
            date_split = cal_day_str_dup.split('{%date%}')
            cal_day_str_dup = date_split[0]+date+date_split[1]
            month_split = cal_day_str_dup.split('{%month%}')
            cal_day_str_dup = month_split[0]+month+month_split[1]
            year_split = cal_day_str_dup.split('{%year%}')
            cal_day_str_dup = year_split[0]+year+year_split[1]
            updates_split = cal_day_str_dup.split('{%updates%}')
            # assemble the first piece of the cal_day.html
            day_html = updates_split[0]
            # for every entry in that day
            entry_html = ''
            for rec in data[year][cal_date]:
                cat,title,desc = rec['cat'],rec['title'],rec['desc']
                if category == 'Dashboard':
                    ud = Update(cat,title,desc)
                    entry_html += ud.render()
                    entry += 1
                elif cat == category:
                    ud = Update('',title,desc)
                    entry_html += ud.render()
                    entry += 1 
            lines = entry_html.split('\n')
            for line in lines:
                day_html += ((' '*indent)+line+'\n')
            # adding the last piece of cal_day.html
            day_html += updates_split[1]
            if entry > 0:
                ud_html += day_html+'\n'
        with open(target_dir+'updates_'+category+'.html','w') as target:
            target.write(ud_html)
    return ud_html


def read_categories(data_addr='data/updates.json'):
    cats = []
    with open(data_addr, 'r') as file:
        data = json.load(file)
    for year in data:
        for cal_date in data[year]:
            for rec in data[year][cal_date]:
                cat = rec['cat']
                if cat not in cats and cat not in ['',' ']:
                    cats.append(cat)
    return cats


def build_cat_templ(cat,mot_templ_addr):
    pass


# print(read_categories())

render_updates() # category='Dashboard'
render_updates(category='Physics')
render_updates(category='Mathematics')
render_updates(category='Computer Science')

page_mode_dict = {
    'Index'             :'publish',
    'Dashboard'         :'publish',
    'Physics'           :'publish',
    'Mathematics'       :'preview',
    'Computer Science'  :'publish'
}

for title in page_mode_dict:
    m = page_mode_dict[title]
    index = pageworks.Page(title)
    index.replace_brics(mode=m)
    
# sess.close()

print(f'Process completed at {datetime.now()}')