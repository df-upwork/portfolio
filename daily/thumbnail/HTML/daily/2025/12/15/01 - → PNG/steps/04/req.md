#
```bash
(
	o=(
		--disable-features=ExtensionManifestV2Unsupported,ExtensionManifestV2Disabled
		--headless=new
		--profile-directory="Default"
		--screenshot
		--window-size=800,600
	)
	chrome "${o[@]}" "file://$(cygpath -m "$(pwd)")/1.html"
)	
```

#
В какой папке будет создан файл `screenshot.png`?
Как изменить эту папку?
