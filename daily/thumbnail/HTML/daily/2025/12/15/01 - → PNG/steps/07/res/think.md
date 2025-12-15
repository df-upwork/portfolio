Проблема заключается в том, что Chrome в режиме `--headless` делает скриншот сразу после загрузки DOM, не дожидаясь завершения сетевых запросов на скачивание шрифтов. Из-за параметра `display=swap` в CSS браузер отрисовывает текст запасным шрифтом.

Для решения нужно добавить флаг `--virtual-time-budget` в `C๏`. Это заставит браузер ждать указанное количество миллисекунд (позволяя загрузить шрифты) перед снятием скриншота.

`C๏` ≔

```bash
(
	p=$(cygpath -m "$(pwd)")
	o=(
		--disable-features=ExtensionManifestV2Unsupported,ExtensionManifestV2Disabled
		--headless=new
		--profile-directory="Default"
		--screenshot="$p/.png"
		--virtual-time-budget=5000
		--window-size=1000,800
	)
	chrome "${o[@]}" "file://$p/.html" 
)
```