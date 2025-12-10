There are **2** main **reasons**: the **technical** and the **strategic**.  
I will present the technical reason first, because the strategic reason is unlikely to be pleasing to you, although it is much more important and correct.
## 1. The main technical reason
The main technical reason is that your script in PHP (`SP`) and your script in Node.js (`SJ`) connect to the database in **different ways**: using **different sockets**.  
### 1.1.
`SP` connects via `localhost`.  
This is usually a **Unix socket**, but in fact not always, and it can be overridden in the operating system.  
### 1.2.
`SJ` connects via a **TCP socket** (`127.0.0.1`).  
### 1.3. 
I have 25 years of programming experience, and I have repeatedly seen situations in which a simple **socket switch** from `localhost` to `127.0.0.1` (or vice versa) can change the speed of a program working with a database **multiple times** over.  
### 1.4. 
In **synthetic tests** like yours, connecting via a **Unix socket** is usually **faster**.
#### 1.4.1. 
This is because **Unix sockets** are an **inter-process communication** (**IPC**) mechanism on a single host system.  
Data are transferred directly in **kernel space**, **bypassing** several layers of the **network stack**.  
#### 1.4.2.
By contrast, **TCP sockets** involve:  
- The **IP layer** (even through the loopback interface).  
- The **TCP layer** (window management, acknowledgments, delivery order).  
- Additional **kernel data structures** (routing table, TCP connection state tables, ports, etc.).   

For **local data transfer**, so many layers are **unnecessary**, since we are simply sending bytes from one process to another within the **same computer**.
#### 1.4.3.  
Even if the **loopback** interface (`127.0.0.1`) is used, the TCP/IP implementation includes: 
- Formation of the **IP packet**: adding an IP header (20 bytes for IPv4 or more for IPv6).  
- Formation of a **TCP segment**: adding a TCP header (at least 20 bytes).   
- Calculation of **checksums** for TCP and IP.  
- Processing **ACK packets** (confirmation of data reception).  
- Management of **TCP windows** (window size, congestion control).

### 1.5.   
In my 25 years of experience, I have encountered **opposite** scenarios where `127.0.0.1` is faster than `localhost`.  
For example, if the **Unix socket** is located on a **filesystem** with **high load** or **slow access** (e.g. due to file descriptor contention), it can slow down a connection through `localhost` compared to `127.0.0.1`. 

## 2. The strategic reason
The strategic reason is that **PHP** is a much **more mature** system for working with **MySQL** than Node.js is.  
### 2.1. 
The **PHP** communication with MySQL is almost entirely **implemented in C**: the PHP community has put a lot of effort into it for the last ***25 years**.
Until version 5.4 (2012), PHP by default used the `libmysqlclient` library written in C by the creators of MySQL.
However, the PHP community did not stop there, and in 2009 (PHP 5.3) developed its own, even more powerful library in C: `mysqlnd`, super-optimized specifically for PHP, and with PHP 5.4 (2012), `mysqlnd` became the **default library**.
### 2.2.
**Node.js** only appeared in **2009**, and only came into vogue in **2012**: by then the **eCommerce** niche and the niche of prominent software working with **relational databases** were **already taken**.
At the time, Node.js projects typically used MongoDB, which also appeared in 2009: Node.js and MongoDB were born and gained popularity almost simultaneously, and were used by the same people.  
This is why the implementation of MySQL operations in Node.js is frankly **mediocre**: all the modules you listed (`mysql2`, `mysql`, `promise-mysql`, `mariadb`) are implemented almost entirely in **JavaScript**, **without advanced techniques** or optimisations.  
A **twofold speed difference** between the same algorithm in **C** and **JavaScript** is still good for JavaScript, usually it is **much worse**.  
### 2.3. 
For Node.js, there is practically **no hope** of correcting this situation: among **hipsters**, Node.js is already **out of fashion**, they have now **switched to Python**, there MySQL libraries (e.g. **SQLAlchemy** library) are **even worse**.  
### 2.4. 
The twofold speed difference in a simple test is **far from being the main problem** for Node.js with MySQL.
If a large-scale system is developed on Node.js that works with MySQL (and there are actually very few such systems in the world: for instance, try finding a successful eCommerce project on Node.js and MySQL), then small delays in database queries can be offset by other strong points of Node.js (such as a **fundamentally different implementation** of **asynchrony**, which modern PHP also has (for example, in PHP-FPM), but implemented differently).  
The main problem is that the integration of Node.js and MySQL is basically **immature** and **simplistic**.
## 3.  
Even though `SP`'s code is faster, it remains **suboptimal**: with a **proper implementation**, the **performance gap** with `SJ` could be even **bigger**.
### 3.1. 
Currently, `SP`'s code calls `$db->prepare()` inside the `for` loop.  
### 3.2. 
In a proper implementation, **prepared statements must be placed outside a loop**.  
Statements should be **prepared once**, and then **reused** in a loop.  
The **correct implementation** should look like this:  
```php
$s = $db->prepare("UPDATE test SET f=? WHERE id=?"); 
for ($i = 0; $i < 10; $i++) {
    <…>
    $s->bind_param("ii", 1, 1);
    $s->execute();
    <…>
}
```
### 3.3.
With repeated calls to prepared statements, the amount of transferred data decreases, and the **client/server communication** can use a **more efficient binary format** (if server-side prepared statements are enabled).  
### 3.4. 
Also, on the first `prepare()`, the server spends time **parsing SQL** and creating an **execution plan**.  
In a proper implementation (point 3.2), this is a one-time operation, and subsequent `execute()` calls go faster.  