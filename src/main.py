from Network import Model
from PSO import optimize
from InputParam import InputParam
import numpy as np
import time

data = np.loadtxt('./data/data.csv', delimiter=',', skiprows=2)[:, 1: 7]
model = Model(stride=30)
param = InputParam()

best_x = [[28.12421607,14.41792793],
[74.20071455, 9.92461491],
[58.43944117, 11.0825983 ],
[69.17058085, 10.75863371],
[36.35079316, 11.28547075],
[57.59862793, 10.92375781],
[27.67301199, 14.30238826],
[75.87876121, 13.22701089],
[100.0, 16.10638031],
[100.0, 13.78599625]]

best_y = 26.45409999049893

# 调用optimize
#best_x, best_y = optimize(20, data, 2, model, param)

print('best_x = ', best_x)
print('best_y = ', best_y)

model.stride = 10
predict_y = model.predict_Net(best_x)
print(predict_y)