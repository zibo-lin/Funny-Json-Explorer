import json  
import os
import cmd

# class Line:
#     def __init__(self,node,indent,is_final,front_len):
#         self.node = node
#         self.indent = indent
#         self.is_final = is_final
#         self.front_len = front_len

class Iterator:
    def __init__(self,container):
        # line = Line(container,[],True,0)
        self.stack = [container]
    def __iter__(self):
        return self
    def __next__(self):
        container = stack[0]
        stack = stack[1:]
        stack += container.sub
        return container

class Visitor:
    def __init__(self):
        pass
    def visit_fje(self):
        pass
    def visit_container(self):
        pass
    def visit_leaf(self):
        pass
class Visitor_tree(Visitor):
    def __init__(self):
        self.indents = []
        self.is_finals = []
    def visit_fje(self,container):
        lines = []
        interator = Iterator(container)
        for ele in interator:
            lines.append(ele)
        # self.indents.append([])
        # self.is_finals.append(True)
        for i in range(len(lines)):
            if (i+1)==len(lines):
                self.is_finals.append(True)
            elif lines[i].level!=lines[i+1].level:
                self.is_finals.append(True)
            else:
                self.is_finals.append(False)
            if i>0:
                pass
        indent_ = []
        for ele in lines:
            ele.draw(self)
    def visit_container(self):
        pass
        # print();print(indent,icon,name,sep='',end='')
    def visit_leaf(self):
        pass
        # if name:
            # print(" : ",name,sep='',end='')
class Visitor_rectangle(Visitor):
    def __init__(self):
        self.indents = []
        self.is_finals = []
        self.front_lens = []
        self.full_len = 0
    def visit_fje(self,container):
        pass
    def visit_container(self):
        pass
    def visit_leaf(self):
        pass

class FunnyJsonExplorer:
    def __init__(self):
        pass
    def show(self,container,visitor):
        visitor.visit_fje(container)
    def _load(self,name,level,data,icon):
        container = Container(icon,name,level)
        if isinstance(data, dict):
            for key, value in data.items():
                sub_container = self._load(key,level+1,value,icon)
                container.sub.append(sub_container)
        else:
            sub_leaf = Leaf(data)
            container.sub.append(None)
            container.sub.append(sub_leaf)
        return container
class Container:
    def __init__(self,icon=[' ',' '],name='',level=0):
        self.icon = icon
        self.name = name
        self.level = level
        self.sub = []
    def draw(self,visitor):
        visitor.visit_container()
class Leaf:
    def __init__(self,name=None):
        self.name = name if name else ''
    def draw(self,visitor):
        visitor.visit_leaf()

def client(data,visitor,icon):
    fje = FunnyJsonExplorer()
    container = fje._load('',0,data,icon)
    fje.show(container,visitor)

class MyCmd(cmd.Cmd):  
    prompt = 'fje> '  
    def do_fje(self, arg): 
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
        icon = {"none":[' ',' '],"diamond":['♢','♦'],"spade":['♤','♠'],"heart":['♡','♥'],"club":['♧','♣']}
        if arg_style == "tree":
            visitor = Visitor_tree()
        elif arg_style == "rectangle":
            visitor = Visitor_rectangle() 
        client(data,visitor,icon[arg_icon])
    def do_quit(self, arg):   
        return True  
    def default(self, line):  
        print(f'Unknown command: {line}') 

if __name__ == '__main__':  
    # 更改运行路径
    directory_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(directory_path)
    MyCmd().cmdloop()
