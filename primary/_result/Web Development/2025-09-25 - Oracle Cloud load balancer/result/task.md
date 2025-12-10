# The client's task
## Title
DevOps, LB in OC spitting 502 when refreshing in a sveltekit SSR project

## Description
Running into a super annoying issue with Oracle Cloud’s load balancer and hoping someone here has seen it before.
### Setup:
Frontend is SvelteKit, sitting behind Nginx.
Traffic goes through an Oracle Cloud public load balancer (HTTPS).
Health checks are green, normal client-side navigation works fine.
### The problem:
If I refresh a page (so the app does a full server-side render instead of just SPA navigation), the load balancer often spits out a 502 Bad Gateway. 
If I hit the backend directly (bypass LB), everything works. It only happens through the LB, and only on refresh/deep links.

### What I’ve tried:
- Bumped up LB timeouts (idle + response) to 60–120s.
- Made sure SSR fetches don’t loop back through the public LB domain.
