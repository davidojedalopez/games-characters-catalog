Author: David Ojeda
Email: david.ojeda.lopez@gmail.com


I. File list
------------
database_setup.py 			Sets up the database used in this project
database_populator.py		Bootstrap data to populate the database (optional)
webserver.py 				Runs the webserver and contains the URL callbacks
oauth.py 					Used for the OAuth2 authentication feature
pg_config.sh 				Provisioning file for Vagrant
Vagrantfile 				Vagrant file containing the configuration details for the Virtual Machine (VM)
static 						Directory containing the CSS files
templates 					Directory containing the HTML templates
README.txt					This file
------------


II. Installation
------------
The ideal way to run this application is to use Vagrant. If you do not have Vagrant installed you can follow these instructions:INSTRUCTINOS TO INSTALL VAGRANT.

With Vagrant:
	From the cmd line:
		1. $ cd /path/to/your/repo
		2. $ vagrant up (Read the Vagrantfile and pg_config.sh files and set up the VM with all the needed dependencies.)
		3. $ python setup.py (Sets up the database, populates it with the example data, and runs the webserver on port 127.0.0.1:5000)

Without Vagrant:
	1. Install all the dependencies listed on the pg_config.sh file.
	From the cmd line:
		2. $ cd /path/to/your/repo
		3. $ python setup.py
------------


III. Usage
------------
Current configuration lets you access the application through your local host at 127.0.0.1:5000 (Change the Vagrantfile if you need another port). From there you can start interacting with the web application.
------------


IV. Comments
------------
 This project is a small and simple web application that has the following features:
 	- CRUD database operations
 	- Authorization and authentication capability using OAuth2
 	- JSON and XML API endpoints available at 127.0.0.1:5000/games/JSON and 127.0.0.1:5000/games/XML respectively
