# Reference:
# 1.https://github.com/kissghosts/data-mining-2013/blob/master/


import sys
import copy


#************************************************Converting the data to sparse matrix*************************************************************************************************
def read_datatosparse(fname):
    #itemset=[]
    items = []
    itemsets = []
    file = open(fname, 'r');

    for line in file:
        itemset = line.strip().split(' ')

        if itemset:
            itemsets.append(sorted(itemset))
            for item in itemset:
                if item not in items:
                    items.append(item)
    numcolumn=len(items)
    matrix = [[0]*numcolumn for i in range(len(itemsets))]
    for i in range(len(itemsets)):
        for j in range(len(items)):
            if items[j]in itemsets[i]:
                matrix[i][j]=1
    #print items
    return  matrix

# ************************************Method to count the Support:It takes input as a candidate set(item set) and calculates its counts in the full itemsets***************************

def support_counting(itemset, itemsets):
    """calc support for a given itemset
    """

    support_count = 0
    for each_set in itemsets:
        if isinstance(itemset, list):
            for each_item in itemset:
                if each_item not in each_set:
                    break
            else:
                support_count += 1
        else:
            if itemset in each_set:
                support_count += 1

    return support_count


#********************************************Method to generate Candidate itemset using Fk-1 * Fk-1***************************************************************

def gen_candidate3(itemsets):
    """generate candidates by using Fk-1 * Fk-1 i.e merge k-1 itemsets only if their first k-2 itemsets are similar
    """

    candidates = []
    num = len(itemsets)

    # the combination method used for k = 1 is different
    if len(itemsets[0]) == 1:
        for n in range(num - 1):
            for m in range(n + 1, num):
                    candidates.append([itemsets[n][0], itemsets[m][0]])
    else:
        for n in range(num - 1):
            for m in range(n + 1, num):
                if (itemsets[n][:-1] == itemsets[m][:-1]
                    and itemsets[n][1:] + [itemsets[m][-1]] in itemsets):
                    candidates.append(itemsets[n] + [itemsets[m][-1]])

    #print candidates
    return candidates

#*********************************************Method to generate Candidate itemset using Fk-1 * F1**********************************************************************

def gen_candidate2(items,itemsets):
    """generate candidates by using Fk-1 * F1 i.e each frequent k-1 item will be merged with other frequent items
    """

    candidates = []
    num = len(itemsets)

    # the combination method used for k = 1 is different
    if len(itemsets[0]) == 1:
        for n in range(num - 1):
            for m in range(n + 1, num):
                    candidates.append([itemsets[n][0], itemsets[m][0]])
    else:
        for n in range(num - 1):
            for m in range(len(items)):
                if (items[m][0][0] not in itemsets[n]):
                   if (sorted(itemsets[n] + [items[m][0][0]]) not in candidates):
                       candidates.append(sorted(itemsets[n] + [items[m][0][0]]))
    #print "generated candidates using Fk-1 * F1"
    return candidates

#*********************************************Method to find Subset*****************************************************************************************************
def is_subset(set1, set2):
    """check whether set1 is subset of set2, returen True or False
    """

    for item in set1:
        if item not in set2:
            return False
    else:
        return True



def sub(set1, set2):
    """return = set2 - set1
    """

    result = []
    for each in set2:
        if not each[0] in set1:
            result.append(each[0])
    return result

#*************************************Rule generation using Confidance Based Pruning:****************************************************************************************

def gen_rulesConfidance(minconf, frequent_itemsets):
    """rule generation
    """

    result = {}

    for n in range(2, len(frequent_itemsets) + 1):
        for itemset in frequent_itemsets[n]:
            h = []
            for each in itemset[0]:
                h.append([each])

            k_itemset = copy.deepcopy(h)
            count = len(k_itemset)
            for i in range(count - 1):
                for each in k_itemset:
                    div = sub(each, k_itemset)
                    for l in frequent_itemsets[len(div)]:
                        if sorted(div) == sorted(l[0]):
                            sup = l[1]
                            break

                    conf = itemset[1] / sup
                    if conf < minconf:
                        if each in h:
                            h.remove(each)
                    elif (result.has_key(conf)
                        and [div, each] not in result[conf]):
                        result[conf].append([div, each])
                    else:
                        result[conf] = [[div, each]]

                if h:

                    h = gen_candidate3(h)
                else:
                    break

    return result


#*************************************Rule generation using Lift Based Pruning:****************************************************************************************
def gen_rulesLift(minlift, frequent_itemsets):
    """rule generation using Lift based Pruning
    """

    result = {}

    for n in range(2, len(frequent_itemsets) + 1):
        for itemset in frequent_itemsets[n]:
            h = []
            for each in itemset[0]:
                h.append([each])

            k_itemset = copy.deepcopy(h)
            count = len(k_itemset)
            for i in range(count - 1):
                for each in k_itemset:
                    div = sub(each, k_itemset)
                    for l in frequent_itemsets[len(div)]:
                        if sorted(div) == sorted(l[0]):
                            sup = l[1]
                            break
                    for l1 in frequent_itemsets[len(each)]:
                        if sorted(each) == sorted(l1[0]):
                            sup1 = l1[1]
                            break

                    conf = itemset[1] / sup
                    lift=conf/sup1
                    if lift < minlift:
                        if each in h:
                            h.remove(each)
                    elif (result.has_key(lift)
                        and [div, each] not in result[lift]):
                        result[lift].append([div, each])
                    else:
                        result[lift] = [[div, each]]

                if h:

                    h = gen_candidate3(h)
                else:
                    break

    return result


#**************************************methods -Fk-1*Fk-1, FK-1 * F1, Brute Force for Frequent Itemset generation***********************************************


def Method2(items,itemsets):

    #print "generating candidate set(s) ..."
    print "generated candidates using Fk-1 * F1 "
    lenFreq=0
    lenCand=0
    # generate the 1-size itemsets
    frequent_itemsets[1] = []
    for each in items:
        sup = support_counting(each, itemsets) / itemset_count
        if sup >= minsup:
            frequent_itemsets[1].append([[each], sup])
            lenFreq=lenFreq+1
    # generate frequent itemset
    if not frequent_itemsets:
        print "no set generated"
        sys.exit(0)

    n = 1
    while n < maxsize:
        frequent_itemsets[n + 1] = []
        k_freq_itemsets = []
        for each in frequent_itemsets[n]:
            k_freq_itemsets.append(each[0])
        #candidates = gen_candidate(itemsets)
        candidates = gen_candidate2(frequent_itemsets[1],k_freq_itemsets) #----------------will be used in Fk-1 and F1
        #print candidates
        if candidates:
            print "Candidates generated at this level :" ,len(candidates)
            print candidates
            lenCand=lenCand+len(candidates)
        for each in candidates:
            sup = support_counting(each, itemsets) / itemset_count
            if sup >= minsup:

                frequent_itemsets[n + 1].append([each, sup])
                lenFreq=lenFreq+1

        if frequent_itemsets[n + 1] == []:
            frequent_itemsets.pop(n + 1)
            break

        n += 1
    print "\n"
    print "Frequent itemsets using Fk-1 and f1 are:"
    print frequent_itemsets
    print "\n"
    print "Total Candidates generated after candidates pruning using Fk-1 and f1 : ", lenCand+len(items)
    print "Total frequent itemset generated after candidates pruning using Fk-1 and f1 :", lenFreq
    #nextstep(conf,frequent_itemsets)


def Method3(lift,items,itemsets):

    #print "generating candidate set(s) ..."
    print "generating candidates set(s) using Fk-1 * Fk-1.... "
    lenFreq=0
    lenCand=0
    # generate the 1-size itemsets
    frequent_itemsets[1] = []
    for each in items:
        sup = support_counting(each, itemsets) / itemset_count
        if sup >= minsup:
            frequent_itemsets[1].append([[each], sup])
            lenFreq=lenFreq+1
    # generate frequent itemset
    print lenFreq
    if not frequent_itemsets:
        print "no set generated"
        sys.exit(0)

    n = 1
    while n < maxsize:
        frequent_itemsets[n + 1] = []
        k_freq_itemsets = []
        for each in frequent_itemsets[n]:
            k_freq_itemsets.append(each[0])
        #candidates = gen_candidate(itemsets)
        candidates = gen_candidate3(k_freq_itemsets) #----------------will be used in Fk-1 and Fk-1
        #print candidates
        if candidates:
            lenCand=lenCand+len(candidates)
            print "Number of Candidates generated at this level: ",len(candidates)
            print candidates
        for each in candidates:
            sup = support_counting(each, itemsets) / itemset_count
            if sup >= minsup:
                frequent_itemsets[n + 1].append([each, sup])
                lenFreq=lenFreq+1

        if frequent_itemsets[n + 1] == []:
            frequent_itemsets.pop(n + 1)
            break

        n += 1
    print "\n"
    print "Frequent itemsets using Fk-1 and Fk-1 are:"
    countofitms=0
    p=2
    print frequent_itemsets
#     while p<len(frequent_itemsets)+1:
#         countofitms+= (2**len(frequent_itemsets[p]))-2
#         p+=1
#     print 'number of rules generated by brute',countofitms
      
    
    print "\n"
    print "Total Candidates generated after candidates pruning using Fk-1 and fK-1 : ", lenCand+len(items)
    print "Total frequent itemset generated after candidates pruning using Fk-1 and Fk-1 :", lenFreq
    print "\n"


    #print len(frequent_itemsets)
    nextstep(lift,conf,frequent_itemsets)

#******************************************************Method to select and generate rules or Maximal or Closed frequent itemsets after the frequent itemset has been generated****************
def nextstep(lift,conf,frequent_itemsets):
# maximal, closed or rule generation
 
    print "Association rules are getting generated using confidance based pruning"
    minconf = conf / 100.0
    print 'minconf',minconf
#         print "frequent itemset after candidates pruning"
#         print frequent_itemsets
    rules = gen_rulesConfidance(minconf, frequent_itemsets)
    #print 'rules:    ', rules


    print "writing Association Rules..."
    num = 0
    for each in sorted(rules.keys(), reverse=True):

        if len(rules[each]) > 1:
            for rule in rules[each]:
                print("%s => %s (%s)\n" % (rule[0],
                    rule[1], each))
                num += 1
        else:
            print("%s => %s (%s)\n" % (rules[each][0][0],
                rules[each][0][1], each))
            num += 1

    print "%s set(s) generated" % num
    print "\n"
    #****************************************Lift***********************************
    print "Association rules are getting generated using Lift"
    minlift = lift / 100.0
    print 'minlift',minlift
#         print "frequent itemset after candidates pruning"
#         print frequent_itemsets
    rules1 = gen_rulesLift(minlift, frequent_itemsets)
    #print 'rules:    ', rules
 
 
    print "writing Association Rules..."
    num = 0
    for each in sorted(rules1.keys(), reverse=True):
 
        if len(rules1[each]) > 1:
            for rule1 in rules1[each]:
                print("%s => %s (%s)\n" % (rule1[0],
                    rule1[1], each))
                num += 1
        else:
            print("%s => %s (%s)\n" % (rules1[each][0][0],
                rules1[each][0][1], each))
            num += 1
 
    print "%s set(s) generated" % num
    print "\n"
    #**************************ENd of lift****************************************
   
#***********************************************Main Method: Program Start**************************************************************************************************
if __name__ == '__main__':
    #f1=sys.argv[1]
    f1="car.data.txt"
    #f1="flare.data1.txt"
    #f1="nursery.data.txt"
    #f1="test.txt"
    #print f1
    #Hard coding the input
    support=25
    conf=50
    minsup = support / 100.0
    maxsize = 30  #maximum size of frequent itemsets"
    minsize = 1   #minimal size of frequent itemsets"
    lift=75
    # end of hard coding





    fname=f1
    #sparse=read_datatosparse(fname)

    #print "Data as sparse Matrix"
    #print( sparse)
    print "\n"
    file=open(f1,'r')   # change to datset name
    items = []
    itemsets = []
    frequent_itemsets = {}
    bruteForceitemsets ={}
    for line in file:
        itemset = line.strip().split(',')

        if itemset:
            itemsets.append(sorted(itemset))
            for item in itemset:
                if item not in items:
                    items.append(item)

    print "items:"
    print items
    print "\n"
    #print "itemsets:"
    #print itemsets
    print "\n"
    items.sort()
    itemset_count = float(len(itemsets))
    print "%s item(s), %s transaction(s)" % (len(items), len(itemsets))
    print "\n"
    #Method3(items,itemsets)   # for Fk-1 and Fk-1
    #Method2(items,itemsets)   # for Fk-1 and F1
    #Method1(items,itemsets)   # for BruteForce





    method="2"
    if method=="3":
        Method3(lift,items,itemsets)   # for Fk-1 and Fk-1

    elif method=="1":
        Method1(items,itemsets)   # for BruteForce

    elif method=="2":
        Method2(items,itemsets)   # for Fk-1 and F1

    method="3"
    if method=="3":
        Method3(lift,items,itemsets)   # for Fk-1 and Fk-1

    elif method=="1":
        Method1(items,itemsets)   # for BruteForce

    elif method=="2":
        Method2(items,itemsets)   # for Fk-1 and F1
