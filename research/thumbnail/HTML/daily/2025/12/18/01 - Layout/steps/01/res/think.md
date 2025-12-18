https://gemini.google.com/share/dbb93b3b0fae

# 1. Удаление дублирующихся свойств в `@font-face`

Замени строки с 6 по 17 в `H⸙` на следующий код. В нём удалено дублирующееся свойство `font-style: normal` и свойство `font-weight: 400` (являются значениями по умолчанию), что устраняет избыточность без изменения визуального отображения.

```css
		@font-face {
			font-family: 'Carlito';
			src: local('Carlito'), local('Carlito-Regular');
		}
		@font-face {
			font-family: 'Carlito';
			font-weight: 700;
			src: local('Carlito Bold'), local('Carlito-Bold');
		}

```