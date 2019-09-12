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

data "template_file" "dlab_ui_values" {
  template = file("./modules/helm_charts/dlab-ui-chart/values.yaml")
  vars = {
      mongo_db_name          = var.mongo_dbname
      mongo_user             = var.mongo_db_username
      mongo_port             = var.mongo_service_port
      mongo_service_name     = var.mongo_service_name
      ssn_k8s_alb_dns_name   = data.kubernetes_service.nginx_service.load_balancer_ingress.0.ip
      provision_service_host = "127.0.0.1" # var.endpoint_eip_address
      env_os                 = var.env_os
      service_base_name      = var.service_base_name
      ldap_host              = var.ldap_host
      ldap_dn                = var.ldap_dn
      ldap_ou                = var.ldap_users_group
      ldap_user              = var.ldap_user
      ldap_password          = var.ldap_bind_creds
  }
}

resource "helm_release" "dlab_ui" {
    name       = "dlab-ui"
    chart      = "./modules/helm_charts/dlab-ui-chart"
    depends_on = [helm_release.mongodb, kubernetes_secret.mongo_db_password_secret]
    wait       = true

    values     = [
        data.template_file.dlab_ui_values.rendered
    ]
}
