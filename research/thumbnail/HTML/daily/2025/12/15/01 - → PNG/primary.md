#
https://issues.chromium.org/issues/405165895

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
	chrome "${o[@]}" "file://$p/.html"	
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
		# 2025-12-16 https://chromium.googlesource.com/chromium/src/+/main/components/headless/screen_info/README.md	
		--screen-info={1000x800} 
		--screenshot="$p/.png"
		--window-size=1000x800
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