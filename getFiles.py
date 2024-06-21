from typing import *
import os
import glob
import math
import datetime
import subprocess


def get_video_length(filename:str):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of",
                                "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return float(result.stdout)


def date_from_name(filename:str):
    date, time = (filename.split('.')[0]).split('_')
    
    
    date_ = [int(i) for i in date.split('-')]
    date__ = [date_[2], date_[0], date_[1]]

    time_ = [int(i) for i in time.split('-')]
    
    t = datetime.datetime(
        year=date__[0],
        month=date__[1],
        day=date__[2],

        hour=time_[0],
        minute=time_[1],
        second=time_[2]
    )
    return t

def sortable_name(filename:str)->int:
    t = date_from_name(filename)
    b = datetime.datetime.fromtimestamp(0)
    return int((t-b).total_seconds())

def binary_search(arr:List[str], searchKey=str, s=0, e=None, baseFn=None)->int:
    e = e if e is not None else len(arr)

    if s>e or e<0 or s>=len(arr):
        return -1
    
    m = (s+e)//2

    if (arr[m] if baseFn is None else baseFn(arr[m])) == (searchKey if baseFn is None else baseFn(searchKey)):
        return m
    elif (arr[m] if baseFn is None else baseFn(arr[m])) > (searchKey if baseFn is None else baseFn(searchKey)):
        return binary_search(arr, searchKey, s, m-1, baseFn)
    else:
        return binary_search(arr, searchKey, m+1, e, baseFn)




def get_file_range(start_time:str, end_time:str, file_dir:str = "./testFiles")->List[str]:
    start_time_d = date_from_name(start_time)
    end_time_d = date_from_name(end_time)

    start_time_d -= datetime.timedelta(days=1)
    end_time_d += datetime.timedelta(days=1)

    file_list = []

    for i in range(0, 1 + int((end_time_d - start_time_d).total_seconds())//(3600*24)):
        f_list = glob.glob(os.path.join(file_dir, (start_time_d + datetime.timedelta(days=i)).strftime("%m-%d-%Y"), "*.ts"))
        file_list.extend(f_list)
    
    file_list = sorted(file_list, key=lambda x: sortable_name(os.path.basename(x)))

    return file_list


def get_valid_start_idx(start_time:str, file_list:List[str]):
    start_not_exact_flag = False
    if sortable_name(os.path.basename(file_list[-1])) < sortable_name(start_time):
        start_not_exact_flag = True
        return (len(file_list)-1, start_not_exact_flag)
    
    if sortable_name(os.path.basename(file_list[0])) > sortable_name(start_time):
        start_not_exact_flag = True
        return (0, start_not_exact_flag)
    


    search_idx_1 = binary_search(
        [os.path.basename(f) for f in file_list], start_time, baseFn=sortable_name
    )    
    if search_idx_1 != -1:
        return (search_idx_1, start_not_exact_flag)
    



    start_not_exact_flag = True
    idx = 0
    gap = int(math.sqrt(len(file_list))//1)
    while((idx < len(file_list)) and (sortable_name(os.path.basename(file_list[idx])) < sortable_name(start_time))):
        idx += gap
    
    idx = min(idx, len(file_list)-1)
    for i in range(max(idx-gap, 0), min(idx+gap, len(file_list))):
        if sortable_name(os.path.basename(file_list[i])) > sortable_name(start_time):
            return (i-1, start_not_exact_flag)
        

def get_valid_end_idx(end_time:str, file_list:List[str]):
    end_not_exact_flag = False
    if sortable_name(os.path.basename(file_list[-1])) < sortable_name(end_time):
        end_not_exact_flag = True
        return (len(file_list)-1, end_not_exact_flag)
    
    if sortable_name(os.path.basename(file_list[0])) > sortable_name(end_time):
        end_not_exact_flag = True
        return (0, end_not_exact_flag)
    


    search_idx_1 = binary_search(
        [os.path.basename(f) for f in file_list], end_time, baseFn=sortable_name
    )    
    if search_idx_1 != -1:
        return (search_idx_1, end_not_exact_flag)
    


    
    end_not_exact_flag = True
    idx = 0
    gap = int(math.sqrt(len(file_list))//1)
    while((idx < len(file_list)) and (sortable_name(os.path.basename(file_list[idx])) < sortable_name(end_time))):
        idx += gap
    
    idx = min(idx, len(file_list)-1)
    for i in range(max(idx-gap, 0), min(idx+gap, len(file_list))):
        if sortable_name(os.path.basename(file_list[i])) > sortable_name(end_time):
            return (i, end_not_exact_flag)
        





def get_files(start_time:str, end_time:str, file_dir="./testFiles"):
    file_list = get_file_range(start_time, end_time, file_dir)

    start_idx, start_flg = get_valid_start_idx(start_time, file_list=file_list)
    end_idx, end_flg = get_valid_end_idx(end_time, file_list=file_list)

    sum_of_video_len = sum([get_video_length(f_v) for f_v in file_list[start_idx:end_idx]])
    duration = (date_from_name(os.path.basename(file_list[end_idx])) - date_from_name(os.path.basename(file_list[start_idx]))).total_seconds()

    return (
        file_list[start_idx:end_idx], 
        "Ends Not Exact" if (start_flg or end_flg) else "Ends Exact",
        "Incomplete" if (duration < sum_of_video_len) else "Complete"
        )



start_time = "06-17-2024_23-44-00"
end_time = "06-18-2024_00-30-00"

print(
    get_files(start_time, end_time, "./testFiles")
)

