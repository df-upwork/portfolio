# 1.
`C๏` ≔
```bash
(
	o=(
		--disable-features=ExtensionManifestV2Unsupported,ExtensionManifestV2Disabled
		--headless=new
		--profile-directory="Default"
		--screenshot="$(cygpath -w "$(pwd)/1.png")"
		--window-size=800,600
	)
	chrome "${o[@]}" "file://$(cygpath -m "$(pwd)")/1.html"
)	
```

#
Как убрать дублирование `cygpath` из `C๏`?

# 
## 
Не пиши никогда «Конечно» и другой подобный мусор в начале ответа.
Мне подобное пиздобольство не нужно.

## 
Не добавляй в код свои комментарии.

##
Отступы в коде делай табуляцией, не пробелами.