import numpy as np
from wzk import new_fig

#
# def iterate(x):
#     if x % 2 == 0:
#         return x // 2
#     else:
#         return 3 * x + 1
#
#
# x_list = []
# for x in range(1, 10):
#     xi_list = [x]
#     for j in range(10):
#         if xi_list[-1] == 1:
#             break
#         else:
#             xi_list.append(iterate(xi_list[-1]))
#     x_list.append(xi_list)
#
#
#
# fig, ax = new_fig()
# # ax.set_ylim(0, 100)
#
# for x in x_list:
#     if x[-1] == 1:
#         ax.plot(x, color='black')



x = [1]
for i in range(0, 10):
    x2