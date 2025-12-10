# My analysis
# I. Most likely causes of your problem:
## 1. CPU Burst Capacity
### 1.1. Essence
AWS Lightsail instances operate on the **burstable performance model**.
This model provides a **low baseline** of CPU performance with the ability to **temporarily exceed** it by consuming accumulated **CPU credits**.
If the CPU load exceeds the baseline level, these credits are consumed.
When the credits are depleted, the CPU performance is **forcibly limited** to the baseline level (e.g., **5-40%** of a full **vCPU's power**, depending on the instance plan).
This **limitation** (throttling) leads to a **sharp slowdown** in request processing or complete website unavailability.
### 1.2. Rationale
The nature of the problem, described as «**intermittent**», perfectly matches the cycle of **CPU credit exhaustion** under load and their slow recovery during idle time.
This is the **most common reason** for sudden performance degradation on Lightsail and EC2 T-series instances.
The baseline performance is often insufficient to serve a production WordPress website under load, especially when running background tasks or handling peak traffic.
## 2. RAM shortage and OOM Killer activation
### 2.1. Essence
The Linux kernel manages memory utilization by moving less frequently used memory pages from RAM to swap space when memory pressure increases.
This process can begin well before physical RAM is exhausted, depending on the configuration of the `vm.swappiness` parameter.
Intensive swap usage drastically reduces performance due to slow disk input/output operations, potentially leading to a critical state known as thrashing.
This intensive usage can be caused by either a high `vm.swappiness` setting or actual memory exhaustion.
If physical memory and swap space are exhausted, the Linux kernel activates the Out-of-Memory (OOM) Killer mechanism.
The OOM Killer forcibly terminates critical processes (often MySQL or Apache) to free up memory, causing a complete website unavailability.
### 2.2. Rationale
Lightsail instances, especially on lower-tier plans (e.g., 1GB or 2GB), often have insufficient RAM for a LAMP stack under load.
WordPress, especially with a large number of plugins, can consume a significant amount of memory.
A memory shortage is a typical cause of failures, such as the «Error establishing a database connection» message, which occurs when the MySQL process is terminated by the OOM Killer.
## 3. Suboptimal stack configuration (Apache / MySQL / PHP)
### 3.1. Essence
The configuration of the web server (Apache), the database (MySQL), and the PHP execution environment determines the resource consumption and the maximum concurrency allowed.
If these settings permit more concurrent processes than the available server resources (primarily RAM) can support, the system becomes unstable under load.
In setups using PHP-FPM, this occurs if parameters like `pm.max_children` are set too high, leading to excessive PHP processes.
In setups using Apache with the older `mod_php`, this occurs if the Multi-Processing Module (MPM) settings (e.g., `MaxRequestWorkers` in `mpm_prefork`) are set too high, leading to excessive, memory-heavy Apache processes.
An excessive number of processes leads to excessive consumption of RAM, exacerbating the problem from point 2.
If the parameters are set too low, the server will not be able to handle the incoming traffic efficiently, leading to service unavailability or slow response times.
### 3.2. Rationale
Default configurations provided by distributions or pre-packaged stacks (like Bitnami on Lightsail) are often not optimized for resource-constrained environments.
Automated tuning mechanisms might overestimate the available resources, especially if MySQL configuration (e.g., buffer pool size) consumes significant memory.
Whether using PHP-FPM or `mod_php`, tuning the balance between parallelism (the number of concurrent processes) and memory consumption is critically important on small servers.
If the configuration allows excessive concurrency, it leads to excessive memory consumption and causes the server to use swap, severely degrading performance.
## 4. Malicious traffic and bots (Brute-Force, XML-RPC, DDoS)
### 4.1. Essence
Automated attacks and aggressive bots create excessive load on the server, consuming CPU and memory resources and causing a denial of service.
The main attack vectors on WordPress include brute-force password attacks on `wp-login.php` and attacks via the `xmlrpc.php` interface.
### 4.2. Rationale
WordPress is a frequent target for automated attacks.
Attacks on `xmlrpc.php` leverage the `system.multicall` function to check hundreds of passwords in a single HTTP request.
This significantly amplifies the load and the effectiveness of the attack.
The Pingback feature can be exploited to conduct DDoS attacks, overwhelming the server with requests.
The intermittent nature of the problem is highly consistent with the patterns of attacks or bot activity.
Even low-intensity attacks can overload a small Lightsail instance.

# II. What monitoring and alerting stack do you typically recommend for small production environments?
## 1. Native AWS Stack (Lightsail Metrics + CloudWatch Agent)
### 1.1. Essence
This approach uses exclusively Amazon Web Services.
Built-in Lightsail metrics automatically collect hypervisor-level data (CPU utilization, network, CPU Burst Capacity).
Collecting operating system-level metrics (memory, disk) and application logs (Apache, MySQL) requires the installation of the CloudWatch Agent on the instance.
Data is centralized in Amazon CloudWatch for visualization, alerting (CloudWatch Alarms), and log analysis (Logs Insights).
### 1.2. Advantages
This approach leverages the native AWS monitoring capabilities (Lightsail Metrics and Amazon CloudWatch).
These capabilities are the definitive source for tracking CPU Burst Capacity (**I.1**) — the most likely cause of your problem.
Third-party monitoring solutions can also integrate with AWS APIs (e.g., the Lightsail API) to retrieve this metric.
However, the native stack provides the most direct access to this hypervisor-level data.
### 1.3. Disadvantages
The standard granularity for built-in Lightsail metrics is 5-minute intervals, and for standard CloudWatch custom metrics, it is 1-minute intervals.
This resolution is insufficient for diagnosing the rapid, transient spikes that characterize resource exhaustion scenarios (**I.2**, **I.3**).
Collecting custom metrics (memory, disk) via the CloudWatch Agent incurs charges based primarily on metric storage (cost per metric per month).
While CloudWatch offers high-resolution custom metrics (down to 1-second granularity), enabling them further increases costs.
This increase is driven by higher API usage (`PutMetricData` calls) due to more frequent data transmission.
Additionally, high-resolution alarms carry a higher price compared to standard alarms.
Collecting logs incurs additional charges for log ingestion and storage.
The configuration of the CloudWatch Agent, especially for log collection and custom application metrics, requires manual setup and maintenance compared to solutions with automated discovery.
A noticeable latency (seconds to minutes) exists between an event occurring and the corresponding metric or log appearing in CloudWatch, which complicates real-time troubleshooting.
## 2. High-granularity diagnostic monitoring (Netdata)
### 2.1. Essence
Netdata is an open-source tool for real-time system performance monitoring.
It is installed as a lightweight agent on the Lightsail instance.
The agent automatically discovers services (Apache, MySQL) and collects thousands of metrics with per-second granularity.
Data is available through a local web interface or the free Netdata Cloud service.
### 2.2. Advantages
The solution provides per-second granularity, which is invaluable for diagnosing the intermittent performance spikes characteristic of **I.2** and **I.3**.
The agent is extremely lightweight, consuming minimal CPU and memory resources, which is critical for a resource-constrained server.
The installation is straightforward and does not require configuration for standard LAMP stacks due to its auto-detection capabilities.
The solution offers excellent, pre-configured visualization of all system components and application performance.
While optimized for real-time troubleshooting, its database engine (`dbengine`) also provides efficient long-term storage for historical trend analysis using a multi-tiered architecture.
The alerting capabilities are sophisticated, supporting complex logic, hysteresis, and dynamic thresholds.
### 2.3. Disadvantages
The agent cannot directly monitor hypervisor-level metrics (such as AWS CPU Burst Capacity), as these are not visible from within the operating system.
Monitoring these metrics requires retrieving data from the AWS API (e.g., by implementing a lightweight custom collector that queries the Lightsail API via the AWS CLI or SDKs).
This adds complexity and latency.
It is not designed for centralized log management.
Compared to CloudWatch Alarms, its alerting capabilities offer fewer native integrations with the broader AWS ecosystem.
However, Netdata provides robust support for generic webhooks and direct integration with Amazon SNS.
This enables functionally equivalent integrations with key AWS services (such as AWS Lambda or Amazon EventBridge) to implement automated remediation actions.
The dashboard can appear complex due to the vast number of metrics presented.
## 3. Recommendation: Hybrid Approach (AWS Stack + Netdata)
### 3.1. Essence
For a comprehensive and cost-effective solution in a small production environment facing stability issues, I recommend a hybrid monitoring approach.
This strategy combines the strengths of the native AWS stack for infrastructure-level visibility and Netdata for high-granularity, real-time diagnostics.
### 3.2. Rationale
The two approaches are complementary, not mutually exclusive.
The AWS stack (**II.1**) is essential for monitoring hypervisor-level metrics, specifically CPU Burst Capacity.
Accurate tracking of this metric is critical for diagnosing the most probable cause of the issue (I.1), and it is not visible from within the operating system (and thus invisible to Netdata).
Netdata (**II.2**) is essential for diagnosing resource exhaustion at the OS and application levels (**I.2**, **I.3**).
Its per-second granularity, minimal overhead, and detailed visualization provide the necessary insights that the standard AWS stack lacks due to its lower resolution and latency.
This combination ensures complete coverage: AWS monitors the infrastructure constraints, while Netdata monitors the application's resource utilization within those constraints.
### 3.3. Implementation
Use built-in Lightsail metrics to monitor CPU Burst Capacity and configure critical CloudWatch Alarms based on low remaining capacity.
Install the Netdata agent for real-time performance troubleshooting and detailed analysis of memory, swap usage, disk I/O, Apache, MySQL, and PHP-FPM performance.
Optionally, if long-term centralized log management is required, deploy the CloudWatch Agent configured specifically for log collection (e.g., Apache `access.log`/`error.log`, MySQL `error.log`/`slow_query_log`), but carefully monitor the associated ingestion costs.

# III. «What’s your approach to finding the root cause of recurring Apache/MySQL downtime?»
My approach is a structured, multi-phase diagnostic workflow.
It is designed to systematically identify the root cause, **prioritizing the most probable causes** (**Section I**) while **starting with the least intrusive methods**.
It **progresses** from the **infrastructure layer** up to the **application layer**.

## 1. Phase 1: Non-Intrusive Data Collection and Configuration Review
This phase focuses on quickly understanding the failure mechanism and identifying immediate triggers related to resource exhaustion, high load, or misconfiguration.
This is achieved by analyzing existing data (metrics, logs, and configuration files).

### 1.1. Basic Infrastructure Metrics Monitoring
#### 1.1.1. Essence
This method utilizes the built-in AWS Lightsail monitoring tools to analyze the key performance metrics of the instance.
The primary focus is on CPU Utilization and remaining CPU Burst Capacity metrics.
#### 1.1.2. Advantages
This method is **critically important for diagnosing** **I.1**, as CPU Burst Capacity exhaustion leads to CPU throttling on Lightsail instances.
The metrics provide objective data to confirm the hypothesis of performance degradation due to AWS infrastructure limitations.
The tools are built into the AWS platform and do not require configuration on the server itself.
Analyzing historical data allows identifying CPU usage patterns and the frequency of quota exhaustion.
#### 1.1.3. Disadvantages
Standard Lightsail metrics do not include monitoring of RAM utilization and disk space usage, which is **critical for diagnosing I.2**.
The metrics show CPU resource exhaustion, but they do not indicate which specific processes caused this exhaustion.
The low granularity of the standard metrics can hide short load spikes.

### 1.2. System Log Analysis
#### 1.2.1. Essence
This method involves examining the Linux kernel logs (`dmesg`, `/var/log/kern.log`) and system logs (`/var/log/syslog`, `journalctl`) to identify critical events at the operating system level.
The main focus is on finding messages from the OOM Killer mechanism and service startup errors.
#### 1.2.2. Advantages
The method provides direct evidence of OOM Killer activation (**I.2**).
The analysis precisely identifies which process was terminated and when it occurred.
Analyzing existing system logs is non-intrusive and has virtually no impact on server performance.
Timestamps in the logs help to establish a precise timeline of events.
#### 1.2.3. Disadvantages
System logs record the failure mechanism (e.g., OOM) but not the root cause of memory exhaustion (e.g., a traffic spike).
Critical messages can be lost due to incorrect log rotation configuration or a kernel ring buffer overwrite.

### 1.3. Application Log Analysis
#### 1.3.1. Essence
This method involves a detailed analysis of existing web server logs (Apache `access.log` and `error.log`), database logs (MySQL `error.log` and, if available, `slow_query_log`), and PHP logs.
The goal is to understand traffic patterns, identify application errors, and determine inefficient database operations.
#### 1.3.2. Advantages
Analysis of the `access.log` is critically important for identifying traffic spikes, bot activity, or DDoS attacks (**I.4**).
This analysis enables the identification of attacks on vulnerable WordPress endpoints (`xmlrpc.php`, `wp-login.php`) that create excessive load.
If available, MySQL slow query logs directly indicate inefficient SQL queries that consume excessive resources.
Apache and PHP error logs record script execution failures, such as reaching the PHP memory limit or timeouts.
#### 1.3.3. Disadvantages
The volume of access logs can be very large, which makes manual analysis difficult without specialized aggregation tools.
Application logs do not provide direct information about the overall utilization of system resources (CPU, RAM) at the OS or infrastructure level.
If MySQL slow query logging is disabled, specific slow queries cannot be identified during this phase.

### 1.4. Stack Configuration Audit
#### 1.4.1. Essence
This method involves an audit of the Apache, MySQL, and PHP-FPM configurations relative to the available server resources (RAM and CPU).
If PHP-FPM is used, the Process Manager configuration is analyzed (**I.3**), focusing on the `pm` setting (e.g., dynamic, ondemand) and parameters controlling the number of child processes, primarily `pm.max_children`.
In Apache, the Multi-Processing Module (MPM) configuration (e.g., `mpm_event`, `mpm_prefork`) is reviewed to ensure efficient connection handling and to assess the PHP execution model (integration with PHP-FPM or use of `mod_php`).
In MySQL, parameters that affect memory consumption are examined, primarily the buffer pool size (`innodb_buffer_pool_size`).
1.4.2) Advantages
A suboptimal configuration is often a key factor in instability on resource-constrained servers.
The audit identifies potential configuration issues non-intrusively, without requiring any changes or service restarts.
It helps assess whether the stack configuration (Apache MPM and/or PHP-FPM) might allow creating an excessive number of processes, leading to memory exhaustion (**I.2**).
It also determines whether the MySQL configuration strikes an appropriate balance between database performance and overall system memory consumption.

## 2. Phase 2: Active Diagnostics and Intervention
If Phase 1 is inconclusive or indicates a need for more detailed data, this phase involves active interventions, such as implementing granular monitoring or activating detailed diagnostic logging.

### 2.1. Advanced Resource Monitoring
#### 2.1.1. Essence
This method focuses on obtaining detailed metrics that are unavailable in the standard Lightsail monitoring, primarily RAM and swap space usage.
This requires installing a monitoring agent (e.g., the AWS CloudWatch Agent) or using external systems.
#### 2.1.2. Advantages
Monitoring RAM and swap usage is absolutely essential for diagnosing the conditions leading to OOM Killer activation (**I.2**).
The method also enables the identification of performance degradation due to intensive swap usage (thrashing).
It fills critical gaps in the basic Lightsail metrics, providing a complete picture of the server's resource status.
Historical data enables the analysis of resource usage leading up to the downtime and the identification of trends such as memory leaks.

### 2.2. Diagnostic Configuration Activation
If critical diagnostic information was unavailable in Phase 1 (e.g., MySQL `slow_query_log` or detailed PHP error reporting was disabled), this step involves activating these features.
This provides the necessary data to correlate application behavior with resource consumption.

## 3. Phase 3: Deep Application Profiling
This phase focuses on analyzing application efficiency at the code level and is necessary if instability persists after infrastructure, traffic, and configuration issues are resolved.
This is the most intrusive phase and therefore requires specific mitigation strategies to protect the production website.

### 3.1. Risk Mitigation: Prioritizing Staging and Safe Production Profiling
Traditional, intrusive profiling tools can generate significant overhead.
Performing deep diagnostics with them on the live production server risks exacerbating the existing instability.
Therefore, the primary strategy is to reproduce the issue and conduct detailed profiling in a dedicated staging environment.
This environment must be an exact replica of the production setup, including the Lightsail instance size, operating system, stack configuration, and website data.

### 3.2. Application and Database Profiling
This method involves using specialized tools to analyze WordPress performance at the code and database query level.
When conducted in the staging environment, intrusive tools (e.g., detailed tracing profilers like Xdebug, plugins like Query Monitor) can be used under simulated load.
When conducted in the production environment, only low-overhead tools (e.g., continuous profiling via eBPF or lightweight APM agents) are used to identify slow PHP code and resource-intensive SQL queries under real load.
