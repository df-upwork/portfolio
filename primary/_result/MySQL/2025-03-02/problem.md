# The client's problem
## 1. Title
Urgent: Node vs PHP mySQL performance investigation

## 2. Description
### 2.1. Environment
setup:
- ubuntu 24.02
- node 22
- mysql 8 (apt install mysql-server)

### 2.2. Problem
Our team is seeking someone to help debug node performance issue.
For very simple SQL statements node performs significantly worse.
Using any module:  mysql2, mysql, promise-mysql, mariadb similar performance is shown.
- Sample PHP script attached (пункт 1.5.2 ниже)
- Sample Node script attached (пункта 1.5.1 ниже)
Is the problem in system configuration, module configuration, mysql server configuration or ubuntu configuration?

### 2.3. Benchmarks
#### 2.3.1. Node.js (using the script of point 3)
```csv
0.739
1.337
1.784
1.762
1.455
1.244
1.205
1.093
0.768
0.888
0.904
1.042
```

#### 2.3.2. PHP (using the script of point 4)
```csv
0.293
0.494
0.440
0.430
0.454
0.457
0.445
0.400
0.487
0.607
```

#### 2.3.3. Consequences from 2.3.1 and 2.3.2
- Node is at least twice as slow or worse. 
- This same discrepancy is shown for simple statements such as "SELECT 1".

## 3. `sample_perf.js`
```javascript
import mysql from 'mysql2/promise';

const db = await mysql.createConnection({'host':'127.0.0.1','user':'test','password':'test','database':'test'});

async function test() {
	const startTime = process.hrtime.bigint();
	await db.query('UPDATE test SET f=1 WHERE id=1');
	//await db.query('SELECT 1');
	var MS = Number(process.hrtime.bigint()-startTime)/1000000;
	console.log(MS);
	setTimeout(test, 250);
}
async function go() {
	await db.query('DROP TABLE IF EXISTS test');
	await db.query('CREATE TABLE `test` ( `id` int NOT NULL, `f` int NOT NULL, PRIMARY KEY (`id`)) ENGINE=MEMORY');
	await db.query('INSERT INTO `test` (`id`, `f`) VALUES(1, 1)');
	test();
}
go();
```
## 4. `sample_perf.php`
Этот скрипт я буду коротко обозначать `SP`.
```php
<?php
$db = new mysqli();
$db->real_connect(hostname:'localhost',password:null, username: 'test', database:'test');

$s = $db->prepare("DROP TABLE IF EXISTS test"); $s->execute();
$s = $db->prepare("CREATE TABLE `test` ( `id` int NOT NULL, `f` int NOT NULL, PRIMARY KEY (`id`)) ENGINE=MEMORY"); $s->execute();
$s = $db->prepare("INSERT INTO `test` (`id`, `f`) VALUES(1, 1)"); $s->execute();
for($i=0; $i<10; $i++) {
	$startTime = microtime(true)*1000;
	$s = $db->prepare("UPDATE test SET f=1 WHERE id=1"); $s->execute();
	//$s = $db->prepare("SELECT 1"); $s->execute(); $s->free_result();
	$MS = microtime(true)*1000-$startTime;
	echo "$MS\n";
	usleep(250*1000);
}
```