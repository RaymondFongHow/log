import os, shutil

class Page(object):

    def __init__(self,addr):
        # print('Initializing Page')
        self.addr = addr

    def read_brics(self):
        with open(self.addr) as templ:
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
        with open(self.addr) as templ:
            txt_str = templ.read()
        lst = txt_str.split('<bric>')
        for i in range(len(lst)):
            lst[i] = lst[i].split('</bric>')
        lst = sum(lst, [])
        return lst
    
    def replace_brics(self,mode='preview',target_dir='static/partial_templates/'): # Edit target addr!!!
        self.mode = mode
        dup_addr = self.addr.split('.')[0]+'_'+self.mode+'.html'
        shutil.copyfile(self.addr,dup_addr)
        with open(self.addr) as templ:
            txt_str = templ.read()
        offset = 0
        for bric in self.read_brics():
            str_head = bric[0][0]
            str_tail = bric[0][1]
            target_title = bric[1]
            with open(target_dir+target_title+'.html') as target:
                rep_str = target.read()
            txt_str = txt_str[:str_head+offset]+rep_str+txt_str[str_tail+offset:]
            offset = offset + len(rep_str) - 13 - len(target_title) # <bric></bric> and title removed, thus shorter
            # print(txt_str)
        with open(dup_addr,'w') as dup:
            dup.write(txt_str)