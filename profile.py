"""
Allocates a VM running Ubuntu 18

Instructions:
Wait for the profile instance to start, and then log in to the VM via the
ssh port specified below.  (Note that in this case, you will need to access
the VM through a high port on the physical host, since we have not requested
a public IP address for the VM itself.)
"""

import geni.portal as portal
import geni.rspec.pg as pg

def raiseError(msg):
    portal.context.reportError(portal.ParameterError(msg))

portal.context.defineParameter( "cores", "Number of Cores per VM", portal.ParameterType.INTEGER, 4 )
portal.context.defineParameter( "vms", "Number of Virtual Machines", portal.ParameterType.INTEGER, 4 )
portal.context.defineParameter( "image", "Image", portal.ParameterType.IMAGE, "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD" )
portal.context.defineParameter( "docker", "Install Docker?", portal.ParameterType.BOOLEAN, True )
portal.context.defineParameter( "p3_tools", "Install Python3 tools?", portal.ParameterType.BOOLEAN, False )
portal.context.defineParameter( "pyspark", "Install PySpark?", portal.ParameterType.BOOLEAN, False )

# Retrieve the values the user specifies during instantiation.
params = portal.context.bindParameters()

request = portal.context.makeRequestRSpec()

if params.vms < 1 or params.vms > 8:
    raiseError("You must choose at least 1 and no more than 8 VMs.")

if params.vms < 1 or params.vms > 12:
    raiseError("You must choose at least 1 and no more than 12 coress.")

for i in range(0, params.vms):
    node = request.XenVM("node-" + str(i))
    node.cores = params.cores

    node.disk_image = params.image

    if params.docker:
        node.addService(pg.Execute(shell="bash", command="/local/repository/docker.bash"))

    if params.p3_tools:
        node.addService(pg.Execute(shell="bash", command="/local/repository/python.bash"))
    
    if params.pyspark:
        if not params.p3_tools:
            node.addService(pg.Execute(shell="bash", command="/local/repository/python.bash"))
        node.addService(pg.Execute(shell="bash", command="/local/repository/pyspark.bash"))

portal.context.printRequestRSpec()
