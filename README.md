<h1>Games Character Catalog</h1>

<p>Author: David Ojeda</p>
<p>Email: david.ojeda.lopez@gmail.com</p>


I. File list
------------
<table>
	<tr>
		<td>database_setup.py</td> 	<td>Sets up the database used in this project</td>
	</tr>
	<tr>
		<td>database_populator.py</td> 	<td>Bootstrap data to populate the database (optional)</td>
	</tr>
	<tr>
		<td>webserver.py</td> 	<td>Runs the webserver and contains the URL callbacks</td>
	</tr>
	<tr>
		<td>oauth.py</td>		<td>Used for the OAuth2 authentication features</td>
	</tr>
	<tr>
		<td>pg_config.sh </td> <td>Provisioning file for Vagrant</td>
	</tr>
	<tr>
		<td>Vagrantfile</td>	<td>Vagrant file containing the configuration details for the Virtual Machine (VM)</td>
	</tr>
	<tr>
		<td>static</td>	<td>Directory containing the CSS files</td>
	</tr>
	<tr>
		<td>templates</td>	<td>Directory containing the HTML templates</td>
	</tr>
	<tr>
		<td>README.txt</td>	<td>This file</td>
	</tr>
</table>
------------


II. Installation
------------
<p>The ideal way to run this application is using Vagrant. If you do not have Vagrant installed you can follow these instructions: https://docs.vagrantup.com/v2/installation/.<p>

<ul>
	<li>
		<p>With Vagrant:</p>
		<p>From the cmd line:</p>
			<ol>
				<li>$ cd /path/to/your/repo</li>
				<li>$ vagrant up (Read the Vagrantfile and pg_config.sh files and set up the VM with all the needed dependencies.)</li>
				<li>$ python database_setup.py (Sets up the database)</li>
				<li>$ python database_populator.py (Optional. Populates the database)</li>
				<li>$ python webserver.py (Starts the webserver at 127.0.0.1:5000)</li>
			</ol>		
	</li>
	<li>
		<p>Without Vagrant:</p>
		<ol>
			<li>Install all the dependencies listed on the pg_config.sh file.</li>
			<ol>
				<li>$ cd /path/to/your/repo</li>
				<li>$ python database_setup.py (Sets up the database)</li>
				<li>$ python database_populator.py (Optional. Populates the database)</li>
				<li>$ python webserver.py (Starts the webserver at 127.0.0.1:5000)</li>
			</ol>
		</ol>
	</li>
</ul>
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
