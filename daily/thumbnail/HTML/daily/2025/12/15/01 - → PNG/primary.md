#
```bash
chrome --headless=new --screenshot --window-size=W,H "file:///путь/к/файлу.html"
```

#
```bash
chrome --headless=new --screenshot --window-size=W,H "file://$(pwd)/файл.html"
```

#
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

#
```bash
(
	o=(
		--headless=new
		--screenshot
		--window-size=W,H
	)
	chrome "${o[@]}" "file://$(cygpath -m "$(pwd)")/файл.html"
)	
```