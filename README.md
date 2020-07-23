# Tautulli IP Enforcer

## Description

Tautulli IP Enforcer is a python script / application that I put together to allow us to blacklist (Ban) IP addresses as well as enforce a set number of concurrent streams per users unique IP to discourage / stop account sharing. For example we can set a user to have a 1 unique IP address limit. The user can watch as many streams as they want on that IP but as soon as another IP attempts to stream media, all the streams for that user will be terminicated and a message will be displayed to the user. This limit can be set to any number to allow a bit more freedom to other users.

## Requirements

Python 3

Note: This application has been written and tested on Ubuntu Linux where Tautull is set up in a Docker container. This should work fine on other versions of Linux and shoudln't matter if Tautulli is in a docker container or not.

A windows version will be coming out at a later date.






git clone https://github.com/Dosk3n/Tautulli_IP_Enforcer.git

Edit bash script

Edit Service File #https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6

Copy service file to /etc/systemd/system/
sudo cp tautulliipenforcer.service /etc/systemd/system/

Enable the service for reboot
sudo systemctl enable tautulliipenforcer.service

Start the service
sudo systemctl start tautulliipenforcer.service

sudo systemctl status tautulliipenforcer.service