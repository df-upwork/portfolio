## 1.
Your CSV either does not contain one of the required fields, or the mapping of your CSV columns to NetSuite fields is set incorrectly.

## 2.
For «**Asset Revaluation**», the required set of fields depends on:
2.1) The settings of the «**Fixed Assets Management**» (FAM) module.
2.2) The number (and type) of depreciation books (Asset Books) used — if you have multiple Books, you will need to specify a particular book (Book Name / Book ID).
2.3) Additional customizations (custom fields, custom scripts) that affect the revaluation.

## 3.
In most cases, the following fields are required for «**Asset Revaluation**»:
### 3.1.
It is necessary to provide at least one identifier («**Internal ID**» / «**Asset ID**» / «**Asset Name**») so that NetSuite can determine which specific asset is being revalued.

### 3.2.
«**Revaluation Date**»

### 3.3.
«**Book Name**» / «**Book ID**»: if you keep records for several books (for example, Accounting Book, Tax Book, etc.), it is necessary to explicitly indicate in which book the revaluation is being performed.

### 3.4.
«**Revaluation Amount**» / «**Fair Value**» / «**New Value**»: the new value to which the asset’s cost should be revalued.

### 3.5.
«**Account**»: the account(s) to which the revaluation is posted.
This may not be explicitly required in some configurations, but usually the system requests an account to record «**Revaluation Adjustment**».

### 3.6.
«**Posting Period**»: in configurations where the «**Accounting Periods**» functionality is enabled, it is necessary to specify the period in which the revaluation is carried out (for example, Jan 2025).

### 3.7.
«**Depreciation**» / «**Amortization Fields**»: In some cases (especially if the revaluation changes the useful life or depreciation method), NetSuite requires the specification of new values for:
3.7.1) «**Depreciation Method**» (amortization method)
3.7.2) «**Remaining Life**» or «**End Date**»
3.7.3) «**Salvage Value**»

### 3.8.
«**Subsidiary**»: in the context of NetSuite OneWorld (and sometimes in regular accounts if a multi-subsidiary structure is enabled), each financial event (transaction, record, document) must be tied to a specific legal entity or subsidiary.
That is why the «Subsidiary» field may be required.

### 3.9.
«**Department**»: if in your account (especially in OneWorld) the «Department» field is configured as required, then any transaction or record  that affects accounting (including asset revaluation) must specify a department.

### 3.10.
«**Class**», «**Location**» (similar to «Department»).