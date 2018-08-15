from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl
 
#Get all the Clusters from vCenter invetory and printing its name
#Below is Python 2.7.x code, which can be easily converted to python 3.x version
 
s=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode=ssl.CERT_NONE
si= SmartConnect(host="x.x.x.x", user="Administrator@vsphere.local", pwd="your_password",sslContext=s)
content=c.content
 
# Method that populates objects of type vimtype
def get_all_objs(content, vimtype):
        obj = {}
        container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        for managed_object_ref in container.view:
                obj.update({managed_object_ref: managed_object_ref.name})
        return obj
 
#Calling above method
clusters=get_all_objs(content, [vim.ClusterComputeResource])
 
#Iterating each cluster object and printing its name
for cluster in clusters:
        print (cluster.name)
