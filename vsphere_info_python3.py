#!/usr/bin/env python

import pyVmomi
import argparse
import atexit
import itertools
from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, Disconnect
import humanize

MBFACTOR = float(1 << 20)

printVM = False
printDatastore = True
printHost = True


def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %s" % (attr, getattr(obj, attr)))


def GetArgs():

    parser = argparse.ArgumentParser(
        description='Process args for retrieving all the Virtual Machines')
    parser.add_argument('-s', '--host', required=True, action='store',
                        help='Remote host to connect to')
    parser.add_argument('-o', '--port', type=int, default=443, action='store',
                        help='Port to connect on')
    parser.add_argument('-u', '--user', required=True, action='store',
                        help='User name to use when connecting to host')
    parser.add_argument('-p', '--password', required=False, action='store',
                        help='Password to use when connecting to host')
    args = parser.parse_args()
    return args


def printHostInformation(host):
    try:
        summary = host.summary
        stats = summary.quickStats
        hardware = host.hardware
        cpuUsage = stats.overallCpuUsage
        memoryCapacity = hardware.memorySize
        memoryCapacityInMB = hardware.memorySize/MBFACTOR
        memoryUsage = stats.overallMemoryUsage
        freeMemoryPercentage = 100 - (
            (float(memoryUsage) / memoryCapacityInMB) * 100
        )
        print("--------------------------------------------------")
        print("Host name: ", host.name)
        # dump(host)
        print("Host CPU usage: ", cpuUsage)
        print("Host memory capacity: ", humanize.naturalsize(memoryCapacity,
                                                             binary=True))
        print("Host memory usage: ", memoryUsage / 1024, "GiB")
        print("Free memory percentage: " + str(freeMemoryPercentage) + "%")
        print("--------------------------------------------------")
    except Exception as error:
        print("Unable to access information for host: ", host.name)
        print(error)
        pass


def printComputeResourceInformation(computeResource):
    try:
        hostList = computeResource.host
        print("##################################################")
        print("Compute resource name: ", computeResource.name)
        print("##################################################")
        for host in hostList:
            printHostInformation(host)
    except Exception as error:
        print("Unable to access information for compute resource: ",
              computeResource.name)
        print(error)
        pass


def printDatastoreInformation(datastore):
    try:
        summary = datastore.summary
        capacity = summary.capacity
        freeSpace = summary.freeSpace
        uncommittedSpace = summary.uncommitted
        freeSpacePercentage = (float(freeSpace) / capacity) * 100
        print("##################################################")
        print("Datastore name: ", summary.name)
        print("Capacity: ", humanize.naturalsize(capacity, binary=True))
        if uncommittedSpace is not None:
            provisionedSpace = (capacity - freeSpace) + uncommittedSpace
            print("Provisioned space: ", humanize.naturalsize(provisionedSpace,
                                                              binary=True))
        print("Free space: ", humanize.naturalsize(freeSpace, binary=True))
        print("Free space percentage: " + str(freeSpacePercentage) + "%")
        print("##################################################")
    except Exception as error:
        print("Unable to access summary for datastore: ", datastore.name)
        print(error)
        pass


def printVmInformation(virtual_machine, depth=1):
    maxdepth = 10
    if hasattr(virtual_machine, 'childEntity'):
        if depth > maxdepth:
            return
        vmList = virtual_machine.childEntity
        for c in vmList:
            printVmInformation(c, depth + 1)
        return

    try:
        summary = virtual_machine.summary
        print("##################################################")
        print("Name : ", summary.name)
        print("MoRef : ", summary.vm)
        print("State : ", summary.runtime.powerState)
        print("##################################################")
    except Exception as error:
        print("Unable to access summary for VM: ", virtual_machine.name)
        print(error)
        pass


def main():
    args = GetArgs()
    # try:
    si = SmartConnect(host=args.host, user=args.user,
                      pwd=args.password, port=int(args.port),
                      unverified=True)
    print("Kebab? why not.")
    atexit.register(Disconnect, si)
    print("Kebab? aha.")
    content = si.RetrieveContent()

    print("Kebab? si.")

    for datacenter in content.rootFolder.childEntity:
        print("##################################################")
        print("##################################################")
        print("### datacenter : " + datacenter.name)
        print("##################################################")

        if printVM:
            if hasattr(datacenter.vmFolder, 'childEntity'):
                vmFolder = datacenter.vmFolder
                vmList = vmFolder.childEntity
                for vm in vmList:
                    printVmInformation(vm)

        if printDatastore:
            datastores = datacenter.datastore
            for ds in datastores:
                printDatastoreInformation(ds)

        if printHost:
            if hasattr(datacenter.hostFolder, 'childEntity'):
                hostFolder = datacenter.hostFolder
                computeResourceList = hostFolder.childEntity
                for computeResource in computeResourceList:
                    printComputeResourceInformation(computeResource)

    # except Exception as error:
    #     print("Caught vmodl fault : " + error.msg)
    #     return -1
    return 0

if __name__ == "__main__":
    main()
