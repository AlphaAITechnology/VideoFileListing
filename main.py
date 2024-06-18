from typing import *
import os
import glob
import math
import re


def sortable_name(filename:str)->str:
    date, time = (filename.split('.')[0]).split('_')
    date_ = date.split('-')
    date__ = "".join([str(int(date_[-1])-1960), date_[0], date_[1]])

    time_ = [int(i) for i in time.split('-')]
    time__ = f"{((time_[0]*3600)+(time_[1]*60)+time_[2]):05}"

    return f"{date__}_{time__}"

def binarySearch(arr:List[str], searchKey=str, s=0, e=None, baseFn=None)->int:
    e = e if e is not None else len(arr)

    if s>e or e<0 or s>=len(arr):
        return -1
    
    m = (s+e)//2

    if (arr[m] if baseFn is None else baseFn(arr[m])) == (searchKey if baseFn is None else baseFn(searchKey)):
        return m
    elif (arr[m] if baseFn is None else baseFn(arr[m])) > (searchKey if baseFn is None else baseFn(searchKey)):
        return binarySearch(arr, searchKey, s, m-1, baseFn)
    else:
        return binarySearch(arr, searchKey, m+1, e, baseFn)



# def getValidFiles_byGap(searchTime:str, searchGap:int=1, file_dir:str = "./testFiles")->List[str]:
#     file_list = glob.glob(os.path.join(file_dir, "*.ts"))
#     file_list = sorted(file_list, key=lambda x: sortable_name(os.path.basename(x)))

#     search_idx = binarySearch(
#         [os.path.basename(f) for f in file_list], searchTime, baseFn=sortable_name
#     )

#     if search_idx < 0:
#         return []
#     else:
#         return file_list[search_idx:min(search_idx+searchGap, len(file_list))]


def getValidStart(searchTime:str, file_dir:str = "./testFiles"):

    file_list = glob.glob(os.path.join(file_dir, "*.ts"))
    file_list = sorted(file_list, key=lambda x: sortable_name(os.path.basename(x)))


    if (sortable_name(os.path.basename(file_list[0])) > sortable_name(f"{searchTime}.ts")):
        return os.path.basename(file_list[0])
    if (sortable_name(os.path.basename(file_list[-1])) < sortable_name(f"{searchTime}.ts")):
        return os.path.basename(file_list[-1])
    

    idx = 0
    gap = int(math.sqrt(len(file_dir))//1)
    while((idx < len(file_list)) and (sortable_name(os.path.basename(file_list[idx])) < sortable_name(f"{searchTime}.ts"))):
        idx += gap
    
    idx = min(idx, len(file_list)-1)

    for i in range(max(idx-gap, 0), min(idx+gap, len(file_list))):
        if sortable_name(os.path.basename(file_list[i])) > sortable_name(f"{searchTime}.ts"):
            return os.path.basename(file_list[i-1])
        
def getValidEnd(searchTime:str, file_dir:str = "./testFiles"):

    file_list = glob.glob(os.path.join(file_dir, "*.ts"))
    file_list = sorted(file_list, key=lambda x: sortable_name(os.path.basename(x)))


    if (sortable_name(os.path.basename(file_list[0])) > sortable_name(f"{searchTime}.ts")):
        return os.path.basename(file_list[0])
    if (sortable_name(os.path.basename(file_list[-1])) < sortable_name(f"{searchTime}.ts")):
        return os.path.basename(file_list[-1])
    

    idx = 0
    gap = int(math.sqrt(len(file_dir))//1)
    while((idx < len(file_list)) and (sortable_name(os.path.basename(file_list[idx])) < sortable_name(f"{searchTime}.ts"))):
        idx += gap
    
    idx = min(idx, len(file_list)-1)

    for i in range(max(idx-gap, 0), min(idx+gap, len(file_list))):
        if sortable_name(os.path.basename(file_list[i])) > sortable_name(f"{searchTime}.ts"):
            return os.path.basename(file_list[i])

def getValidFiles_byStamp(searchTime_1:str, searchTime_2:str, file_dir:str = "./testFiles")->List[str]:
    searchTime_1 = getValidStart(f"{searchTime_1}.ts", file_dir)
    searchTime_2 = getValidEnd(f"{searchTime_2}.ts", file_dir)

    file_list = glob.glob(os.path.join(file_dir, "*.ts"))
    file_list = sorted(file_list, key=lambda x: sortable_name(os.path.basename(x)))

    search_idx_1 = binarySearch(
        [os.path.basename(f) for f in file_list], searchTime_1, baseFn=sortable_name
    )
    search_idx_2 = binarySearch(
        [os.path.basename(f) for f in file_list], searchTime_2, baseFn=sortable_name
    )

    return file_list[search_idx_1:search_idx_2+1]




file_dir = "./testFiles" # dir where ts files are held
# mm-dd-yyyy_hh-MM-SS
print(
    getValidFiles_byStamp("11-01-2024_01-03-20", "11-01-2024_01-27-00")
)
