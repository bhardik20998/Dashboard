from django.shortcuts import render
from rest_framework.response import Response
from io import BytesIO
import pandas as pd
from django.http import JsonResponse, HttpResponse
from pymongo import MongoClient
from .functions import SaveDataframe, FetchDataframe, UpdateDataFrame, SortColumn, SortArray, sortArrayParan, inner, delete_all_entries
import json
import numpy as np
import math
import re
from itertools import product
from bson import json_util

client = MongoClient('mongodb://localhost:27017/')
db = client['Dashboard']
# Create your views here.
required_columns = ['Age_Bucket', 'Zone_Bucket','ABB_TIMES_EMI_Bucket','RLTV_Bucket','Score_Bucket','CIBIL_Bucket','STATE','GBTAG_30P_12M_WM','GBTAG_30P_6M_WM','GBTAG_30P_9M_WM','GBTAG_60P_12M_WM','GBTAG_90P_12M_WM','GBTAG_90P_18M_WM','GBTAG_90P_24M_WM','Coincidental30+_fin','Coincidental60+_fin','Coincidental90+_fin','GB_Total','ASSET_MAKE']

def UploadFunction(request):

    delete_all_entries("Master_Data")


    
    df=pd.read_excel(BytesIO(((request.FILES['file']).open()).read()))

    flag=True

    for x in required_columns:
        if(x in df.columns):
            flag=True
        else:
            print(x)
            flag=False
            break
    
    

    

    if flag:
        df['FinalResult']="AR"
        if(SaveDataframe(df,"Master_Data")):
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)


        

        


    else:
        print("DataFrame is missing some required columns.")
        return JsonResponse({'error': "Columns in excel are not correct!"}, status=400)
    



def Summary(request):

    df=FetchDataframe("Master_Data").dropna()
    if(len(df)>0):
        unique_Age_Buckets = (df['Age_Bucket'].unique()).tolist()
        unique_RLTV_Buckets = (df['RLTV_Bucket'].unique()).tolist()
        unique_Zone_Buckets = (df['Zone_Bucket'].unique()).tolist()
        unique_State_Buckets = (df['STATE'].unique()).tolist()
        unique_ABBEMI_Ratio_Buckets = (df['ABB_TIMES_EMI_Bucket'].unique()).tolist()
        unique_ASSET_MAKE = (df['ASSET_MAKE'].unique()).tolist()
        filter_values={'Age_Bucket':unique_Age_Buckets,'RLTV_Bucket':unique_RLTV_Buckets,'Zone_Bucket':unique_Zone_Buckets,'ABB_TIMES_EMI_Bucket':unique_ABBEMI_Ratio_Buckets, 'STATE':unique_State_Buckets,'ASSET_MAKE':unique_ASSET_MAKE}



        if(request.body.decode('utf-8')!=''):

            dropDownDict=(json.loads(request.body.decode('utf-8')))['dropDownDict']


            Selection=(json.loads(request.body.decode('utf-8')))['Selection']

            filter_dict=((json.loads(request.body.decode('utf-8')))['Filters'])


            changes=(json.loads(request.body.decode('utf-8')))['changed']





            


            if(filter_dict!={}):
                for key in filter_dict:
                    for k in filter_dict[key]:
                        if(filter_dict[key][k]==False):
                            df = df[df[key] != k]
            
            onlyTrue={}

            for x in filter_dict:
                onlyTrue[x]=[]
            for x in filter_dict:
               for y in filter_dict[x]:
                   if filter_dict[x][y]==True:
                       onlyTrue[x].append(y)
            
            # combinations = list(product(*onlyTrue.values()))

            # result_array = [{key: value for key, value in zip(onlyTrue.keys(), combination)} for combination in combinations]

                       
           
            if changes=='dropdownValues':

                if(len(onlyTrue)>0):
                
                    # print("hello")
                    for i in list( dropDownDict.keys()):
                        Cibil_Bucket =(i.split('_')[0])
                        Score_Bucket=(i.split('_')[1])
                        value=(dropDownDict[i])
                        if value in  ['AA','AR','L1','L2','L3','L4']:
                            db['Master_Data'].update_many({'Score_Bucket':Score_Bucket,"CIBIL_Bucket":Cibil_Bucket, 'Age_Bucket':{'$in': onlyTrue['Age_Bucket']} , 'RLTV_Bucket':{'$in': onlyTrue['RLTV_Bucket']}, 'Zone_Bucket':{'$in': onlyTrue['Zone_Bucket']}, 'ABB_TIMES_EMI_Bucket':{'$in': onlyTrue['ABB_TIMES_EMI_Bucket']},'STATE':{'$in': onlyTrue['STATE']} }, {'$set': {"FinalResult":value}}, upsert=True)

            df=FetchDataframe("Master_Data").dropna()

            if(filter_dict!={}):
                for key in filter_dict:
                    for k in filter_dict[key]:
                        if(filter_dict[key][k]==False):
                            df = df[df[key] != k]
            


            bads = df.groupby('FinalResult').agg({ 'GBTAG_30P_12M_WM': 'sum','GBTAG_30P_6M_WM': 'sum','GBTAG_30P_9M_WM': 'sum','GBTAG_60P_12M_WM': 'sum','GBTAG_90P_12M_WM': 'sum','GBTAG_90P_18M_WM': 'sum','GBTAG_90P_24M_WM': 'sum','Coincidental30+_fin': 'sum','Coincidental60+_fin': 'sum','Coincidental90+_fin': 'sum','GB_Total': 'sum','GB_Total':'sum'}).reset_index()
           
           # List of columns to calculate percentages
            columns_to_percentage = ['GBTAG_30P_12M_WM','GBTAG_30P_6M_WM','GBTAG_30P_9M_WM','GBTAG_60P_12M_WM','GBTAG_90P_12M_WM','GBTAG_90P_18M_WM','GBTAG_90P_24M_WM','Coincidental30+_fin','Coincidental60+_fin','Coincidental90+_fin']

            # Calculate percentages
            df_percentage = (bads[columns_to_percentage].div(bads['GB_Total'], axis=0) * 100).round(2)
            GB_Total_Sum=bads['GB_Total'].sum()

            
           

            # Combine 'FinalResult' with the percentages DataFrame

            result_df = pd.concat([bads['FinalResult'],((bads['GB_Total']/GB_Total_Sum)*100).round(2), df_percentage], axis=1)

          

                    
           
           
            # Melt the DataFrame
            melted_df = result_df.melt(id_vars='FinalResult', var_name='Bad Definations', value_name='Value')

            # Pivot the melted DataFrame
            pivot_df = melted_df.pivot_table(index='Bad Definations', columns='FinalResult', values='Value', aggfunc='sum')

            pivot_df=pivot_df.reset_index()
            # if(UpdateDataFrame('Master_Data',df)):
            #     return HttpResponse(status=200)
            # else:

            pivot_df = pivot_df.to_json(orient='records')



            
            df["Joined_Key"]=df['CIBIL_Bucket']+'_'+df['Score_Bucket']

            

            # Calculate the mean for each group
            values = df.groupby('Joined_Key')['FinalResult'].apply(lambda x: ' / '.join(pd.unique(x))).reset_index()
            dropDownDict=values.set_index('Joined_Key')['FinalResult'].to_dict()

            

            




            
            if(Selection!='GB_Total'):
                crosstab_selection = pd.crosstab(index=df['CIBIL_Bucket'], columns=df['Score_Bucket'], values=df[Selection], aggfunc='sum',margins=True, margins_name='Total')
                crosstab_gb_total = pd.crosstab(index=df['CIBIL_Bucket'], columns=df['Score_Bucket'], values=df['GB_Total'], aggfunc='sum',margins=True, margins_name='Total')

                # Calculate the percentage by dividing the two crosstabs
                percentage_result = (crosstab_selection / crosstab_gb_total) * 100

                # Reset index to have a clean DataFrame
                percentage_result.reset_index(inplace=True)

                # If needed, replace NaN or inf values with 0
                percentage_result.fillna(0, inplace=True)
                percentage_result.replace([np.inf, -np.inf], 0, inplace=True)
                # Convert the DataFrame to a string with percentage values
                percentage_result = percentage_result.map(lambda x: '{:.2f}%'.format(x) if isinstance(x, (int, float)) else x)

                percentage_result=SortColumn(percentage_result,"CIBIL_Bucket")
                total_applications = percentage_result.to_json(orient='records')
                filter_values = {key: [value for value in values if not (isinstance(value, float) and np.isnan(value))] for key, values in filter_values.items()}

                if any('<' in bucket.strip() for bucket in filter_values['Age_Bucket']):
                    index_of_less_than = next(i for i, bucket in enumerate(filter_values['Age_Bucket']) if '<' in bucket.strip())
                    filter_values['Age_Bucket'].insert(0, filter_values['Age_Bucket'].pop(index_of_less_than))
                if any('<' in bucket.strip() for bucket in filter_values['RLTV_Bucket']):
                    index_of_less_than = next(i for i, bucket in enumerate(filter_values['RLTV_Bucket']) if '<' in bucket.strip())
                    filter_values['RLTV_Bucket'].insert(0, filter_values['RLTV_Bucket'].pop(index_of_less_than))
                if any('<' in bucket.strip() for bucket in filter_values['ABB_TIMES_EMI_Bucket']):
                    index_of_less_than = next(i for i, bucket in enumerate(filter_values['ABB_TIMES_EMI_Bucket']) if '<' in bucket.strip())
                    filter_values['ABB_TIMES_EMI_Bucket'].insert(0, filter_values['ABB_TIMES_EMI_Bucket'].pop(index_of_less_than))


                            
                
                return JsonResponse({'total_applications': total_applications,"filter_values":filter_values,'dropDownDict':dropDownDict,"KPIs Table":pivot_df})
        

        total_applications = pd.DataFrame((pd.crosstab(index=df['CIBIL_Bucket'], columns=df['Score_Bucket'], values=df['GB_Total'], aggfunc='sum',margins=True, margins_name='Total')).to_records())
        total_applications=SortColumn(total_applications,"CIBIL_Bucket")
        temp=list(total_applications.columns.to_numpy())
        temp.pop(0)
        total_applications.columns=(["CIBIL_Bucket"]+inner(temp))
        total_applications = total_applications.to_json(orient='records')
        
       
        filter_values = {key: [value for value in values if not (isinstance(value, float) and np.isnan(value))] for key, values in filter_values.items()}
        if any('<' in bucket.strip() for bucket in filter_values['Age_Bucket']):
            index_of_less_than = next(i for i, bucket in enumerate(filter_values['Age_Bucket']) if '<' in bucket.strip())
            filter_values['Age_Bucket'].insert(0, filter_values['Age_Bucket'].pop(index_of_less_than))
        if any('<' in bucket.strip() for bucket in filter_values['RLTV_Bucket']):
            index_of_less_than = next(i for i, bucket in enumerate(filter_values['RLTV_Bucket']) if '<' in bucket.strip())
            filter_values['RLTV_Bucket'].insert(0, filter_values['RLTV_Bucket'].pop(index_of_less_than))
        if any('<' in bucket.strip() for bucket in filter_values['ABB_TIMES_EMI_Bucket']):
            index_of_less_than = next(i for i, bucket in enumerate(filter_values['ABB_TIMES_EMI_Bucket']) if '<' in bucket.strip())
            filter_values['ABB_TIMES_EMI_Bucket'].insert(0, filter_values['ABB_TIMES_EMI_Bucket'].pop(index_of_less_than))

        return JsonResponse({'total_applications': total_applications,"filter_values":(filter_values),"dropDownDict":dropDownDict,"KPIs Table":pivot_df})
    else:
        return JsonResponse({})



def Table_Summary(request):

    
     

    if(request.body.decode('utf-8')!=''):
        

            dropDownDict=json.loads(request.body.decode('utf-8'))
            df=FetchDataframe("Master_Data")
            for i in list( dropDownDict.keys()):
                Score_Bucket=(i.split('_')[0])
                Cibil_Bucket=(i.split('_')[1])

                value=(dropDownDict[i])
                # df.loc[(df['Score_Bucket']==Score_Bucket)&(df['CIBIL_Bucket']==Cibil_Bucket),'FinalResult']=value

                db['Master_Data'].update_many({'Score_Bucket':Score_Bucket,"CIBIL_Bucket":Cibil_Bucket}, {'$set': {"FinalResult":value}}, upsert=True)

            

            df = df.groupby('FinalResult').agg({ 'GBTAG_30P_12M_WM': 'sum','GBTAG_30P_6M_WM': 'sum','GBTAG_30P_9M_WM': 'sum','GBTAG_60P_12M_WM': 'sum','GBTAG_90P_12M_WM': 'sum','GBTAG_90P_18M_WM': 'sum','GBTAG_90P_24M_WM': 'sum','Coincidental30+_fin': 'sum','Coincidental60+_fin': 'sum','Coincidental90+_fin': 'sum','GB_Total': 'sum'}).reset_index()
           
           # List of columns to calculate percentages
            columns_to_percentage = ['GBTAG_30P_12M_WM','GBTAG_30P_6M_WM','GBTAG_30P_9M_WM','GBTAG_60P_12M_WM','GBTAG_90P_12M_WM','GBTAG_90P_18M_WM','GBTAG_90P_24M_WM','Coincidental30+_fin','Coincidental60+_fin','Coincidental90+_fin', 'GB_Total']

            # Calculate percentages
            df_percentage = (df[columns_to_percentage].div(df['GB_Total'], axis=0) * 100).round(2)

            # Combine 'FinalResult' with the percentages DataFrame
            result_df = pd.concat([df['FinalResult'], df_percentage], axis=1)

                    
           
           
            # Melt the DataFrame
            melted_df = result_df.melt(id_vars='FinalResult', var_name='Bad Definations', value_name='Value')

            # Pivot the melted DataFrame
            pivot_df = melted_df.pivot_table(index='Bad Definations', columns='FinalResult', values='Value', aggfunc='sum')

            pivot_df=pivot_df.reset_index()
            # if(UpdateDataFrame('Master_Data',df)):
            #     return HttpResponse(status=200)
            # else:

            pivot_df = pivot_df.to_json(orient='records')
            return JsonResponse({"KPIs Table":pivot_df})
            
        
            
    else:
        return HttpResponse(status=500)
    

def DownloadData(request):
    try:
        # Connect to your MongoDB server
       
        collection = FetchDataframe('Master_Data')

        

        collection=((collection.drop(columns='_id').dropna())).to_json(orient='records')
        

        return JsonResponse({'data': collection})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
         

            




    
     

    

    

    
 