import remi.gui as gui
from remi import start, App
import random
total_cnt=0
correct_cnt=0
class question:
    def __init__(self, question,options, answer,knowledge_point):
        self.type=0
        self.question = question
        self.options = options
        self.answers =[]
        print("answer="+answer)
        for i in answer:
            if i=='A':
                self.answers.append(0)
            elif i=='B':
                self.answers.append(1)
            elif i=='C':
                self.answers.append(2)
            elif i=='D':
                self.answers.append(3)
            elif i=='Y':
                self.type=-1
                self.answers.append(0)
            elif i=='N':
                self.type=-1
                self.answers.append(1)
        print("ans="+str(self.answers));
        self.knowledge_point = knowledge_point
        self.cnt = 0
        if len(self.answers)!=1:
            self.type=1
        if(self.type==-1):
            self.options.append("正确")
            self.options.append("错误")
            self.options.append("不确定")
            self.options.append("不知道")
    def judege(self,options):
        global correct_cnt
        global total_cnt
        total_cnt+=1
        print(self.answers);
        if options == self.answers:
            self.cnt += 1
            correct_cnt+=1
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
    knowledge_point=''
    ans=''
    options=[]
    qes=''
    for i in tiku:
        if i=='@':
            if flag==2:
                knowledge_point=tmp
            else:
                answers=tmp
            flag=0
            arr.append(question(qes,options,ans,knowledge_point))
            knowledge_point=''
            ans=''
            options=[]
            qes=''
            tmp=""
        elif i=='#':
            if flag == 0:
                qes=tmp
                flag=1
                tmp=""
            else:
                options.append(tmp)
                tmp=""
        elif i=='%':
            if flag == 0:
                qes=tmp
            else:
                options.append(tmp)
            tmp=""
        elif i=='$':
            ans=tmp
            tmp=""
            flag=2;
        else:
            tmp+=i
    return arr
arr = init_tiku()
fst=arr[1]
def gettp(a):
    if arr[a].type==1:
        return "多选题："
    elif arr[a].type==0:
        return "单选题："
    elif arr[a].type==-1:
        return "判断题："
def correct_rt():
    global correct_cnt
    global total_cnt
    if total_cnt==0:
        return 0
    return correct_cnt/total_cnt
class main_container(App):
    question_num=1
    is_clicked=[-1,-1,-1,-1]
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
        self.question=gui.Label(gettp(1)+fst.question,width=700,height=100,style={'margin':'0px auto', 'padding':'0px','font-size':'30px'})
        self.tbl=gui.Table.new_from_list([
                                   (['[ ]'+fst.options[0]]),
                                   (['[ ]'+ fst.options[1]]),
                                   (['[ ]'+ fst.options[2]]),
                                   (['[ ]'+ fst.options[3]]),] ,width=600, height=200, margin='10px',fill_title=False)
        self.tbl.on_table_row_click.do(self.on_table_row_click)
        self.correct_rate=gui.Label("当前正确率为："+str(correct_rt()),width=200,height=50)
        mainContainer.append(self.question)
        mainContainer.append(self.tbl)
        mainContainer.append(self.btn)
        mainContainer.append(self.nxt)
        mainContainer.append(self.ans)
        mainContainer.append(self.knowledge_point)
        mainContainer.append(self.correct_rate)
        return mainContainer
    def on_table_row_click(self, row, col,item):
        for i in range(4):
            if self.is_clicked[i]==1 and arr[self.question_num].type!=1:
                self.is_clicked[i]=-1
            if item.get_text().find(arr[self.question_num].options[i])!=-1:
                self.is_clicked[i]=-self.is_clicked[i];
        self.tbl.empty()
        tmp=[]
        for i in range(4):
            if self.is_clicked[i]==1:
                tmp.append(["[X]  "+arr[self.question_num].options[i]])
            else:
                tmp.append(["[ ]  "+arr[self.question_num].options[i]])
        self.tbl.append_from_list(tmp);
    def submit(self, widget):
        tans=[]
        for i in range(4):
            if self.is_clicked[i]==1:
                tans.append(i)
        print(tans);
        if fst.judege(tans):
            self.ans.set_text('正确')
        else:
            self.ans.set_text('错误')
        self.correct_rate.set_text("当前正确率为："+str(correct_rt()))
    def to_next(self, widget):
        to=1
        while True:
            to=random.randint(0,len(arr)-1)
            if arr[to].cnt>=4:
                continue
            else: 
                break
        self.question_num=to
        self.question.set_text(gettp(self.question_num)+arr[self.question_num].question)
        self.knowledge_point.set_text(arr[self.question_num].knowledge_point)
        self.question_tp=arr[self.question_num].type
        for i in range(4):
            self.is_clicked[i]=-1
        tmp=[]
        for i in range(4):
            tmp.append(["[ ]  "+arr[self.question_num].options[i]])
        self.tbl.empty()
        self.tbl.append_from_list(tmp);
        self.ans.set_text('')
        print("question_num="+str(self.question_num))
start(main_container)