# -*- coding: utf-8 -*-

# General syntax to import specific functions in a library: 
##from (library) import (specific library function)
from pandas import DataFrame, read_csv

# General syntax to import a library but no functions: 
##import (library) as (give the library a nickname/alias)
import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number
import os

#folder = "E:\\python\\F4838\\data\\all_temp\\"
folder = "E:\\python\\F4838\\data\\sh600399\\"
filelist = os.listdir(folder)
print(filelist)
print ("日期-00-00.csv","power"+"\t"+"成交量"+"\t"+"连续买入量"+"\t"+"连续卖出量"+"\t"+"小单差"+"\t"+"小单买入量"+"\t"+"四个点的价格"+"\t"+"小单比例")         

com_list = []
com_rate = 0   
com_all = 0    
power_list = []
power_rate = 0
for file in filelist:
    df = pd.read_csv(folder+file,encoding="gbk",sep="\t")
    #print (df.columns)
    #Index(['成交时间', '成交价', '价格变动', '成交量(手)', '成交额(元)', '性质'], dtype='object')
    power = 0
    small_bill_buy = 0;
    small_bill_sell = 0
    small_bill_cha = 0;
    p_index = 0;
    p_all_vol = 0;
    
    # 8个区间价格 和买卖量.
    m_b=0
    m_1000 = 0
    m_1030 = 0
    m_1100 = 0
    m_e=0
    a_1330 = 0
    a_b=0
    a_1430 = 0
    a_e=0
    q8_1_buy = 0;
    q8_1_sell = 0
    q8_2_buy =0
    q8_2_sell =0
    q8_3_buy=0
    q8_3_sell=0
    q8_4_buy=0
    q8_4_sell=0
    q8_5_buy=0
    q8_5_sell=0
    q8_6_buy=0
    q8_6_sell=0
    q8_7_buy=0
    q8_7_sell=0
    q8_8_buy=0
    q8_8_sell=0    
    
    
    # 连续买入变量 
    lianxu_buy = 0;
    lianxu_buy_vol = 0;
    lianxu_sell = 0;
    lianxu_sell_vol = 0;
    all_sell_vol = 0;
    all_buy_vol = 0;
    
    mf = 0;
    all_amount = 0;
    ic = 0; 
    p_m = 0
    #  主动性买单和被东兴买单
    zhudong_buy = 0;
    beidong_buy = 0;
    
    #异常情况
    exceptions = []
    exception_num = 0
    exception_vol = 0
    if (df.size > 10):
        for index,row in df.iterrows():
            v_date = row['成交时间']
            open_date = v_date.split(":")[0]+v_date.split(":")[1]
            v_price = row['成交价']
            v_change = row['价格变动']
            if v_change == "--" :
                v_change = "0" 
            v_vol = row['成交量(手)']
            v_amount = row['成交额(元)']
            v_type = row['性质']
            
            p_all_vol += v_vol;
            #1-------------power--------------------
            this_power = float(v_change) * v_vol
            if open_date != "0925":
                power +=this_power
                
            if v_amount <= 40000 :
                if v_type == "买盘" :
                   small_bill_buy +=v_vol
                if v_type == "卖盘" :
                   small_bill_sell +=v_vol
                   
           #3------------总笔数--------------------
            p_index = p_index + 1
            #4-------------4个区价格
            cj_date = v_date.split(":")[0]+v_date.split(":")[1]+v_date.split(":")[2];
            #print(cj_date)
            if open_date == "0925":
               m_b = v_price
            if open_date == "1130":
                m_e = v_price
            if open_date == "1400":
                a_b = v_price
            if open_date == "1500":
                a_e = v_price
            #5 --连续买入
            if v_type == "买盘" :  
                lianxu_buy = lianxu_buy + 1
                lianxu_buy_vol += v_vol
                if (lianxu_sell >=5):
                    all_sell_vol += lianxu_sell_vol
                
                lianxu_sell = 0;
                lianxu_sell_vol  = 0    
            if v_type == "卖盘" :
                
                lianxu_sell = lianxu_sell + 1
                lianxu_sell_vol += v_vol
                if (lianxu_buy >=5):
                    all_buy_vol += lianxu_buy_vol
                lianxu_buy = 0;
                lianxu_buy_vol = 0    
            #6 ---mf，资金流净额:资金流金额。正表示流入、负表示流出 
            #7ic，资金流信息含量:abs（资金流净额/交易额）。ic>10%表明指标的信息含量较高。         
            #8mfp，资金流杠杆倍数:abs（流通市值/资金流净额）。用于衡量资金流的撬动效应。
            if float(v_change) > 0 :
               mf = mf + v_amount
            if float(v_change) < 0:
               mf = mf - v_amount
            if float(v_change) == 0:
                if v_type == "买盘" :
                   p_m += v_amount
                if v_type == "卖盘" :
                   p_m -= v_amount
               
            #主被动买单
            if v_amount >= 400000 :
                if v_type == "买盘" :
                   zhudong_buy +=v_vol
                if v_type == "卖盘" :
                   beidong_buy +=v_vol
            
            
            all_amount += v_amount
            
            
            #8个区间
            if float(open_date) <= float("1000") : 
                if v_type == "买盘" :
                   q8_1_buy += v_vol
                if v_type == "卖盘" :
                   q8_1_sell += v_vol
            if float(open_date) > float("1000") and float(open_date) <= float("1030") : 
                if v_type == "买盘" :
                   q8_2_buy += v_vol
                if v_type == "卖盘" :
                   q8_2_sell += v_vol
            if float(open_date) > float("1030") and float(open_date) <= float("1100") : 
                if v_type == "买盘" :
                   q8_3_buy += v_vol
                if v_type == "卖盘" :
                   q8_3_sell += v_vol
            if float(open_date) > float("1100") and float(open_date) <= float("1130") : 
                if v_type == "买盘" :
                   q8_4_buy += v_vol
                if v_type == "卖盘" :
                   q8_4_sell += v_vol
            if float(open_date) > float("1130") and float(open_date) <= float("1330") : 
                if v_type == "买盘" :
                   q8_5_buy += v_vol
                if v_type == "卖盘" :
                   q8_5_sell += v_vol
            if float(open_date) > float("1330") and float(open_date) <= float("1400") : 
                if v_type == "买盘" :
                   q8_6_buy += v_vol
                if v_type == "卖盘" :
                   q8_6_sell += v_vol
            if float(open_date) > float("1400") and float(open_date) <= float("1430") : 
                if v_type == "买盘" :
                   q8_7_buy += v_vol
                if v_type == "卖盘" :
                   q8_7_sell += v_vol
            if float(open_date) > float("1430") and float(open_date) <= float("1500") : 
                if v_type == "买盘" :
                   q8_8_buy += v_vol
                if v_type == "卖盘" :
                   q8_8_sell += v_vol
            #移动平均
            #ma_5 = pd.rolling_mean(v_price,5)
                   
            #异常情况
            #if v_type == "卖盘" :
            #    exceptions.append(v_price)
            #if len(exceptions) == 2 :
            #    pre_price = exceptions
        #盈利 高于收盘价，低于收盘价
        p_win_hc = 0
        p_lose_lc = 0
        for index,row in df.iterrows():
            v_price = row['成交价']
            v_vol = row['成交量(手)'] * 100
            if v_price >= a_e:
                p_win_hc += (a_e - v_price)* v_vol
            if v_price < a_e:
                p_lose_lc +=(a_e - v_price)* v_vol
        #数据分组
        group_price = df.groupby('成交价') 
        group_vol = group_price[u'成交量(手)']
        #print(group_vol)
        big_end = df[df[u'成交价']>a_e]
        small_end = df[df[u'成交价']<=a_e]
        #big_end.groupby('性质')[u'成交量(手)'].sum()
        #print("高于收盘价成交量:",big_end.groupby('成交时间')[u'成交量(手)'].sum())
        #print("低于收盘价成交量:",small_end.groupby('成交时间')[u'成交量(手)'].sum())
        small_bill_cha = small_bill_buy - small_bill_sell 
        if p_all_vol > 0:          
            small_rate = (small_bill_buy + small_bill_sell )/p_all_vol
        if all_amount > 0:
            ic = mf / all_amount;        
        #print (small_bill_cha)  
        #if power > 0 :
        power_list.append(power)
        com_list.append(a_e)
        com_all += 1
        if len(com_list) == 2:  
           #print(com_list,power_list) 
           if com_list[1] > com_list[0] and power_list[0] > 0:
              com_rate +=1
           if small_bill_cha > 0   :
              power_rate+=1 
           com_list.remove(com_list[0])
           power_list.remove(power_list[0])
        #print (com_rate,com_all,power_rate)
        #if power_rate > 0 :
            #print(com_rate/power_rate)
        print (file,format(power,'.2f')+"["+format(p_win_hc,'.2f')+":"+format(p_lose_lc,'.2f') +"],["+str(zhudong_buy)+":"+str(beidong_buy)+"]"+ "\t"+str(mf)+":"+str(p_m)+"\t"+format(ic,'.2f')+"\t"+ str(p_all_vol) +"\t"+str(all_buy_vol)+"\t"+str(all_sell_vol)+"\t"+ "\t"+ str(small_bill_cha) + "\t"+str(small_bill_buy)+"\t ["+str(m_b)+","+str(m_e)+","+str(a_b)+","+str(a_e)+"]" +str(small_rate)) 
        print (str(q8_1_buy)+":"+str(q8_1_sell)+","+str(q8_2_buy)+":"+str(q8_2_sell)+","+str(q8_3_buy)+":"+str(q8_3_sell)+","+str(q8_4_buy)+":"+str(q8_4_sell)+","+str(q8_5_buy)+":"+str(q8_5_sell)+","+str(q8_6_buy)+":"+str(q8_6_sell)+","+str(q8_7_buy)+":"+str(q8_7_sell)+","+str(q8_8_buy)+":"+str(q8_8_sell))
       