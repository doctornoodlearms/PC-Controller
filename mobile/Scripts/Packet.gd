extends Node

var packet = PacketPeerUDP.new()
var disable = true

func sendPacket(command:String, args=[]):
	if(disable):
		return
	var msg = "c="+command
	for i in args.size():
		msg += "&arg"+str(i)+"="+str(args[i])
	packet.put_packet(msg.to_utf8())
	
func connectToHost(ip:String):
	
	ip = IP.resolve_hostname(ip,IP.TYPE_IPV4)
	print("Address: ",ip)
	
	if(packet.connect_to_host(ip, 4242) == OK):
		packet.put_packet("connect".to_utf8())
		if(packet.get_packet().get_string_from_utf8() == "connected"):
			disable = false
			print("Connected")
			return OK
	else:
		disable = true
		return ERR_CANT_CONNECT

func isConnected():
	return packet.is_connected_to_host()
	
func getPacket():
	return packet.get_packet()
