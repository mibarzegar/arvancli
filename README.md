# ArvanCloud Command Line Tools

This repository contains [ArvanCloud](arvancloud.com) CLI tool that can be used to benefit from this provider services using terminal (not the **crappy** GUI!).

This tool currently supports below services and actions of the provider:

* **IaaS** Service:  

  * **region** Entitiy

    * **ls** command: get list of regions

      ```Bash
      arvancli iaas region ls
      ```

      List will be appeared in a tabular format with below columns:

      * Country
      * City
      * Datacenter
      * Code
      * Available
      * Coming Soon
    
  * **server** Entity

    * **id** command: get id of specified server

      ```bash
      arvancli iaas server id --name "{SERVER_NAME}"
      ```

    * **status** command: get status of specified server

      ```bash
      arvancli iaas server status --name "{SERVER_NAME}"
      ```

    * **list** command: list servers in configured zone

      ```bash
      arvancli iaas server ls
      ```

    * List will be appeared in a tabular format with below columns:

      * Name
      * Status
      * Operating System
      * Resource
      * Username
      * IP Address(es)
      
    * **reboot** command: reboot specified server

      ```bash
      arvancli iaas server reboot --name "{SERVER_NAME}"
      ```

    * **poweroff** command: poweroff specified server

      ```bash
      arvancli iaas server poweroff --name "{SERVER_NAME}"
      ```

  * **firewall** Entitiy

    * **ls** command: get list of firewall groups

      ```Bash
      arvancli iaas firewall ls
      ```

      List will be appeared in a tabular format with below columns:

      * Name
      * Description
      * Real Name
      * Servers

    * **id** command: get id of specified firewall group

      ```bash
      arvancli iaas firewall id --name "{FIREWALL_GROUP_NAME}"
      ```

    * **create** command: create firewall group with specified name and description

      ```bash
      arvancli iaas firewall create --name "{FIREWALL_GROUP_NAME}" --description "{FIREWALL_GROUP_DESCRIPTION}"
      ```

      **Note:** To Add ArvanCDN Servers firewall group to the list of firewall groups, *FIREWALL_GROUP_NAME* must be set to arCDN  and no description is required.

    * **delete** command: delete firewall group with specified name

      ```bash
      arvancli iaas firewall delete --name "{FIREWALL_GROUP_NAME}"
      ```

    * **list-rules** command: list rules inside a firewall group with specified name

      ```bash
      arvancli iaas firewall list-rules --name "{FIREWALL_GROUP_NAME}" 
      ```

      List will be appeared in a tabular format with below columns:

      * \#
      * Type
      * Direction
      * Protocol
      * Ports
      * Origin/Destination
      * Access Type
      
    * **add-rule** command: add rule to the firewall group with specified name

      ```bash
      arvancli iaas firewall add-rule --name "{FIREWALL_GROUP_NAME}" --description "{FIREWALL_RULE_DESCRIPTION}" --direction "{FIREWALL_RULE_DIRECTION}" --cidr "{FIREWALL_RULE_CIDR(s)}" --protocol "{FIREWALL_RULE_PROTOCOL}" --port "{FIREWALL_RULE_PORTS}"
      ```

      *FIREWALL_RULE_DIRECTION* can be:

      - ingress
      - egress

      *FIREWALL_RULE_PROTOCOL* can be:

      - tcp
      - udp
      - *PROTOCOL_NUMBER*. In this way a custom protocol with specified number can be applied for the rule. With custom protocols there is no need for "--port" argument

      For multiple source cidrs, *FIREWALL_RULE_CIDR* can be written in the form of *cidr1,cidr2,...*

      For a port range, *FIREWALL_RULE_PORTS* should be specified in the form of *sport:dport*

      For all source IPs or ports, "--cidr" and "--port" arguments can be skipped, respectively
      
    * **delete-rule** command: delete rule from the firewall group with specified name
    
      ```bash
      arvancli iaas firewall delete-rule --name "{FIREWALL_GROUP_NAME}" --number "{FIREWAULL_RULE_NUMBER}"
      ```
    
      *FIREWALL_RULE_NUMBER* can be achieved from "list-rules" command
    
    * **attach-server** command: attach server to the firewall group with specified name
    
      ```bash
      arvancli iaas firewall attach-server --name "{FIREWALL_GROUP_NAME}" --server "{SERVER_NAME}"
      ```
    
    * **detach-server** command:  detach server from the firewall group with specified name
    
      ```bash
      arvancli iaas firewall detach-server --name "{FIREWALL_GROUP_NAME}" --server "{SERVER_NAME}"
      ```
    


## Usage

1. First of all use python3.9 to prevent future problems!

2. Then install required packages and run setup script:

   ```bash
   pip install -e . -r requirements.txt
   ```
   
3. Then configure cli:

   ```bash
   arvancli configure --token="{API_TOKEN}" --zone="{DEFAULT_ZONE}"
   ```

4. And then run the cli:

   ```bash
   arvancli --help
   ```
