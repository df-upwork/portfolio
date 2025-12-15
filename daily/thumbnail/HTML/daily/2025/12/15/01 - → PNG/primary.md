#
```bash
(
	p=$(cygpath -m "$(pwd)")
	o=(
		--disable-blink-features=AutomationControlled
		--disable-features=ExtensionManifestV2Unsupported,ExtensionManifestV2Disabled
		--disable-infobars
		--headless=new
		--hide-scrollbars		
		--profile-directory="Default"
		--screenshot="$p/.png"
		--window-size=1000,800
	)
	chrome "${o[@]}" "file://$p/.html"	
)
```

#
```bash
(
	p=$(cygpath -m "$(pwd)")
	o=(
		--disable-features=ExtensionManifestV2Unsupported,ExtensionManifestV2Disabled
		--disable-gpu
		--headless
		--hide-scrollbars
		--no-sandbox
		--profile-directory="Default"
		--screenshot="$p/.png"
		--window-size=1000,800
	)
	chrome "${o[@]}" "file://$p/.html"	
)
```


```bash
(
	p=$(cygpath -m "$(pwd)")
	o=(
		--disable-features=ExtensionManifestV2Unsupported,ExtensionManifestV2Disabled
		--headless=new
		--screenshot="$p/.png"
		--window-size=1000,800
	)
	"$(cygpath "C:\Program Files\Opera\opera.exe")"  "${o[@]}" "file://$p/.html"	
)
```