__author__ = 'kosttek'
import math

def foo(num):
    if num == 0:
        return []
    log_result = math.log(math.fabs(num),2)
    if log_result - int(log_result) > 0:
        index = int(log_result)+1
    else:
        index = int(log_result)

    sameSign = sign((-2)**index) == sign(num)
    result = list()
    if sameSign:
        result.append(index)
        next_num = -((-2)**index - num)
    else:
        result.append(index)
        result.append(index + 1)
        next_num = -((-2)**index + (-2)**(index+1) - num)

    if next_num == 0:
        return result
    else:
        return result + foo(next_num)


def sign(num):
    if num >=0:
        return +1
    else:
        return -1

def check(lis):
    result = 0
    for index in lis:
        result += (-2)**index
    return result

for x in range(-100,100):
    reslist = foo(x)
    res = check(reslist)
    if res == x:
        print 'OK'
    else:
        print "wrong ",x
        break