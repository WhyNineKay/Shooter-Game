Issues that I'm having with the project.
I'm having trouble with delta time, most of the movement scripts do not work with different fps values.


For testing:
change FPS value in constants.py.


Utility/entities.py
	class Bullet:
		delta time not working

Utility/entities.py
	class Player:
		in update function, movement is different for different fps
		(delta time not working)


Utility/explosions.py
	basically everything
		in update functions
		movement is different for different fps
		(delta time not working)
