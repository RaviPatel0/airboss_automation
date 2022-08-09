import os
import json


# Read SOW file
f = open('sow.json','r')
data = json.loads(f.read())

# Get Spec File
get_spec = "cloudctl stacks get devonenergy -o json  >  test.json"
str(os.system(get_spec))

# Check cloudctl login
if open('test.json','r').readlines()[0]=='"Unauthorized"\n':
    print("Please login using cloudctl")
    exit()
    
# Create Blank File    
f1 = open('test.json','r')
final_spec_file = json.loads(f1.read())
final_spec_file = final_spec_file["spec"]

# Apps functions
def apps(sow,spec):
    for i in range(len(sow)):
        flag = 0
        for j in range(len(spec)):
            if  sow[i]['id']==spec[j]['id']:
                spec[j]=sow[i]
                flag = 1
                break
        if flag==0:    
            spec.append(sow[i])   
         
           
def maintenance(sow,spec):
    spec["maintenanceWindow"]=sow


def other_conf(sow,spec,type):
    for i in sow:
        flag = 0
        for j in spec[type]:
            if i==j:
                spec[type][i]=sow[i]
                flag = 1
                break
        if flag == 0:
            spec[type][i]=sow[i]

def cert(sow,spec):
    for i in sow:
        spec["certs"][i]=sow[i]
         
         
def sh_conf(sow,spec):
    for i in range(len(sow)):
        for j in range(len(spec)):
            print((sow[i])["name"])
            if (sow[i])['name']==(spec["inputsDataManagers"][j])['name']:
                if (sow[i])["count"]:
                    (spec["inputsDataManagers"][i])["count"]=(sow[i])["count"]

     
for item_1 in data:
    for item_2 in final_spec_file:
        if item_1==item_2:
            if item_1=="apps":
                apps(data[item_1],final_spec_file[item_2])
            elif item_1=="maintenanceWindow":
                maintenance(data["maintenanceWindow"],final_spec_file)
            elif item_1=="featureFlags":
                other_conf(data["featureFlags"],final_spec_file,"featureFlags")
            elif item_1=="features":
                other_conf(data["features"],final_spec_file,"features")
            elif item_1=="noah":
                other_conf(data["noah"],final_spec_file,"noah")
            elif item_1=="platformSettings":
                other_conf(data["platformSettings"],final_spec_file,"platformSettings")    
            elif item_1=="releaseInfo":
                other_conf(data["releaseInfo"],final_spec_file,"releaseInfo")   
            elif item_1=="certs":
                cert(data["certs"],final_spec_file)  
            elif item_1=="indexerCluster":
                other_conf(data["indexerCluster"],final_spec_file,"indexerCluster")   
            elif item_1=="inputsDataManagers":
                sh_conf(data["inputsDataManagers"],final_spec_file) 


                
with open('test.json', 'w') as outfile:
    json.dump(final_spec_file, outfile)