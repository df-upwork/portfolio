# My analysis
# 0.
Your cookie error is most likely caused by the reverse proxy server changing the interaction context between the client and the backend application.  
Cookies set by the backend for the internal context (domain, path, protocol) become invalid for the client's browser.  
I consider **5 hypotheses** to be the most likely in your situation.
# 1. Hypothesis #1: Cookie `Domain` attribute mismatch
## 1.1. The essence
The backend application sets a Cookie with a `Domain` attribute that matches its internal address (e.g., `internal.local`).  
The client's browser, which connects via the external address (e.g., `proxy.com`), rejects this Cookie due to the domain mismatch.
## 1.2. Plausibility arguments
### 1.2.1. 
In the project description, you specified access to the website in a «restricted network».  
This strongly implies the use of internal domain names that differ from external ones.
### 1.2.2. 
By default, Nginx does not modify the `Domain` attribute in the `Set-Cookie` header returned by the backend.  
The `proxy_cookie_domain` directive is required to rewrite this attribute correctly.
# 2. Hypothesis #2: Issues with SSL/TLS termination and the `Secure` flag
## 2.1. The essence
Nginx terminates SSL/TLS (accepts HTTPS from the client), but interacts with the backend over insecure HTTP.  
The backend is not aware of the original secure connection and perceives the request as HTTP.  
This leads to authentication errors because the backend generates incorrect absolute URLs for redirection (using `http://` instead of `https://`) or refuses to establish a session, considering the transport insecure.
## 2.2. Plausibility arguments
### 2.2.1. 
Your phrase «Ensure secure access» implies the use of HTTPS.  
SSL termination on the reverse proxy is a standard practice.  
### 2.2.2. 
If Nginx does not forward information about the original protocol (e.g., via the `X-Forwarded-Proto: https` header), the backend considers the connection insecure, leading to the issues described in 2.1.  
Furthermore, if the backend incorrectly perceives the connection as insecure (HTTP), it will likely not set the `Secure` flag on cookies.  
This is problematic because modern browsers require the `Secure` flag for any cookie marked with `SameSite=None` (which is often necessary in reverse proxy scenarios).
# 3. Hypothesis #3: Incorrect `Host` header forwarding
## 3.1. The essence
Nginx forwards an incorrect `Host` header to the backend (e.g., the upstream server's name or its IP address instead of the external domain name used by the client).  
The backend uses this value to generate absolute redirect URLs after login.  
Additionally, this value is used as the target origin for Cross-Site Request Forgery (CSRF) protection.
## 3.2. Plausibility arguments
Many web frameworks compare the value of the `Host` header (target origin) with the values of the `Origin` and/or `Referer` headers (source origin) for CSRF protection.  
A mismatch, caused by an incorrect `proxy_set_header Host` configuration, causes this check to fail (e.g., a 403 Forbidden error), resulting in authentication failure.  
If the application uses the `Host` header to set the `Domain` attribute in the Cookie, this scenario is the root cause of Hypothesis #1.
# 4. Hypothesis #4: Cookie path mismatch
## 4.1. The essence
The backend application sets a cookie with a `Path` attribute matching its internal path (e.g., `/internal-app/`).  
The client's browser accesses the application via the proxy using a different path (e.g., `/`).  
The browser does not send the cookie in subsequent requests because the current request path does not match the cookie's `Path` attribute.
## 4.2. Plausibility arguments
### 4.2.1. 
Changing the URL structure is a common practice when publishing an internal application via a reverse proxy.
### 4.2.2. 
By default, Nginx does not modify the `Path` attribute in the `Set-Cookie` header.
The `proxy_cookie_path` directive is required to rewrite this attribute correctly.
# 5. Hypothesis #5: Cookie blocking due to the `SameSite` attribute
## 5.1. The essence
When the reverse proxy configuration causes a change of domain (site), the interaction context, from the browser's perspective, shifts from same-site to cross-site.  
Consequently, the browser blocks authentication cookies, as they do not meet the requirements for the cross-site context.
## 5.2. Plausibility arguments
Modern browsers apply the `SameSite=Lax` policy by default if the `SameSite` attribute is not explicitly set.  
Both `Lax` and `Strict` policies prevent cookies from being sent in cross-site requests (e.g., `POST` requests after a redirect).  
Using cookies in a cross-site context requires explicitly setting `SameSite=None`.   
This setting must be accompanied by the `Secure` flag.  
If the backend does not set these attributes correctly, or if they are not modified by Nginx (e.g., using the `proxy_cookie_flags` directive), authentication will fail.