## Использование наследования координат

В спецификации SVG первый вложенный элемент `tspan` автоматически начинает рендеринг с координат `x` и `y`, заданных в родительском элементе `text`, если в самом `tspan` не указаны иные значения.

Поскольку значение `y` в `id='L1'` полностью совпадает со значением `y` в `id='text1'`, атрибут в дочернем элементе можно удалить.

## Обновленный код

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