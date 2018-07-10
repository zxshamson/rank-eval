# encoding=utf-8
# rankedlist structure: pairs of (predict_value, real_value)
import math


def cal_dcg_k(rankedlist, k):
    res = 0.0
    for i in xrange(k):
        numerator = 2 ** rankedlist[i][1] - 1.0
        denominator = math.log(2+i, 2)
        res += numerator / denominator

    return res


def cal_ndcg_k(unrankedlist, k):
    rankedlist = sorted(unrankedlist, key=lambda x: x[0], reverse=True)
    dcg = cal_dcg_k(rankedlist, k)

    rankedlist = sorted(unrankedlist, key=lambda x: x[1], reverse=True)
    idcg = cal_dcg_k(rankedlist, k)
    # If all in list are not relevant, the list is not counted
    if idcg == 0:
        return -1
    else:
        return dcg / idcg


def cal_ndcg_all(users_num, unrankedlist_allusers, k):
    ndcg = 0.0
    users_count = users_num
    for u in xrange(users_num):
        unrankedlist = unrankedlist_allusers[u]
        if k <= len(unrankedlist) and len(unrankedlist) >= 2:
            res = cal_ndcg_k(unrankedlist, k)
            if res != -1:
                ndcg += res
            else:
                users_count -= 1
        else:
            users_count -= 1
    if users_count <= 0:
        ndcg = -1
    else:
        ndcg /= users_count

    return ndcg


def cal_ndcg_nok(users_num, unrankedlist_allusers):
    ndcg = 0.0
    users_count = users_num
    for u in xrange(users_num):
        unrankedlist = unrankedlist_allusers[u]
        k = len(unrankedlist)
        if k >= 2:
            res = cal_ndcg_k(unrankedlist, k)
            if res != -1:
                ndcg += res
            else:
                users_count -= 1
        else:
            users_count -= 1
    if users_count <= 0:
        ndcg = -1
    else:
        ndcg /= users_count

    return ndcg


def cal_mrr(users_num, unrankedlist_allusers):
    mrr = 0.0
    users_count = 0
    for u in xrange(users_num):
        unrankedlist = unrankedlist_allusers[u]
        l = len(unrankedlist)
        if l >= 2:
            rankedlist = sorted(unrankedlist, key=lambda x: x[0], reverse=True)
            pos = 1
            for m in xrange(l):
                if rankedlist[m][1] == 1:
                    break
                pos += 1
            if pos != l + 1:
                mrr += 1 / float(pos)
                users_count += 1
    if users_count <= 0:
        mrr = -1
    else:
        mrr /= users_count

    return mrr


if __name__ == '__main__':

    uNum = 3
    scorelist = []
    for u in xrange(uNum):
        scorelist.append([])
    scorelist[0] = [(0.5, 1), (0.8, 0), (0.2, 0)]
    scorelist[1] = [(0.5, 1), (0.8, 1), (0.2, 0), (0.7, 0)]
    scorelist[2] = [(0.4, 1), (0.5, 1), (0.8, 0), (0.2, 0)]
    z = cal_mrr(uNum, scorelist)
    print "mrr: ", z


