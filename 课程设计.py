'''

 1.	statmt → id=exp
 2.	exp → exp addop term
 3.	exp → term
 4.	addop → +
 5.	addop → -
 6.	term → term mulop factor
 7.	term → factor
 8.	mulop → *
 9.	mulop → /
10.	factor → (exp)
11.	factor → id
12.	factor → number

'''
MAX_ID_NUM = 1000  # 符号表最大行数
KEY_NUM = 8  # 关键字最大数
DELIM_NUM = 11  # 分界符最大数
OPER_NUM = 4  # 算术运算符最大数
RELOP_NUM = 6  # 关系算符最大数

STATES_NUM = 27  # 定义状态数
NON_TERMIAT_NUM = 5  # 定义非终结符数
TERMIAT_NUM = 10  # 定义终结符数
MAX_STACK = 20  # 定义栈最大空间
state_stack = [0 for i in range(MAX_STACK)]  # 状态栈
attribs_stack = [[0, 0] for i in range(MAX_STACK)]  # 属性值栈  需要同时记录两个值如，等addop  1、linenum=16，代表+  2、number （主要是为了给number记录）



# 关键字表
key_word = [{'name': 'break', 'address': 0}, {'name': 'do', 'address': 1}, {'name': 'else', 'address': 2}, {'name': 'float', 'address': 3},  {'name': 'if', 'address': 4}, {'name': 'int', 'address': 5}, {'name': 'void', 'address': 6}, {'name': 'while', 'address': 7}]

# 算术运算符表
operate_word = [{'name': '+', 'address': 16}, {'name': '-', 'address': 17}, {'name': '*', 'address': 32}, {'name': '/', 'address': 33}]

# 关系运算符表
relationship_word = [{'name': '<', 'address': 0}, {'name': '<=', 'address': 1}, {'name': '==', 'address': 2}, {'name': '>', 'address': 3}, {'name': '>=', 'address': 4}, {'name': '!=', 'address': 5}]

# 分界符表
apart_word = [{'name': ',', 'address': 0}, {'name': ';', 'address': 1}, {'name': '.', 'address': 2}, {'name': '=', 'address': 3}, {'name': '(', 'address': 4}, {'name': ')', 'address': 5}, {'name': '[', 'address': 6}, {'name': ']', 'address': 7}, {'name': '{', 'address': 8}, {'name': '}', 'address': 9}, {'name': '$', 'address': 10}]

# 转换矩阵
move = [
    [7,15,8,9,10,11,13,13,13,13,14,14,14,14,14,14,14,14,14,14,0,0],
    [],  # 状态1，接收状态
    [],  # 状态2，接收状态
    [],  # 状态3，接收状态
    [],  # 状态4，接收状态
    [],  # 状态5，接收状态
    [],  # 状态6，接收状态
    [7,7,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [4,4,4,12,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
    [2,2,2,12,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [0,0,0,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [4,4,4,12,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
    [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [5,15,5,5,5,5,5,5,5,5,5,5,16,5,5,5,5,5,5,5,5,5],
    [6,17,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
    [5,17,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,18,5],
    [6,20,6,6,6,6,19,19,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
    [6,20,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
    [5,20,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
]

lds = ['_A', 'digit', '<', '=', '!', '>', '+', '-', '*', '/', ',', ';', '.', '(', ')', '[', ']', '{', '}', '$', 'E']

global entry
entry = ''
global Token
Token = {'property': 0, 'linenum': 0, 'number': 0}
# property记录单词所属的类别为1，linenume表示该单词在相应单词表中是第几个，number数值数据仍以字符串形式存放
global ch
global top


# ACTION表
ACTION = [
  #  +, -, *, /, (, ), =, id, num, $
    ['','','','','','','','s1','',''],               # 0
    ['','','','','','','s2','','',''],               # 1
    ['','','','','s6','','','s7','s8',''],           # 2
    ['s10','s11','','','','','','','','acc'],        # 3
    ['r3','r3','s13','s14','','','','','','r3'],     # 4
    ['r7','r7','r7','r7','','','','','','r7'],       # 5
    ['','','','','s18','','','s19','s20',''],        # 6
    ['r11','r11','r11','r11','','','','','','r11'],  # 7
    ['r12','r12','r12','r12','','','','','','r12'],  # 8
    ['','','','','s6','','','s7','s8',''],           # 9
    ['','','','','r4','','','r4','r4',''],           # 10
    ['','','','','r5','','','r5','r5',''],           # 11
    ['','','','','s6','','','s7','s8',''],           # 12
    ['','','','','r8','','','r8','r8',''],           # 13
    ['','','','','r9','','','r9','r9',''],           # 14
    ['s10','s11','','','','s24','','','',''],        # 15
    ['r3','r3','s13','s14','','r3','','','',''],     # 16
    ['r7','r7','r7','r7','','r7','','','',''],       # 17
    ['','','','','s18','','','s19','s20',''],        # 18
    ['r11','r11','r11','r11','','r11','','','',''],  # 19
    ['r12','r12','r12','r12','','r12','','','',''],  # 20
    ['r2','r2','s13','s14','','','','','','r2'],     # 21
    ['r6','r6','r6','r6','','','','','','r6'],       # 22
    ['','','','','s18','','','s19','s20',''],        # 23
    ['r10','r10','r10','r10','','','','','','r10'],  # 24
    ['','','','','s18','','','s19','s20',''],        # 25
    ['s10','s11','','','','s29','','','',''],        # 26
    ['r2','r2','s13','s14','','r2','','','',''],     # 27
    ['r6','r6','r6','r6','','r6','','','',''],       # 28
    ['r10','r10','r10','r10','','r10','','','','']   # 29
]


# GOTO表
GOTO = [
 # exp,term,factor,mulop,addop
    ['','','','',''],   #0
    ['','','','',''],   #1
    [3,4,5,'',''],      #2
    ['','','','',9],    #3
    ['','','',12,''],   #4
    ['','','','',''],   #5
    [15,16,17,'',''],   #6
    ['','','','',''],   #7
    ['','','','',''],   #8
    ['',21,5,'',''],    #9
    ['','','','',''],   #10
    ['','','','',''],   #11
    ['','',22,'',''],   #12
    ['','','','',''],   #13
    ['','','','',''],   #14
    ['','','','',23],   #15
    ['','','',25,''],   #16
    ['','','','',''],   #17
    [26,16,17,'',''],   #18
    ['','','','',''],   #19
    ['','','','',''],   #20
    ['','','',12,''],   #21
    ['','','','',''],   #22
    ['',27,17,'',''],   #23
    ['','','','',''],   #24
    ['','',28,'',''],   #25
    ['','','','',23],   #26
    ['','','',25,''],   #27
    ['','','','',''],   #28
    ['','','','','']    #29
]


identifier_list = []  # 符号表


# 检验是否标识符是否在符号表中, 如果不在则添加，在就直接返回标识符所在列表位置
def is_in_identifier_list(name):
    if len(identifier_list) == 0:
        identifier = {'name': name, 'address': 0}  # 标识符类型先赋为空
        identifier_list.append(identifier)  # 把标识符添加到符号表最末端
        return 0
    for i in range(len(identifier_list)):  # 遍历符号表列表
        if identifier_list[i]['name'] == name:
            return i
        i += 1
    # 运行到这一步，说明在符号表中没有这个标识符，那么就在符号表最后添加这个标识符
    identifier = {'name': name, 'address': i}
    identifier_list.append(identifier)
    return i


def is_in_lds(ch):
    global state
    if state == 17 and ch == 'E':
        type = 'E'
    elif ch >= '0' and ch <= '9':
        type = 'digit'
    elif ch >= 'A' and ch <= 'Z' or ch >= 'a' and ch <= 'z' or ch == '_':
        type = '_A'
    else:
        type = ch
    i = 0
    while lds[i] != type and i <= len(lds) - 1:
        i += 1
        if i == len(lds):
            break
    return i


global state
state = 0  # 一开始进入，初始状态为0


# 单词分析子程序
def nextToken():
    global Token
    global ch
    global state
    state = 0
    global entry
    entry = ''
    Token['property'] = 0
    while True:
        p = is_in_lds(ch)  # 计算字符在转换表中的列数
        state = move[state][p]  # 根据当前状态和输入符号，转换到下一个状态
        if state < 7:  # 0-6为接收状态
            break
        entry = entry + ch
        ch = f.read(1)  # 读取下一个符号
    if state == 0:
        ch = f.read(1)
    elif state == 1:  # 识别为标识符，里面还要进行关键字查询
        i = is_in_identifier_list(entry)
        flag = False
        for j in range(0, 6):  # 遍历关键字表
            if entry == key_word[j]['name']:
                flag = True  # 是关键字时，flag设为True
                t = 1
                Token['property'] = t  # 记录单词所属的类别为1，
                Token['linenum'] = key_word[j]['address']
                break
        if not flag:  # 当flag为False时，就说明只是普通标识符，不是关键字
            t = 6
            Token['property'] = t  # 记录单词所属的类别为6，
            Token['linenum'] = i  # 表示该单词在相应单词表中是第几个
    elif state == 2:  # 识别为分界符
        for i in range(len(apart_word)):
            if entry == apart_word[i]['name']:
                t = 2
                Token['property'] = t  # 记录单词所属的类别为2，
                Token['linenum'] = apart_word[i]['address']
                break
    elif state == 3:  # 识别为算术运算符
        for i in range(len(operate_word)):
            if entry == operate_word[i]['name']:
                t = 3
                Token['property'] = t  # 记录单词所属的类别为3，
                Token['linenum'] = operate_word[i]['address']
                break
    elif state == 4:  # 识别为关系运算符
        for i in range(0, 6):
            if entry == relationship_word[i]['name']:
                t = 4
                Token['property'] = t  # 记录单词所属的类别为4，
                Token['linenum'] = relationship_word[i]['address']
                break
    elif state == 5:  # 识别为无符号常数
        t = 5
        Token['property'] = t  # 记录单词所属的类别为5，
        Token['linenum'] = entry  # 表示该单词在相应单词表中是第几个
        Token['number'] = entry
    elif state == 6:  # number出错,在LR函数中会检测到出错，所以这里可以不用处理
        t = -1
        Token['property'] = t
        Token['linenum'] = None


global count  # t0, t1..
count = 0


def produces(p):
    global top
    global count
    if p == 1:
        print("归约式：statmt → id = exp ")
        print("三地址代码：{} = {}".format(attribs_stack[1][1], attribs_stack[top][1]))  # 把最终结果输出
        f1.write("归约式：statmt → id = exp \n")
        f1.write("三地址代码：{} = {}".format(attribs_stack[1][1], attribs_stack[top][1]) + '\n')
        count = 0
        top = top - 1
        column = 0
    elif p == 2:
        print("归约式：exp → exp addop term ")
        f1.write("归约式：exp → exp addop term \n")
        # 在计算属性之前，首先要判断addop是 + 还是 -
        if attribs_stack[top-1][0] == 16:  # +
            attribs_stack[top-2][1] = str(attribs_stack[top-2][1]) + ' + ' + str(attribs_stack[top][1])
            print('三地址代码：t{} = {}'.format(count, attribs_stack[top-2][1]))
            f1.write('三地址代码：t{} = {}'.format(count, attribs_stack[top-2][1]) + '\n')
            attribs_stack[top - 2][1] = 't%s' % count
            count += 1
        else:  # -
            attribs_stack[top-2][1] = str(attribs_stack[top-2][1]) + ' - ' + str(attribs_stack[top][1])
            print('三地址代码：t{} = {}'.format(count, attribs_stack[top-2][1]))
            f1.write('三地址代码：t{} = {}'.format(count, attribs_stack[top-2][1]) + '\n')
            attribs_stack[top - 2][1] = 't%s' % count
            count += 1
        top = top - 3
        column = 0
    elif p == 3:
        print("归约式：exp → term ")
        f1.write("归约式：exp → term \n")
        attribs_stack[top][1] = str(attribs_stack[top][1])
        print('三地址代码：t{} = {}'.format(count, attribs_stack[top][1]))
        f1.write('三地址代码：t{} = {}'.format(count, attribs_stack[top][1]) + '\n')
        attribs_stack[top][1] = 't%s' % count
        count += 1
        top = top - 1
        column = 0
    elif p == 4:
        print("归约式：addop → + ")
        f1.write("归约式：addop → + \n")
        top = top - 1
        column = 4
    elif p == 5:
        print("归约式：addop → - ")
        f1.write("归约式：addop → - \n")
        top = top - 1
        column = 4
    elif p == 6:
        print("归约式：term → term mulop factor ")
        f1.write("归约式：term → term mulop factor \n")
        # 在计算属性之前，首先要判断mulop是 * 还是 /
        if attribs_stack[top-1][0] == 32:  # *
            attribs_stack[top-2][1] = str(attribs_stack[top-2][1]) + ' * ' + str(attribs_stack[top][1])
            print('三地址代码：t{} = {}'.format(count, attribs_stack[top-2][1]))
            f1.write('三地址代码：t{} = {}'.format(count, attribs_stack[top-2][1]) + '\n')
            attribs_stack[top - 2][1] = 't%s' % count
            count += 1
        else:  # /
            attribs_stack[top-2][1] = str(attribs_stack[top-2][1]) + ' / ' + str(attribs_stack[top][1])
            print('三地址代码：t{} = {}'.format(count, attribs_stack[top-2][1]))
            f1.write('三地址代码：t{} = {}'.format(count, attribs_stack[top-2][1]) + '\n')
            attribs_stack[top - 2][1] = 't%s' % count
            count += 1
        top = top - 3
        column = 1
    elif p == 7:
        print("归约式：term → factor ")
        f1.write("归约式：term → factor \n")
        attribs_stack[top][1] = str(attribs_stack[top][1])
        print('三地址代码：t{} = {}'.format(count, attribs_stack[top][1]))
        f1.write('三地址代码：t{} = {}'.format(count, attribs_stack[top][1]) + '\n')
        attribs_stack[top][1] = 't%s' % count
        count += 1
        top = top - 1
        column = 1
    elif p == 8:
        print("归约式：mulop → * ")
        f1.write("归约式：mulop → * \n")
        top = top - 1
        column = 3
    elif p == 9:
        print("归约式：mulop → / ")
        f1.write("归约式：mulop → /\n")
        top = top - 1
        column = 3
    elif p == 10:
        print("归约式：factor → (exp) ")
        f1.write("归约式：factor → (exp)\n")
        attribs_stack[top-2][1] = str(attribs_stack[top-1][1])
        print('三地址代码：t{} = {}'.format(count, attribs_stack[top-2][1]))
        f1.write('三地址代码：t{} = {}'.format(count, attribs_stack[top-2][1]) + '\n')
        attribs_stack[top-2][1] = 't%s' % count
        count += 1
        top = top - 3
        column = 2
    elif p == 11:
        print("归约式：factor → id ")
        f1.write("归约式：factor → id\n")
        attribs_stack[top][1] = str(attribs_stack[top][1])
        print('三地址代码：t{} = {}'.format(count, attribs_stack[top][1]))
        f1.write('三地址代码：t{} = {}'.format(count, attribs_stack[top][1]) + '\n')
        attribs_stack[top][1] = 't%s' % count
        count += 1
        top = top - 1
        column = 2
    elif p == 12:
        print("归约式：factor → num ")
        f1.write("归约式：factor → num\n")
        attribs_stack[top][1] = str(attribs_stack[top][1])
        print('三地址代码：t{} = {}'.format(count, attribs_stack[top][1]))
        f1.write('三地址代码：t{} = {}'.format(count, attribs_stack[top][1]) + '\n')
        attribs_stack[top][1] = 't%s' % count
        count += 1
        top = top - 1
        column = 2
    else:
        column = NON_TERMIAT_NUM  # NON_TERMIAT_NUM定义非终结符数
    return column


def LR1():
    global top
    top = 0
    column = STATES_NUM
    state_stack[top] = 0  # 状态0入栈
    while True:
        if Token['property'] == 2:  # 分界符
            if Token['linenum'] == 4:  # （
                column = 4
            elif Token['linenum'] == 5:  # ）
                column = 5
            elif Token['linenum'] == 3:  # =
                column = 6
            else:  # $
                column = 9
        elif Token['property'] == 3:  # 算术运算符
            if Token['linenum'] == 16:  # +
                column = 0
            elif Token['linenum'] == 17:  # -
                column = 1
            elif Token['linenum'] == 32:  # *
                column = 2
            elif Token['linenum'] == 33:  # /
                column = 3
        elif Token['property'] == 6:  # id
            column = 7
        elif Token['property'] == 5:  # num
            column = 8

        if column >= TERMIAT_NUM:
            return 0

        # 根据状态栈顶状态和输入符号 ，去ACTION表中查找，如果是s开头，那么就代表是移进
        if ACTION[state_stack[top]][column] == '':  # 报错
            return 0
        if ACTION[state_stack[top]][column][0] == 's':  # 移进
            # s后面的数字代表移进之后状态栈顶要添加的状态值
            state = ACTION[state_stack[top]][column][1:]
            top = top + 1
            state_stack[top] = int(state)

            # 属性值进栈
            if Token['property'] == 1:  # 关键字标识符
                attribs_stack[top][1] = entry
                attribs_stack[top][0] = Token['linenum']
            elif Token['property'] == 2:  # 分界符
                attribs_stack[top][1] = entry
                attribs_stack[top][0] = Token['linenum']
            elif Token['property'] == 3:  # 算术运算符
                attribs_stack[top][1] = entry
                attribs_stack[top][0] = Token['linenum']
            elif Token['property'] == 4:  # 关系运算符
                attribs_stack[top][1] = entry
                attribs_stack[top][0] = Token['linenum']
            elif Token['property'] == 5:  # num
                attribs_stack[top][1] = Token['number']  # 如果是number只要记录number值就行
                attribs_stack[top][0] = Token['linenum']
            elif Token['property'] == 6:  # 普通标识符
                attribs_stack[top][1] = entry
                attribs_stack[top][0] = Token['linenum']
            else:  # state=6时
                return 0  # 报错

            nextToken()  # 继续取下一个字符

        # 据状态栈顶状态和输入符号 ，去ACTION表中查找，如果是r开头，那么就代表是归约
        elif ACTION[state_stack[top]][column][0] == 'r':  # 归约
            # r后面的数字代表是按哪一个式子进行归约
            p = int(ACTION[state_stack[top]][column][1:])
            # 进入归约子程序produce
            column = produces(p)
            # 归约完成之后，要在状态栈中添加新的状态，从goto表按当前栈顶状态值和归约的非终结符查找
            state = GOTO[state_stack[top]][column]
            if state == '':
                return 0
            top = top + 1
            state_stack[top] = int(state)

        elif ACTION[state_stack[top]][column][0] == 'a':  # acc接受
            column = produces(1)
            return 1


global index


if __name__ == '__main__':
    global index
    index = 0
    # 打开输入文件
    with open('explist.txt', 'r') as f:
        f1 = open('text2.txt', 'w')  # 输出文件
        # 分析开始
        ch = f.read(1)
        entry = ''
        while ch:
            nextToken()  # 分析出一个单词
            while ch and entry == '':
                nextToken()
            if LR1():  # return 1
                print("---------------------{}号语句Right！\n\n".format(index+1))
                f1.write("---------------------{}号语句Right！\n\n".format(index+1))
                index += 1
            else:  # return 0
                count = 0  # t*(count为*数字)，清零
                print("---------------------{}号语句Error！\n\n".format(index+1))
                f1.write("---------------------{}号语句Error！\n\n".format(index+1))
                while ch and ch != '$' and ch != '\n':
                    ch = f.read(1)
                index += 1
            if ch:
                ch = f.read(1)

    f.close()
    f1.close()




