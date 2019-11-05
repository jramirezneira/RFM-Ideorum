#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%: import libraries
import pandas as pd
import numpy as np
import datetime as dt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import json
# Though the following import is not directly being used, it is required
# for 3D projection to work
 #%% create functions for calculating scores by order
def scoreRecency(x,p,d): # low recency is best and is assigned 1+
    
   
    if x <= d[p][0.25]:return 1
    elif x <= d[p][0.50]:return 2
    elif x <= d[p][0.75]:return 3
    else:return 4
def scoreFrequency(x,p,d): # high frequency is best and is assigned 1
    if x <= d[p][0.25]:return 4
    elif x <= d[p][0.50]:return 3
    elif x <= d[p][0.75]:return 2
    else:return 1
def scoreMonetary(x,p,d): # high monetary is best and is assigned 1
    if x <= d[p][0.25]:return 4
    elif x <= d[p][0.50]:return 3
    elif x <= d[p][0.75]:return 2
    else:return 1
    

df_raw = pd.read_excel('retail-data.xlsx')
#%% drop duplicates and group by country and customer ID
df = df_raw.copy()
df.country.nunique()
df.country.unique()

#%% drop duplicates and group by country and customer ID
cc = df[['country','customerid']].drop_duplicates()
cc.groupby(['country'])['customerid']. \
    aggregate('count').reset_index(). \
    sort_values('customerid', ascending=False)

#%% remove customers without customer ID
df = df[pd.notnull(df['customerid'])]
df.isnull().sum(axis=0)

#%% ensure only positive quantities and prices
df.UnitPrice.min()
df.Quantity.min()
df = df[(df['Quantity']>0)]

#%% check unique value for each column
def unique_counts(df):
   for i in df.columns:
       count = df[i].nunique()
       print(i, ": ", count)
unique_counts(df)

#%% add column for total price
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

#%% determine first and last order date
df['InvoiceDate'].min()
df['InvoiceDate'].max()

#%% establish day after last purchase as point of calculation for recency
now = dt.datetime(2011,12,10)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

#%% create RFM table
rfmTable = df.groupby('customerid').agg({
        'InvoiceDate':  lambda x: (now - x.max()).days,      #recency
        'InvoiceNo':    lambda x: len(x),                    #frequency
        'TotalPrice':   lambda x: x.sum()})                  #monetary
rfmTable['InvoiceDate'] = rfmTable['InvoiceDate'].astype(int)


#%% convert invoice date to integer and rename columns for RFM
rfmTable.rename(columns={
        'InvoiceDate':  'recency_total', 
        'InvoiceNo':    'frequency_total', 
        'TotalPrice':   'monetary_total'}, inplace=True)

#%% shift rfmTable data to quantiles for segmentation
quantiles = rfmTable.quantile(q=[0.25,0.5,0.75])
quantiles = quantiles.to_dict()
quantiles

#%% create a segmented RFM table
rfmSegment = rfmTable.copy()

#%% create new columns for RFM and assign values based on quantile
rfmSegment['r_qt'] = rfmSegment['recency_total'].apply(scoreRecency, args=('recency_total',quantiles,))
rfmSegment['f_qt'] = rfmSegment['frequency_total'].apply(scoreFrequency, args=('frequency_total',quantiles,))
rfmSegment['m_qt'] = rfmSegment['monetary_total'].apply(scoreMonetary, args=('monetary_total',quantiles,))

#%% calculate total RFM score as string composed of individual RFM quantiles
rfmSegment['rfm'] = rfmSegment.r_qt.map(str) \
                  + rfmSegment.f_qt.map(str) \
                  + rfmSegment.m_qt.map(str)

    
    
#%% create categories from rfm
datacomb=[]
datacomb.append([3,3,1,"Big Spenders","331",7])
datacomb.append([1,2,1,"Big Spenders","121",7])
datacomb.append([1,3,1,"Big Spenders","131",7])
datacomb.append([1,4,1,"Big Spenders","141",7])
datacomb.append([2,2,1,"Big Spenders","221",7])
datacomb.append([2,3,1,"Big Spenders","231",7])
datacomb.append([2,4,1,"Big Spenders","241",7])
datacomb.append([3,2,1,"Big Spenders","321",7])
datacomb.append([3,4,1,"Big Spenders","341",7])
datacomb.append([4,2,1,"Big Spenders","421",7])
datacomb.append([4,3,1,"Big Spenders","431",7])
datacomb.append([2,1,1,"Loyal Customers-Big Spenders","211",6])
datacomb.append([3,1,1,"Almost Lost","311",4])
datacomb.append([1,1,1,"Best Customers","111",8])
datacomb.append([4,1,1,"Lost Customers","411",3])
datacomb.append([4,4,4,"Lost Cheap Customers","444",1])
datacomb.append([1,1,2,"Loyal Customers","112",5])
datacomb.append([1,1,3,"Loyal Customers","113",5])
datacomb.append([1,1,4,"Loyal Customers","114",5])
datacomb.append([2,1,2,"Loyal Customers","212",5])
datacomb.append([2,1,3,"Loyal Customers","213",5])
datacomb.append([2,1,4,"Loyal Customers","214",5])
datacomb.append([3,1,2,"Loyal Customers","312",5])
datacomb.append([3,1,3,"Loyal Customers","313",5])
datacomb.append([3,1,4,"Loyal Customers","314",5])
datacomb.append([4,1,2,"Loyal Customers","412",5])
datacomb.append([4,1,3,"Loyal Customers","413",5])
datacomb.append([4,1,4,"Loyal Customers","414",5])
datacomb.append([1,4,2,"Others","142",2])
datacomb.append([1,4,3,"Others","143",2])
datacomb.append([1,4,4,"Others","144",2])
datacomb.append([4,4,1,"Big Spenders","441",7])
datacomb.append([1,2,2,"Others","122",2])
datacomb.append([1,2,3,"Others","123",2])
datacomb.append([1,2,4,"Others","124",2])
datacomb.append([1,3,2,"Others","132",2])
datacomb.append([1,3,3,"Others","133",2])
datacomb.append([1,3,4,"Others","134",2])
datacomb.append([2,2,2,"Others","222",2])
datacomb.append([2,2,3,"Others","223",2])
datacomb.append([2,2,4,"Others","224",2])
datacomb.append([2,3,2,"Others","232",2])
datacomb.append([2,3,3,"Others","233",2])
datacomb.append([2,3,4,"Others","234",2])
datacomb.append([2,4,2,"Others","242",2])
datacomb.append([2,4,3,"Others","243",2])
datacomb.append([2,4,4,"Others","244",2])
datacomb.append([3,2,2,"Others","322",2])
datacomb.append([3,2,3,"Others","323",2])
datacomb.append([3,2,4,"Others","324",2])
datacomb.append([3,3,2,"Others","332",2])
datacomb.append([3,3,3,"Others","333",2])
datacomb.append([3,3,4,"Others","334",2])
datacomb.append([3,4,2,"Others","342",2])
datacomb.append([3,4,3,"Others","343",2])
datacomb.append([3,4,4,"Others","344",2])
datacomb.append([4,2,2,"Others","422",2])
datacomb.append([4,2,3,"Others","423",2])
datacomb.append([4,2,4,"Others","424",2])
datacomb.append([4,3,2,"Others","432",2])
datacomb.append([4,3,3,"Others","433",2])
datacomb.append([4,3,4,"Others","434",2])
datacomb.append([4,4,2,"Others","442",2])
datacomb.append([4,4,3,"Others","443",2])


dfdatacomb= pd.DataFrame(datacomb, columns=['r_qt','r_qt','r_qt', 'description', 'rfm', 'sort'])


#%% import data and clone working dataframe


#%% create data for month to display in chart detail
df_raw['year'] = df_raw['InvoiceDate'].dt.year
df_raw['month'] = df_raw['InvoiceDate'].dt.month


df_final= pd.DataFrame()
df_date = df_raw[['month','year']].drop_duplicates()
for k, r in df_date.iterrows():
    
    #%% get number of unique countries and their names
    df = df_raw [(df_raw['month']== r['month']) & (df_raw['year']== r['year'])]   
  
    
    df.country.nunique()
    df.country.unique()
    
    #%% drop duplicates and group by country and customer ID
    cc = df[['country','customerid']].drop_duplicates()
    cc.groupby(['country'])['customerid']. \
        aggregate('count').reset_index(). \
        sort_values('customerid', ascending=False)
    
    #%% remove customers without customer ID
    df = df[pd.notnull(df['customerid'])]
    df.isnull().sum(axis=0)
    
    #%% ensure only positive quantities and prices
    df.UnitPrice.min()
    df.Quantity.min()
    df = df[(df['Quantity']>0)]
    
    #%% check unique value for each column
    def unique_counts(df):
       for i in df.columns:
           count = df[i].nunique()
           print(i, ": ", count)
    unique_counts(df)
    
    #%% add column for total price
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    
    #%% determine first and last order date
    df['InvoiceDate'].min()
    df['InvoiceDate'].max()
    
    #%% establish day after last purchase as point of calculation for recency
    now = df['InvoiceDate'].max()
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    #%% create RFM table
    rfmTable = df.groupby(['customerid']).agg({
            'InvoiceDate':  lambda x: (now - x.max()).days,      #recency
            'InvoiceNo':    lambda x: len(x),                    #frequency
            'TotalPrice':   lambda x: x.sum()})                  #monetary
    rfmTable['InvoiceDate'] = rfmTable['InvoiceDate'].astype(int)
    
    #print(rfmTable)
    #%% convert invoice date to integer and rename columns for RFM
    rfmTable.rename(columns={
            'InvoiceDate':  'recency', 
            'InvoiceNo':    'frequency', 
            'TotalPrice':   'monetary'}, inplace=True)
    
    #%% shift rfmTable data to quantiles for segmentation
    quantiles = rfmTable.quantile(q=[0.25,0.5,0.75])
    quantiles = quantiles.to_dict()
    #quantiles
    
    #%% create a segmented RFM table
    rfmSegment2 = rfmTable.copy()
    
   
    
    #%% create new columns for RFM and assign values based on quantile
    rfmSegment2['r_qt'] = rfmSegment2['recency'].apply(scoreRecency, args=('recency',quantiles,))
    rfmSegment2['f_qt'] = rfmSegment2['frequency'].apply(scoreFrequency, args=('frequency',quantiles,))
    rfmSegment2['m_qt'] = rfmSegment2['monetary'].apply(scoreMonetary, args=('monetary',quantiles,))
    
    #%% calculate total RFM score as string composed of individual RFM quantiles
    rfmSegment2['rfm'] = rfmSegment2.r_qt.map(str) \
                      + rfmSegment2.f_qt.map(str) \
                      + rfmSegment2.m_qt.map(str)
    
    
    
    #%% translate raw RFM values to log values for plotting, common log
    rfmSegment2 = rfmSegment2.assign(r_lg = lambda x: np.log10(x.recency))
    rfmSegment2 = rfmSegment2.assign(r_lg = lambda x: np.log10(x.frequency))
    rfmSegment2 = rfmSegment2.assign(r_lg = lambda x: np.log10(x.monetary))

   
    rfmSegment2['month'] =  r['month']
    rfmSegment2['year'] =  r['year']
    rfmSegment2['customerid'] =  rfmSegment2.index
    
    df_final= df_final.append(rfmSegment2, ignore_index=True)



#df_final = df_final[df_final['customerid'].isin(bestCustomers['customerid'])].sort_values('monetary', ascending=False)
df_final = pd.merge(df_final, dfdatacomb, how='left', on=['rfm', 'rfm'])[['recency','frequency','monetary','rfm','customerid','month','year','sort']]


df_final['date']= df_final['month'].map(str) + " - " + df_final['year'].map(str)
dic = {}

rfmSegment['customerid'] = rfmSegment.index

for k, r in  rfmSegment.iterrows():
    
    #calculate score variation among last two month
    rfmSegmentLoc = df_final[(df_final['customerid']==r['customerid'])]    
    if len(rfmSegmentLoc.index) > 1:
        rfmSegment.loc[k, 'variation'] =  rfmSegmentLoc.iloc[len(rfmSegmentLoc)-1][['sort']].iloc[0]   - rfmSegmentLoc.iloc[len(rfmSegmentLoc)-2][['sort']].iloc[0]
    else:
        rfmSegment.loc[k,'variation'] = 0
    
    #create dictionary for detail chart
    dic.update({   str(int(r['customerid'])): {"customerid" : str(int(r['customerid'])) , "result":[
        {
        "labels": list(df_final[df_final['customerid']== r['customerid']] ['date']),
        'datasets': [{'label': str(r['customerid']) , 'data':list(df_final[df_final['customerid']== r['customerid']] ['sort']),  'lineTension': 0.1,
      'backgroundColor': 'rgba(75,192,192,0.4)',
      'borderColor': 'rgba(75,192,192,1)', }]
        },
        {
            "labels": list(df_final[df_final['customerid']== r['customerid']] ['date']),
            'datasets': [{'label': "Customer ID " + str(r['customerid']) , 'data': list(df_final[df_final['customerid']== r['customerid']] ['recency']), 'lineTension': 0.1,
                          'backgroundColor': 'rgba(75,192,192,0.4)',
                          'borderColor': 'rgba(75,192,192,1)', }]
        }
        ,
        {
            "labels": list(df_final[df_final['customerid']== r['customerid']] ['date']),
            'datasets': [{'label': "Customer ID " + str(r['customerid']) , 'data': list(df_final[df_final['customerid']== r['customerid']] ['frequency']), 'lineTension': 0.1,
                          'backgroundColor': 'rgba(75,192,192,0.4)',
                          'borderColor': 'rgba(75,192,192,1)', }]
        }
        ,
        {
            "labels": list(df_final[df_final['customerid']== r['customerid']] ['date']),
            'datasets': [{'label': "Customer ID " + str(r['customerid']) , 'data': list(df_final[df_final['customerid']== r['customerid']] ['monetary']), 'lineTension': 0.1,
                          'backgroundColor': 'rgba(75,192,192,0.4)',
                          'borderColor': 'rgba(75,192,192,1)', }]
        }
    ]}}
    )


with open('rfmcustomersTimeSeries.json', 'w') as fp:
    json.dump(dic, fp)




#%% variation among last 2 month
                  
    


#%% create json files

#create json for doughnut chart
rfmSegment['customerid']=rfmSegment.index
rfmSegment= pd.merge(rfmSegment, dfdatacomb, how='left', on=['rfm', 'rfm'])
rfmSegment.index=rfmSegment['customerid']
rfmSegment[['recency_total','frequency_total','monetary_total','customerid','sort', 'description', 'rfm', 'variation']].to_json("rfmcustomers.json", orient='records')

#create json for table
rfmSegment.groupby(['sort','description']).size().reset_index(name='counts').to_json("rfmSegment.json", orient='records')








