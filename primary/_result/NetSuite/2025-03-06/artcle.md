## 1. NetSuite → 3PL
Orders can be uploaded from NetSuite to a 3PL server via SFTP in SuiteScript 2.1 as follows: [gist.github.com/dmitrii-fediuk/79c708dd1291eae3b6dafcbcbed57347](https://gist.github.com/dmitrii-fediuk/79c708dd1291eae3b6dafcbcbed57347)  
### 1.1. Import modules 
```javascript
import file from 'N/file';
import search from 'N/search';
import sftp from 'N/sftp';
export function execute() {
	// <…>
}
```  
### 1.2. List orders to transfer  
```javascript
const orders = search.load({id: 'customsearch_export_orders'}).run().map(r => ({
	entity: r.getText({name: 'entity'})
	,salesOrderId: r.getValue({name: 'internalid'})
	,total: r.getValue({name: 'total'})
	,tranId: r.getValue({name: 'tranid'})
}));
```  
### 1.3. [Serialize](https://en.wikipedia.org/wiki/Serialization) the orders 
```javascript
let csvA = ['SalesOrderId,TranId,Entity,Total'];
orders.forEach(o => {csvA.push(
	[o.salesOrderId, o.tranId, o.entity, o.total]
		.map(v => `"${v}"`)
		.join(',')
);});
```  
### 1.4. Create a [DTO](https://en.wikipedia.org/wiki/Data_transfer_object) file  
```javascript
const f = file.create({
	contents: csvA.join('\n')
	,description: '<…>'
	,encoding: file.Encoding.UTF_8
	,fileType: file.Type.CSV
	,folder: 123 // The folder ID in NetSuite File Cabinet
	,name: '<…>.csv'
});
f.save();
```  
### 1.5. Connect to the 3PL server via SFTP  
```javascript
const conn = sftp.createConnection({
	directory: '<…>'
	,hostKey: 'AAAAB3NzaC1yc2E<…>'
	,hostKeyType: sftp.HostKeyType.RSA
	,passwordGuid: '<…>'
	,port: 22
	,url: '<…>'
	,username: '<…>'
});
```  
### 1.6. Upload the file to the 3PL server  
```javascript
conn.upload({file: f, replaceExisting: true});	
```  
## 2. 3PL → NetSuite 
Order confirmations can be downloaded from a 3PL server to NetSuite via SFTP in SuiteScript 2.1 as follows: [gist.github.com/dmitrii-fediuk/93841deb2bd60ee8e2c952f4be41e7ea](https://gist.github.com/dmitrii-fediuk/93841deb2bd60ee8e2c952f4be41e7ea)  
### 2.1. Import modules  
```javascript
import record from 'N/record';
import search from 'N/search';
import sftp from 'N/sftp';
export function execute() {
	// <…>
}
```  
### 2.2. Connect to the 3PL server via SFTP
Same as point 1.5.  
### 2.3. List files to download  
```javascript
const path = '<…>';
conn.list({path: path}).forEach(rf => {
	if (rf.name && rf.name.toLowerCase().endsWith('.csv')) {
		// <…>	
	}		
});
```  
### 2.4. For each file  
#### 2.4.1. Download  
```javascript
const contents = conn.download({directory: path, filename: rf.name}).getContents();
```  
#### 2.4.2. Extract orders information from the file  
```javascript
const lines = contents.split(/\r?\n/);
for (let i = 1; i < lines.length; i++) {
	let line = lines[i].trim();
	if (line) {
		let fields = line.split(',');
        // <…>	
    }
```  
#### 2.4.3. For each order from the file  
##### 2.4.3.1. Find the order in NetSuite 
```javascript
const findOrder = id => {
	const s = search.create({
		columns: ['internalid']
		,filters: [['mainline', 'is', 'T'], 'AND', ['tranid', 'is', id]]
		,type: search.Type.SALES_ORDER
	}).run().getRange({end: 1, start: 0});
	return !s || !s.length ? null : record.load({
		id: parseInt(s[0].getValue({name: 'internalid'})), type: record.Type.SALES_ORDER
	});
};
let o = findOrder(fields[0]);
if (o) {
    // <…>					
}
```  
##### 2.4.3.2. Update the order in NetSuite  
```javascript
o.setValue({fieldId: 'custbody_shipping_status', value: fields[1]});
o.setValue({fieldId: 'custbody_tracking_number', value: fields[2]});
o.save();
```  
### 2.4.4. Delete the processed file on the 3PL server so that it will not be processed again on the next connection  
```javascript
conn.remove({directory: '<…>', filename: rf.name});
```  
