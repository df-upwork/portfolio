# 1.
`T` ≔
~~~markdown
# The client's task
## Title
Cyber risk expert to ideate on risk scoring algorithms

## Description
Looking for someone to ideate cyber risk scoring formulas for vulnerabilities based on CVSS, EPSS, KEV, and environmental variables like asset configuration, sensitive data, etc.
~~~

# 2.
`S` ≔
~~~markdown
# My analysis
1) I outline my recommended approach in point 9.
Before that, I will describe the shortcomings of well-known approaches to provide context.
2) CVSS evaluates the theoretical severity of a vulnerability, but it correlates poorly with the actual likelihood of exploitation.
This leads to alert fatigue, where security teams face thousands of high-priority vulnerabilities, the majority of which will never be exploited by threat actors.
3) KEV indicates vulnerabilities with confirmed exploitation, making it very accurate.
However, KEV is reactive by nature — a vulnerability is added to the catalog only after an attack has already occurred.
It misses new and emerging threats.
4) EPSS is a more modern approach, a significant step forward compared to CVSS and KEV.
EPSS uses machine learning to predict the probability that a specific vulnerability will be exploited within the next month.
But it produces both false positives and false negatives.
5) The most recent approach is VMC (June–July 2025): https://arxiv.org/abs/2506.01220
It is based on CVSS, KEV, and EPSS and aims to address their shortcomings.
However, it does not consider «environmental variables», which are required in your case.
Reflecting on VMC and «environmental variables» led me to my own approach (point 9 below).
Before that, I will outline the essence of VMC:
5.1) Threat-Based Filtering.
At this stage, the presence of a real or predicted threat is assessed.
For each new vulnerability, a check is first performed for its presence in the KEV catalog.
5.1.1) If the vulnerability is found in KEV, it means there is a confirmed fact of exploitation, and it is passed on to the next stage (point 5.2).
5.1.2) If the vulnerability is not in KEV, the system checks its EPSS score.
An EPSS threshold of ≥ 0.088 is used, which, according to the research, represents an optimal balance between efficiency and coverage. 
5.1.3) Vulnerabilities that fail both of these checks (are absent from KEV and have an EPSS < 0.088) are considered not to pose an immediate threat and are deferred to standard patching cycles.
5.2) Vulnerability Severity Assessment.
This stage applies only to vulnerabilities that were identified as a threat in point 5.1.
Here, the traditional CVSS metric is used, but in a new role — as a filter for deprioritization.
For each vulnerability, its base CVSS score is checked against a threshold of CVSS ≥ 7.0.
5.3) After the previous step, 4 clear, actionable prioritization categories are obtained:
5.3.1) «Critical Priority»: vulnerabilities present in the KEV catalog and having a CVSS score ≥ 7.
These are confirmed, actively exploited vulnerabilities with high potential impact.
They require immediate remediation, typically within a few days.
5.3.2) «High Priority»: vulnerabilities with EPSS ≥ 0.088 and CVSS ≥ 7.
They have a high predicted probability of exploitation and high potential impact.
They should be addressed within an accelerated, but planned cycle (e.g., within 2-4 weeks).
5.3.3) «Monitor»: vulnerabilities that have signs of a threat (presence in KEV or a high EPSS) but with low potential impact (CVSS < 7). 
They require active monitoring for changes in the threat landscape or a reassessment of their impact, but do not require emergency remediation.
5.3.4) «Defer»: vulnerabilities with no signs of a threat (absent from KEV and EPSS < 0.088).
They can be remediated within standard, planned software update cycles.
6) The principle of VMC (point 5) is shown in the attached diagram, `1.png`.
7) Within VMC, CVSS is applied at the final stage, after a vulnerability has already been identified as a threat.
This allows CVSS's strengths, such as assessing potential technical impact, to be used for informed deprioritization.
8) VMC does not account for «environmental variables»; therefore, vulnerabilities with identical KEV, EPSS, and CVSS scores will have the same priority regardless of whether they reside on an insignificant development server or on a critically important production server that processes financial transactions.
9) My recommended approach (based on VMC and accounting for «environmental variables»).
9.1) Calculate the Environment Risk Modifier (ERM).
9.1.1)  The ERM adjusts the vulnerability risk.
9.1.2) The ERM should not be linear because the difference in urgency between remediating a vulnerability on an «important» asset versus a «critical» asset is disproportionately large.
9.1.3) For large organizations, I recommend calculating the ERM based on NIST.
9.1.4) Since your company is small (10-99 employees), in your case, I recommend (unless you are intermediaries) a simplified method: e.g., based on just 4 factors:
9.1.4.1) Assign a numerical score to each asset based on a formal matrix.
This matrix must be developed based on a business impact analysis (BIA) and contain clear criteria for each criticality level.
9.1.4.2) Assign a data sensitivity level (DSL) to each asset.
9.1.4.3) Classify each asset by its level of network exposure.
This is a critical factor because internet-facing services are primary attack vectors.
9.1.4.4) For each asset, document the existing compensating controls (particularly, firewalls, web application firewalls, intrusion prevention systems, endpoint detection and response, as well as practices such as network segmentation).
9.2) Apply VMC (points 5.1 - 5.3 above).
Thus, I take advantage of VMC's main benefit of filtering out ~87% of noise (an estimate from the article in point 5) belonging to the «Defer» category (point 5.3.4 above).
9.3) Assign a VMC weight (`VW`) to the categories 5.3.1 - 5.3.3 above:
- «Critical Priority» → 100
- «High Priority» → 50
- «Monitor» → 10
9.4) Calculate the final risk score (FRS): `FRS = VW * ERM`.
9.5) As a result, instead of the 4 static lists that VMC provides, my approach yields 3 dynamically ranked (in descending order of `FRS`) lists of tasks for the security team.
E.g., a vulnerability with `FRS = 200` (`VW = 100`, `ERM = 2.0`, i.e., on a critical server) will be remediated before a vulnerability with `FRS = 80` (`VW = 100`, `ERM = 0.8`, on a less important asset).
My approach preserves the main advantage of VMC — a radical reduction in the volume of work — and elegantly adds the required business context, enabling precise decisions about which critical vulnerability to remediate first.

~~~

# 3.
⊤ (`S` — это мой анализ изложенной в `T` задачи)





