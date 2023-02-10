# SOURCES 

# https://www.javatpoint.com/monitoring-devices-using-python (get_storage_info())
# https://www.thepythoncode.com/article/make-a-network-usage-monitor-in-python  (get_network_info())
# https://stackoverflow.com/questions/276052/how-to-get-current-cpu-and-ram-usage-in-python  (get_compute_info())





import psutil  

def getSize(bytes, suffix = "B"):  

    the_factor = 1024  
    for the_unit in ["", "K", "M", "G", "T", "P"]:  
        if bytes < the_factor:  
            return f"{bytes:.2f}{the_unit}{suffix}"  
        bytes /= the_factor  

def get_storage_info():
    print( "Hard Disk Information\nPartitions and Usage:")  


    the_partitions = psutil.disk_partitions()  
    for the_partition in the_partitions:  
        print("Device: ", the_partition.device)  
        print("Partition Mount point: ", the_partition.mountpoint)  
        print("Partition File system type: ", the_partition.fstype)  
        try:  
            partitionUsage = psutil.disk_usage(the_partition.mountpoint)  
        except PermissionError:  
            continue  
        print("Total Size: ", getSize(partitionUsage.total))  
        print("Used Space: ", getSize(partitionUsage.used))  
        print("Free hard disk Space", getSize(partitionUsage.free))  
        print("Hard disk Used Percentage: ", partitionUsage.percent, "%")  
        if(partitionUsage.percent > 82):  
            print("Disk space nearing full")  



def get_network_info():
        
    import psutil
    import time
    import os
    import pandas as pd

    UPDATE_DELAY = 1 # in seconds

    def get_size(bytes):
        """
        Returns size of bytes in a nice format
        """
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if bytes < 1024:
                return f"{bytes:.2f}{unit}B"
            bytes /= 1024

    
    
    # get the network I/O stats from psutil on each network interface
    # by setting `pernic` to `True`
    io = psutil.net_io_counters(pernic=True)

    while True:
        # sleep for `UPDATE_DELAY` seconds
        time.sleep(UPDATE_DELAY)
        # get the network I/O stats again per interface 
        io_2 = psutil.net_io_counters(pernic=True)
        # initialize the data to gather (a list of dicts)
        data = []
        for iface, iface_io in io.items():
            # new - old stats gets us the speed
            upload_speed, download_speed = io_2[iface].bytes_sent - iface_io.bytes_sent, io_2[iface].bytes_recv - iface_io.bytes_recv
            data.append({
                "iface": iface, "Download": get_size(io_2[iface].bytes_recv),
                "Upload": get_size(io_2[iface].bytes_sent),
                "Upload Speed": f"{get_size(upload_speed / UPDATE_DELAY)}/s",
                "Download Speed": f"{get_size(download_speed / UPDATE_DELAY)}/s",
            })
        # update the I/O stats for the next iteration
        io = io_2
        # construct a Pandas DataFrame to print stats in a cool tabular style
        df = pd.DataFrame(data)
        # sort values per column, feel free to change the column
        df.sort_values("Download", inplace=True, ascending=False)
        # sleep for `UPDATE_DELAY` seconds
        time.sleep(UPDATE_DELAY)

        # clear the screen based on your OS
        os.system("cls") if "nt" in os.name else os.system("clear")
        # print the stats
        print(df.to_string())



def get_compute_info():
    from tqdm import tqdm
    from time import sleep
    import psutil

    with tqdm(total=100, desc='cpu%', position=1) as cpubar, tqdm(total=100, desc='ram%', position=0) as rambar:
        while True:
            rambar.n=psutil.virtual_memory().percent
            cpubar.n=psutil.cpu_percent()
            rambar.refresh()
            cpubar.refresh()
            sleep(0.5)




# get_storage_info()
# get_network_info()
get_compute_info()