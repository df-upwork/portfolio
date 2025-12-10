# My checklist
In my experience, the primary causes of poor performance in Next.js applications are the following:
# 1. Inefficient data fetching and processing
## 1.1. 
Sequential requests (`fetch` waterfalls) instead of parallel ones.
## 1.2. 
Slow queries to the database/API.
## 1.3. 
Over-fetching.
## 1.4. 
Blocking operations on the server that affect Time to First Byte (TTFB).
# 2. Suboptimal rendering and caching strategy
## 2.1. 
Using dynamic rendering (rendering at request time) for content suitable for static rendering (rendering at build time or upon revalidation).
## 2.2. Inefficient use of server-side caching mechanisms in the App Router
### 2.2.1. 
Incorrect data cache configuration. 
This includes unnecessarily using the `cache: 'no-store'` option for `fetch` requests or failing to utilize `unstable_cache` for data that could be cached. 
This increases the load on data sources.
### 2.2.2. 
Suboptimal revalidation strategies for data cache and full route cache (time-based revalidation or on-demand revalidation), leading to the display of stale data or too frequent content regeneration.
### 2.2.3. 
Unintentional disabling of the full route cache due to the use of dynamic functions (e.g., `cookies()`, `headers()`), opting the route into dynamic rendering and preventing caching of the rendering result.
### 2.2.4. 
Failing to use React `cache` for non-`fetch` requests (e.g., via an ORM or direct database queries), resulting in the duplication of identical requests within a single render pass, as these requests (unlike `fetch` requests) are not automatically memoized.
# 3. Large JavaScript bundles and hydration issues
## 3.1. 
Importing unnecessary libraries.
## 3.2. 
Insufficiently granular component-level code splitting: failing to utilize lazy loading (with `next/dynamic` or `React.lazy`) for non-critical or large client components.
## 3.3. 
Slow hydration due to excessive size or complexity of client components, leading to increased Time to Interactive (TTI) and Total Blocking Time (TBT).
## 3.4. 
Using client components instead of server components for non-interactive parts of the interface, leading to an excessive JavaScript bundle size and increased hydration workload.
# 4. Unoptimized resources and third-party scripts
## 4.1. 
Failing to use `next/image` for automatic image optimization (e.g., serving modern formats like WebP/AVIF, responsive sizing, and lazy loading).
## 4.2. 
Render-blocking fonts and third-party scripts (analytics, ads).
# 5 Infrastructure configuration issues (Cloudflare)
## 5.1. 
Inefficient CDN caching rules.
## 5.2. 
Runtime environment limitations (e.g., Edge Runtime), such as resource constraints (CPU time, bundle size) and incompatibilities with third-party libraries that rely on unsupported Node.js APIs.
