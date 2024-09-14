# import os
# import yaml

# def check_traefik_config(file_path):
#     """
#     Check if the file contains the specific Traefik configuration.
#     If it matches, return the hostName.
#     """
#     with open(file_path, 'r') as stream:
#         try:
#             config = yaml.safe_load(stream)
#             if config:
#                 traefik_config = config.get('traefik', {})
#                 if traefik_config.get('enabled') == True and \
#                    traefik_config.get('namespace') == 'traefik' and \
#                    traefik_config.get('hostName') and \
#                    'path' in traefik_config and \
#                    'stripPrefix' in traefik_config:
#                     return traefik_config.get('hostName')
#         except yaml.YAMLError as exc:
#             print(f"Error reading {file_path}: {exc}")
#     return None

# def list_hostnames(directory):
#     """
#     Traverse the directory and subdirectories to find YAML files and check for Traefik hostnames.
#     """
#     hostnames = []
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith(('.yml', '.yaml')):  # Looking for YAML files
#                 file_path = os.path.join(root, file)
#                 hostName = check_traefik_config(file_path)
#                 if hostName:
#                     hostnames.append(hostName)

#     return hostnames

# # The directory containing the 'Services' folder
# directory = 'Services'

# # List out all the hostnames that match the Traefik configuration
# hostnames = list_hostnames(directory)

# # Output the results
# if hostnames:
#     print("Found hostnames:")
#     for host in hostnames:
#         print(host)
# else:
#     print("No matching hostnames found.")

import subprocess

def get_httproutes(namespace):
    try:
        # Execute the kubectl command to get httproutes
        command = f"kubectl get httproutes -n {namespace} --no-headers"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if there is an error
        if result.stderr:
            print(f"Error: {result.stderr}")
            return []

        # Process the output
        httproutes = []
        for line in result.stdout.strip().split('\n'):
            columns = line.split()
            if len(columns) >= 2:
                name = columns[0].rsplit('-', 1)[0]  # Remove the "-httproute" suffix
                path = columns[1].strip('[]"')  # Clean up the path (remove brackets and quotes)
                httproutes.append((name, path))

        return httproutes

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage:
namespace = "elasticdt"
httproutes = get_httproutes(namespace)

# Print the result
if httproutes:
    print("Discovered HTTP routes:")
    for name, path in httproutes:
        print(f"Name: {name}, Path: {path}")
else:
    print("No HTTP routes found.")
