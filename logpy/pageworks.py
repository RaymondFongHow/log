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
    
    def replace_brics(self,mode='preview',target_dir='static/brics/'): # Edit target addr!!!
        self.mode = mode
        if mode == 'preview':
            dup_addr = self.addr.split('_')[0]+'_'+self.mode+'.html'
        if mode == 'publish':
            dup_addr = self.addr.split('_')[0]+'.html'
        shutil.copyfile(self.addr,dup_addr)
        with open(self.addr) as templ:
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
                with open(target_dir+target_title+'.html') as target:
                    add_lst = target.readlines()
                dup_str += add_lst[0]
                for ind in range(1,len(add_lst)):
                    dup_str += ' '*indent
                    dup_str += add_lst[ind]
                dup_str += rem_str
        with open(dup_addr,'w') as dup:
            dup.write(dup_str) 