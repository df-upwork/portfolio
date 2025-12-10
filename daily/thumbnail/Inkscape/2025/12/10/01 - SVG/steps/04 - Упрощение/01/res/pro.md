## Использование CSS (SVG 2)

В спецификации SVG 2 атрибуты геометрии, такие как `x`, могут определяться через CSS. Это позволяет задать координату глобально для всех вложенных элементов `tspan`, избегая дублирования в разметке.

Для реализации необходимо добавить селектор `.common tspan` (или аналогичный) в секцию `<style>` с правилом `x: 0;`.

### Обновленный блок `<style>`

```css
.common {
	-inkscape-font-specification: Carlito;
	font-family: Carlito;
	line-height: 1.1;
	stroke-width: 0.264583;
	text-align: center;
	text-anchor: middle;
}
.common tspan {
	x: 0;
}
.p12 {
	-inkscape-font-specification: 'Carlito Bold';
	fill: #000000;
	font-weight: bold;
}
.p1 {
	font-size: 28px;
}
.p2 {
	font-size: 20px;
}
.p3 {
	fill: #4d4d4d;
	font-size: 16px;
}
```

### Упрощенный фрагмент `Fᨀ`

```svg
<text
	class='common'
	id='text1'
	inkscape:label='Text'
	style='font-size:22.5778px;'
	transform='translate(140.18362)'
	x='0'
	y='44.533066'
>
	<tspan
		class='p3'
		id='L1'
		sodipodi:role='line'
		y='44.533066'
	>Overcoming</tspan>
	<tspan
		class='p12 p2'
		id='L2'
		sodipodi:role='line'
		y='70'
	>legislative, zoning,</tspan>
	<tspan
		class='p12 p2'
		id='L3'
		sodipodi:role='line'
		y='92'
	>wastewater discharge</tspan>
	<tspan
		class='p3'
		id='L4'
		sodipodi:role='line'
		y='122'
	>barriers for</tspan>
	<tspan
		class='p12 p1'
		id='L5'
		sodipodi:role='line'
		y='156'
	>alkaline hydrolysis</tspan>
	<tspan
		class='p3'
		id='L6'
		sodipodi:role='line'
		y='186'
	>in Massachusetts</tspan>
</text>
```