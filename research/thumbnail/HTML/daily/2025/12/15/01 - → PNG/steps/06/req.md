# 1.
`C๏` ≔
```bash
(
	p=$(cygpath -m "$(pwd)")
	o=(
		--disable-features=ExtensionManifestV2Unsupported,ExtensionManifestV2Disabled
		--headless=new
		--profile-directory="Default"
		--screenshot="$p/1.png"
		--window-size=800,600
	)
	chrome "${o[@]}" "file://$p/1.html"	
)	
```

#
Как убрать дублирование basename файла из `C๏`?
Я хочу, чтобы PNG создавался с тем же basename, что и HTML.

# 
## 
Не пиши никогда «Конечно» и другой подобный мусор в начале ответа.
Мне подобное пиздобольство не нужно.

## 
Не добавляй в код свои комментарии.

##
Отступы в коде делай табуляцией, не пробелами.