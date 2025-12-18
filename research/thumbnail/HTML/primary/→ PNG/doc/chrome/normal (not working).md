#
https://issues.chromium.org/issues/405165895

#
https://gemini.google.com/share/e30c541f4189

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