import wmi 
import argparse

# Obtain network adaptors configurations
nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)

def ipChange(args):
	ip =  args.IP
	sub = args.SUBNET
	gateway = args.GATWAY

	nic = nic_configs[0]
	nic.EnableStatic(IPAddress=[ip], SubnetMask=[sub])
	nic.SetGateways(DefaultIPGateway=[gateway])

def listNics(args):
	for nic in nic_configs:
		print(nic)

def autoAquireIP():
	# Enable DHCP
	nic = nic_configs[0]
	nic.EnableDHCP()

# Get arguments
parser = argparse.ArgumentParser(prog="pyip", description='Some usefull network commands')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
#parser.add_argument('--listNics', action='listNics', help='list network interface cards information')
parser.add_argument('IP', help='ip')
parser.add_argument('SUBNET', help='subnetmask')
parser.add_argument('GATWAY', help='gateway')

args = parser.parse_args()
ipChange(args)

#if args.listNics is not None:
#	listNics(args)




