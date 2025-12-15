https://gemini.google.com/share/4dc74fdfad84

# 5\. `᛭T`

## 

Причиной `P†` является наличие атрибута `xml:space="preserve"` в теге `<text>`. Этот атрибут заставляет рендерер учитывать все пробельные символы (переносы строк и табуляцию) из исходного кода как часть текста. В сочетании с форматированием кода, это приводит к появлению лишних текстовых узлов, которые при выравнивании `text-anchor="middle"` смещают текст и нарушают позиционирование строк.

## 

Предлагаю следующие точечные правки для `Sᨀ` (используй их для замены соответствующих фрагментов кода):

# 1\.

В открывающем теге элемента `<text>` с `id="text1"` удали атрибут `xml:space="preserve"`.

```xml
	<text
		id="text1"
		inkscape:label="Text"
		style="font-size:22.5778px;line-height:1.1;font-family:Carlito;-inkscape-font-specification:Carlito;fill:#df3d16;stroke-width:0.264583"
		x="140.18362"
		y="44.533066"
	>
```

# 2\.

Замени блок кода с `id="tspan8"` на вариант без лишних пробельных символов и переносов строк внутри содержимого, чтобы исключить появление паразитных пробелов.

```xml
		<tspan
			id="tspan8"
			sodipodi:role="line"
			style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:20px;line-height:1.1;font-family:Carlito;-inkscape-font-specification:Carlito;text-align:center;text-anchor:middle;fill:#4d4d4d;fill-opacity:1;stroke-width:0.264583"
			x="140.18362"
			y="70"
		><tspan
				id="tspan13"
				style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:20px;font-family:Carlito;-inkscape-font-specification:'Carlito Bold';fill:#000000"
			>legislative</tspan>, <tspan
				id="tspan16"
				style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:20px;font-family:Carlito;-inkscape-font-specification:'Carlito Bold';fill:#000000"
			>zoning</tspan>,</tspan>
```

# 3\.

Замени блок кода с `id="tspan14"` на упрощенную версию без вложенности и лишних пробелов.

```xml
		<tspan
			id="tspan14"
			sodipodi:role="line"
			style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:20px;line-height:1.1;font-family:Carlito;-inkscape-font-specification:'Carlito Bold';text-align:center;text-anchor:middle;fill:#000000;fill-opacity:1;stroke-width:0.264583"
			x="140.18362"
			y="92"
		>wastewater discharge</tspan>
```