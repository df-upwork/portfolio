```bash
(
	o=(
		--headless=new
		--screenshot
		--window-size=W,H
	)
	chrome "${o[@]}" "file://$(pwd)/файл.html"
)	
```
Как изменить `$(pwd)` для Cygwin?