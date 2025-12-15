#
```bash
(
	o=(
		--disable-features=ExtensionManifestV2Unsupported,ExtensionManifestV2Disabled
		--headless=new
		--profile-directory="Default"
		--screenshot="$(cygpath -w "$(pwd)/1.png")"
		--window-size=800,600
	)
	chrome "${o[@]}" "file://$(cygpath -m "$(pwd)")/1.html"
)	
```