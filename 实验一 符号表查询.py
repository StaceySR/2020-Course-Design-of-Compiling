# ----------实验一：查填符号表-----------

# 转换函数，共有0和1两个状态行
# 输入符号有下划线、大小写字母、数字符号、other
move = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],  # 第一行是状态0
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]   # 第二行是状态1
       ]

lds = "_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
entry = ''  # 输入字符串初始化


def is_in_lds(ch):  # 判断由ch字符是否在str字符串中
    i = 0
    while lds[i] != ch and i <= len(lds) - 1:
        i += 1
        if i == len(lds):
            break
    return i


identifier_list = []  # 符号表


# 检验是否标识符是否在符号表中, 如果不在则添加，在就直接返回标识符所在列表位置
def is_in_identifier_list(name):
    if len(identifier_list) == 0:
        identifier = {'name': name, 'type': '', 'address': 0}  # 标识符类型先赋为空
        identifier_list.append(identifier)  # 把标识符添加到符号表最末端
        return 0
    for i in range(len(identifier_list)):  # 遍历符号表列表
        if identifier_list[i]['name'] == name:
            return i
        i += 1
    # 运行到这一步，说明在符号表中没有这个标识符，那么就在符号表最后添加这个标识符
    identifier = {'name': name, 'type': '', 'address': i}
    identifier_list.append(identifier)
    return i


f = open('text2.txt', 'r')  # 打开文件，开始读取字符

state = 0  # 一开始进入，初始状态为0
while True:
    ch = f.read(1)  # 每次读取一个字符
    if not ch:  # 没读到就说明已经读完，直接跳出循环
        f.close()  # 关闭文件
        break
    p = is_in_lds(ch)  # 判断输入的ch字符是否在lds字符串中。如果在，p就定位到字符所在的位置
                       # 当字符不在lds字符串中时，p就会等于字符串的长度，在move矩阵中该列就是other字符
    state = move[state][p]  # 更新当前的状态
    if state == 1:
        entry = entry + ch  # 把字符ch拼接到entry上面，最终entry会是一个标识符
        continue     # 继续读入字符
    elif state == 2:  # 说明已经出现一个标识符，那么就要把它放到放到符号表中     标识符名 + 类型 + 地址
        i = is_in_identifier_list(entry)
        # print('标识符：', entry, '所在符号表位置：', i)  # 每遇到一个标识符，就输出
        state = 0   # 因为要开始识别下一个标识符了，所以把初始状态 变为0
        entry = ''  # 因为要开始识别下一个标识符了，所以把entry清空
    else:  # 说明状态仍为0，那就什么都不做，继续读取下一个字符
        continue


# 跳出循环时，说明所有字符text2.txt文件中的所有字符已经遍历完毕
# 打印符号表，只输出标识符名和标识符地址
print('-------------------符号表-----------------\n')
f1 = open('text1.txt', 'w+')  # 输出结果到text1.txt文件
for i in range(len(identifier_list)):
    name = identifier_list[i]['name']
    address = identifier_list[i]['address']
    result = '标识符名：%s  ' % name +  '标识符地址：%d  ' % address
    f1.write(result + '\n')
    print(result)  # 输出结果到控制台

f1.close()  # 关闭text1.txt文件



