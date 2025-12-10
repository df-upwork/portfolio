Используй атрибут `transform` на родительском теге `<text>`, чтобы задать систему координат, смещённую по горизонтали. Это позволит заменить длинное дробное значение `x` во всех вложенных элементах на `0`.

Так как класс `.common` содержит `text-anchor: middle`, все строки с `x='0'` будут выравнены по центру относительно новой оси.

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
       x='0'
       y='44.533066'
    >Overcoming</tspan>
    <tspan
       class='p12 p2'
       id='L2'
       sodipodi:role='line'
       x='0'
       y='70'
    >legislative, zoning,</tspan>
    <tspan
       class='p12 p2'
       id='L3'
       sodipodi:role='line'
       x='0'
       y='92'
    >wastewater discharge</tspan>
    <tspan
       class='p3'
       id='L4'
       sodipodi:role='line'
       x='0'
       y='122'
    >barriers for</tspan>
    <tspan
       class='p12 p1'
       id='L5'
       sodipodi:role='line'
       x="0"
       y="156"
    >alkaline hydrolysis</tspan>
    <tspan
       class='p3'
       id='L6'
       sodipodi:role='line'
       x='0'
       y='186'
    >in Massachusetts</tspan>
</text>
```