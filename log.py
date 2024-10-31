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

    target_title = 'updates_'+category+'.html'
    target_addr = target_dir+target_title
    with open(target_addr,'w') as target:
        target.write(ud_html)
        print(f'Rendered {target_title} at log/{target_dir}')
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


def build_cat_templ(category,target_dir='static/templates/',mother_templ_addr='static/templates/Category_template.html'):
    with open(mother_templ_addr) as mother_templ:
        mt_str = mother_templ.read()
    title = category
    title_split = mt_str.split('{%title%}')
    mt_str = title_split[0]+title+title_split[1]
    category_split = mt_str.split('{%category%}')
    mt_str = category_split[0]+category+category_split[1]
    target_title = category+'_template.html'
    target_addr = target_dir+target_title
    with open(target_addr,'w') as target:
        target.write(mt_str)
        print(f'Built {target_title} at log/{target_dir}')
    return mt_str

def build_cats_bric(target_dir='static/brics/'): # for displaying categories in Fields
    bric_str = ''
    for cat in read_categories():
        bric_str += f"<div class='cat_link'><a href='{cat}.html'>{cat}</a></div>\n"
    target_title = 'categories.html'
    with open(target_dir+target_title,'w') as target:
        target.write(bric_str)
        print(f"Built {target_title} at log/{target_dir}")
    return bric_str


render_updates() # category='Dashboard'
print('\n')

cats = read_categories()
# print("Categories:")
for cat in read_categories():
    print(cat)
    build_cat_templ(category=cat)
    render_updates(category=cat)
    print('\n')

build_cats_bric()

page_mode_dict = {
    'Index'             :   'publish',
    'Dashboard'         :   'publish',
    'Fields'            :   'publish',
    'Physics'           :   'publish',
    'Mathematics'       :   'preview',
    'Computer Science'  :   'publish'
    # 'New Field'         :   'publish'
}

for title in page_mode_dict:
    m = page_mode_dict[title]
    index = pageworks.Page(title)
    index.replace_brics(mode=m)
    
# sess.close()

print(f'\n\n\nProcess completed at {datetime.now()}')