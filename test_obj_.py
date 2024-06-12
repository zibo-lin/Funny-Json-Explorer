import json  
import os

class FunnyJsonExplorer:
    def __init__(self):
        pass
    def show(self,container):
        container.draw([],True,0)
        pass
    def _load(self,name,level,data):
        container = Container('',name,level)
        if isinstance(data, dict):
            for key, value in data.items():
                sub_container = self._load(key,level+1,value)
                container.sub.append(sub_container)
        else:
            sub_leaf = Leaf(data)
            container.sub.append(None)
            container.sub.append(sub_leaf)
        return container

class Container:
    def __init__(self,icon='',name='',level=0):
        self.icon = icon
        self.name = name
        self.level = level
        self.sub = []
        self.full_len = 44
    def draw(self,indent,is_final,front_len):
        indent_ = indent.copy()
        if not self.name:
            # print('.',end='')
            pass
        else:
            print()
            for i in range(self.level-1):
                print(indent_[i], end='')
            # if is_final:
            #     print('└─ ', end='')
            # else:
            #     print('├─ ', end='')
            print('├─ ', end='')
            print(f'{self.icon}{self.name}',end='') 
            front_len = self.level*3
            rest_len = self.full_len - front_len
            rest_len -= len(self.name)
            if self.sub[0]:
                print(' '+'─'*(rest_len-2)+'┤',end='')
            # c = '    ' if is_final else '│   '
            c = '│  '
            indent_.append(c)
            # print(f' so indent is {indent_}',end='')
        for i in range(len(self.sub)):
            if self.sub[i]:
                self.sub[i].draw(indent_,i==len(self.sub)-1,front_len+len(self.name))

class Leaf:
    def __init__(self,name=None):
        self.name = name
        self.full_len = 44
    def draw(self,indent,is_final,front_len):
        rest_len = self.full_len - front_len
        if self.name:
            rest_len -= len(self.name)+3
            print(f' : {self.name}',end='')
        print(' '+'─'*(rest_len-2)+'┤',end='')  # ┌ ┐ └ ┘┴ ┤; ┠ ┨┯ ┷┏ ┓┗ ┛

def main():
    # 更改运行路径
    directory_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(directory_path)
    # 读取JSON文件  
    with open('./test/test_.json', 'rb') as file:  
        data = json.load(file)  

    # print(type(data))
    fje = FunnyJsonExplorer()
    container = fje._load('',0,data)
    fje.show(container)
    return 

if __name__ == "__main__":
    main()