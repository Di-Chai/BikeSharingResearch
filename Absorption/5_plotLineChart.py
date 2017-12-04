import matplotlib
from numpy import *
import numpy as np
import matplotlib.pyplot as plt


# 画柱状图
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2-0.05, 1.03*height, '%s' % float(height))

plt.xlabel('week')
plt.ylabel('workday weekly demand')
plt.title('Demand Change')
rect = plt.bar(left = (-1,1),height = (1,1),width = 0.1,align="center")
autolabel(rect)
plt.show()