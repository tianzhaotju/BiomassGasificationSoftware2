# MPC

#### 介绍
由于路径和import的问题，这里用了__init__.py将咱们各自的代码都封装成了一个模块，具体调用在test_*.py文件里，即每次更新代码后把接口更新在test_*.py中即可，同时保证test_*.py可以正确运行。

lzh写的代码在InputParam文件夹（模块）中，对应的调用方法和测试地方在test_InputParam.py。

zzz写的代码在PSO文件夹（模块中），对应的调用方法和测试地方在test_PSO.py中。即原来SS.py中的运行代码。
关于张至臻的代码，我把param改成PSO的一个参数了，不用从PSO.py中import的了，到时候稍微注意一下就行。

tz写的代码在Network文件夹（模块）中，对应的调用方法和测试地方在test_Network.py中。可取代原来的Interface.py。
关于tz的代码，由于运行路径的不一致，里面一些关于文件路径的代码有所更改，如Model.py中的383行和411行。
还有那个Net.py和LSTM.py，我这里是命令行运行的，可能不如pycharm好使，运行torch时它要求torch.load()的运行路径下必须有Net.py和LSTM.py，不然就报错，所以我就先把Net.py和LSTM.py复制到这个src的根目录下了。