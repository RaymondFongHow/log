import shutil, json

class Page(object):

    def __init__(self,title,addr='',templ_dir='static/templates/'):
        # print('Initializing Page')
        self.title = title
        self.addr = addr
        self.templ_dir = templ_dir
        self.templ_addr = templ_dir+self.title+'_template.html'

    def read_brics(self):
        print(self.templ_addr)
        with open(self.templ_addr) as templ:
            txt_str = templ.read()
        brics_lst = []
        for i in range(len(txt_str)-7):
            if txt_str[i:i+6] == '<bric>':
                j = 0
                while txt_str[i+j:i+j+7] != '</bric>':
                    j += 1
                brics_lst.append([[i,i+j+7],txt_str[i+6:i+j]])
        return brics_lst
    
    def bric_split(self):
        with open(self.templ_addr) as templ:
            txt_str = templ.read()
        lst = txt_str.split('<bric>')
        for i in range(len(lst)):
            lst[i] = lst[i].split('</bric>')
        lst = sum(lst, [])
        return lst
    
    def replace_brics(self,mode='preview',brics_dir='static/brics/'): # Edit target addr!!!
        self.mode = mode
        if mode == 'preview':
            dup_addr = self.addr+self.title+'_'+self.mode+'.html'
        if mode == 'publish':
            dup_addr = self.addr+self.title+'.html'
        print(dup_addr)
        shutil.copyfile(self.templ_addr,dup_addr)
        with open(self.templ_addr) as templ:
            txt_str = templ.read()
        dup_str = ''
        lst = txt_str.split('<bric>')
        for i in range(len(lst)):
            string = lst[i]
            sublst = string.split('</bric>')
            if len(sublst) == 1:
                dup_str += string
            else:
                indent = 0
                n = -1
                while lst[i-1][n] == ' ':
                    indent += 1
                    n -= 1
                target_title = sublst[0]
                rem_str = sublst[1]
                with open(brics_dir+target_title+'.html') as target:
                    add_lst = target.readlines()
                dup_str += add_lst[0]
                for ind in range(1,len(add_lst)):
                    dup_str += ' '*indent
                    dup_str += add_lst[ind]
                dup_str += rem_str
        with open(dup_addr,'w') as dup:
            dup.write(dup_str) 

    def bric_construct(self,dict):
        pass

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


def render_updates(addr='data/updates.json',cal_day_addr='static/brics/cal_day.html',target_dir='static/brics/'):
    with open(addr, 'r') as file:
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
    for cal_date in data:
        cal_day_str_dup = cal_day_str
        month,date = cal_date.split(' ')[0],cal_date.split(' ')[1]
        # print(date,month)
        date_split = cal_day_str_dup.split('{%date%}')
        # print(cal_day_str_dup)
        cal_day_str_dup = date_split[0]+date+date_split[1]
        month_split = cal_day_str_dup.split('{%month%}')
        cal_day_str_dup = month_split[0]+month+month_split[1]
        updates_split = cal_day_str_dup.split('{%updates%}')
        # assemble the first piece of the cal_day.html
        day_html = updates_split[0]
        # for every entry in that day
        entry_html = ''
        for rec in data[cal_date]:
            # print(rec)
            cat,title,desc = rec['cat'],rec['title'],rec['desc']
            ud = Update(cat,title,desc)
            entry_html += ud.render()
        lines = entry_html.split('\n')
        for line in lines:
            day_html += ((' '*indent)+line+'\n')
        # adding the last piece of cal_day.html
        day_html += updates_split[1]
        ud_html += day_html+'\n'
    with open(target_dir+'all_updates.html','w') as target:
        target.write(ud_html)
    return ud_html