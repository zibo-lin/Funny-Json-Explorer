import json  
import os
import cmd

class FJE_factory:
    @staticmethod
    def create_FJE(fje_type):
        if fje_type=="tree":
            fje = FunnyJsonExplorer_tree()
        elif fje_type=="rectangle":
            fje = FunnyJsonExplorer_rectangle()
        return fje

class FunnyJsonExplorer:
    def __init__(self):
        pass
    def show(self):
        pass
    def _load(self):
        pass
class Container:
    def __init__(self,icon=[' ',' '],name='',level=0):
        self.icon = icon
        self.name = name
        self.level = level
        self.sub = []
    def draw(self):
        pass
class Leaf:
    def __init__(self,name=None):
        self.name = name if name else ''
    def draw(self):
        pass

class FunnyJsonExplorer_tree(FunnyJsonExplorer):
    def show(self,container):
        container.draw([],True)
        print()
        pass
    def _load(self,name,level,data,icon):
        container = Container_tree(icon,name,level)
        if isinstance(data, dict):
            for key, value in data.items():
                sub_container = self._load(key,level+1,value,icon)
                container.sub.append(sub_container)
        else:
            sub_leaf = Leaf_tree(data)
            container.sub.append(None)
            container.sub.append(sub_leaf)
        return container
class Container_tree(Container):
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
            if not self.sub[0]:
                print(f'{self.icon[1]}{self.name}',end='') 
            else:
                print(f'{self.icon[0]}{self.name}',end='') 
            c = '    ' if is_final else '│   '
            indent_.append(c)
            # print(f' so indent is {indent_}',end='')
        for i in range(len(self.sub)):
            if self.sub[i]:
                self.sub[i].draw(indent_,i==len(self.sub)-1)
class Leaf_tree(Leaf):
    def draw(self,indent,is_final):
        if self.name:
            print(f' : {self.name}',end='')

class FunnyJsonExplorer_rectangle(FunnyJsonExplorer):
    def show(self,container):
        full_len = container.check()
        print("┌","─"*(full_len-1),"┐",sep='',end='')
        container.draw([],True,0,full_len)
        print()
        print("└","─"*(full_len-1),"┘",sep='') # ┌ ┐ └ ┘
        pass
    def _load(self,name,level,data,icon):
        container = Container_rectangle(icon,name,level)
        if isinstance(data, dict):
            for key, value in data.items():
                sub_container = self._load(key,level+1,value,icon)
                container.sub.append(sub_container)
        else:
            sub_leaf = Leaf_rectangle(data)
            container.sub.append(None)
            container.sub.append(sub_leaf)
        return container
class Container_rectangle(Container):
    def check(self):
        len_max = self.level*4 + len(self.name)
        if not self.sub[0]:
            len_max += self.sub[1].check()
        else:
            for i in self.sub:
                len_sub = i.check()
                if len_max < len_sub:
                    len_max = len_sub 
        return len_max
    def draw(self,indent,is_final,front_len,full_len):
        indent_ = indent.copy()
        if self.name:
            print()
            for i in range(self.level-1):
                print(indent_[i], end='')
            print('├──', end='')
            if not self.sub[0]:
                print(f'{self.icon[1]}{self.name}',end='') 
            else:
                print(f'{self.icon[0]}{self.name}',end='') 
            front_len = self.level*3
            rest_len = full_len - front_len
            rest_len -= len(self.name)
            if self.sub[0]:
                print(' '+'─'*(rest_len-2)+'┤',end='')
            c = '│  '
            indent_.append(c)
        for i in range(len(self.sub)):
            if self.sub[i]:
                self.sub[i].draw(indent_,i==len(self.sub)-1,front_len+len(self.name),full_len)
class Leaf_rectangle(Leaf):
    def check(self):
        len_max = len(self.name) + 3
        return len_max
    def draw(self,indent,is_final,front_len,full_len):
        rest_len = full_len - front_len
        if self.name:
            rest_len -= len(self.name)+3
            print(f' : {self.name}',end='')
        print(' '+'─'*(rest_len-2)+'┤',end='')

class MyCmd(cmd.Cmd):  
    prompt = 'fje> '  
      
    def do_fje(self, arg):   
        # 公共代码部分，添加新风格时不用改写
        if not arg:  
            return
        arg_file = None
        arg_style = None
        arg_icon = "none"
        # 解析命令arg
        args = arg.split()
        for i in range(len(args)):
            if args[i] == '-f':
                arg_file = args[i+1]
            elif args[i] == '-s':
                arg_style = args[i+1]
            elif args[i] == '-i':
                arg_icon = args[i+1]
        # 读取JSON文件  
        with open(arg_file, 'rb') as file:  
            data = json.load(file)  
        # 处理JSON文件
        fje = FJE_factory.create_FJE(arg_style)
        icon = {"none":[' ',' '],"diamond":['♢','♦'],"spade":['♤','♠'],"heart":['♡','♥'],"club":['♧','♣']}
        container = fje._load('',0,data,icon[arg_icon])
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
