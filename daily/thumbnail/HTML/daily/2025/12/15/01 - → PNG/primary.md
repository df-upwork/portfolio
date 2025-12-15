#
```bash
(
	f=1
	p=$(cygpath -m "$(pwd)")
	o=(
		--disable-features=ExtensionManifestV2Unsupported,ExtensionManifestV2Disabled
		--headless=new
		--profile-directory="Default"
		--screenshot="$p/$f.png"
		--window-size=800,600
	)
	chrome "${o[@]}" "file://$p/$f.html"	
)
```