# 实验二  词法分析器
#   第一种方法 ： 单词分类信息附加在程序中的方法。预先确认单词种类识别单词。
#      四种单词种类：
#              关键字： else  if  int  return  void  while  （6个）（小写）
#              标识符
#              常数
#              专用符号：  +  -  *  /  <  <=  >  >=  ==  !=  =  ;  ,  (  )  [  ]  {  }

# 关键字表
key_word = [{'name': 'else', 'address': 0}, {'name': 'if', 'address': 1}, {'name': 'int', 'address': 2}, {'name': 'return', 'address': 3}, {'name': 'void', 'address': 4}, {'name': 'while', 'address': 5}]

# 算术运算符表
operate_word = [{'name': '+', 'address': 16}, {'name': '-', 'address': 17}, {'name': '*', 'address': 32}, {'name': '/', 'address': 33}]

# 关系运算符表
relationship_word = [{'name': '<', 'address': 0}, {'name': '<=', 'address': 1}, {'name': '==', 'address': 2}, {'name': '>', 'address': 3}, {'name': '>=', 'address': 4}, {'name': '!=', 'address': 5}]

# 分界符表
apart_word = [{'name': ',', 'address': 0}, {'name': ';', 'address': 1}, {'name': '.', 'address': 2}, {'name': '=', 'address': 3}, {'name': '(', 'address': 4}, {'name': ')', 'address': 5}, {'name': '{', 'address': 6}, {'name': '}', 'address': 7}]


# 标识符转换函数，共有0和1两个状态行
# 输入符号有下划线、大小写字母、数字符号、other
move_for_character = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],  # 第一行是状态0
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]   # 第二行是状态1
       ]

# 无符号常数转换函数  -1为error
move_for_digit = [
    [1,0,0,0,0],
    [1,2,4,-1,7],
    [3,-1,-1,-1,-1],
    [3,-1,4,-1,7],
    [6,-1,-1,5,-1],
    [6,-1,-1,-1,-1],
    [6,-1,-1,-1,7]
]

# 关系运算符转换函数  -1为error
move_for_operator = [
    [1,2,3,4,-1],
    [6,5,6,6,6],
    [-2,5,-2,-2,-2],  # 状态2如果遇到other那么就是=，归为界符
    [-1,5,-1,-1,-1],
    [6,5,6,6,6],
    [6,6,6,6,6]
]

lds = "_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

changshu = ['digit', '.', 'E', '+/-']

operator = ['<', '=', '!', '>']

entry = ''  # 输入字符串初始化


# 在标识符转换表中找到所在列
def is_in_lds(ch):  # 判断由ch字符是否在str字符串中
    i = 0
    while lds[i] != ch and i <= len(lds) - 1:
        i += 1
        if i == len(lds):
            break
    return i


# 在常数转换表中找到所在列
def is_in_changshu(ch):
    if ch >= '0' and ch <= '9':
        type = 'digit'
    elif ch == '+' or ch == '-':
        type = '+/-'
    elif ch == '.':
        type = '.'
    elif ch == 'E':
        type = 'E'
    else:
        type = ''

    i = 0
    while changshu[i] != type and i <= len(changshu) - 1:
        i += 1
        if i == len(changshu):
            break
    return i


# 在关系运算符转换表中找到所在列
def is_in_operator(ch):
    i = 0
    while operator[i] != ch and i <= len(operator) - 1:
        i += 1
        if i == len(operator):
            break
    return i


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


f = open('text2.txt', 'r')  # 打开文件，开始读取字符

f1 = open('result1.txt', 'w+')  # 打开文件，将结果录入


state = 0  # 一开始进入，初始状态为0

while True:

    ch = f.read(1)  # 每次读取一个字符
    if not ch:  # 没读到就说明已经读完，直接跳出循环
        f.close()  # 关闭文件
        break

    p = is_in_lds(ch)  # 判断输入的ch字符是否在lds字符串中。如果在，p就定位到字符所在的位置
                       # 当字符不在lds字符串中时，p就会等于字符串的长度，在move矩阵中该列就是other字符

    while not ch == 32:  # 只有当不是空格时才进入

        # 表示当前输入字符是字母，那就进入关键字和标识符分析程序
        if p >= 0 and p <= 52:
            while not ch == 32:  # 当没遇到空格时，就扫描完整个单词
                state = move_for_character[state][p]  # 更新当前的状态
                if state == 1:
                    entry = entry + ch  # 把字符ch拼接到entry上面，最终entry会是一个标识符
                    ch = f.read(1)
                    p = is_in_lds(ch)

                elif state == 2:  # 说明已经出现一个标识符，那么就要把它放到放到符号表中     标识符名 + 类型 + 地址
                    i = is_in_identifier_list(entry)
                    flag = False
                    for j in range(0, 6):  # 遍历关键字表
                        if entry == key_word[j]['name']:
                            flag = True  # 是关键字时，flag设为True

                            result = 't=1  ' + 'i=%d    ' % key_word[j]['address'] + key_word[j]['name'] + '\n'
                            print('t=1  ', 'i=%d    ' % key_word[j]['address'], key_word[j]['name'])
                            f1.write(result)
                            break
                    if not flag:  # 当flag为False时，就说明只是普通标识符，不是关键字

                        result = 't=6  ' + 'i=%d    ' % i + identifier_list[i]['name'] + '\n'
                        print('t=6  ', 'i=%d    ' % i, identifier_list[i]['name'])
                        f1.write(result)

                    state = 0  # 因为要开始识别下一个标识符了，所以把初始状态 变为0
                    entry = ''  # 因为要开始识别下一个标识符了，所以把entry清空

                    break

        # 说明当前输入字符是数字，进入常数分析程序
        elif p <= len(lds)-1:
            changshu_flag = False
            while not ch == 32:
                while not changshu_flag:
                    q = is_in_changshu(ch)
                    state = move_for_digit[state][q]
                    if state == -1:  # -1就是error,考虑！

                        # 回退一个读取的字符
                        index = f.tell()
                        f.seek(index - 1, 0)

                        changshu_flag = False
                        break  # 退出循环
                    elif state == 7:  # 7为接收状态
                        changshu_flag = True
                        break
                    else:  # 其他状态都进行读取下一个字符的操作
                        entry = entry + ch
                        ch = f.read(1)
                        q = is_in_changshu(ch)
                        continue
                break

            if changshu_flag:

                # 回退一个读取的字符
                index = f.tell()
                f.seek(index - 1, 0)

                # 退出循环就说明，遇到空格了，那么一个单词已经识别完成
                result = 't=5  ' + 'i=%s   ' % entry + entry + '\n'
                print('t=5  ', 'i=%s   ' % entry, entry)
                f1.write(result)
            entry = ''  # 要开始识别下一个单词
            state = 0  # 要开始识别下一个单词
            break

        # 说明既不是数字也不是字母，那么就进入其他单词分析程序。这里包括 关系运算符、算术运算符、分节符识别
        else:
            # 关系运算符识别
            relationship_flag = False
            while not ch == 32:
                while not relationship_flag:
                    r = is_in_operator(ch)
                    state = move_for_operator[state][r]
                    if state == 6:  # 当state=6为接收状态
                        relationship_flag = True
                        break
                    elif state == -1:  # 当state=-1时，说明error
                        entry = ''
                        state = 0
                        break
                    elif state == -2:  # 当state=-2时，说明error，但是是=号，这里归为分界符

                        result = 't=2  ' + 'i=3   ' + entry + '\n'
                        print('t=2  ', 'i=3   ', entry)
                        f1.write(result)

                        entry = ''
                        state = 0

                        # 回退一个读取的字符
                        index = f.tell()
                        f.seek(index - 1, 0)

                        break
                    else:
                        entry = entry + ch
                        ch = f.read(1)
                        continue
                break

            if relationship_flag:
                # 退出循环说明遇到空格了，一个关系运算符已经识别完成
                for i in range(0, 6):
                    if entry == relationship_word[i]['name']:
                        result = 't=4  ' + 'i=%d    ' % relationship_word[i]['address'] + entry + '\n'
                        print('t=4  ', 'i=%d    ' % relationship_word[i]['address'], entry)
                        f1.write(result)

                entry = ''
                state = 0

                # 回退一个读取的字符
                index = f.tell()
                f.seek(index - 1, 0)

                break

            # 算术运算符识别
            for i in range(len(operate_word)):
                if ch == operate_word[i]['name']:
                    result = 't=3  ' + 'i=%d    ' % operate_word[i]['address'] + ch + '\n'
                    print('t=3  ', 'i=%d    ' % operate_word[i]['address'], ch)
                    f1.write(result)
                    break

            # 分界符识别
            for i in range(len(apart_word)):
                if ch == apart_word[i]['name']:
                    result = 't=2  ' + 'i=%d      ' % apart_word[i]['address'] + ch + '\n'
                    print('t=2  ', 'i=%d      ' % apart_word[i]['address'], ch)
                    f1.write(result)
                    break

            break

f1.close()


