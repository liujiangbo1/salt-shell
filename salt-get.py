# coding=utf-8  
import salt.client as sc
#tgt="service_midd-ule_ufa-tw_yc-11.66"

#tgt="service-ule_ufa-hk_nw-193.37"
tgt="*"
local = sc.LocalClient()
grains = local.cmd(tgt, "grains.items")  
diskusage = local.cmd(tgt, "disk.usage")
iousage = local.cmd(tgt,"disk.iostat")
#print(iousage)
#cols = "主机,IP,内存(GB),CPU型号,CPU核数,操作系统 ,/容量(GB),/(使用率）,/data容量(GB),/data(使用率）,/data1容量
###打开一个.csv文件，以便写入  
#ret_file = open("hostinfo.csv", "w")  
###首先写入开头，有点字段名的意思  
#ret_file.write(cols + "\n")  
tt='''
########################线上服务器巡检结果####################################
'''
print(tt)
try:  
    for i in grains.keys(): 
        print("---------------------------------------" + i)
  
        ###去掉127.0.0.1这个地址  
        hostname = grains[i]["nodename"]  
        ipv4 = str(grains[i]["ipv4"]).replace("'127.0.0.1',", "")  
        ipv4 = ipv4.replace(",", "|")  
        mem = grains[i]["mem_total"] / 1024 + 1  
        num_cpu = grains[i]["num_cpus"]  
        OS = grains[i]["os"] + ' ' + grains[i]["osrelease"]  
        cpu = grains[i]["cpu_model"]  
        virtual = grains[i]["virtual"]  
        io_idle=iousage[i]["sys"]["%idle"]
        print("磁盘空闲io为:%s" %(io_idle))
#        print("内存是%s," %(mem,num_cpu,OS,cpu))
  
        ##磁盘容量  
        if "/" not in diskusage[i]:  
            disk_used = " "  
            disk_capacity = " "  
        else:  
            disk_used = float(diskusage[i]["/"]["1K-blocks"])/1048576  
            disk_capacity = diskusage[i]["/"]["capacity"]  
#        print(type(disk_used))
#        print(type(disk_capacity))
#        print(disk_used,disk_capacity)
        print("/磁盘使用量:%f,     / 磁盘使用率:%s" %(disk_used,disk_capacity))       
        if "/home" not in diskusage[i]:  
            disk_data_used = " "  
            disk_data_capacity = " "  
        else:  
            disk_data_used = float(diskusage[i]["/home"]["1K-blocks"])/1048576  
            disk_data_capacity = diskusage[i]["/home"]["capacity"] 
#        print(type(disk_data_used)) 
#        print(type(disk_data_capacity)) 

        print("/home使用量:%f,    /home 磁盘使用率:%s" %(disk_data_used,disk_data_capacity))

        print("\n")
except Exception, e:  
    print "Exception:\n", e
