import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from apyori import apriori

def doTheory():
    store_data = pd.read_csv('babystore.csv')

    # print(store_data.tail())
    # print(store_data.shape)

    records = []
    for i in range(1, 138):
        records.append([str(store_data.values[i, j]) for j in range(0, 8)])

    # print(type(records))

    association_rules = apriori(records, min_support=0.045, min_confidence=0.2, min_lift=3, min_length=2)
    association_results = list(association_rules)

    # print("There are {} Relation derived.".format(len(association_results)))

    # for i in range(0, len(association_results)):
    #     print(association_results[i][0])

    data_list = []

    for item in association_results:
        # first index of the inner list
        # Contains base item and add item
        
        pair = item[0]
        items = [x for x in pair if x!= 'nan']
        # if len(items) == 2:
        #     print("Rule: " + items[0] + " -> " + items[1])
        # elif len(items) == 3:
        #     print("Rule: " + items[0] + " -> " + items[1] + " -> " + items[2])
        # elif len(items) == 4:
        #     print("Rule: " + items[0] + " -> " + items[1] + " -> " + items[2]+ " -> " + items[3])
        # elif len(items) == 5:
        #     print("Rule: " + items[0] + " -> " + items[1] + " -> " + items[2]+ " -> " + items[3]+ " -> " + items[4])
        # elif len(items) == 6:
        #     print("Rule: " + items[0] + " -> " + items[1] + " -> " + items[2]+ " -> " + items[3]+ " -> " + items[4]+ " -> " + items[5])
        
        data_list.append(items)
            
        # second index of the inner list
        # print("Support: " + str(item[1]))

        # third index of the list located at 0th
        # of the third index of the inner list

        # print("Confidence: " + str(item[2][0][2]))
        # print("Lift: " + str(item[2][0][3]))
        # print("=====================================")

    return data_list

# data_list = doTheory()
# print("==================================================================")
# print(data_list)