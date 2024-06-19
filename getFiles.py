from typing import *
import os
import glob
import math
import datetime
import subprocess


def get_video_length(filename):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of",
                                "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return float(result.stdout)


def sortable_name(filename:str)->int:
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

def get_valid_start(searchTime:str, file_dir:str = "./testFiles"):

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
        if sortable_name(os.path.basename(file_list[i])) == sortable_name(f"{searchTime}.ts"):
            return os.path.basename(file_list[i])
        if sortable_name(os.path.basename(file_list[i])) > sortable_name(f"{searchTime}.ts"):
            return os.path.basename(file_list[i-1])
        
def get_valid_end(searchTime:str, file_dir:str = "./testFiles"):

    file_list = glob.glob(os.path.join(file_dir, "*.ts"))
    file_list = sorted(file_list, key=lambda x: sortable_name(os.path.basename(x)))


    if (sortable_name(os.path.basename(file_list[0])) > sortable_name(f"{searchTime}.ts")):
        return os.path.basename(file_list[0])
    if (sortable_name(os.path.basename(file_list[-1])) < sortable_name(f"{searchTime}.ts")):
        return os.path.basename(file_list[-1])
    

    idx = 0
    gap = int(math.sqrt(len(file_dir))//1)
    while((idx < len(file_list)) and (sortable_name(os.path.basename(file_list[idx])) < sortable_name(searchTime))):
        idx += gap
    
    idx = min(idx, len(file_list)-1)

    for i in range(max(idx-gap, 0), min(idx+gap, len(file_list)),1):
        # if sortable_name(os.path.basename(file_list[i])) >= sortable_name(searchTime):
        if sortable_name(os.path.basename(file_list[i])) == sortable_name(searchTime):
            return os.path.basename(file_list[i])
        if sortable_name(os.path.basename(file_list[i])) > sortable_name(searchTime):
            return os.path.basename(file_list[i-1])
        

def get_valid_files_byStamp(searchTime_1:str, searchTime_2:str, file_dir:str = "./testFiles")->List[str]:
    searchTime_1 = get_valid_start(f"{searchTime_1}.ts", file_dir)
    searchTime_2 = get_valid_end(f"{searchTime_2}.ts", file_dir)

    file_list = glob.glob(os.path.join(file_dir, "*.ts"))
    file_list = sorted(file_list, key=lambda x: sortable_name(os.path.basename(x)))

    search_idx_1 = binary_search(
        [os.path.basename(f) for f in file_list], searchTime_1, baseFn=sortable_name
    )
    search_idx_2 = binary_search(
        [os.path.basename(f) for f in file_list], searchTime_2, baseFn=sortable_name
    )

    return file_list[search_idx_1:search_idx_2+1]

def get_valid_files_byGap(searchTime_1:str, minutes_gap:int=5, file_dir:str = "./testFiles")->List[str]:
    start_time, end_time = datetime.datetime.fromtimestamp(sortable_name(searchTime_1) - (minutes_gap*60)).strftime("%m-%d-%Y_%H-%M-%S"), datetime.datetime.fromtimestamp(sortable_name(searchTime_1) + (minutes_gap*60)).strftime("%m-%d-%Y_%H-%M-%S")

    start_time = get_valid_start(start_time)
    end_time = get_valid_end(end_time)

    return get_valid_files_byStamp(start_time, end_time, file_dir)


def get_videos(searchTime_1:str, minutes_gap:int=5, file_dir:str = "./testFiles")->Tuple[List[str], bool]:
    video_files = get_valid_files_byGap(searchTime_1, minutes_gap = minutes_gap, file_dir = file_dir)
    video_len = sum([get_video_length(v) for v in video_files[:-1]])
    # duration_len = (sortable_name(os.path.basename(video_files[-1]))-sortable_name(os.path.basename(video_files[0])))
    duration_len = (sortable_name(searchTime_1)+minutes_gap)-sortable_name(os.path.basename(video_files[0]))

    return (video_files, not (duration_len > video_len))





# 00:00.ts
# 00:03.ts    
# 00:06.ts
# 00:08.ts
# 00.10.ts
# 00.15.ts

# 00:07 -> 00:02-00:12

file_dir = "./testFiles" # dir where ts files are held

# # mm-dd-yyyy_hh-MM-SS

print(get_videos('06-19-2024_00-12-00', minutes_gap = 4, file_dir = file_dir))
# print(get_valid_files_byGap('06-19-2024_00-12-00', minutes_gap = 4, file_dir = file_dir))


