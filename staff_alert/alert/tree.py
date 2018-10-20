# -*- coding: utf-8 -*-

import numpy as np
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
# Create a random dataset
def de_tree(data,target,predict):

    X= data
    y = target

    # Fit regression model
    regr_1 = DecisionTreeRegressor(max_depth=100)

    regr_1.fit(X, y)

    y_3 = regr_1.predict(predict)
    # Plot the results

    plt.figure()
    print(len(X))
    print(len(y))
    l = len(X[0])-1
    l1 = l

    for ky in y:


        for kx in X[l-l1]:
            plt.scatter(kx, ky, c="darkorange")
        l1 = l1-1
    for k in predict[0]:

        plt.scatter(k,y_3,color ='green')
    plt.plot(X, y, color="yellowgreen", linewidth=2)
    plt.xlabel("data")
    plt.ylabel("target")
    plt.title("Decision Tree Regression")
    plt.legend()
    plt.show()

de_tree([[1,2,1,2],[1.2,3,.8,1.8],[4,3,2.5,3]],[1,1,3],[[3,2,3.5,4]])