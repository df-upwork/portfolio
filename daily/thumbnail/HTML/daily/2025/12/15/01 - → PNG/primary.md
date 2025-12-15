#
```bash
(
	p=$(cygpath -m "$(pwd)")
	o=(
		--disable-features=ExtensionManifestV2Unsupported,ExtensionManifestV2Disabled
		--headless=new
		--profile-directory="Default"
		--screenshot="$p/.png"
		--window-size=1000,800
	)
	chrome "${o[@]}" "file://$p/.html"	
)
```