# My analysis
I have identified the **2 most likely causes** of this problem, which can occur independently or in combination.  
I outline them in **points 1** and **2** below.  
The «**WordPress sessions**» cause, to which LearnDash support pointed you, is **far less likely**.  
I discuss it in **point 3**.
# Cause #1: Incorrect configuration of caching or intermediary layers (Proxy/CDN)
## 1.1. Essence
This cause **most likely** manifests under **scenario 1.1.1**.  
**Scenario 1.1.2** is **much less likely** for the reason detailed in point **1.2.3**.
### 1.1.1. Incorrect operation of page caching and redirect caching
This is the most common mechanism.  
WordPress authentication is based on cookies (whose names start with `wordpress_logged_in_`).  
Page caching systems (e.g., at the web server level, such as Apache, Proxy, CDN, or caching plugins) must be configured to bypass the cache when these cookies are present.  
Using the cache variation mechanism (e.g., the `Vary` header) is inappropriate in this case.  
The value of authentication cookies is unique for each user session.  
Varying the cache based on a unique value will create a separate cache entry for each session.  
This completely negates the effectiveness of page caching (cache hit rate).  
If the configuration is incorrect, the caching system ignores these cookies and processes the request as if it were anonymous.  
When an authorized user requests a protected URL (e.g., a course or a lesson), the caching system may return a response previously generated for a guest (cache hit).  
If a redirection response (an HTTP `302` to the login page, which is generated for guests) has been cached for this URL, the user is immediately redirected back to the login page.  
In this scenario, the request is served by the caching system.  
PHP may not execute at all (if the cached response is served by the Apache web server, a Proxy, or a CDN).  
Alternatively, PHP execution may be halted at an early stage (e.g., via the `advanced-cache.php` drop-in mechanism when using WordPress caching plugins).
### 1.1.2. Incorrect cookie stripping
An intermediate layer (e.g., a CDN, Proxy, Load Balancer, or the Apache web server configuration) might be incorrectly stripping authentication cookies before the request reaches the WordPress application.  
In this scenario, the request reaches the WordPress Core.  
However, since the authentication cookies are absent, the `is_user_logged_in()` function returns `false`.  
To protect the content, WordPress (often via the `auth_redirect()` function) or LearnDash initiates a redirection to the login page.
## 1.2. Rationale
### 1.2.1. 
You write that clearing the cache or logging in via an incognito/private browser often «fixes» the issue temporarily.
### 1.2.2. 
This indicates that the user is receiving a stale response, which strongly suggests a cached redirect (**scenario 1.1.1**).  
Client-side actions cannot fix the server configuration, but they can temporarily bypass the issue by changing the state of the request or the local cache.  
This occurs through **2 mechanisms**:
#### 1.2.2.1. Interaction with browser cache
In scenario 1.1.1, the server-side caching system incorrectly returns a cached redirect response (e.g., HTTP 302) to an authenticated user.  
If this response contains cache control headers (e.g., `Cache-Control` or `Expires`) added by the caching layer, the browser may store it locally.  
In this case, the browser performs the redirection locally without contacting the server again.  
Clearing the browser cache or using incognito mode forces the browser to discard the locally stored response and send a new request to the server.
#### 1.2.2.2. Temporary bypass of server-side cache
Incognito mode or clearing cookies requires re-authentication.  
The login process changes the session characteristics.  
For example, the `wp-login.php` response contains the `Set-Cookie` header.  
Some caching systems may interpret this as a signal to temporarily disable the cache for this session (e.g., the Hit-for-Pass mechanism).  
Additionally, the request immediately following login may contain a specific `Referer` header.  
These factors may allow the first request after login to successfully reach WordPress, bypassing the incorrect cached response.  
However, the problem returns on subsequent requests when these conditions are no longer met.
### 1.2.3. 
Symptom **1.2.1** makes **scenario 1.1.2** **much less likely** than scenario 1.1.1.  
If the infrastructure configuration were homogeneous, a persistent cookie stripping rule would be applied to every request, and client-side actions would not result in a temporary fix.  
However, in a non-homogeneous environment (e.g., multiple servers behind a load balancer), configurations might differ across nodes, making it possible that only some nodes incorrectly strip cookies.  
In such a case, starting a new session might direct the user to a correctly functioning node, which would appear as a temporary fix.
# 2. Cause #2: Incorrect operation of object caching.
## 2.1. Essence
In the project tags, you have specified Redis and Memcached.  
If your system uses these technologies for object caching, critical authentication data is cached in memory.  
WordPress uses session tokens (stored in `wp_usermeta`) to track the user's login state.  
Under high load, the state of these tokens in the object cache can become inconsistent with the actual state in the MariaDB database.  
When a user navigates to a protected page, WordPress performs an authentication check using the `wp_validate_auth_cookie()` function.  
When a persistent object cache is active, this function uses the cache as the primary data source to retrieve session tokens (e.g., via `get_user_meta()`).  
If WordPress reads an incorrect (stale or corrupted) session token from the cache (cache hit), the authentication check fails.  
As a result, WordPress considers the user unauthenticated (`is_user_logged_in()` returns `false`) and initiates a redirection to the login page.  
This can occur in **2 scenarios**:
### 2.1.1. Stale Cache
When session tokens are updated in the database (e.g., upon login, logout, or automatic session extension), the corresponding data in the object cache must be invalidated or updated.  
If the invalidation mechanism works incorrectly (e.g., due to a configuration error, a plugin conflict, or database replication issues), subsequent requests may receive stale data from the cache.  
Using a stale token leads to an authentication failure.
### 2.1.2. Race Condition
Under high load and concurrent requests (e.g., AJAX), a race condition can occur when updating session tokens in the cache.  
Although the basic operations (e.g., GET, SET) in Redis and Memcached are atomic, the race condition occurs at the application logic level in the read-modify-write cycle.  
This cycle (the application reads the token array from the cache, modifies it in PHP, and writes it back) is not atomic.  
If multiple processes simultaneously modify this array, it can lead to a lost update and an inconsistent state in the cache.  
Reading this inconsistent state leads to an authentication failure.
## 2.2. Rationale
### 2.2.1. 
The combination of high user activity (which is present on production but not on staging) and the use of an external object cache creates the conditions for stale cache and race conditions.
### 2.2.2. 
This mechanism explains why users are redirected, «even though they are already logged in».  
The authentication cookie is present in the browser, but the authentication check fails due to a temporary inconsistency of the session tokens in the object cache during a specific request.
# 3. Cause #3: Problems with PHP native sessions
## 3.1. Essence
This cause is **far less likely** (rationale in point **3.2**), but it should be considered, as there are indications that PHP native sessions (`$_SESSION`) are used in your system.  
Although WordPress Core does not use `$_SESSION` for authentication, some plugins (e.g., BuddyBoss, mentioned in the tags) can initiate these sessions.  
The fact that you are deleting `/tmp` session files also suggests their use.  
If PHP sessions are active, their use creates concurrency challenges under high load (which occurs on production but not on staging).  
Specific problems depend on the PHP `session.save_handler` configuration and manifest themselves in 2 main scenarios:
### 3.1.1. Session Locking
If the standard handler (`session.save_handler = files`) is used, parallel requests (e.g., AJAX) block each other when calling `session_start()`.  
This leads to resource contention and significant delays.
### 3.1.2. Race Conditions
If an external handler (e.g., Redis or Memcached, mentioned in the tags) is used with disabled or ineffective locking, parallel requests can corrupt session data.
## 3.2. Rationale for low probability
These scenarios are unlikely to be the direct cause of the redirection loop due to a symptom mismatch.
### 3.2.1. 
**Session Locking** (point **3.1.1**) leads to **performance bottlenecks**.  
Symptoms typically include server errors (e.g., HTTP `504 Gateway Timeout` or HTTP `500 Internal Server Error`), rather than a simple redirect (HTTP `302`) to the login page.
### 3.2.2. 
**Race Conditions** (point **3.1.2**) cause **data corruption** in `$_SESSION`.  
This can affect the logic of plugins (LearnDash/BuddyBoss), but it **does not affect** the standard **WordPress Core authentication** mechanism.  
WordPress Core authentication is based on cookies and session tokens, not on `$_SESSION`.
### 3.2.3. 
Overall, these mechanisms contribute to the general instability of the system under load, rather than specifically causing this problem with the redirection loop.
# 4. «How would you approach debugging this issue without disrupting live students?»
## 4.1. Passive Diagnostics
The goal of this stage is to identify the layer generating the redirection (CDN, Proxy, Apache, or WordPress/PHP) without making changes to the production code or configuration.
### 4.1.1. Analysis of configuration and HTTP Headers (diagnosing Cause #1)
#### 4.1.1.1. 
Analyze the configuration of all page caching layers (CDN, Proxy, Apache modules, WordPress plugins) regarding authentication cookie handling rules.
#### 4.1.1.2. 
Analyze HTTP Response headers (e.g., `X-Cache`, `Cache-Control`, `Age`) of requests to protected URLs.
The presence of headers indicating a cache hit in the HTTP `302` response will confirm **scenario 1.1.1**.
### 4.1.2. Object Cache Analysis (diagnosing Cause #2)
#### 4.1.2.1. 
Analyze the Redis/Memcached integration configuration.
#### 4.1.2.2. 
Analyze cache operations (GET/SET/DELETE) related to session tokens during test login attempts using real-time monitoring tools (e.g., `redis-cli monitor`).  
This allows for observing potential inconsistencies (stale cache or race conditions) without flushing the global cache, which would cause a forced logout of all students.
### 4.1.3. Analysis of existing logs
Perform a correlation analysis of the Apache `domlogs`, `login-audit.log`, and the logs from your MU plugin to identify redirection patterns.
## 4.2. Conditional Debugging
If passive diagnostics does not provide a definitive answer, proceed to active debugging methods.
### 4.2.1. Enhanced Logging
Modify the MU plugin for detailed logging of the authentication process (e.g., the result of `wp_validate_auth_cookie()`) and the state of cookies.
This logging will be activated only by using a special debug cookie or for a specific test `user_id`.
### 4.2.2. Controlled Cache Bypass
Temporarily configure rules to force a page cache bypass only for test requests.
Use the `wp_using_ext_object_cache` filter to temporarily disable the object cache only for my test session.
## 4.3. Staging Reproduction
Since the problem depends on the load, conduct Load Testing on the Staging environment.  
Using tools (e.g., Apache JMeter or k6), simulate parallel authenticated sessions to artificially create race conditions (**Cause 2.1.2**).  
This will allow to safely reproduce the problem and test the fixes before deployment to production.
# 5. «What’s your process for isolating a plugin conflict vs. WordPress Core issue?»
## 5.1. General principle: systematic isolation
This involves systematically simplifying the Runtime Environment to a minimal configuration (vanilla WordPress).  
This makes it possible to determine whether the failure is caused by the code of third-party components (plugins or the theme) or by the base platform (WordPress Core or infrastructure).
## 5.2. Isolation procedure on production
### 5.2.1. 
Creating a **clean environment** using the **conditional deactivation** technique.  
This is implemented via a Must-Use Plugin (`mu-plugin`) or specialized tools (e.g., the «Health Check & Troubleshooting» plugin).  
This method creates a clean environment (**deactivates plugins** and **switches the theme** to a **default** one, e.g., Twenty Twenty-Five) only for an admin session.  
Other users continue to use the website unaffected.
### 5.2.2. Baseline Check
Attempt to reproduce the problem in the isolated clean environment (point **5.2.1**).
#### 5.2.2.1. 
If the problem is reproduced, this indicates a problem in WordPress Core, Must-Use Plugins (including your custom MU plugin for logging) or the infrastructure configuration (server configuration, caching layers).  
In this case, proceed to the analysis of the infrastructure and WordPress Core (point **5.2.4**).
#### 5.2.2.2. 
If the problem is not reproduced, this strongly indicates a **plugin conflict** or a **theme conflict**.
In this case, proceed to the isolation of the conflicting component (point **5.2.3**).
### 5.2.3. Isolating the conflicting component
Activate components while maintaining the isolated session.
#### 5.2.3.1. 
Activate the current theme.   
If the problem returns, the source of the conflict is in the theme.
#### 5.2.3.2. 
If not, activate the critical plugins (LearnDash, BuddyBoss) and check if the problem returns.     
If it does, the conflict is related to these plugins.
#### 5.2.3.3. 
If the problem still does not return, use the **binary search** method on the remaining plugins: activate half of them and check again.   
Repeat the process, narrowing the search to identify the specific plugin or combination of plugins causing the conflict.
### 5.2.4. Differentiating between WordPress Core and infrastructure
#### 5.2.4.1. 
Check the integrity of WordPress Core files for modifications.
#### 5.2.4.2. 
Analyze the infrastructure configuration (Apache, PHP-FPM, Redis/Memcached, Caching rules), as these are the most likely causes for problems that only manifest in the production environment (as described in points 1-3).
#### 5.2.4.3. 
If the previous steps do not reveal the cause, consider the possibility of an error in WordPress Core.  
In this case, perform deep debugging using Xdebug to analyze the authentication flow and search for known issues in WordPress Trac.