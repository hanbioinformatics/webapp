# webapp
Webapplicatie Blok 4a HAN projectgroep 1

PREREQUISITES:
- MySQL server 5.5 or higher
- Linux Based OS (i.e Debian, Ubuntu or CentOS)
- Python 2.7 with modules: BioPython and MySQL-Connector
- Apache 2 with mod_python installed

INSTALLATION:
This guide assumes all prerequisites are already installed on the server.

step 1:
Create MySQL user to be used by the scripts. You can define the MySQL credentials in the .py and .psp scripts.
From the 'documents' folder run the SQL script called 'script-to-create-database.sql'. This will create the database.

step 2:
Move content of 'serverfiles' folder to the hostingdirectory of choosing.

NOTE:
- Make sure both .py and .psp files are enabled in httpd.conf
- Make sure hostingdirectory has correct privileges set to it
