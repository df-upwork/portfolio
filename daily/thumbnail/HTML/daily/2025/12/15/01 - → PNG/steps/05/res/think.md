```bash
(
	p=$(cygpath -m "$(pwd)")
	o=(
		--disable-features=ExtensionManifestV2Unsupported,ExtensionManifestV2Disabled
		--headless=new
		--profile-directory="Default"
		--screenshot="$p/1.png"
		--window-size=800,600
	)
	chrome "${o[@]}" "file://$p/1.html"
)
```