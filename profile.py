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


# Describe the parameter(s) this profile script can accept.
portal.context.defineParameter( "cores", "Number of Cores", portal.ParameterType.INTEGER, 4 )
portal.context.defineParameter( "vms", "Number of Virtual Machines", portal.ParameterType.INTEGER, 4 )
portal.context.defineParameter( "image", "Image", portal.ParameterType.IMAGE, "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD" )
portal.context.defineParameter( "b", "Are you happy?", portal.ParameterType.BOOLEAN, True )

# Retrieve the values the user specifies during instantiation.
params = portal.context.bindParameters()

request = portal.context.makeRequestRSpec()

if params.vms < 1 or params.vms > 8:
    raiseError("You must choose at least 1 and no more than 8 VMs.")

for i in range(0, params.vms):
    node = request.XenVM("node-" + str(i))

    # Ubuntu 18.04 LTS 64-bit
    node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD"

portal.context.printRequestRSpec()
