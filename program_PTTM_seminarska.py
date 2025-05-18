# -*- coding: utf-8 -*-
"""
Created on Sat May 10 21:46:47 2025

@author: Jernej Kušar
"""

import sys
sys.path.append("C:/Users/Jernej Kusar/Documents/LFDT splošno/Dodiplomska/Main")


import datalib as jdl
import os
import cv2
import numpy as np




import shutil
import re



data = jdl.getFiles_recursive(folder_path=r"D:\CFD\PTM\jernej_turbina\ERN_combustion_radiation_files", 
                              suffix=None, include=["temp_outlet"], exclude=["rfile"])

data = sorted(data, key=lambda x: int(re.search(r'dp(\d+)', x).group(1)))

newpath = r"D:\CFD\PTM\final_data\temp_out"
if not os.path.exists(newpath):
    os.makedirs(newpath)



for i in data:
    name = "temp_data"
    dp = i.split("\\")[5]
    if os.path.basename(i).split(".")[-1] != "png":
        new_name = f"{newpath}\{name}_{dp}.txt"
    else:
        new_name = f"{newpath}\{name}_{dp}.png"
    try:
        shutil.copy2(i, new_name)
        print(r"Succes in creating the file: " + new_name)
    except IOError as e:
        print("Unable to copy file. %s" % e)

    


vel_inlet_d = jdl.getFiles_recursive(folder_path=r"D:\CFD\PTM\final_data\vel_in", 
                              suffix="txt")

vel_outlet_d = jdl.getFiles_recursive(folder_path=r"D:\CFD\PTM\final_data\vel_out", 
                              suffix="txt")

mass_flow_out_d = jdl.getFiles_recursive(folder_path=r"D:\CFD\PTM\final_data\mf_out", 
                              suffix="txt")

mass_flow_in_d = jdl.getFiles_recursive(folder_path=r"D:\CFD\PTM\final_data\mf_in", 
                              suffix="txt")

temp_out_d = jdl.getFiles_recursive(folder_path=r"D:\CFD\PTM\final_data\temp_out", 
                              suffix="txt")

temp_in_d = jdl.getFiles_recursive(folder_path=r"D:\CFD\PTM\final_data\temp_in", 
                              suffix="txt")

cp_in_d = jdl.getFiles_recursive(folder_path=r"D:\CFD\PTM\final_data\cp_in", 
                              suffix="txt")

cp_out_d = jdl.getFiles_recursive(folder_path=r"D:\CFD\PTM\final_data\cp_out", 
                              suffix="txt")

vel_inlet_d = sorted(vel_inlet_d, key=lambda x: int(re.search(r'dp(\d+)', x).group(1)))
vel_outlet_d = sorted(vel_outlet_d, key=lambda x: int(re.search(r'dp(\d+)', x).group(1)))
mass_flow_out_d = sorted(mass_flow_out_d, key=lambda x: int(re.search(r'dp(\d+)', x).group(1)))
mass_flow_in_d = sorted(mass_flow_in_d, key=lambda x: int(re.search(r'dp(\d+)', x).group(1)))
temp_out_d = sorted(temp_out_d, key=lambda x: int(re.search(r'dp(\d+)', x).group(1)))
temp_in_d = sorted(temp_in_d, key=lambda x: int(re.search(r'dp(\d+)', x).group(1)))
cp_in_d = sorted(cp_in_d, key=lambda x: int(re.search(r'dp(\d+)', x).group(1)))
cp_out_d = sorted(cp_out_d, key=lambda x: int(re.search(r'dp(\d+)', x).group(1)))









vel_inlet = []
vel_outlet = []
mass_flow_outlet = []
mass_flow_inlet = []
temp_out = []
temp_in = []
cp_in = []
cp_out = []
for i in range(len(vel_inlet_d)):
    vi = open(vel_inlet_d[i], mode="r").readlines()[5:-2]
    vi_list = []
    for j in range(len(vi)):
        vi_list.append(float(vi[j].split(" ")[-1].rstrip("\n")))
    vel_inlet.append(vi_list)
    vo = open(vel_outlet_d[i], mode="r").readlines()[5:]
    vel_outlet.append(float(str(vo).split(" ")[-1].split("\\n")[0]))
    mo = open(mass_flow_out_d[i], mode="r").readlines()[4]
    mass_flow_outlet.append(float(str(mo).split(" ")[-1].split("\\n")[0]))
    mi = open(mass_flow_in_d[i], mode="r").readlines()[4:-2]
    mi_list = []
    for j in range(len(mi)):
        mi_list.append(float(mi[j].split(" ")[-1].rstrip("\n")))
    mass_flow_inlet.append(mi_list)
    to = open(temp_out_d[i], mode="r").readlines()[-1]
    temp_out.append(float(str(to).split(" ")[-1].split("\\n")[0]))
    ti = open(temp_in_d[i], mode="r").readlines()[5:-2]
    ti_list = []
    for j in range(len(ti)):
        ti_list.append(float(ti[j].split(" ")[-1].rstrip("\n")))
    temp_in.append(ti_list)
    cp = open(cp_in_d[i], mode="r").readlines()[5:-2]
    cp_list = []
    for j in range(len(cp)):
        cp_list.append(float(cp[j].split(" ")[-1].rstrip("\n")))
    cp_in.append(cp_list)
    cpo = open(cp_out_d[i], mode="r").readlines()[-1]
    cp_out.append(float(str(cpo).split(" ")[-1].split("\\n")[0]))
    



W = []
W_kin_tot = []
W_term_tot = []
for i in range(len(vel_inlet)):
    W_kin_in = 0
    for j in range(len(vel_inlet[i])):
        w_kin_in = (mass_flow_inlet[i][j] * vel_inlet[i][j]**2)/2
        W_kin_in += w_kin_in
    W_kin_out = (np.abs(mass_flow_outlet[i]) * vel_outlet[i]**2)/2
    
    W_kin = W_kin_out - W_kin_in #To je narobe (more bit -) samo drugače nima smisla (premajhne cifre)
    W_kin_tot.append(W_kin)
    
    
    W_term_in = 0
    for j in range(len(mass_flow_inlet[i])):
        w_term_in = mass_flow_inlet[i][j] * cp_in[i][j] * temp_in[i][j]
        W_term_in += w_term_in
    
    W_term_out = np.abs(mass_flow_outlet[i] * cp_out[i] * temp_out[i])
    
    W_term = W_term_out - W_term_in #Enako kot za kinetično
    W_term_tot.append(W_term)
    
    W.append(W_term + W_kin)



import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 1000

h2_frac = ["0"]
for i in range(len(W)-1):
    ch4 = 95 - i*5
    air = 3
    h2 = 100 - ch4 - air
    h2_frac.append(f"{int(h2)}")
    
    
plt.scatter(h2_frac, W)
plt.grid()
plt.xlabel("$H_2$ percentage [%]")
plt.ylabel("Power [W]")
plt.title("Calculated power")
plt.show()



plt.scatter(h2_frac, W_term_tot, label="Thermal power")
plt.scatter(h2_frac, W_kin_tot, label="Kinetic power")
plt.grid()
plt.legend()
plt.xlabel("$H_2$ percentage [%]")
plt.ylabel("Power [W]")
plt.title("Thermal and kinetic power")
plt.show()


ex_data = jdl.getFiles_recursive(folder_path=r"D:\CFD\PTM\final_data", 
                              suffix="txt", include=["co_data"])   
    

mf = jdl.getFiles_recursive(folder_path=r"D:\CFD\PTM\final_data\mf_out", 
                              suffix="txt", include=["mf_data"])   
    
ex_data = sorted(ex_data, key=lambda x: int(re.search(r'dp(\d+)', x).group(1)))
mf = sorted(mf, key=lambda x: int(re.search(r'dp(\d+)', x).group(1)))



gas_outlet = []
for i in range(len(ex_data)):
    n = abs(float(open(ex_data[i], mode="r").readlines()[-1].split(" ")[-1].rstrip("\n")))
    mf_ = abs(float(open(mf[i], mode="r").readlines()[-1].split(" ")[-1].rstrip("\n")))
    gas_outlet.append(n*mf_)
    
    
plt.scatter(h2_frac, gas_outlet)
plt.grid()
plt.xlabel("$H_2$ mass fraction [%]")
plt.ylabel("No mass flow [kg/s]")
plt.title("Outlet mass flow")
plt.show()



temp_data = jdl.getFiles_recursive(folder_path=r"D:\CFD\PTM\final_data\temp_out", 
                              suffix="txt", include=["temp_data"])   
    
temp_data = sorted(temp_data, key=lambda x: int(re.search(r'dp(\d+)', x).group(1)))

temp_out = []
for i in range(len(temp_data)):
    n = abs(float(open(temp_data[i], mode="r").readlines()[-1].split(" ")[-1].rstrip("\n")))
    temp_out.append(n-273)


plt.scatter(h2_frac, temp_out)
plt.grid()
plt.xlabel("$H_2$ mass fraction [%]")
plt.ylabel("Average temperature @ outlet [°C]")
plt.title("Outlet temperature")
plt.show()




#plt.scatter(inter, vel_outlet, label = "vel_out")
#plt.scatter(inter, mass_flow_outlet, label = "mf_out")
plt.scatter(inter, temp_out, label="temp_out")
#plt.scatter(inter, cp_data, label="cp_data")
#plt.hlines(vel_inlet[0], inter[0], inter[-1], label="vel_inlet", color="blue")
plt.hlines(temp_in[0], inter[0], inter[-1], label="temp_inlet", color="red")
#plt.hlines(mass_flow_inlet[0], inter[0], inter[-1], label="mf_inlet", color="green")


plt.grid()
plt.xlabel("$CH_4$ mass fraction")
plt.ylabel("Temperature [K]")

plt.title("Temperature")
plt.legend(loc="center left")
plt.show()









n = "5000	5350	5700	6050	6400	6750	7100	7450	7800	8150	8500	8850	9200	9550	9900	10250	10600	10950	11300	11650"
LHV = n.split("\t")
eff = []
for i in range(len(W)):
    e = np.abs(W[i])/float(LHV[i])
    eff.append(e)
    
plt.scatter(h2_frac, eff)
plt.grid()
plt.xlabel("$H2$ mass fraction")
plt.ylabel("Efficiency [\]")
plt.title("Efficiency")
plt.show()



    
key = "vel"


video = jdl.getFiles_recursive(folder_path=r"D:\CFD\PTM\final_data", 
                              suffix="png", include=[f"{key}_path"], exclude=[f"{key}_", f"{key}_cont"])

video = sorted(video, key=lambda x: int(re.search(r'(\d+)', x).group(1)), reverse = False)
#video = sorted(video, key=lambda x: int(re.search(r'dp(\d+)', x).group(1)))



imgs = []
for i in video:
    im = cv2.imread(i)
    imgs.append(im)


jdl.frames_to_video(frames=imgs, output_path=r"D:\CFD\PTM\final_videos", video_name=f"{key}.mp4", fps=2)






newpath = r"D:\CFD\PTM\final_data\numbers"
if not os.path.exists(newpath):
    os.makedirs(newpath)



for i in range(len(data)):
    
    jdl.create_num_img(num=f"{92 - i*5}" + r"% h2", img_size=(200,100), number_size=50, save_path=newpath + f"\{i}.png")


jdl.create_num_img(num=r"0" + r"% h2", img_size=(200,100), number_size=50, save_path=newpath + r"\19.png")



v_path = r"D:\CFD\PTM\final_data\vel\path"
o_path = r"D:\CFD\PTM\final_data\numbers"

vid = jdl.getFiles_recursive(folder_path=v_path, 
                              suffix="png")

over = jdl.getFiles_recursive(folder_path=o_path, 
                              suffix="png")


vid = sorted(vid, key=lambda x: int(re.search(r'dp(\d+)', x).group(1)))
over = sorted(over, key=lambda x: int(re.search(r'(\d+)', x).group(1)), reverse = True)


newpath = v_path + r"\enum"
if not os.path.exists(newpath):
    os.makedirs(newpath)


for i in range(len(vid)):
    jdl.overlay_image(background=vid[i], overlay=over[i], over_pos=(1180, 50), over_resize=None, save_path=newpath, save_name = v_path.split("\\")[-1] + f"_{i+5}.png")







data_vmes = jdl.get_data_fromTXT(r"D:\CFD\PTM\jernej_turbina\workbench_journals\rn_in_vmes.txt")

header = data_vmes[:3]
data_copy = data_vmes[3:]

f = open(r"D:\CFD\PTM\jernej_turbina\workbench_journals\rn_in.txt", "w")

for i in header:
    f.write(i + "\n")
    
#dp set
all_save = []
for i in range(len(data)):
    data_copy[0] = data_copy[0].replace("5", f"{i+5}")
    print(data_copy[0])
    for j in range(len(data_copy)):
        #all_save.append(str(data_copy))
        f.write(data_copy[j] + "\n")
    data_copy = data_vmes[3:]
f.close()




a = str(data_copy)[1:-1]


jdl.save_data(folder_path=r"D:\CFD\PTM\jernej_turbina", data=all_save, file_name="koncni")
