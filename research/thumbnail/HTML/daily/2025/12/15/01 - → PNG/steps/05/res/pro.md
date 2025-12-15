Используйте переменную для сохранения результата `cygpath`. Флаг `-m` (mixed) создает путь с прямыми слешами, который корректно воспринимается Chrome и в аргументе `--screenshot`, и в URL `file://`.

```bash
cwd=$(cygpath -m "$(pwd)")
(
	o=(
		--disable-features=ExtensionManifestV2Unsupported,ExtensionManifestV2Disabled
		--headless=new
		--profile-directory="Default"
		--screenshot="$cwd/1.png"
		--window-size=800,600
	)
	chrome "${o[@]}" "file://$cwd/1.html"
)
```

