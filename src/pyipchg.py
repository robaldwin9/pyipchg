import wmi 
import argparse
import sys
import os

# Obtain network adaptors configurations
nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)

# Current values for ip configuration, TODO make nic_configs index an argument!
currentSubnet = nic_configs[0].IPSubnet[0]
currentGateway = nic_configs[0].DefaultIPGateway[0]
currentIP = nic_configs[0].IPAddress[0]

# Change ip based on users args
def ipChange(args):
	ip =  args.ip

	# Set Gateway
	gateway = currentGateway
	if args.gat is not None:
		gateway = args.gat
	
	# Set Subnet
	sub = currentSubnet
	if args.sub is not None:
		sub = args.sub
	
	# Set IP
	nic = nic_configs[0]
	nic.EnableStatic(IPAddress=[ip], SubnetMask=[sub])
	nic.SetGateways(DefaultIPGateway=[gateway])

# List all network interface information
def listNics(args):
	for nic in nic_configs:
		print(nic)

# Assign ip using DHCP
def autoAquireIP():
	nic = nic_configs[0]
	nic.EnableDHCP()

# TODO: Change to something better than ping!
def reachable(ip):
	response = os.system("ping -n 1 -c 1 " + ip)
	output = ip + " Was unreachable "
	if response == 0:
		output = ip + " Acked "

	return output

# Get arguments
parser = argparse.ArgumentParser(prog="pyipchg", description='description: Change ip to static, or aquire from DHCP without dealin with windows GUI')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('-lnic', action='store_true', default=False,  help='list network interface cards information')
parser.add_argument('-ip', help='ipv4 address')
parser.add_argument('-sub', help='subnetmask, changes only if ip provided')
parser.add_argument('-gat', help='Default Gateway, changes only if ip provided')
parser.add_argument('-dhcp', action='store_true', default=False, help='Auto attain IP from DHCP')
parser.add_argument('-reach', action='store', help='Check if ip is reachable')
args = parser.parse_args()

# Program flow dependant on optional args provided
if args.lnic:
	listNics(args)

if args.ip is not None:
	ipChange(args)

elif args.dhcp is not None:
	autoAquireIP()

if len(sys.argv) == 1:
	print("\tIP:     " + str(currentIP))
	print("\tSubnet  " + str(currentSubnet))
	print("\tGateway " + str(currentGateway))

if args.reach is not None:
		print(reachable(args.reach))

