#
```bash
(
	p=$(cygpath -m "$(pwd)")
	o=(
		--screenshot="$p/.png"
		--window-size=1000,800
	)
	chrome-headless-shell "${o[@]}" "file://$p/.html"	
)
```