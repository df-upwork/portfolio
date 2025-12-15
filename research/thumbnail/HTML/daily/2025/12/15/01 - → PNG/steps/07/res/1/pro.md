https://gemini.google.com/share/23986a9fd02d

Причина `P†` заключается в состоянии гонки (race condition): Chrome в режиме `headless` делает скриншот сразу после события загрузки страницы (load event), не дожидаясь асинхронной загрузки и рендеринга внешних веб-шрифтов.

Для устранения проблемы необходимо дать браузеру время на загрузку ресурсов перед снимком. Самый надежный способ сделать это через аргументы командной строки — использовать параметр `--virtual-time-budget`.

Ниже приведена исправленная версия `C๏`.

### Правки к `C๏`

В массив опций добавлен параметр `--virtual-time-budget=5000` (5000 миллисекунд), который заставляет браузер отложить финальную отрисовку, позволяя завершиться сетевым запросам шрифтов.

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

### Альтернативные рекомендации к `H⸙`

Хотя правка `C๏` решает проблему гарантированно, использование `@import` внутри `<style>` скрывает запрос шрифта от предзагрузчика браузера. Для ускорения загрузки в `H⸙` рекомендуется заменить блок `@import` на стандартный тег `<link>` внутри `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Carlito:wght@400;700&display=swap" rel="stylesheet">
```

Вам достаточно применить только обновленный код `C๏`.

### Дальнейшие шаги

Хотите, я подготовлю версию скрипта с автоматической проверкой наличия установленного шрифта в системе, чтобы избежать зависимости от сети?