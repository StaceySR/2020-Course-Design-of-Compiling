
# 关键字表
key_word = [{'name': 'else', 'address': 0}, {'name': 'if', 'address': 1}, {'name': 'int', 'address': 2}, {'name': 'return', 'address': 3}, {'name': 'void', 'address': 4}, {'name': 'while', 'address': 5}]

# 算术运算符表
operate_word = [{'name': '+', 'address': 16}, {'name': '-', 'address': 17}, {'name': '*', 'address': 32}, {'name': '/', 'address': 33}]

# 关系运算符表
relationship_word = [{'name': '<', 'address': 0}, {'name': '<=', 'address': 1}, {'name': '==', 'address': 2}, {'name': '>', 'address': 3}, {'name': '>=', 'address': 4}, {'name': '!=', 'address': 5}]

# 分界符表
apart_word = [{'name': ',', 'address': 0}, {'name': ';', 'address': 1}, {'name': '.', 'address': 2}, {'name': '=', 'address': 3}, {'name': '(', 'address': 4}, {'name': ')', 'address': 5}, {'name': '[', 'address': 6}, {'name': ']', 'address': 7}, {'name': '{', 'address': 8}, {'name': '}', 'address': 9}]

# 转换矩阵
move = [
    [7,15,8,9,10,11,13,13,13,13,14,14,14,14,14,14,14,14,14,0,0],
    [],  # 状态1，接收状态
    [],  # 状态2，接收状态
    [],  # 状态3，接收状态
    [],  # 状态4，接收状态
    [],  # 状态5，接收状态
    [],  # 状态6，接收状态
    [7,7,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [4,4,4,12,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
    [2,2,2,12,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [0,0,0,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [4,4,4,12,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
    [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [5,15,5,5,5,5,5,5,5,5,5,5,16,5,5,5,5,5,5,5,5],
    [6,17,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
    [5,17,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,18,5],
    [6,20,6,6,6,6,19,19,6,6,6,6,6,6,6,6,6,6,6,6,6],
    [6,20,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
    [5,20,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
]

lds = ['_A', '9', '<', '=', '!', '>', '+', '-', '*', '/', ',', ';', '.', '(', ')', '[', ']', '{', '}', 'E']

entry = ''
global Token
global ch

Token = {'property': 0, 'linenum': 0}

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
    if ch >= '0' and ch <= '9':
        type = '9'
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


# 单词分析子程序
def nextToken():
    global Token
    global ch
    state = 0  # 一开始进入，初始状态为0
    entry = ''

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
                Token['linenum'] = j  # 表示该单词在相应单词表中是第几个

                result = key_word[j]['name']
                print(key_word[j]['name'], end='')
                f1.write(result)

                break
        if not flag:  # 当flag为False时，就说明只是普通标识符，不是关键字

            t = 6
            Token['property'] = t  # 记录单词所属的类别为1，
            Token['linenum'] = i  # 表示该单词在相应单词表中是第几个
            result = identifier_list[i]['name']
            print(identifier_list[i]['name'], end='')
            f1.write(result)

    elif state == 2:  # 识别为分界符
        for i in range(len(apart_word)):
            if entry == apart_word[i]['name']:

                t = 2
                Token['property'] = t  # 记录单词所属的类别为1，
                Token['linenum'] = i  # 表示该单词在相应单词表中是第几个

                result = entry
                print(entry, end='')
                f1.write(result)
                break

    elif state == 3:  # 识别为算术运算符
        for i in range(len(operate_word)):
            if entry == operate_word[i]['name']:

                t = 3
                Token['property'] = t  # 记录单词所属的类别为1，
                Token['linenum'] = i  # 表示该单词在相应单词表中是第几个

                result = entry
                print(entry, end='')
                f1.write(result)
                break

    elif state == 4:  # 识别为关系运算符
        for i in range(0, 6):
            if entry == relationship_word[i]['name']:

                t = 4
                Token['property'] = t  # 记录单词所属的类别为1，
                Token['linenum'] = i  # 表示该单词在相应单词表中是第几个

                result = entry
                print(entry, end='')
                f1.write(result)
                break

    elif state == 5:  # 识别为无符号常数
        if ch == 'E':  # 这里的‘E’必须单独考虑，不然会把E当作letter处理
            state = 17
            entry = entry + ch
            p = 19  # 'E'在转换表中的列数
            state = move[state][p]
            ch = f.read(1)
            while True:
                if not ch:
                    f.close()
                    break
                p = is_in_lds(ch)  # 计算字符在转换表中的列数
                state = move[state][p]  # 根据当前状态和输入符号，转换到下一个状态
                if state < 7:
                    break
                entry = entry + ch
                ch = f.read(1)  # 读取下一个符号
            entry = entry + ch
            ch = f.read(1)
        if state == 5:

            t = 5
            Token['property'] = t  # 记录单词所属的类别为1，
            Token['linenum'] = entry  # 表示该单词在相应单词表中是第几个

            result = entry
            print(entry, end='')
            f1.write(result)
        elif state == 6:
            result = 'error'
            print('error')
            f1.write(result)

    elif state == 6:
        result = 'error'
        print('error')
        f1.write(result)


# 对错误表达式的处理
def error(str):
    print('   ---', str)
    f1.write('   ---' + str + '\n')
    # exit()  # 因为要把所有表达式都遍历完，所有遇到错误不退出


# 匹配子程序
def match(property, value):
    result = 1

    if property == 1:  # 关键字
        result = (key_word[Token['linenum']]['address'] == value)
    elif property == 2:  # 分界符
        result = (apart_word[Token['linenum']]['address'] == value)
    elif property == 3:  # 算术运算符
        result = (operate_word[Token['linenum']]['address'] == value)
    elif property == 4:  # 关系运算符
        result = (relationship_word[Token['linenum']]['address'] == value)
    elif property == 5:  # 无符号数
        result = 1
    elif property == 6:  # 标识符
        result = (Token['linenum'] < len(identifier_list))  # 在符号表所有符号之内
    else:
        result = 0
    if result:
        nextToken()
    else:
        error('Entry Word Error!')

    return result


def exp():  # exp →term exp1
    term()
    exp1()


def exp1():  # exp1 → addop term exp1 |ε
    if Token['property'] == 3 and (Token['linenum'] == 0 or Token['linenum'] == 1):  # +或-
        addop()
        term()
        exp1()
    # else:  # 什么也不执行


def addop():  # addop → + | -
    if Token['property'] == 3 and Token['linenum'] == 0:
        match(Token['property'], 16)  # '+'
    else:
        match(Token['property'], 17)  # '-'


def term():  # term →factor term1
    factor()
    term1()


def term1():  # term1 →mulop factor term1 |ε
    if Token['property'] == 3 and (Token['linenum'] == 2 or Token['linenum'] == 3):  # *或/
        mulop()
        factor()
        term1()
    # else:  # 什么也不执行


def mulop():  # mulop → * | /
    if Token['property'] == 3 and Token['linenum'] == 2:
        match(Token['property'], 32)  # '*'
    else:
        match(Token['property'], 33)  # '/'


def factor():  # factor → (exp) | id | number
    if Token['property'] == 6:  # 标识符id
        match(Token['property'], Token['linenum'])
    elif Token['property'] == 5:  # 无符号常数number
        match(Token['property'], 0)
    elif Token['property'] == 2:  # 分界符
        match(Token['property'], 4)  # （
        exp()
        match(Token['property'], 5)  # ）
    else:
        error('Entry Word Error!')


if __name__ == '__main__':
    f = open('text2.txt', 'r')  # 打开文件，开始读取字符
    f1 = open('result2.txt', 'w+')  # 打开文件，录入结果

    ch = f.read(1)  # 读取第一个字符
    nextToken()
    exp()

    # 识别多个表达式，每个表达式占一行
    while True:
        print()
        f1.write('\n')
        # 回退
        index = f.tell()
        f.seek(index - 3, 0)
        ch = f.read(1)
        if ch != '\n':
            break
        else:
            ch = f.read(1)
            nextToken()
            exp()

    f.close()
    f1.close()


