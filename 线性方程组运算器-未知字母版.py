import re
import sympy as sp
import random
import subprocess

def show(num):
    if isinstance(num, sp.Expr):
        # 如果是 SymPy 对象
        num_str = str(sp.simplify(num))
        if num_str[0] != '-':
            num_str = '+' + num_str
        return num_str
    elif num >= 0:
        return '+' + str(num)
    else:
        return str(num)

def PrintMatrix():  #输出
    lineshow = []
    for i in range(m):
        lineshow.append([])
        for j in range(n+1):
            lineshow[i].append(matrix[i][j])
    for line in lineshow:
        width = [8 for _ in range(n+1)]
        for j in range(n+1):
            for i in range(m):
                if len(str(lineshow[i][j]))+2 > width[j]:
                    width[j] = len(str(lineshow[i][j]))+2
        row_str = ''
        for j in range(len(line)):
            row_str += f"{str(line[j]):>{width[j]}}"
        print(row_str)

def toImage():
    lineshow = []
    for i in range(m):
        lineshow.append([])
        for j in range(n+1):
            lineshow[i].append(sp.simplify(matrix[i][j]))
    expr = sp.Matrix(lineshow)
    sp.init_printing(use_latex=False, use_unicode=True, use_mpmath=False)
    sp.preview(expr, viewer='file', filename='sympy_output.png')
    subprocess.Popen(['start', '', 'sympy_output.png'], shell=True)
    
def Interchange(i, j):  #互换指令
    matrix[i],matrix[j]=matrix[j],matrix[i]
    print(f'R{i+1},{j+1}')

def Multi(i, k):  #倍乘指令
    for a in range(n+1):
        matrix[i][a] *= k
    print(f'{k}R{i+1}')

def Addition(i,j,k):  #倍加指令，i+=j*k
    for a in range(n+1):
        matrix[i][a] = matrix[i][a]+k*matrix[j][a]
    if k==1:
        print(f'R{i+1} + R{j+1}')
    else:
        print(f'R{i+1} {show(k)} R{j+1}')

def ClearX(i):  #一键消元，把第i行的首项变成阶梯头
    for a in range(n+1): #找到阶梯头
        if matrix[i][a] != 0:
            j = a
            break
    for a in range(i+1, m):
        k = -matrix[a][j] / matrix[i][j]
        Addition(a,i,k)
    k = 1 / matrix[i][i]
    Multi(i, k)
    xj = [0 for _ in range(m)] #以下是整理，避免逆阶梯出现
    for b in range(i+1, m):
        for a in range(n+1):
            if matrix[b][a] != 0:
                xj[b] = a
                break
    for b in range(i+1,m-1):
        for a in range(b,m-1):
            if xj[a] > xj[a+1]:
                xj[a],xj[a+1]=xj[a+1],xj[a]
                matrix[a],matrix[a+1]=matrix[a+1],matrix[a]
    
def rank():   #增广矩阵
    rank = 0
    for b in range(i+1, m):
        for a in range(n+1):
            if matrix[b][a] != 0:
                rank = b+1
                break
    return rank

def rank_co():   #系数矩阵
    rank = 0
    for b in range(i+1, m):
        for a in range(n):
            if matrix[b][a] != 0:
                rank = b+1
                break
    return rank
    
def simple():  #最简形式
    for i in range(m-1):
        for j in range(i+1,m):
            k = -matrix[i][j] / matrix[j][j]
            Addition(i,j,k)
    k = 1 / matrix[m-1][m-1]
    Multi(m-1, k)


ch = input("[1]随机常数矩阵\n[2]随机变量矩阵\n[3]自定义常数矩阵\n[4]自定义变量矩阵\n")

if ch == "1":
    m=5;n=5
    matrix = [[sp.sympify(random.randint(1, 10)) for _ in range(6)] for _ in range(5)]
    print("5x6 随机矩阵:")
    PrintMatrix()
if ch == "2":
    m=3;n=3
    a, b, c = sp.symbols('a b c')
    lib = [sp.sympify(0),sp.sympify(1),sp.sympify(2),sp.sympify(3),\
           sp.sympify(4),sp.sympify(5),sp.sympify(6),sp.sympify(7),\
            sp.sympify(8),sp.sympify(9),sp.sympify('a'),sp.sympify('b'),sp.sympify('c')]
    matrix = [[random.choice(lib) for _ in range(4)] for _ in range(3)]
    print("3x4 随机矩阵:")
    PrintMatrix()
elif ch == "3":
    m = int(input("矩阵行数："))
    n = m
    matrix = [[] for i in range(m)]
    print("输入矩阵，用空格分隔每个元素，支持整数或分数")
    for i in range(m):
        line = input()
        line = line.split()
        line = list(map(sp.sympify, line))
        matrix[i]=line
elif ch == "4":
    sp.symbols(input("输入未知字母，用空格分隔："))
    m = int(input("矩阵行数："))
    n = m
    matrix = [[] for i in range(m)]

    print("输入矩阵，用空格分隔每个元素，支持整数或分数")
    for i in range(m):
        line = input()
        line = line.split()
        line = list(map(sp.sympify, line))
        matrix[i]=line


print("[1]互换指令\n[2]倍乘指令\n[3]倍加指令\n[4]一键消元\n[5]最简阶梯化\n[6]解方程组\n[7]输出图片\n")

while 1:
    cmd = input("请输入指令：")

    if cmd=="1":
        cmd=input("输入两个行号，中间用空格分隔：")
        match = re.match(r'^(\d+) (\d+)$', cmd)
        i = int(match.group(1))-1
        j = int(match.group(2))-1
        Interchange(i, j)
    elif cmd=="2":
        cmd=input("输入行号和倍数，中间用空格分隔：")
        match = re.match(r'^(\d+) (\S+)$', cmd)
        i = int(match.group(1))-1
        k = sp.sympify(match.group(2))
        Multi(i,k)
    elif cmd=="3":
        cmd=input("输入行号、行号和倍数，中间用空格分隔：")
        match = re.match(r'^(\d+) (\d+) (\S+)$', cmd)
        i = int(match.group(1))-1
        j = int(match.group(2))-1
        k = sp.sympify(match.group(3))
        Addition(i,j,k)
    elif cmd=="4":
        cmd=input("输入行号：")
        i = int(cmd)-1
        ClearX(i)
    elif cmd=="5":
        for i in range(m-1):
            ClearX(i)
    elif cmd=="6":
        for i in range(m-1):
            ClearX(i)
        PrintMatrix()
        ra = rank_co() #系数矩阵
        ra_ = rank()  #增广矩阵
        print(f"系数矩阵的秩是{ra}\n增广矩阵的秩是{ra_}\n未知数个数是{n}")
        if ra == ra_:
            if ra == n:
                print("线性方程组有唯一解")
                simple()
            else:
                print("线性方程组有无穷多个解")
        else:
            print("线性方程组无解")
    elif cmd=="7":
        toImage()
        continue
        
        
    PrintMatrix()