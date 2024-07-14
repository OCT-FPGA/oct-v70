"""OCT Alveo V70 profile with post-boot script. DO NOT USE
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.


# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# We use the URN library below.
import geni.urn as urn
# Emulab extension
import geni.rspec.emulab

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Pick your image.
imageList = [('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD', 'UBUNTU 20.04'),
             ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD', 'UBUNTU 22.04')] 

dockerImageList = [('pytorch'), ('tensorflow'), ('tensorflow2')]
                   
pc.defineParameter("osImage", "Select Image",
                   portal.ParameterType.IMAGE,
                   imageList[0], imageList,
                   longDescription="Supported operating systems are Ubuntu and CentOS.")    

pc.defineParameter("dockerImage", "Docker Image",
                   portal.ParameterType.STRING,
                   dockerImageList[0], dockerImageList,
                   longDescription="Supported docker images.")  

# Retrieve the values the user specifies during instantiation.
params = pc.bindParameters()        

pc.verifyParameters()

# Process nodes, adding to FPGA network
# Create a node and add it to the request
name = "node" 
node = request.RawPC(name)
node.disk_image = params.osImage
# Assign to the node hosting the FPGA.
node.hardware_type = "fpga-r760-v70"
# Set Storage
#node.disk = 40
bs = node.Blockstore("bs", "/docker")
bs.size = "50GB"
node.component_manager_id = "urn:publicid:IDN+cloudlab.umass.edu+authority+cm"
#node.addService(pg.Execute(shell="bash", command="sudo /local/repository/post-boot.sh " + params.dockerImage + " >> /local/repository/output_log.txt"))

pc.printRequestRSpec(request)
