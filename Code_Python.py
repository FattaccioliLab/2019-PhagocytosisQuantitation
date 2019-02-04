# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 15:38:30 2019

@author: Lorraine Montel

This code is an example of extraction of the Phagocytic index from the database obtained with the Cell Profiler Pipeline 
described in http://dx.doi.org/10.1101/482547
"""

import numpy as np
import sqlite3


def ConnectDB(file):
    # file is the string of the localtion of the database file
    # Output is a cursor for the database
    DB=sqlite3.connect(file)
    cur=DB.cursor()
    return cur

def request(SQLString,cur):
    # SQLString is SQL query, cur a cursor as obtained from ConnectDB
    stock=[]
    result=cur.execute(SQLString)
    for r in result:
        if len(r)==1:
            stock.append(r[0])
        elif len(r)>1:
            stock.append(r)
    return np.array(stock)

def Phagocytic_stats(cur):
    #cur is a cursor as obtained from ConnectDB
    #Output is the Phagocytic index for each group of Plate_ID
    r=request("SELECT SUM(Image_Count_FilteredIn),SUM(Image_Count_FilteredCytoplasm),Image_Metadata_PlateID FROM Cyto_Per_Image GROUP BY Image_Metadata_PlateID",cur)
    drop=[]
    cell=[]
    label=[]
    for line in r:
        drop.append(int(line[0]))
        cell.append(int(line[1]))        
        label.append(line[2])
    for l in label:
        print(l+" "+str(drop[label.index(l)]/max(cell[label.index(l)],1)))
    return r
    
# Input your database location here
file=""
cur=ConnectDB(file)
Phagocytic_stats(cur)
