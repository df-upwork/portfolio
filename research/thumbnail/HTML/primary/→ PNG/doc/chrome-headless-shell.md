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

#
https://developer.chrome.com/blog/chrome-headless-shell

#
https://pptr.dev/browsers-api

#
```bash
# Download the latest available `chrome-headless-shell` binary corresponding to the Stable channel.
npx @puppeteer/browsers install chrome-headless-shell@stable

# Download a specific `chrome-headless-shell` version.
npx @puppeteer/browsers install chrome-headless-shell@139.0.7258.155
```