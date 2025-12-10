# The client's task
## Title
Urgent: WordPress/LearnDash Developer Needed to Fix Login Redirection Issue

## Description
Users are being redirected back to the login page when trying to access courses or lessons, even though they are already logged in.

This creates daily frustration for users and a massive support burden for our staff.

We’ve tried numerous solutions with different developers, and even LearnDash support has pointed out it’s likely tied to WordPress sessions, cookies, or permalink handling. 
Our current developer has been investigating, but we need someone who can come in quickly, isolate the root cause, and implement a permanent fix.

### What’s Happening:
- Users log in successfully, but when they click into a course/lesson, they are redirected back to the login page.
- Clearing cache or logging in via an incognito/private browser often “fixes” the issue temporarily.
- We’ve tested staging, but staging doesn’t replicate live user sessions (problem only shows with real user activity).

### Environment Details:
- Platform: WordPress; LearnDash LMS
- Hosting: cPanel/WHM (Apache, PHP-FPM, MariaDB), with Google Cloud storage integration in progress

### Logs we have:
- Custom MU plugin logging logins, cookies, and referrers
- login-audit.log tracking user logins in real time
- Apache/domlogs

### What We’ve Already Tried:
- Clearing and resetting server/session caches
- Restarting Apache/PHP-FPM
- Flushing OPcache, deleting /tmp session files
- Creating custom logging MU plugin to track login/session cookies
- Testing staging (problem does not reproduce there — only live with active users)

### What We Need From You:
- Diagnose and fix the root cause of the login redirection issue
- Audit session/cookie handling (WordPress core, LearnDash, any custom plugins)
- Ensure the fix works across all courses and lessons without having to manually update permalinks
- Provide a clear report of the root cause and implemented solution so we can maintain it long term

### Bonus Points if You Can:
- Suggest and implement hardening for session handling, caching, and redirects
- Audit our LearnDash & WordPress setup for other performance or stability issues
- Set up better logging so future issues can be quickly diagnosed

### Requirements:
- Proven experience with WordPress core session/auth systems
- Deep knowledge of LearnDash (courses, lessons, redirects, logins)
- Strong debugging skills (server logs, PHP logs, WordPress hooks/filters)
- Able to start immediately and work directly on our live system during peak hours (with our oversight)

### Deliverables
1. Permanent fix to the login redirection issue
2. Documentation of root cause + steps taken
3. Recommendations for long-term maintenance

### Questions
- How would you approach debugging this issue without disrupting live students?
- What’s your process for isolating a plugin conflict vs. WordPress core issue?