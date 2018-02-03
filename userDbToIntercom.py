import yaml
import MySQLdb as myDb
import json
import requests
import sys

db_config_key = "db_config"
intercom_param_key = "intercom_config"
user_db_table = "user"


"""
Defining the keys to access intercom parameters from the config.yml. These keys are not changed often
"""
user_id_key = "user_id_key"
user_name_key = "user_name_key"
user_email_key = "user_email_key"
access_token_key = "access_token"
url_key = "update_api_url"

"""
Defining the keys to access DB config parameters from the config.yml. These keys are not changed often
"""
db_host_key = "host"
db_user_key = "user"
db_password_key = "password"
db_name_key = "db"


"""
Desc: This function reads the necessary DB configuration from the config.yml file
"""
def get_db_config_params():
    with open(config_file_path) as paramStream:
        param_dict = yaml.load(paramStream)
        return param_dict[db_config_key]


def get_intercom_api_params():
    with open(config_file_path) as paramStream:
        param_dict = yaml.load(paramStream)
        return param_dict[intercom_param_key]


def update_user_in_intercom(user_data_list):
    intercom_api_params = get_intercom_api_params()
    user_id = user_data_list[0]
    user_name = user_data_list[1]
    user_email = user_data_list[2]
    user_attrib_dict = {
        intercom_api_params[user_id_key] : user_id,
        intercom_api_params[user_name_key]: user_name,
        intercom_api_params[user_email_key]: user_email
    }
    user_attrib_json = json.dumps(user_attrib_dict)
    request_url = intercom_api_params[url_key]
    post_data_payload = user_attrib_json
    auth_headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : "Bearer " + intercom_api_params[access_token_key]
    }
    response_data = requests.post(url = request_url, data = post_data_payload, headers = auth_headers)

    if response_data.status_code == 200:
        print("User is successfully added/updated")
    elif response_data.status_code == 400:
        print("Bad Request: Failed to add/update the user")
    elif response_data.status_code == 403 or response_data.status_code == 401:
        print("Unable to authorize: Failed to add/update the user")


def update_db_data_to_intercom():
    db_params = get_db_config_params()
    host = db_params[db_host_key]
    user = db_params[db_user_key]
    password = db_params[db_password_key]
    db_name = db_params[db_name_key]
    db_connection = myDb.connect(host,user,password,db_name)
    with db_connection:
        cursor = db_connection.cursor()
        sql_query = "SELECT * FROM " + user_db_table
        tuple = cursor.fetchone()
        while tuple is not  None:
            print(tuple)
            update_user_in_intercom(tuple)
            tuple = cursor.fetchone()


def main():
    global config_file_path
    args = sys.argv
    if len(args) > 1:
        config_file_path = args[1]
    else:
        print("Please provide the configuration file to add/update the users")
        return
    update_db_data_to_intercom()


main()
