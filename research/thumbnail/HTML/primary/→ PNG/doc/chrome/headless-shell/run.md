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

#
```bash
(
	p=$(cygpath -m "$(pwd)")
	o=(
		--disable-blink-features=AutomationControlled
		--disable-features=ExtensionManifestV2Unsupported,ExtensionManifestV2Disabled
		--disable-infobars
		--force-device-scale-factor=1
		--headless=new
		--hide-scrollbars
		--high-dpi-support=1		
		--profile-directory="Default"
		--screenshot="$p/.png"
		--window-size=1000,800
	)
	chrome-headless-shell "${o[@]}" "file://$p/.html"	
)
```