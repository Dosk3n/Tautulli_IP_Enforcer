# Tautulli IP Enforcer (v1.0.0b (beta))

## Description

Tautulli IP Enforcer is a python script / application that I put together to allow us to blacklist (Ban) IP addresses as well as enforce a set number of concurrent streams per users unique IP to discourage / stop account sharing. For example we can set a user to have a 1 unique IP address limit. The user can watch as many streams as they want on that IP but as soon as another IP attempts to stream media, all the streams for that user will be terminicated and a message will be displayed to the user. This limit can be set to any number to allow a bit more freedom to other users.

## Requirements

Python3 / requests (usually included with python3)<br>
Tautulli (fantastic app that you should be using anyway)
PlexPass

Note: This application has been written and tested on Ubuntu Linux where Tautull is set up in a Docker container. This should work fine on other versions of Linux and shoudln't matter if Tautulli is in a docker container or not.

A windows version will be coming out at a later date.

## Installation & Set up

The main python script (tautulliIpEnforcer.py) does all the work but I have purposefully not scripped it to loop. So it runs once, does its thing and closes. The reason I have did it this way is I prefer to have this set up as a service so it starts automatically when the system boots. I do this by having the service start a bash script that runs the python file on loop. You can set up the python script to run however you want but the way I run this on my system is as follows.

(For more info on creating services this an informative guide that I use: 
https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6)

Now on to the set up...

#### Clone this repository to a location on your server:

git clone https://github.com/Dosk3n/Tautulli_IP_Enforcer.git

#### Add your settings to the main python3 script (tautulliIpEnforcer.py):

At the top of this file you have a section for user defined variables. This is where you will put the IP address of Tautulli. In my set up this is the IP address of the docker container that Tautulli is installed to. You also have to add the Tautulli port (8181 by default) as well as the Tautulli API key which you can find in Tautulli settings.

You can also change the messages that are displayed to the user for both blacklisted IPs and account sharing.

#### Edit the bash script (tautulliIpEnforcer.sh):

In this file you need to edit this line: "cd /home/dean/Tautulli_IP_Enforcer && python3 tautulliIpEnforcer.py" <br>
Specifically you need to edit this part: "/home/dean/Tautulli_IP_Enforcer" <br>
Change this to the path of where you cloned this repository. It must be the path, not just the folder name.

#### Edit the service file (tautulliipenforcer.service):

In this file you need to edit these lines: <br>
    User=dean <br>
    ExecStart=/bin/bash /home/dean/Tautulli_IP_Enforcer/tautulliIpEnforcer.sh <br>

User needs to be the user that you want the script to run as
On this line: "ExecStart=/bin/bash /home/dean/Tautulli_IP_Enforcer/tautulliIpEnforcer.sh" <br>
Specifically this part: "/home/dean/Tautulli_IP_Enforcer/tautulliIpEnforcer.sh" <br>
Change this to path (including the file) of the bash script you edited in the previous step.

If you need any more information on servi

#### Copy service file to /etc/systemd/system/ (must be done as root):

sudo cp tautulliipenforcer.service /etc/systemd/system/

#### Enable the service to boot on start:

sudo systemctl enable tautulliipenforcer.service

#### Start the service

sudo systemctl start tautulliipenforcer.service

#### Check the status of the serive to confirm working:

sudo systemctl status tautulliipenforcer.service

## How to Use

If you followed the above set up then the service will be running and you just need to add the IP addresses to blacklist or users to limit concurrent streams.

If you didnt want to set up a service then once you add the blacklisted IP addresses or limited users you will need to manually run the python script manually however you decided on.

#### To blacklist / ban an IP Address:

Edit the file "banned_ips.txt" and add the IP address that you want to blacklist. This can be both IPv4 or IPv6. Make sure that it is one IP per line.

#### To limit concurrent streams based on unique IPs:

Edit the file "concurrent_ip_limit.txt" and add the username followed by a semicolon and the limit of unique IP addresses that are allowed. For example: Dosk3n;2 will only allow a maximum of 2 unique IP addresses for this user. If a user is not in the text file then they are ignored and there for have unlimited allowance.

#### How to view logs:

Any time a user has their stream terminated for violating a ban or having their concurrent IP limit reached it will be added to the log "enforce_log.txt".
