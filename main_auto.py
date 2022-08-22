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
         
         
def sh_conf(sow,spec,conf_stanza,unique_idenify):
    for i in range(len(sow)):
        for j in range(len(spec[conf_stanza])):
            if sow[i][unique_idenify]==spec[conf_stanza][j][unique_idenify]:
                if 'count' in sow[i]:
                    spec[conf_stanza][j]["count"]=sow[i]["count"]
                if 'instanceType' in sow[i]:
                    spec[conf_stanza][j]["instanceType"]=sow[i]["instanceType"]
                if 'primary' in sow[i]:
                    spec[conf_stanza][j]["primary"]=sow[i]["primary"]
                if 'dnsAltNames' in sow[i]:
                    spec[conf_stanza][j]["dnsAltNames"]=sow[i]["dnsAltNames"]     
                if 'app' in sow[i]:
                    spec[conf_stanza][j]["app"]=sow[i]["app"]
                if 'diskCapacity' in sow[i]:
                    spec[conf_stanza][j]["diskCapacity"]=sow[i]["diskCapacity"]   
                if 'size' in sow[i]:
                    spec[conf_stanza][j]["size"]=sow[i]["size"]     
                if 'ensure' in sow[i]:
                    spec[conf_stanza][j]["ensure"]=sow[i]["ensure"]
                if 'version' in sow[i]:
                    spec[conf_stanza][j]["version"]=sow[i]["version"]   
                if 'context' in sow[i]:
                    spec[conf_stanza][j]["context"]=sow[i]["context"]    
                if 'targets' in sow[i]:
                    spec[conf_stanza][j]["targets"]+= sow[i]["targets"]
      
            else:
                spec[conf_stanza].append(sow[i])


for item_1 in data:
    for item_2 in final_spec_file:
        if item_1==item_2:
            if item_1=="apps":
                # apps(data[item_1],final_spec_file[item_2])
                sh_conf(data["apps"],final_spec_file,"apps","id") 
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
                sh_conf(data["inputsDataManagers"],final_spec_file,"inputsDataManagers","name") 
            elif item_1=="searchHeads":
                sh_conf(data["searchHeads"],final_spec_file,"searchHeads","name") 
            elif item_1=="searchHeadCluster":
                sh_conf(data["searchHeadCluster"],final_spec_file,"searchHeadCluster","name") 


                
with open('test.json', 'w') as outfile:
    json.dump(final_spec_file, outfile)