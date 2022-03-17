# f = open('text2.txt', 'r')
#
# while True:
#     ch = f.read(1)
#     print('1:', ch)
#     if not ch:
#         f.close()
#         break
#     # 回退
#     index = f.tell()
#     f.seek(index - 1, 0)
#     ch = f.read(1)
#     print('2:', ch)


