## 1.
Потенциальный клиент опубликовал на Upwork следующий проект:
### 1.1. Title
Juniper & Cisco Network Configuration Expert Needed

### 1.2. Description
We are seeking a skilled network expert with experience in Juniper and Cisco technologies to assist in configuring high availability (HA), getting our existing 4G failover to work on Juniper SRX300 HA pair, and a Cisco Catalyst switch stack.
The ideal candidate will have a strong background in network security and performance optimization. You will be responsible for providing JunOS and Cisco IOS configuration changes required to get the 4G WAN failover working, as well as appropriate config to setup LAG (or other) to enable multiple uplinks to our Cisco core switch stack.
4G WAN failover must use multiple probes, and adjust DNS forwarding as necessary.

### 1.3. Tags
Juniper
Network Administration
Network Equipment
Cisco IOS
Cisco Certified Network Professional
Cisco Router
Junos OS
JNCIA-Junos

## 2. Мой ответ клиенту
Я хочу ответить клиенту так:
~~~
HA on a Juniper SRX300 pair is done as follows:
1) Connect `ge-0/0/1` (node0) with `ge-1/0/1` (node1) for the control link.
2) Connect `ge-0/0/7` (node0) with `ge-1/0/7` (node1) for the fabric link.
3) Connect 4G modems: I recommend 2 modems (one for each node) to physically provide 4G on both SRX devices.
4) Connect multiple ports (for LAG) from each SRX300 to the Cisco Catalyst stack.
5)
```
set system host-name srx300-node0
set system root-authentication plain-text-password
set system services ssh
```
6) On the primary SRX300, configure the chassis cluster:
6.1) If the SRX is still in standalone mode, then enable the cluster:
```
set chassis cluster cluster-id 1 node 0 reboot
commit
```
After the reboot, switch to the cluster mode, and interfaces will be renamed to the format `ge-0/0/x`, `ge-1/0/x`.
6.2)
```
set chassis cluster cluster-id 1 node 0
set chassis cluster reth-count 2
set chassis cluster redundancy-group 0 node 0 priority 200
set chassis cluster redundancy-group 0 node 1 priority 100
set chassis cluster redundancy-group 1 node 0 priority 200
set chassis cluster redundancy-group 1 node 1 priority 100
set chassis cluster redundancy-group 1 node 0 interface-monitor ge-0/0/2 weight 255
set chassis cluster redundancy-group 1 node 0 interface-monitor ge-0/0/0 weight 255
set chassis cluster redundancy-group 1 node 1 interface-monitor ge-1/0/2 weight 255
set chassis cluster redundancy-group 1 node 1 interface-monitor ge-1/0/0 weight 255
set chassis cluster control-link ge-0/0/1
set chassis cluster cluster-id 1 node 0 fabric-link ge-0/0/7
commit check
commit
request system reboot
```
Wait for the reboot to complete.
7) On the secondary SRX300 (node1) configure the chassis cluster:
7.1) If the SRX is still in standalone mode, first enable the cluster (similar to 6.1):
```
set chassis cluster cluster-id 1 node 1 reboot
commit
```
7.2)
```
set chassis cluster cluster-id 1 node 1
set chassis cluster control-link ge-1/0/1
set chassis cluster cluster-id 1 node 1 fabric-link ge-1/0/7
commit check
commit
request system reboot
```
8) Configure redundant Ethernet interfaces:
```
set interfaces reth0 redundant-ether-options redundancy-group 1
set interfaces reth0 aggregated-ether-options lacp active
set interfaces reth0 aggregated-ether-options minimum-links 1
set interfaces reth0 unit 0 family inet address 192.168.1.254/24

set interfaces reth1 redundant-ether-options redundancy-group 1
set interfaces reth1 aggregated-ether-options lacp active
set interfaces reth1 unit 0 family inet address 10.0.0.254/30
```
9) Bind physical interfaces to the redundant interfaces:
```
set interfaces ge-0/0/0 gigether-options redundant-parent reth0
set interfaces ge-1/0/0 gigether-options redundant-parent reth0
set interfaces ge-0/0/2 gigether-options redundant-parent reth1
set interfaces ge-1/0/2 gigether-options redundant-parent reth1
```
10) Configure a 4G interface on the primary SRX300 (PPP):
```
set interfaces pp0 unit 0 family inet negotiate-address
set interfaces pp0 unit 0 ppp-options chap access-profile 4g-profile
set interfaces pp0 unit 0 ppp-options pap access-profile 4g-profile
set access profile 4g-profile authentication-order [ chap pap ]
set access profile 4g-profile client [username] secret [password]
```
11) Configure a backup route over 4G:
```
set routing-options static route 0.0.0.0/0 qualified-next-hop 10.0.0.253 preference 10
set routing-options static route 0.0.0.0/0 next-hop pp0.0 preference 20
```
12) Configure `ip-monitoring` to check the main link:
```
set services ip-monitoring enable

set services ip-monitoring policy MAIN-LINK test test1 probe-count 5
set services ip-monitoring policy MAIN-LINK test test1 test-interval 5
set services ip-monitoring policy MAIN-LINK test test1 target 8.8.8.8
set services ip-monitoring policy MAIN-LINK test test1 source-interface reth1.0

set services ip-monitoring policy MAIN-LINK then preferred-route route 0.0.0.0/0 next-hop 10.0.0.253 qualified-next-hop pp0.0
set services ip-monitoring policy MAIN-LINK then failover-route route 0.0.0.0/0 next-hop pp0.0
```
13) Configure DNS servers for the main link:
```
set system name-server 8.8.8.8
set system name-server 8.8.4.4
```
14) Configure DNS forwarding with automatic switching:
```
set system services dns forwarding server 8.8.8.8
set system services dns forwarding server 8.8.4.4

set event-options policy primary-down events chassiscluster_status_change
set event-options policy primary-down within 30
set event-options policy primary-down match "RG1: node0 lost the primary role"
set event-options policy primary-down then execute-commands commands "delete system services dns forwarding server 8.8.8.8"
set event-options policy primary-down then execute-commands commands "delete system services dns forwarding server 8.8.4.4"
set event-options policy primary-down then execute-commands commands "set system services dns forwarding server [the 4G provider's DNS server]"
set event-options policy primary-down then execute-commands commands "commit"

set event-options policy primary-up events chassiscluster_status_change
set event-options policy primary-up within 30
set event-options policy primary-up match   "RG1: node0 gained the primary role"
set event-options policy primary-up then execute-commands commands "delete system services dns forwarding server [the 4G provider's DNS server]"
set event-options policy primary-up then execute-commands commands "set system services dns forwarding server 8.8.8.8"
set event-options policy primary-up then execute-commands commands "set system services dns forwarding server 8.8.4.4"
set event-options policy primary-up then execute-commands commands "commit"
```
15) Configure link aggregation on the SRX300:
```
set interfaces ge-0/0/3 gigether-options redundant-parent reth0
set interfaces ge-1/0/3 gigether-options redundant-parent reth0
```
16) Configure EtherChannel on Cisco Catalyst:
```
interface range GigabitEthernet1/0/1-2
 description Link to SRX300 HA Pair
 channel-group 1 mode active
 no shutdown

interface Port-channel1
 description LAG to SRX300 HA Pair
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
 no shutdown
```
17) Check the status of the HA cluster:
```
show chassis cluster status
show chassis cluster interfaces
```
18) Check the LAG operation:
```
show interfaces reth0 extensive
show lacp interfaces reth0
```
19) Test the failover:
19.1) Physically disconnect the main WAN link.
19.2) Check if the connection has switched to 4G.
19.3) Verify that the DNS forwarding has changed correctly.
19.4) Plug the main link back in and check its reversion.
20) Test HA:
20.1) Power off the primary SRX300 device.
20.2) Verify that the secondary device has taken over.
20.3) Power on the primary device and verify that the cluster recovers correctly.
21) Configure security zones:
```
set security zones security-zone TRUST interfaces reth0.0 host-inbound-traffic system-services all
set security zones security-zone TRUST interfaces reth0.0 host-inbound-traffic protocols all
set security zones security-zone UNTRUST interfaces reth1.0 host-inbound-traffic system-services ping
set security zones security-zone UNTRUST interfaces reth1.0 host-inbound-traffic protocols bgp  # example
set security zones security-zone UNTRUST interfaces pp0.0 host-inbound-traffic system-services ping
```
22) Configure NAT and security policies:
```
set security nat source rule-set RS1 from zone TRUST to zone UNTRUST
set security nat source rule-set RS1 rule R1 match source-address 192.168.1.0/24
set security nat source rule-set RS1 rule R1 then source-nat interface
set security policies from-zone TRUST to-zone UNTRUST policy ALLOW-ALL match source-address any
set security policies from-zone TRUST to-zone UNTRUST policy ALLOW-ALL match destination-address any
set security policies from-zone TRUST to-zone UNTRUST policy ALLOW-ALL match application any
set security policies from-zone TRUST to-zone UNTRUST policy ALLOW-ALL then permit
```
~~~

## 3. Твоя задача
Я хочу опубликовать ответ на своём сайте в виде статьи.
Дай статье заголовок.
Заголовок должен начинаться со слов «How to».
Заголовок должен быть вопросительным предложением.
Заголовок должен быть максимально точным: упоминать все используемые технологии, весь контекст задачи.
Предложи 5 вариантов заголовка.
