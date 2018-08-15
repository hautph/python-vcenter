from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl
#Get DRS VM-VM rules associated with a VM.
 
s=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode=ssl.CERT_NONE
si= SmartConnect(host="x.x.x.x", user="Administrator@vsphere.local", pwd="your_password",sslContext=s)
content=c.content
 
def get_all_objs(content, vimtype):
        obj = {}
        container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        for managed_object_ref in container.view:
                obj.update({managed_object_ref: managed_object_ref.name})
        return obj
 
# Scanning a input VM inside inventory using special  python construct i.e. List comprehension
# It will get all the Vms and check whether input VM is available inside inventory or not, finally it returns list with matching condition
 
vmToScan = [vm for vm in get_all_objs(content,[vim.VirtualMachine]) if "NTP-Bangalore" == vm.name]
 
# Scanning a input cluster inside invetory the way we did for VM above. here also we used list comprehension.
 
cluster = [cluster for cluster in get_all_objs(content,[vim.ClusterComputeResource]) if "DRSCluster-India" == cluster.name]
 
# Now we can call the method on input cluster by passing input VM as parameter, it returns array of rule objects associated with input VM.
ClusterRuleInfo=cluster[0].FindRulesForVm(vmToScan[0])
 
# Now iterate through rule objects and print the rule name
 
for rule in ClusterRuleInfo:
        print rule.name
