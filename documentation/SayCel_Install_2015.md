# SayCel Installation Guide
###### This document is the step by step guide to setting up an OpenBSC and BTS radio via a Puppet master running on a remote server.      

##### UBUNTU INSTALLATION

1. Download the ISO image of Ubuntu 12.04.5 LTS (Precise Pangolin)  http://releases.ubuntu.com/precise/ubuntu­12.04.5­server­amd64.iso
2. Make a bootable USB flash drive using "Startup Disk Creator" from Ubuntu.
3. Go to Puppet section of the Rhizomatica Git repository: https://github.com/Rhizomatica/puppet.git
4. Take the ```rhizomatica.seed``` file and copy it to the bootable usb flash drive inside the preseed directory folder.
5. Delete ```ubuntu-server.seed``` file and then rename ```rhizomatica.seed``` to ```ubuntu-server.seed```.

##### OpenVPN INSTALLATION AND CONNECTION
###### 1. From Digital Ocean server navigate to openvpn:
```
cd /etc/openvpn
```

###### 2. Compress conf and key files: 
```
tar -zcvf <name of zip file name>.tar.gz <location of folder being zipped>
tar -zcvf openvpn.tar.gz openvpn
```
###### 3. Copy files to BSC:
```
scp <openvpn configuration files>.tar.gz rhizomatica@<ip address of bsc>:.
scp openvpn.tar.gz rhizomatica@<ip address of bsc>:.
```
###### 4. Move files to openvpn folder on BSC:
```
sudo mv <openvpn configuration files>.tar.gz /etc/openvpn/.
```
###### 5. UnZip Files:
```
sudo tar xzf <openvpn configuration files>.tar.gz
```
use the ```update-resolv-conf``` from original openvpn
###### 6. Run OpenVPN on Server (Digital Ocean)
use ```server.conf``` file in this repository and place it in ```/etc/openvpn```

###### 7. Run OpenVPN on Client (BSC)
use ```client.conf``` file on this repository and place it in ```/etc/openvpn```

###### 8. Configure openVPN and start the connection between the server and client:

On Server:
    ```
    sudo openvpn --config /etc/openvpn/server.conf
    ```
On Client:
    ```
    sudo openvpn --config /etc/openvpn/client.conf
    ```
When this runs, you should connection initiate on Server.

 On Server:
    ```
    /etc/init.d/openvpn start
    ```
Check ```ifconfig```      tun0 should display

 On Client:
```
sudo /etc/init.d/openvpn start
```
Check ```ifconfig```     tun0 should display

##### INSTALLING PUPPET AGENT ON BSC
###### 1. Install Puppet
```
wget https://apt.puppetlabs.com/puppetlabs-release-precise.deb
sudo dpkg -i puppetlabs-release-precise.deb
sudo apt-get update
sudo apt-get install puppet
```
if you get errors after sudo apt-get update
do the following: 
```
sudo rm /var/lib/apt/lists/* -vf
sudo apt-get clean
sudo apt-get autoremove
sudo apt-get update
```
 
###### 2. Configure Network Settings:

   Navigate to ```/etc/hosts``` and add line:
```10.99.0.1       puppet```.

   Navigate to  ```/etc/network/interfaces```  and add:
```
auto eth1
iface eth1 inet static
        address 172.16.0.1
        netmask 255.255.255.0
```
###### 3. Configure Puppet Agent
To Enable Puppet Agent to start on bootup edit:

    ```/etc/default/puppet``` 
    
    and change:
    ```START=no```to ```START=yes```.
    
    Give proper permissions to cron jobs by: ```chmod 644 /etc/cron.d/rhizomatica```.
###### 4. SSL Certification
 *First*, check that the dates of the BSC and the remote server are in synch with ```date``` command.
*Next*, on BSC, ```sudo -i``` to switch to root user.  Run ```puppet agent --test```. It will hang until the RSA certification is signed by the remote server.
On the remote server, run ```puppet cert sign rhizo-bsc.rhizomatica.org``` and sign the certificate. 

***If there is an error,*** you will have to delete and reissue the certificate. Do the following and repeat the previous step.
    
***On BSC/Agent:***  ```rm -r  /var/lib/puppet/ssl```
    
***On Master/Remote Server:*** ```find /var/lib/puppet/ssl -name rhizo-bsc.rhizomatica.org.pem -exec rm {} \;```
###### 5. Move the RCCN folders
Copy the file from this repo, ```rccn-09062015.tar.gz``` to the BSC. 
```
scp rccn-09062015.tar.gz rhizomatica@<ip address of bsc>:.
```
    
Uncompress the file: ```sudo tar -xzf <openvpn configuration files>.tar.gz``` and move them into place: ```mv rccn-09062015 /var/rhizomatica```.

###### 6. Set up databases.
Create the hlr through osmo-nitb:  ```/etc/sv osmo-nitb start```. 
Run: ```puppet agent --test```.
Now, run ```python /var/rhizomatica/rccn/install.py``` to install the RIA database.
***If there is an error***, you will have to reset both of these data bases.
To do this: enter psql as user postgres: ```sudo -u postgres psql```. In POSTGRES:
```
drop database rhizomatica;
```
ctrl+d to exit POSTGRES. Repeat the database setup.
   
##### UPDATE FIRMWARE ON BTS

1. Connect your computer and the BTS to a router via ethernet and find the BTS's two IP address from the router's admin page. Change date on each system by ssh root@IP1  + ssh root@IP2 and running the command: ```date -s "3 JUN 2015 18:57:00" ```with your local date and time.

2. On your computer, install: [Fabric](http://www.fabfile.org/).
3. From your computer, run ```python setup-bts.py``` script. When prompted type in IP1.  When this intall finished, repeat with IP2. 
    
##### FINAL STEPS
4. Connect BTS to the BSC via ethernet.  Check connectivity by ```ping <IP1 of BTS>``` and ``` ping <IP2 of BTS>``` from the BSC.  
    ***If there is no response***, you will have to reconnect the BTS to a router and ssh into it again.  On ***both*** of the BTS's ip address, you will have to issue the following commands to update a syslink to a process called BusyBox that is interfering with the static IP address being issued correctly. 
```
cd /etc/rc5.d/
mkdir DISABLED
mv S20busybox-udhcpc DISABLED
ln -s ../init.d/busybox-udhcpc S20busybox-udhcpc
/etc/init.d/networking restart
```
Reconnect the BTS to the BSC and ping both IPs again. 

2. If everything is in communcation, it should be good to go. If your computer is on the same network as the BSC, navigate to  <BSC's IP Adrees>/rai/ in a browser.  You should see the login for the admin panel. 


## A Few Extra Configurations 
## On the BTS 
#### to check status
```sbts2050-util sbts2050-pwr-status```
#### to turn amp on
```sbts2050-util sbts2050-pwr-enable 1 1 1```
#### to turn amp off
```sbts2050-util sbts2050-pwr-enable 1 1 0```

## On the BSC
#### to run puppet agent once
```puppet agent --test```
#### to turn off puppet agent
```puppet agent --disable```
#### to turn on puppet agent
```puppet agent --enable```
    




## TROUBLESHOOTING
#### Error in RAI when provisioning:
Data Tables warning (table id = 'example')...

cd /var/rhizomatica/db/migrations
/etc/init.d/postgresql restart

get password for postgresql 
cat /var/rhizomatica/rccn/config_values.py
pgsql_pwd = 'yourpassword'


psql -U rhizomatica -h localhost < 011_location.sql
enter password from pgsql_pwd 

restart freewitch and rapi
sudo sv restart freeswitch
sudo sv restart rapi

restart bsc
