import pandas as pd
from collections import defaultdict
from functools import reduce


with open("sample.log","r") as f:
    x = f.read()
    x.replace(" ",",")
    lines = x.split('\n')
    formatted_data=[]
    for i in lines:
        parts=i.split()
        if len(parts) >= 7:
            ip=parts[0]
            time_req=parts[3].lstrip('[')
            status=parts[6]
            formatted_data.append([time_req, status, ip])
    columns=['Timestamp','Status','Ip']
    df=pd.DataFrame(formatted_data,columns=columns)
    df['Timestamp']=pd.to_datetime(df['Timestamp'], format='%d/%b/%Y:%H:%M:%S')
    req=defaultdict(list)
    for index,row in df.iterrows():
        ip = row['Ip']
        info = row['Timestamp']
        req[ip].append(info)
    req_per_sec={}
    for ip in req:
        time_list=req[ip]
        req_array=[]
        if len(time_list)>1:
            time_list.sort()
            for i in range(len(time_list)-1):
                gap = (time_list[i+1] - time_list[i]).total_seconds()
                req_array.append(gap)
            total_time=reduce(lambda a,b:a+b,req_array)
            total_intervals=len(req_array)
            req_per_sec[ip]=total_time/total_intervals
    banned_ips = []
    hold=[]
    for i in req_per_sec:
        total_hits = len(req[i])
        if req_per_sec[i]<0.2 and total_hits>10:
            print(f'The IP address {i} is a BOT ban it.')
            banned_ips.append(i)
        elif 0.2<=req_per_sec[i]<1.0:
            print(f'The IP address {i} likely to be a scrapper hold it.')
            hold.append(i)
        else:
            print(f"This ip {i} might be normal human")
    for i in hold:
        if i in req:
            if len(req[i])>20:
                print(f'Ban the IP {i}')
                banned_ips.append(i)
            else:
                print("Not a bot")
    unique_bans = set(banned_ips)
    with open('Blacklist.txt','a') as f:
        for ip in unique_bans:
            f.write(ip+"\n")
        
            

    


    

