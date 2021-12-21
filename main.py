import remi.gui as gui
from remi import start, App
import random
class question:
    def __init__(self, question,options, answers,knowledge_point):
        self.type=0
        self.question = question
        self.options = options
        self.answers =[]
        for i in answers:
            if i=='A':
                self.answers.append(0)
            elif i=='B':
                self.answers.append(1)
            elif i=='C':
                self.answers.append(2)
            elif i=='D':
                self.answers.append(3)
            elif i=='Y':
                self.answers.append(0)
            elif i=='N':
                self.answers.append(1)
        self.knowledge_point = knowledge_point
        self.cnt = 0
    def judege(self,options):
        if options == self.answers:
            self.cnt += 1
            return True
        else:
            self.cnt -= 1
            if self.cnt<0:
                self.cnt=0
            return False
def init_tiku():
    arr=[]
    f = open("tiku.txt",encoding = "utf-8")
    tiku = f.read()
    f.close()
    tmp ="";
    tlist=[]
    flag=0
    q=question(tmp,tlist,tmp,tmp)
    for i in tiku:
        if i=='@':
            if flag==2:
                q.knowledge_point=tmp
            else:
                q.answers=tmp
            flag=0
            arr.append(q)
            tmp=""
            q=question(tmp,[],tmp,tmp)
        elif i=='#':
            if flag == 0:
                q.question=tmp
                flag=1
                tmp=""
            else:
                q.options.append(tmp)
                tmp=""
        elif i=='%':
            if flag == 0:
                q.question=tmp
            else:
                q.options.append(tmp)
            tmp=""
        elif i=='$':
            q.answers=tmp
            tmp=""
            flag=2;
        else:
            tmp+=i
    return arr
arr = init_tiku()
fst=arr[1];
class main_container(App):
    question_num=1
    is_clicked=[0,0,0,0]
    question_tp=0
    def __init__(self, *args):
        super(main_container, self).__init__(*args)
        self.title = "马原自动机_by_randow"
    def main(self):
        mainContainer = gui.VBox(width=1000, height=800, style={'margin':'0px auto', 'padding':'0px'})
        self.btn=gui.Button('提交',width=200,height=50)
        self.btn.onclick.connect(self.submit)
        self.nxt=gui.Button('下一题',width=200,height=50)
        self.nxt.onclick.connect(self.to_next)
        self.ans=gui.Label('',width=200,height=50)
        self.knowledge_point=gui.Label(fst.knowledge_point,width=200,height=50)
        self.question=gui.Label(fst.question,width=200,height=50)
        self.tbl=gui.Table.new_from_list([
                                   ('[ ]', fst.options[0]),
                                   ('[ ]', fst.options[1]),
                                   ('[ ]', fst.options[2]),
                                   ('[ ]', fst.options[3]),], width=300, height=200, margin='10px',fill_title=False)
        self.tbl.on_table_row_click.do(self.on_table_row_click)
        mainContainer.append(self.knowledge_point)
        mainContainer.append(self.ans)
        mainContainer.append(self.nxt)
        mainContainer.append(self.btn)
        mainContainer.append(self.tbl)
        mainContainer.append(self.question)
        return mainContainer
    def on_table_row_click(self, widget, row, col):
        if self.question_tp == 0:
            for i in range(4):
                if self.is_clicked[i]==1:
                    self.is_clicked[i]=1
                    self.tbl.set_cell_value(i,0,'[ ]')
                    break
        self.is_clicked[row]=1
        self.tbl.set_cell_value(row,0,'[X]')
    def submit(self, widget):
        tans=[]
        for i in range(4):
            if self.is_clicked[i]==1:
                tans.append(i)
        if fst.judege(tans):
            self.ans.set_text('正确')
        else:
            self.ans.set_text('错误')
    def to_next(self, widget):
        while True:
            to=random.randint(0,len(arr)-1)
            if arr[to].cnt>=4:
                continue
            else: 
                break
        self.question.set_text(arr[self.question_num].question)
        self.knowledge_point.set_text(arr[self.question_num].knowledge_point)
        self.question_tp=arr[self.question_num].type
        for i in range(4):
            self.is_clicked[i]=0
        self.tbl.set_cell_value(0,0,'[ ]')
        self.tbl.set_cell_value(1,0,'[ ]')
        self.tbl.set_cell_value(2,0,'[ ]')
        self.tbl.set_cell_value(3,0,'[ ]')
        if self.question_tp==0:
            for i in range(4):
                self.tbl.set_cell_value(i,1,arr[self.question_num].options[i])
        else:
            for i in range(4):
                self.tbl.set_cell_value(i,0,'[ ]')
                self.tbl.set_cell_value(i,1,arr[self.question_num].options[i])
        self.question_num=to
        self.ans.set_text('')
start(main_container())