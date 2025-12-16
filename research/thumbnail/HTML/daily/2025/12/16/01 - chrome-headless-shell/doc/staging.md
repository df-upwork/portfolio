```bash
(
	p=$(cygpath -m "$(pwd)")
	o=(
		--screenshot="$p/.png"
	)
	chrome-headless-shell "${o[@]}" "file://$p/.html"	
)
```