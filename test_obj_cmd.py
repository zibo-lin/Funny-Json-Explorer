import json  
import os
import cmd

class FunnyJsonExplorer:
    def __init__(self):
        pass
    def show(self,container):
        container.draw([],True)
        print()
        pass
    def _load(self,name,level,data):
        container = Container('',name,level)
        if isinstance(data, dict):
            for key, value in data.items():
                sub_container = self._load(key,level+1,value)
                container.sub.append(sub_container)
        else:
            sub_leaf = Leaf(data)
            container.sub.append(sub_leaf)
        return container

class Container:
    def __init__(self,icon='',name=None,level=None): # ♢ ♦ ♤ ♠
        self.icon = icon
        self.name = name
        self.level = level
        self.sub = []
    def draw(self,indent,is_final):
        indent_ = indent.copy()
        if not self.name:
            print('.',end='')
        else:
            print()
            for i in range(self.level-1):
                print(indent_[i], end='')
            if is_final:
                print('└──', end='')
            else:
                print('├──', end='')
            print(f'{self.icon}{self.name}',end='') 
            c = '    ' if is_final else '│   '
            indent_.append(c)
            # print(f' so indent is {indent_}',end='')
        for i in range(len(self.sub)):
            self.sub[i].draw(indent_,i==len(self.sub)-1)

class Leaf:
    def __init__(self,name=None):
        self.name = name
    def draw(self,indent,is_final):
        if self.name:
            print(f' : {self.name}',end='')

class MyCmd(cmd.Cmd):  
    prompt = 'fje> '  
      
    def do_fje(self, arg):   
        if arg:  
            # 读取JSON文件  
            with open(arg, 'rb') as file:  
                data = json.load(file)  
            # 处理JSON文件
            fje = FunnyJsonExplorer()
            container = fje._load(None,0,data)
            fje.show(container) 
    def do_quit(self, arg):   
        return True  
    def default(self, line):  
        print(f'Unknown command: {line}')  

if __name__ == '__main__':  
    # 更改运行路径
    directory_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(directory_path)
    MyCmd().cmdloop()