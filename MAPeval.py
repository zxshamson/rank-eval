# encoding=utf-8
# rankedlist structure: pairs of (predict_value, real_value)


def cal_precision(rankedlist, n):
    ones = 0.0
    for m in xrange(len(rankedlist)):
        if rankedlist[m][1] == 1:
            ones += 1
            if ones == n:
                break

    return ones/float(m + 1)


def cal_ap(rankedlist):
    totalsum = 0
    for m in xrange(len(rankedlist)):
        totalsum += rankedlist[m][1]
    # If all in list are not relevant, the list is not counted
    if totalsum == 0:
        return -1
    totalp = 0.0
    for n in range(1, int(totalsum) + 1):
        totalp += cal_precision(rankedlist, n)

    return totalp/totalsum


def cal_map(users_num, unrankedlist_allusers):
    MAP = 0.0
    users_count = 0
    for u in xrange(users_num):
        rankedlist = unrankedlist_allusers[u]
        if len(rankedlist) >= 2:
            rankedlist = sorted(rankedlist, key=lambda x: x[0], reverse=True)
            ap = cal_ap(rankedlist)
            if ap != -1:
                users_count += 1
                MAP += ap
    if users_count <= 0:
        MAP = -1
    else:
        MAP /= users_count

    return MAP


def cal_pn(rankedlist, n):
    ones = 0.0
    for m in xrange(n):
        if rankedlist[m][1] == 1:
            ones += 1

    return ones/float(n)


def cal_precision_N(users_num, unrankedlist_allusers, n):
    precision = 0.0
    users_count = users_num
    for u in xrange(users_num):
        unrankedlist = unrankedlist_allusers[u]
        # If all in list are not relevant, the user is not counted
        totalsum = 0.0
        for m in xrange(len(unrankedlist)):
            totalsum += unrankedlist[m][1]
        if totalsum == 0:
            users_count -= 1
            continue
        rankedlist = sorted(unrankedlist, key=lambda x: x[0], reverse=True)
        if n <= len(rankedlist) and len(rankedlist) >= 2:
            precision += cal_pn(rankedlist, n)
        else:
            users_count -= 1
    if users_count <= 0:
        precision = -1
    else:
        precision /= users_count

    return precision


if __name__ == '__main__':

    uNum = 3
    scorelist = []
    for u in xrange(uNum):
        scorelist.append([])
    scorelist[0] = [(0.5, 1), (0.8, 0), (0.2, 0)]
    scorelist[1] = [(0.5, 1), (0.8, 1), (0.2, 0), (0.7, 0)]
    scorelist[2] = [(0.4, 1), (0.5, 1), (0.8, 0), (0.2, 0)]
    s = cal_map(uNum, scorelist)
    z = cal_precision_N(uNum, scorelist, 3)
    print "MAP: ", s
    print "P@3: ", z


