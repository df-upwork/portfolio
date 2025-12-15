#
```bash
(
	o=(
		--disable-features=ExtensionManifestV2Unsupported,ExtensionManifestV2Disabled
		--headless=new
		--profile-directory="Default"
		--screenshot
		--window-size=W,H
	)
	chrome "${o[@]}" "file://$(cygpath -m "$(pwd)")/файл.html"
)	
```