```bash
(
	n=1
	p=$(cygpath -m "$(pwd)")
	o=(
		--disable-features=ExtensionManifestV2Unsupported,ExtensionManifestV2Disabled
		--headless=new
		--profile-directory="Default"
		--screenshot="$p/$n.png"
		--window-size=800,600
	)
	chrome "${o[@]}" "file://$p/$n.html"
)
```