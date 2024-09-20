# a = {1: 1.1, 2: 2.2, 3: 3}
#
# print(a)
# print(a.keys())
# print(a.items())
# str1 = str(a)
# with open(r'结果.txt', 'w') as f:
#     f.write(str1)
#     f.write('\r\t')

import pickle


# with open('GridModesAdjacentRes.pkl', 'rb') as files:
#     GridM2 = pickle.load(files)
# print(GridM2[(96,283)])


# for self in range(16):
#     self_modes = [0, 0, 0, 0]
#     for i in range(len(self_modes)):
#         if self - 2 ** (len(self_modes)-1 - i) >= 0:
#             self_modes[i] = 1
#             self = self - 2 ** (len(self_modes)-1 - i)
#     print(self_modes)
