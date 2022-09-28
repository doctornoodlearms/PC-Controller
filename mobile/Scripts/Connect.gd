extends Button

onready var packet = get_node("/root/Packet")

func _pressed() -> void:
	
	var port = 4242

	if(packet.connectToHost(get_node("%IP").text) == OK):
		get_tree().change_scene("res://Scenes/Control.tscn")
	
