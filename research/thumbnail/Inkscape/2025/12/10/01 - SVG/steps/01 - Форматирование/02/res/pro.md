https://gemini.google.com/share/d62443419a10

# 5\. ᛭T

## Причина `P†`

Основная причина некорректного отображения (в одну строку или со смещением) заключается в наличии атрибута `xml:space="preserve"` в теге `<text>`.

Этот атрибут заставляет рендерер воспринимать всё форматирование исходного кода (переносы строк и табуляцию внутри тега `<text>`) как значимые текстовые символы. Поскольку в коде используется глубокая вложенность с отступами, между текстовыми фрагментами (`tspan`) вставляются пробельные символы. В сочетании с атрибутом `text-anchor="middle"` и вложенной структурой `tspan`, это нарушает расчёт координат и приводит к тому, что текст либо «слипается» в одну строку (так как координаты `y` могут игнорироваться для inline-контента с принудительными пробелами в некоторых рендерерах), либо отображается с огромными горизонтальными разрывами.

Дополнительный фактор: использование CSS-свойства `line-height` в атрибуте `style`. Это свойство не является частью спецификации SVG 1.1 и может вызывать конфликты позиционирования в браузерах, которые пытаются применить к SVG блочную модель CSS.

## Правки к `Sᨀ`

# 1\.

В строке 52 удали атрибут `xml:space="preserve"`. Это позволит рендереру игнорировать отступы и переносы строк в коде, корректно используя координаты `x` и `y`, заданные в `tspan`.

Замени:

```xml
		xml:space="preserve"
		y="44.533066"
	>
```

на:

```xml
		y="44.533066"
	>
```

# 2\.

В строке 44 удали свойство `line-height:1.1;` из атрибута `style`.

Замени:

```xml
		style="font-size:22.5778px;line-height:1.1;font-family:Carlito;-inkscape-font-specification:Carlito;fill:#df3d16;stroke-width:0.264583"
```

на:

```xml
		style="font-size:22.5778px;font-family:Carlito;-inkscape-font-specification:Carlito;fill:#df3d16;stroke-width:0.264583"
```

# 3\.

Аналогично пункту 2, удали `line-height:1.1;` из атрибутов `style` во всех вложенных `tspan` (строки 62, 70, 75, 79, 93, 102, 111).

Пример для строки 62:
Замени:

```xml
			style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:16px;line-height:1.1;font-family:Carlito;-inkscape-font-specification:Carlito;text-align:center;text-anchor:middle;fill:#4d4d4d;fill-opacity:1;stroke-width:0.264583"
```

на:

```xml
			style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:16px;font-family:Carlito;-inkscape-font-specification:Carlito;text-align:center;text-anchor:middle;fill:#4d4d4d;fill-opacity:1;stroke-width:0.264583"
```

# 4\.

В строке 39 присутствует вероятный артефакт (символ ` ` перед закрытием тега), который может вызывать ошибки парсинга в строгих XML-парсерах.

Замени:

```xml
		showgrid="false"
  />
```

на:

```xml
		showgrid="false"
	/>
```