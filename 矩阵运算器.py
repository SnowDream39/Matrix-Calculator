import re
from fractions import Fraction

def PrintMatrix():
    lineshow = []
    for i in range(len(matrix)):
        lineshow.append([])
        for j in range(len(matrix[i])):
            if matrix[i][j].denominator == 1:
                lineshow[i].append(int(matrix[i][j]))
            else:
                lineshow[i].append(str(matrix[i][j]))
    for line in lineshow:
        row_str = ''
        for i in range(len(line)):
            row_str += "{:>8}".format(line[i])
        print(row_str)

def Interchange(i, j):
    matrix[i],matrix[j]=matrix[j],matrix[i]

def Multi(i, k):
    for a in range(len(matrix[i])):
        matrix[i][a] *= k

def Addition(i,j,k):
    for a in range(len(matrix[i])):
        matrix[i][a] = matrix[i][a]+k*matrix[j][a]

def ClearX(i):
    for a in range(len(matrix[i])):
        if matrix[i][a] != 0:
            j = a
            break
    for a in range(i+1, len(matrix)):
        k = Fraction(-matrix[a][j], matrix[i][j])
        Addition(a,i,k)
        if k==1:
            print(f'R{a+1}+R{i+1}')
        elif k>0:
            print(f'R{a+1}+{k}R{i+1}')
        elif k<0:
            print(f'R{a+1}{k}R{i+1}')


m = int(input("矩阵行数："))
matrix = [[] for i in range(m)]

print("输入矩阵，用空格分隔每个元素，支持整数或分数")
for i in range(m):
    line = input()
    line = line.split()
    line = list(map(Fraction, line))
    matrix[i]=line

print("互换指令：R12")
print("倍乘指令：2R1、2/3R1")
print("倍加指令：R2+3R1、R2-2/3R1")
print("一键消元：R1C")

while 1:
    cmd = input("请输入指令：")
    if re.match(r'^R\d{2}$', cmd):
        print(f"{cmd} 是互换指令。")
        match = re.match(r'^R(\d)(\d)$', cmd)
        i = int(match.group(1))-1
        j = int(match.group(2))-1
        Interchange(i, j)
    elif re.match(r'^(\d+|\d+/\d+)R\d$', cmd):
        print(f"{cmd} 是倍乘指令。")
        match = re.match(r'^(\d+|\d+/\d+)R(\d)$', cmd)
        i = int(match.group(2))-1
        k = Fraction(match.group(1))
        Multi(i,k)
    elif re.match(r'^R(\d)([+-]|[+-]\d+|[+-]\d+/\d+)R\d$', cmd):
        print(f"{cmd} 是倍加指令。")
        match = re.match(r'^R(\d)([+-]|[+-]\d+|[+-]\d+/\d+)R(\d)$',cmd)
        i = int(match.group(1))-1
        if match.group(2)=='+' :
            k = 1
        elif match.group(2)=='-' :
            k = -1
        else:
            k = Fraction(match.group(2))
        j = int(match.group(3))-1
        Addition(i,j,k)
    elif re.match('^R\dC$', cmd):
        print(f"{cmd} 是一键消元。")
        match = re.match(r'^R(\d)C$', cmd)
        i = int(match.group(1))-1
        ClearX(i)

    PrintMatrix()