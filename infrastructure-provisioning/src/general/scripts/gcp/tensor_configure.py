#!/usr/bin/python

# *****************************************************************************
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# ******************************************************************************

import logging
import json
import sys
from dlab.fab import *
from dlab.meta_lib import *
from dlab.actions_lib import *
import os
import traceback


if __name__ == "__main__":
    instance_class = 'notebook'
    local_log_filename = "{}_{}_{}.log".format(os.environ['conf_resource'], os.environ['edge_user_name'],
                                               os.environ['request_id'])
    local_log_filepath = "/logs/" + os.environ['conf_resource'] + "/" + local_log_filename
    logging.basicConfig(format='%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG,
                        filename=local_log_filepath)

    notebook_config = dict()
    try:
        notebook_config['exploratory_name'] = (os.environ['exploratory_name']).lower().replace('_', '-')
    except:
        notebook_config['exploratory_name'] = ''
    notebook_config['service_base_name'] = (os.environ['conf_service_base_name']).lower().replace('_', '-')
    notebook_config['instance_type'] = os.environ['gcp_notebook_instance_size']
    notebook_config['key_name'] = os.environ['conf_key_name']
    notebook_config['edge_user_name'] = (os.environ['edge_user_name']).lower().replace('_', '-')
    notebook_config['instance_name'] = '{0}-{1}-nb-{2}'.format(notebook_config['service_base_name'],
                                                               notebook_config['edge_user_name'],
                                                               notebook_config['exploratory_name'])
    notebook_config['expected_primary_image_name'] = '{}-{}-notebook-primary-image'.format(
                                                        notebook_config['service_base_name'], os.environ['application'])
    notebook_config['expected_secondary_image_name'] = '{}-{}-notebook-secondary-image'.format(
                                                        notebook_config['service_base_name'], os.environ['application'])
    # generating variables regarding EDGE proxy on Notebook instance
    instance_hostname = GCPMeta().get_private_ip_address(notebook_config['instance_name'])
    edge_instance_name = '{0}-{1}-edge'.format(notebook_config['service_base_name'], notebook_config['edge_user_name'])
    notebook_config['ssh_key_path'] = '{0}{1}.pem'.format(os.environ['conf_key_dir'], os.environ['conf_key_name'])
    notebook_config['dlab_ssh_user'] = os.environ['conf_os_user']
    notebook_config['zone'] = os.environ['gcp_zone']
    notebook_config['shared_image_enabled'] = os.environ['conf_shared_image_enabled']
    try:
        if os.environ['conf_os_family'] == 'debian':
            initial_user = 'ubuntu'
            sudo_group = 'sudo'
        if os.environ['conf_os_family'] == 'redhat':
            initial_user = 'ec2-user'
            sudo_group = 'wheel'

        logging.info('[CREATING DLAB SSH USER]')
        print('[CREATING DLAB SSH USER]')
        params = "--hostname {} --keyfile {} --initial_user {} --os_user {} --sudo_group {}".format \
            (instance_hostname, notebook_config['ssh_key_path'], initial_user,
             notebook_config['dlab_ssh_user'], sudo_group)

        try:
            local("~/scripts/{}.py {}".format('create_ssh_user', params))
        except:
            traceback.print_exc()
            raise Exception
    except Exception as err:
        print('Error: {0}'.format(err))
        append_result("Failed creating ssh user 'dlab'.", str(err))
        GCPActions().remove_instance(notebook_config['instance_name'], notebook_config['zone'])
        sys.exit(1)

    # configuring proxy on Notebook instance
    try:
        logging.info('[CONFIGURE PROXY ON TENSOR INSTANCE]')
        print('[CONFIGURE PROXY ON TENSOR INSTANCE]')
        additional_config = {"proxy_host": edge_instance_name, "proxy_port": "3128"}
        params = "--hostname {} --instance_name {} --keyfile {} --additional_config '{}' --os_user {}" \
            .format(instance_hostname, notebook_config['instance_name'], notebook_config['ssh_key_path'],
                    json.dumps(additional_config), notebook_config['dlab_ssh_user'])
        try:
            local("~/scripts/{}.py {}".format('common_configure_proxy', params))
        except:
            traceback.print_exc()
            raise Exception
    except Exception as err:
        print('Error: {0}'.format(err))
        append_result("Failed to configure proxy.", str(err))
        GCPActions().remove_instance(notebook_config['instance_name'], notebook_config['zone'])
        sys.exit(1)

    # updating repositories & installing python packages
    try:
        logging.info('[INSTALLING PREREQUISITES TO TENSOR NOTEBOOK INSTANCE]')
        print('[INSTALLING PREREQUISITES TO TENSOR NOTEBOOK INSTANCE]')
        params = "--hostname {} --keyfile {} --user {} --region {}". \
            format(instance_hostname, notebook_config['ssh_key_path'], notebook_config['dlab_ssh_user'], os.environ['gcp_region'])
        try:
            local("~/scripts/{}.py {}".format('install_prerequisites', params))
        except:
            traceback.print_exc()
            raise Exception
    except Exception as err:
        print('Error: {0}'.format(err))
        append_result("Failed installing apps: apt & pip.", str(err))
        GCPActions().remove_instance(notebook_config['instance_name'], notebook_config['zone'])
        sys.exit(1)

    # installing and configuring TensorFlow and all dependencies
    try:
        logging.info('[CONFIGURE TENSORFLOW NOTEBOOK INSTANCE]')
        print('[CONFIGURE TENSORFLOW NOTEBOOK INSTANCE]')
        params = "--hostname {} --keyfile {} --region {} --os_user {} --exploratory_name {}" \
                 .format(instance_hostname, notebook_config['ssh_key_path'],
                         os.environ['gcp_region'], notebook_config['dlab_ssh_user'],
                         notebook_config['exploratory_name'])
        try:
            local("~/scripts/{}.py {}".format('configure_tensor_node', params))
        except:
            traceback.print_exc()
            raise Exception
    except Exception as err:
        print('Error: {0}'.format(err))
        append_result("Failed to configure TensorFlow.", str(err))
        GCPActions().remove_instance(notebook_config['instance_name'], notebook_config['zone'])
        sys.exit(1)

    try:
        print('[INSTALLING USERs KEY]')
        logging.info('[INSTALLING USERs KEY]')
        additional_config = {"user_keyname": os.environ['edge_user_name'],
                             "user_keydir": os.environ['conf_key_dir']}
        params = "--hostname {} --keyfile {} --additional_config '{}' --user {}".format(
            instance_hostname, notebook_config['ssh_key_path'], json.dumps(additional_config), notebook_config['dlab_ssh_user'])
        try:
            local("~/scripts/{}.py {}".format('install_user_key', params))
        except:
            append_result("Failed installing users key")
            raise Exception
    except Exception as err:
        print('Error: {0}'.format(err))
        append_result("Failed installing users key.", str(err))
        GCPActions().remove_instance(notebook_config['instance_name'], notebook_config['zone'])
        sys.exit(1)

    try:
        print('[SETUP USER GIT CREDENTIALS]')
        logging.info('[SETUP USER GIT CREDENTIALS]')
        params = '--os_user {} --notebook_ip {} --keyfile "{}"' \
            .format(notebook_config['dlab_ssh_user'], instance_hostname, notebook_config['ssh_key_path'])
        try:
            local("~/scripts/{}.py {}".format('common_download_git_certfile', params))
            local("~/scripts/{}.py {}".format('manage_git_creds', params))
        except:
            append_result("Failed setup git credentials")
            raise Exception
    except Exception as err:
        print('Error: {0}'.format(err))
        append_result("Failed to setup git credentials.", str(err))
        GCPActions().remove_instance(notebook_config['instance_name'], notebook_config['zone'])
        sys.exit(1)

    if notebook_config['shared_image_enabled'] == 'true':
        try:
            print('[CREATING IMAGE]')
            primary_image_id = GCPMeta().get_image_by_name(notebook_config['expected_primary_image_name'])
            secondary_image_id = GCPMeta().get_image_by_name(notebook_config['expected_secondary_image_name'])
            if primary_image_id == '':
                print("Looks like it's first time we configure notebook server. Creating images.")
                primary_image_id = GCPActions().create_image_from_instance_disk(
                    notebook_config['expected_primary_image_name'], 'primary',
                    notebook_config['instance_name'], notebook_config['zone'])
                if primary_image_id != '':
                    print("Image of primary disk was successfully created. It's ID is {}".format(primary_image_id))
            if secondary_image_id == '':
                secondary_image_id = GCPActions().create_image_from_instance_disk(
                    notebook_config['expected_secondary_image_name'], 'secondary', notebook_config['instance_name'],
                    notebook_config['zone'])
                if secondary_image_id != '':
                    print("Image of secondary disk was successfully created. It's ID is {}".format(secondary_image_id))
        except Exception as err:
            print('Error: {0}'.format(err))
            append_result("Failed creating image.", str(err))
            GCPActions().remove_instance(notebook_config['instance_name'], notebook_config['zone'])
            GCPActions().remove_image(notebook_config['expected_primary_image_name'])
            GCPActions().remove_image(notebook_config['expected_secondary_image_name'])
            sys.exit(1)

    # generating output information
    ip_address = GCPMeta().get_private_ip_address(notebook_config['instance_name'])
    tensorboard_url = "http://" + ip_address + ":6006/"
    jupyter_ip_url = "http://" + ip_address + ":8888/{}/".format(notebook_config['exploratory_name'])
    ungit_ip_url = "http://" + ip_address + ":8085/{}-ungit/".format(notebook_config['exploratory_name'])
    print('[SUMMARY]')
    logging.info('[SUMMARY]')
    print("Instance name: {}".format(notebook_config['instance_name']))
    print("Private IP: {}".format(ip_address))
    print("Instance type: {}".format(notebook_config['instance_type']))
    print("Key name: {}".format(notebook_config['key_name']))
    print("User key name: {}".format(os.environ['edge_user_name']))
    print("TensorBoard URL: {}".format(tensorboard_url))
    print("TensorBoard log dir: /var/log/tensorboard")
    print("Jupyter URL: {}".format(jupyter_ip_url))
    print("Ungit URL: {}".format(ungit_ip_url))
    print('SSH access (from Edge node, via IP address): ssh -i {0}.pem {1}@{2}'.format(notebook_config['key_name'],
                                                                                       notebook_config['dlab_ssh_user'],
                                                                                       ip_address))

    with open("/root/result.json", 'w') as result:
        res = {"hostname": ip_address,
               "ip": ip_address,
               "instance_id": notebook_config['instance_name'],
               "master_keyname": os.environ['conf_key_name'],
               "tensorboard_log_dir": "/var/log/tensorboard",
               "notebook_name": notebook_config['instance_name'],
               "Action": "Create new notebook server",
               "exploratory_url": [
                   {"description": "TensorBoard",
                    "url": tensorboard_url},
                   {"description": "Jupyter",
                    "url": jupyter_ip_url},
                   {"description": "Ungit",
                    "url": ungit_ip_url}]}
        result.write(json.dumps(res))