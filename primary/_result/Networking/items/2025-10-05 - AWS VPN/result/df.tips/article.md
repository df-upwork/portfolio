# My analysis
The most likely causes of your issue:
# 1. Incorrect configuration of the DNS servers in «**Client VPN endpoint**» (`E`)
[archive.is/dzXYE#selection-2645.11-2645.62](https://archive.is/dzXYE#selection-2645.11-2645.62)
## 1.1.
Old, **inaccessible Akamai DNS servers** might be specified.
## 1.2.
**No DNS servers** might be specified at all (the field is left empty). 
In this case, the DNS configuration is not passed to the client, and the client attempts to use its local DNS settings.
The subsequent behavior depends on the tunneling mode configured on `E` (split-tunnel or full-tunnel).
### 1.2.1. Split-tunnel mode
The client will be able to use local DNS servers to resolve public names.
This includes names defined in a Public Hosted Zone, even if they point to private IP addresses in the VPC.
However, the client **will not be able to resolve private DNS names** (e.g., names managed in a Route 53 Private Hosted Zone) because these can only be resolved by the Route 53 Resolver (`R`) within the VPC.
In this mode, AWS VPN Client on Windows does not set Windows Filtering Platform (`WFP`) rules to block local DNS traffic.
### 1.2.2. Full-tunnel mode
All client traffic is directed into the VPN tunnel through the default route (`0.0.0.0/0`).
This route intercepts traffic, including DNS queries destined for local and public DNS servers.
Additionally, when using the AWS VPN Client on Windows in full-tunnel mode, the AWS VPN Client applies `WFP` rules.
These rules force all DNS traffic into the tunnel and block access to local DNS servers to prevent DNS leaks.
If the DNS servers are not specified in the `E` configuration or are unavailable through the tunnel, this leads to a complete **failure of DNS resolution**.
# 2. Missing required authorization rules
[docs.aws.amazon.com/vpn/latest/clientvpn-admin/cvpn-working-rules.html](https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/cvpn-working-rules.html)
# 3. Incorrect configuration of routes
Routing issues depend on whether the split-tunnel mode is enabled on `E`.
## 3.1. Split-tunnel mode
The `E` route table must contain a route to the network where the DNS servers are located.
In this mode, only the routes defined in the `E` route table are added to the client device's route table. 
If a **route** to the DNS servers (e.g., `R` or Custom DNS) **is missing** from this table, it **will not be propagated to the client device**.
As a result, DNS queries cannot be routed through the VPN tunnel. 
The client device then attempts to route this traffic via its local network. 
Since this network usually does not have routes to the internal IP addresses of the VPC, the queries will fail (time out).
## 3.2. Full-tunnel mode
All client traffic, including DNS requests, is routed into the VPN tunnel via the default route (`0.0.0.0/0`).
In this case, a failure can occur if the **traffic cannot reach the DNS servers after entering the VPC**.
The traffic is routed through the subnets associated with `E`. 
Therefore, the VPC Route Tables of these associated subnets must be checked.
These tables must contain the correct routes to the DNS servers being used.
E.g., if Custom DNS servers in a remote network are used (connected via VPC Peering or a Transit Gateway), the corresponding routes are required in these tables.
Also, if public name resolution over the internet is required, these tables must contain a route to a NAT Gateway or an Internet Gateway.
The **absence** of these **routes** at the VPC level will lead to the **loss of DNS packets**.
# 4. Traffic filtering by Security Groups (`SG`)
## 4.1. 
When `E` is associated with subnets, traffic is filtered by an `SG`.
If Custom DNS servers are used (e.g., on an EC2 instance or an `R` inbound endpoint), this `SG` **must allow outbound traffic** on **port 53** (UDP/TCP) to these servers.
Traffic to `R` is not filtered by `SG`.
## 4.2. 
If Custom DNS servers located inside the VPC (e.g., an EC2 instance or an `R` inbound endpoint) are used, their associated SGs must be verified. 
These `SG`s **must allow inbound traffic** on **port 53** (UDP/TCP).
The Source for this inbound rule should ideally be the `SG` associated with `E`.
## 4.3. 
The network traffic flow has changed since the migration from Akamai.
Necessary rules may not have been added, or existing rules may be blocking traffic from the Client VPN network interfaces.
# 5. Traffic blocking by Network Access Control Lists (NACLs)
This is **unlikely**, primarily because the default NACL configuration allows all inbound and outbound traffic.
Furthermore, NACLs cannot block DNS requests to or from `R`.
Therefore, NACLs are **only relevant** if **Custom DNS servers** are used (e.g., on EC2 instances or an `R` inbound endpoint) and if restrictive custom NACLs have been configured in the VPC.
In that specific scenario, the NACL rules must be verified. 
Unlike `SG`s, NACLs are stateless, requiring explicit rules for both the outbound DNS query (port 53 UDP/TCP) and the inbound return traffic (ephemeral ports, typically `1024-65535`).