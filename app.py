# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 20:21:14 2016

@author: Michael Castillo
"""

import pandas as pd
import matplotlib.pyplot as plt

def readHtmls(path, prefix):
    df = pd.DataFrame()
    for value in prefix:
        tables = pd.read_html(path + value + '.html')
        df = df.append(tables[0])        
    return df

years = ['2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016']
path = 'html/'

#Read dinamically the htmls
data = readHtmls(path, years)    
#drop unnecesary rows
data = data.dropna(axis=0, thresh=4)
#change column names
data.columns = ['sorteo','premio','cayopremio','cayorevancha','revancha','fecha']
#convert sorteo column to number
data['sorteo'] = pd.to_numeric(data['sorteo'], errors='coerce')
#order by sorteo
data = data.sort('sorteo')
#reset index
data = data.reset_index(drop=True)
#change cayÃ³ for 1
data = data.replace('cayÃ³',1)
#change nan for 0
data = data.fillna(0)
#split datasets
dfpremio = data.loc[:,['sorteo','premio','cayopremio','fecha']]
dfrevancha = data.loc[:,['sorteo','revancha','cayorevancha','fecha']]
#split values
columns=['num1','num2','num3','num4','num5','num6']
dfpremio[columns] = pd.DataFrame(dfpremio.premio.str.split(' - ',-1).tolist(),columns=columns)
dfrevancha[columns] = pd.DataFrame(dfrevancha.revancha.str.split(' - ',-1).tolist(),columns=columns)
#drop row with no revancha
dfrevancha = dfrevancha[dfrevancha.revancha != '00 - 00 - 00 - 00 - 00 - 00']
#convert to numeric num columns
dfpremio[['num1','num2','num3','num4','num5','num6']] = dfpremio[['num1','num2','num3','num4','num5','num6']].apply(pd.to_numeric)
dfrevancha[['num1','num2','num3','num4','num5','num6']] = dfrevancha[['num1','num2','num3','num4','num5','num6']].apply(pd.to_numeric)
#histrogram
dfpremio.iloc[:,4:].hist(bins=45)
dfrevancha.iloc[:,4:].hist(bins=45)

plt.figure()
plt.hist([dfpremio['num1'],dfpremio['num2'],dfpremio['num3'],dfpremio['num4'],dfpremio['num5'],dfpremio['num6']],bins=45,stacked=True)

#dfpremio[dfpremio.premio == '06 - 13 - 19 - 26 - 32 - 39']

dfpremio.describe()
dfrevancha.describe()
#'07 - 13 - 20 - 27 - 33 - 39'


