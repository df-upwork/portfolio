Для упрощения кода и удаления дублирующегося атрибута `x='0'` используй CSS. Спецификация SVG 2 (которую поддерживает Inkscape 1.4) позволяет управлять геометрическими атрибутами, такими как `x` и `y`, через стили.

### 1\. Добавь правило в `<style>` (внутри `Sᨀ`)

Это правило принудительно выставит координату `x=0` для всех вложенных `tspan` внутри элементов с классом `.common`.

```css
.common tspan {
	x: 0;
}
```

### 2\. Упрощённый `Fᨀ`

Теперь атрибут `x='0'` можно удалить из разметки, так как он задаётся через CSS. Атрибуты `y` необходимо оставить для вертикального позиционирования строк.

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