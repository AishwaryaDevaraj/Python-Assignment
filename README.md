# Python-Assignment
Python script that goes over our user database and creates users on Intercom.

Instructions to execute this python script:
execute the following command on the terminal: python userDbToIntercom.py PATH_TO_THE_YML_CONFIG_FILE
Ex: python userDbToIntercom.py config.yml

This script takes the configuration file(config.yml) as an argument. The config.yml contains the details of the user database and intercom API Parameters. These parameters are configurable, so the same script can work on different MySql DB's and with different intercom accounts.

NOTE: You must provide the appropriate values for the parameters specified in the config.yml file in order for the script to execute correctly
