import os
import requests
import argparse
import csv
import json
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_input_with_default(prompt, default=None):
    # Prompt the user with the default value
    if default is not None:
        prompt_with_default = f"{prompt} [{default}]: "
    else:
        prompt_with_default = f"{prompt}: "

    # Use input to allow the user to see what they type
    user_input = input(prompt_with_default)

    # Return the user input or the default value if the input was empty
    return user_input if user_input else default

def get_data(nodegrid_ip,username,password,path):
    # Create a session
    url = f'https://{nodegrid_ip}/api/v1/Session'
    headers = {"Content-Type": "application/json", "accept": "application/json"}
    data_content = dict()
    data_content['username'] = username
    data_content['password'] = password
    data = json.dumps(data_content)
    with requests.post(url, data=data, headers=headers, verify=False) as response:
        if response.status_code == 200:
            response_json = response.json()
            session_token = response_json["session"]

            # Get device table
            url = f'https://{nodegrid_ip}/api/v1/access/table'
            headers = { "ticket": session_token, "Content-Type": "application/json", "accept": "application/json"}
            with requests.get(url, headers=headers, params ={"page":"0"}, verify=False) as response:
                if response.status_code == 200:
                    try:
                        response_json = response.json()
                        # Print device details as a table
                        csv_file = open(path+nodegrid_ip+'_device_details.csv','w')
                        for nodegrid in response_json['devices']:
                            device_counter = 0
                            if 'devices' in nodegrid:
                                for device in nodegrid['devices']:
                                    device_counter = device_counter + 1
                                    w = csv.DictWriter(csv_file, device.keys())
                                    if device_counter == 1:
                                        w.writeheader()
                                    w.writerow(device)
                        csv_file.close()
                    except Exception as e:
                        print("Error: {}".format(str(e)))
                        sys.exit(1)
                else:
                    print(f"Error getting device table: {response.status_code}")
                    sys.exit(1)
        else:
            print(f"Error creating session: {response.status_code}")
            sys.exit(1)


if __name__ == '__main__':
    # create parser
    parser = argparse.ArgumentParser()

    # add arguments to the parser
    parser.add_argument("-i","--ip_address", help="IP Address of the nodegrid", default="localhost", dest='nodegrid_ip')
    parser.add_argument("-u","--username", help="Username", default="admin", dest='username')
    parser.add_argument("-p","--password", help="User Password", dest='password')
    parser.add_argument("-fp", "--file_path", help="File Location", dest='path', default="/var/local/file_manager/admin_group/")

    # parse the arguments
    args = parser.parse_args()

    get_data(args.nodegrid_ip,args.username,args.password,args.path)
