# My guidance
# 1. «the new sales tax setup makes no sense»
The system's logic is specifically designed to ensure compliance with complex tax legislation.  
California uses a modified origin sourcing model for intrastate sales.  
State, county, and city taxes are origin-based, whereas district taxes are destination-based.  
Automated Sales Tax (`AST`) in QuickBooks Online (`QBO`) automatically handles these complex rules and thousands of jurisdictions in the Bay Area.  
Managing this manually is highly impractical and prone to errors.  
# 2. «seems that sales tax rate needs to be added manually» 
That is incorrect.  
The purpose of `AST` is specifically to eliminate the need for manual tracking and input of tax rates.  
Intuit automatically updates the rates when the legislation changes.  
# 3. «The customer section has a box checked for “sales tax” but there is nothing further than that»
Since the rate depends on the exact shipping address in a specific transaction, which can change, storing a static rate in the customer profile is incorrect.  
Therefore, `AST` intentionally does not store the rate in the customer profile.  
The profile only determines the tax status (Taxable/Exempt).  
Intuit removed the ability to set a default tax code once `AST` is activated.  
# 4. «I need to have clients sales tax rates setup and flowing to 3rd party tool»
## 4.1.
The `AST` system calculates tax dynamically at the time of the transaction.  
The standard `QBO` Accounting REST API (V3) does not allow a third-party application to retrieve the tax rate calculated by `AST` before a transaction is created and saved in `QBO`.  
## 4.2. 
There are **2** main **approaches** to solving this integration problem.
I outline them in **points 5** and **6** below.  
The feasibility of either approach depends on the technical capabilities of the third-party tool and its ability to integrate with external APIs or to modify its synchronization logic with `QBO`.  
# 5. Approach 1: Implementing a specialized tax service (e.g., Avalara, TaxCloud, TaxJar)
The third-party tool must integrate with the API of this service to retrieve the accurate tax rate in real time.  
# 6. Approach 2: Integrating the third-party tool with the Intuit Sales Tax API (GraphQL)
This allows the tool to retrieve the `AST`-calculated rate in real time.  
# 7. 
In both approaches, during the subsequent synchronization of a transaction with `QBO` via the Accounting REST API (V3), the Sales Tax Override mechanism must be used.  
For a reliable override, this requires not only passing the total tax amount via the `TxnTaxDetail.TotalTax` field, but also providing a reference to a Custom Sales Tax Code (`USER_DEFINED` type) via the `TxnTaxDetail.TxnTaxCodeRef` field.   
Additionally, an up-to-date API version (`minorversion`) must be used.  
# 8. 
**Approach 1** has the following **advantages** compared to Approach 2:
## 8.1. Increased accuracy and compliance
Specialized services use advanced address validation and geolocation methods (address-level accuracy) to account for all local and district taxes.  
This ensures maximum calculation accuracy in complex jurisdictions (Bay Area).
## 8.2. Powerful Proprietary API
The third-party tool can be integrated directly with the specialized service to retrieve rates in real-time, bypassing the limitations of the `QBO` Accounting REST API.
## 8.3. Compliance automation.
This includes automatic rate updates, accurate reporting for the CDTFA, and automated tax filing.
## 8.4. Stability and Scalability
This approach provides a stable, scalable solution that is independent of the limitations or changes in the Intuit API.