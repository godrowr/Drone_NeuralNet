# Drone_NeuralNet
The objective of our 4rth year capstone project is to control a drone remotely using hand gestures instead of an RC controller.

Not all the files for our project is here as some are too large. 

### Abstract

Drone controller systems rely heavily on complex handheld equipment with a series of joysticks, knobs, levers, triggers, buttons, and switches. These controllers rely on the user to be able to understand and learn how to navigate the many possibilities of commands to the drone. The solution is a simplified no-line-of-sight human-drone controller using only the user’s hands. By allowing a drone to comprehend non-verbal cues, this type of interaction can accelerate the union of human-machine interaction and remove third party control mediums, such as a controller.

### Demonstration

https://www.youtube.com/watch?v=BP93dnISaPs

Flight demonstration with the proposed CNN involved the sequence of several steps: 
- Charge the battery to full power prior to the demonstration. 
- Clear the environment of all items for a safe flight demonstration.  
- Start up Mission planner GUI  
- Ensure the drone is connected to the same Wi-Fi and is accessible by the command control computer through SSH 
- Ensure the drone is not experiencing issues with correct logistics 
- Press connect 
{If connection fails}
- Set up connection with raspberry pi 
- ssh pi@192.168.100.133 
- Check if the ip is the same in dhcpd,conf (if its not, change it to the IP the raspberry pi is currently holding) 
- Check if your command computer ip is included under /etc/default/arducopter 
- sudo systemctl daemon-reload 
- sudo reboot 

Start up the CNN (requires HandRecognition.ipynb to execute as a python script)
```
py HandRecognition.py
```
- ensure camera is not in use on command computer 
- Load Script 

```
nano cnn_to_drone.py
```
- Ensure that the TEST variable is set to 0 
- In Mission planner on the Data page, go to Scripts (you can find it if you click the little left arrow under the nav ball) 
- Select cnn_to_drone.py, click ‘run this script’.  
- When prompted, arm drone with controller or from the Mission planner GUI 
- Begin hand gestures in front of camera.  
- Disarm drone when completed.  
