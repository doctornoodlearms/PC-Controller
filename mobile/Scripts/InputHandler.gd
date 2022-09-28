#warnings-disable
extends Control

export var host:String
export var port:int

export var deadzone:int

var multiTouch:bool
var touchPos:PoolVector2Array = [Vector2(-1,-1), Vector2(-1,-1)]

var isPressed:bool

var dragValid:bool

export var panSens:float
var panCenter:Vector2 = Vector2(-1,-1)
var lastCenter:Vector2 = Vector2(-1,-1)
var currentPos:PoolVector2Array = [Vector2(-1,-1), Vector2(-1,-1)]
var panAngle:float

onready var disable = get_node("/root/Packet").disable

onready var packet = get_node("/root/Packet")

export var panningBound:float

func _ready():
	$Timer.connect("timeout",self,"on_timerTimeout")

func _input(event):
#	Screen Touch Event
	if(event is InputEventScreenTouch):
		event = event as InputEventScreenTouch
		
#		Used for the buffer to decide if the input is for a click or mouse down
		isPressed = event.is_pressed()
		
#		Update the touch positions
		if(event.is_pressed() == true):
			if(event.index < 2):
				touchPos[event.index] = event.position
			
#			Starts the click buffer
			if($Timer.is_stopped()):
				$Timer.start()
			
#			Multiple touch inputs
			if(event.index < 2):
				multiTouch = bool(event.index)
		
#		Clear the touch positions
		if(event.is_pressed() == false):
			if(event.index < 2):
				touchPos[event.index] = Vector2(-1,-1)
				currentPos[event.index] = Vector2(-1,-1)
#			No longer dragging
			if(touchPos[0] == Vector2(-1,-1) and touchPos[1] == Vector2(-1,-1)):
				dragValid = false
#			No longer multiple touch inputs
			if(dragValid == true and (touchPos[0] == Vector2(-1,-1) or touchPos[1] == Vector2(-1,-1))):
				multiTouch = false
#			Right Click
			if(event.index == 0):
				if(multiTouch and !dragValid):
					packet.sendPacket("RightMouseClick")
#				Left mouse up
				elif(!multiTouch and dragValid):
					if($Timer.is_stopped()):
						packet.sendPacket("LeftMouseUp")
#		Update the drawing
		update()
	
#	Screen drag input
	if(event is InputEventScreenDrag):
		event = event as InputEventScreenDrag
		
		if(event.index < 2):
			currentPos[event.index] = event.position
#			The drag is valid and is no longer a click
			if(event.position.distance_to(touchPos[event.index]) > deadzone):
				$Timer.stop()
				dragValid = true
		
#		Move the mouse
		if(multiTouch == false and dragValid == true):
			packet.sendPacket(
				"MoveMouse", 
				[round(event.relative.x), 
				round(event.relative.y)])
#		Panning logic
		if(multiTouch == true and dragValid == true):
#			Update the previous center point
			if(panCenter != Vector2(-1,-1)):
				lastCenter = panCenter
#			Update the current center point
			panCenter = (currentPos[0] + currentPos[1])/2
#			Update the angle to the previous center
			if(panCenter.distance_to(lastCenter) > 5 and 
			lastCenter != Vector2(-1,-1)):
				panAngle = lastCenter.angle_to_point(panCenter)
#				Pan up
				if(sin(panAngle) >= panningBound):
					packet.sendPacket(
						"PanVerticle",
						[(lastCenter.y - panCenter.y)*panSens])
#				Pan down
				if(sin(panAngle) <= panningBound * -1):
					packet.sendPacket(
						"PanVerticle",
						[(lastCenter.y - panCenter.y)*panSens])
#				Pan left
				if(cos(panAngle) >= panningBound):
					packet.sendPacket("PanHorizontal",
					[panCenter.x - lastCenter.x])
#				Pan right
				if(cos(panAngle) <= panningBound * -1):
					packet.sendPacket("PanHorizontal",
					[panCenter.x - lastCenter.x])
#		Clear the center points
		else:
			panCenter = Vector2(-1,-1)
			lastCenter = Vector2(-1,-1)
#		Update the drawing
		update()

func _draw():
	
	if(disable):
		draw_rect(Rect2(Vector2(0,0),Vector2(100,100)),Color.red)
#	Draws the current positions
	if(dragValid == true):
		for i in currentPos:
			if(i!=Vector2(-1,-1)):
				draw_circle(i, 20, Color.white)
#	Draw the touched positions for a click
	else:
		for i in touchPos:
			if(i != Vector2(-1,-1)):
				draw_circle(i, deadzone, Color.white)
#	Draw the center point for a pan
	if(multiTouch and dragValid):
		draw_circle(panCenter, 20, Color.yellow)
		draw_line(currentPos[0], currentPos[1], Color.green, 3)

# Click buffer ended
func on_timerTimeout():
#	Check if its a single click or multi click and drag
	if(multiTouch == false and dragValid == false):
#		Mouse down
		if(isPressed == true):
			packet.sendPacket("LeftMouseDown")
#		Mouse click
		else:
			packet.sendPacket("LeftMouseClick")
