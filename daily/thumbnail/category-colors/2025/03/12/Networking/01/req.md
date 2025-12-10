## 1. `U`
Веб-сервис Upwork (`upwork.com`) буду обозначать `U`.
В этом проекте мы анализируем поведение `U`.

## 2. Marketplace
### 2.1.
`U` — это marketplace, в котором взаимодействуют 2 стороны: фрилансеры и клиенты.
### 2.2. `F`
Произвольного фрилансера на `U` буду обозначать `F`.
Произвольное множество `F` буду обозначать `Fs`. 
### 2.3. `C`
Произвольного клиента буду обозначать `C`.
Произвольное множество `C` буду обозначать `Cs`.

Произвольного фрилансера на `U` буду обозначать `F`.
Произвольное множество `F` буду обозначать `Fs`. 

## 3. `PJ`
Клиенты публикуют на `U` проекты.
Произвольный проект на `U` буду обозначать `PJ`.
Произвольное множество `PJ` буду обозначать `PJs`.

## 4. `PP`
Отклик `F` на `PJ` в терминологии `U` называется «proposal».
Произвольный proposal буду обозначать `PP`.
Произвольное множество `PP` буду обозначать `PPs`.

## 5. `Profile`
### 5.1.
Профиль `F` на `U` буду обозначать `Profile`.
Произвольное множество `Profile` буду обозначать `Profiles`.
### 5.2.
`C` может смотреть `Profile`.
### 5.3.
`F` может редактировать свой `Profile`.

## 6. `PF`
Портфолио является частью `Profile`.
Произвольное портфолио буду обозначать `PF`.
Произвольное множество `PF` буду обозначать `PFs`.

## 7 `PF-PJ`
### 7.1.
`PF` состоит из «проектов фрилансера».
Произвольный «проект фрилансера» буду обозначать `PF-PJ`.
Произвольное множество `PF-PJ` буду обозначать `PF-PJs`.
### 7.2.
Не путай `PF-PJ` и `PJ`: это разные сущности.
### 7.3.
`PF-PJ` — это созданный `F` документ, описывающий некую ранее выполненная `F` работу.
Эта работа необязательно была выполнена на `U`.

## 8.
`U` регламентирует некоторые структурные элементы `PF-PJ`:
### 8.1. `PF-PJ-Title`
«Title» — это обязательное к заполнению `F`однострочное текстовое поле не длинее 70 символов.
Это поле буду обозначать `PF-PJ-Title`.
### 8.2. «Description»
«Description» — это обязательное к заполнению `F` многострочное текстовое поле не длинее 600 символов.
### 8.3. «Your role»
«Your role» — это необязательное к заполнению `F` однострочное текстовое поле не длинее 100 символов.
### 8.4. «Skills and deliverables»
«Skills and deliverables» — это необязательное к заполнению `F` поле, где можно указать не более 5 `Skill` (это понятие определено в пункте 9 ниже).
### 8.5. `TH`
«Thumbnail» — это обязательное к заполнению `F` поле.
`F` должен загрузить в это поле квадратную картинку.
Эта картинка будет отображаться в `PF` `F` в списке его `PF-PJs` 
Произвольный «thumbnail» буду обозначать `TH`.
Произвольное множество `TH` буду обозначать `THs`. 

## 9. `Skill`
### 9.1.
`U` содержит предопределённое множество «навыков фрилансера».
Произвольный «навык фрилансера» буду обозначать `Skill`.
Произвольное множество `Skill` буду обозначать `Skills`. 
### 9.2.
По форме `Skill` — это тег: слово или короткая фраза.
### 9.3.
`C` может указывать `Skills` для своего `PJ`.
### 9.4. `Profile-Skills`
`F` может указывать не более 15 `Skills` для своего `Profile`. 
Эти `Skills` буду обозначать `Profile-Skills`.
### 9.5.
`F` может указывать не более 5 `Skills` для своего `PF-PJ`.  

## 10. `PF-L`
### 10.1.
`U` отображает `PF` в виде списка.
Произвольный такой список буду называть `PF-L`.
### 10.2.
`PF-L` выглядит как плитка: по 3 `PF-PJ` в ряд.
### 10.3.
`PF-L` всегда показывает только 1 ряд `PF-PJs`.
### 10.4.
Под единственным рядом `PF-PJs` расположена постраничная навигация для `PF`.
### 10.5.
`PF-L` отображает только 2 поля `PF-PJ`: `PF-PJ-Title` и `TH`.  

## 11.
Я являюсь `F`.

## 12. `DA`
### 12.1.
Я выполняю `PJ` разных предметных областей:
Произвольную предметную область `PJ`, с которой я работаю, буду обозначать `DA`.
Произвольное множество `DA` буду обозначать `DAs`. 
### 12.2.
Частные случаи `DA`:
- Legal
- Magento
- Microsoft
- NetSuite
- Networking

## 13. `TH-BG-Color`
### 13.1.
Я использую для фона моих `TH` сплошную заливку одним цветом.
Произвольный такой цвет буду обозначать `TH-BG-Color`.
Произвольное множество `TH-BG-Color` буду обозначать `TH-BG-Colors`.
### 13.2. 
Разные `TH` могут иметь разный `TH-BG-Color`.
### 13.3.
Я хочу, чтобы `TH-BG-Color` определялся `DA` соответствующего `PJ`.

## 14. `TH-BG-Title`
### 14.1.
Основным содержимым моих `TH` является текст (а не графические элементы).
Произвольный такой текст буду обозначать `TH-BG-Title`.
Произвольное множество `TH-BG-Title` буду обозначать `TH-BG-Titleы`.
### 14.2.
Я хочу составлять `TH-BG-Title` на основе `PF-PJ-Title`.
В отличие от `PF-PJ-Title`, у `TH-BG-Title` отсутствует ограничение в 70 символов.
### 14.3.
Я отображаю `TH-BG-Title` шрифтом «Carlito», чёрным цветом.

## 15. `Profile-T`
«Profile title» является частью `Profile`.
Произвольный «Profile title» буду обозначать `Profile-T`.

## 16. `Profile-O`
«Profile overview» является частью `Profile`.
Произвольное «Profile overview» буду обозначать `Profile-O`.

## 17. `Profile-HR`
`F` указывает в своём `Profile` свой hourly rate (в долларах США) для почасовых проектов.
Такой hourly rate произвольного `F` буду обозначать `Profile-HR`.

## 18. Мой `Profile`
### 18.1. Мой `Profile-T`
Мой `Profile-T`: «The Premium Choice».
### 18.2. Мой `Profile-HR`
90
### 18.3. Мои  `Profile-Skills`
- Magento
- Legal
- Tax Law
- Python
- Data Analysis
- NetSuite Development
- Microsoft Dynamics 365
- Microsoft Power BI
- SQL
- Network Administration
- Amazon
- Amazon Web Services
- API
- PHP
- API Integration
 
### 18.4. Мой `Profile-O`
Мой `Profile-O`:
```
🔸 Premium Quality
🔸 𝟓𝟑𝟒 completed projects
🔸 GitHub: 𝟒𝟒𝐊+ public commits, 𝟐𝟒𝟏 repos
🔸 𝟐𝟓 years of experience
🔸 Magento: top 𝟏𝟎 worldwide, 𝟏𝟐𝟕 open source modules
🔸 OpenAI's 𝐨𝟏 𝐩𝐫𝐨 𝐦𝐨𝐝𝐞 validates all my reasoning against cognitive biases and omissions.
🔸 Advanced university degree in 𝐂𝐨𝐦𝐩𝐮𝐭𝐞𝐫 𝐒𝐜𝐢𝐞𝐧𝐜𝐞 and 𝐌𝐚𝐭𝐡𝐞𝐦𝐚𝐭𝐢𝐜𝐬, specializing in 𝐀𝐈.
🔸 My top publications:
⠀⠀⠀⠀🔅 df.tips?order=views
⠀⠀⠀⠀🔅 dmitry.ai?order=views
⠀⠀⠀⠀🔅 mage2.pro?order=views
🔸 My lifestyle
⠀⠀⠀⠀🔅 I work only after a full night's sleep and a high-intensity physical workout to ensure maximum mental clarity.
⠀⠀⠀⠀🔅 I take 𝟏𝟓+ supplements daily to boost my mental capacity and general health (N-acetylcysteine + glycine, Astragalus membranaceus + TA-65, Ubiquinol, Hericium erinaceus, Cordyceps militaris, Rhodiola rosea, Bacopa monnieri, Ginkgo biloba, Panax ginseng, Matcha, Chaga + Betula pendula bark, Omega-3 + Cod liver oil, Spermidine).
⠀⠀⠀⠀🔅 I eat only what fuels my maximum performance: nuts, greens, fish oil, vegetables, berries, seeds, dairy products (and supplements mentioned above). 
⠀⠀⠀⠀I do not eat sugar-added products, meat, flour, fried food, fast food, or other junk food.
🔸 My workspace
⠀⠀⠀⠀🔅 A perfect workstation with 3 big monitors
⠀⠀⠀⠀🔅 All pop-ups, sound alerts, notifications in my UI are entirely disabled
⠀⠀⠀⠀🔅 A top-tier, ergonomic chair with customized back- and head-support cushions made of the finest goose down
⠀⠀⠀⠀🔅 Total acoustic isolation
⠀⠀⠀⠀🔅 My phone is always silent
⠀⠀⠀⠀🔅 Not distracted by anyone
⠀⠀⠀⠀🔅 Perfectly balanced air conditioning and ventilation
⠀⠀⠀⠀🔅 Overlooking the Sea of Marmara, breathing in clean sea air
🔸 My «Job Success Score» decreased from 100% to 96% on January 31, 2025, because I fell ill on January 30.  
I rarely fall ill: the last time I did was 20 months prior to this case — in May 2023.  
This time, my 2½ years old son was mistakenly taken on public transportation, which caused him to catch a viral respiratory infection and then pass it on to me at home. 
As a result, I was unable to work for 5 days, until February 3 inclusive.
```

## 19. Твоя задача
### 19.1.
Я выбираю `TH-BG-Color` для `DA` «Networking».

### 19.2.
Предложи 10 вариантов.

### 19.3.
Результатом должна быть таблица Markdown с 3 колонками:
#### 19.3.1.
Порядковый номер варианта (начиная с 1).
#### 19.3.2. 
Цвет в формате `#<hex>` (как в CSS).
Эту же ячейку залей этим же цветом.
#### 19.3.3.
Твоё обоснование выбора цвета.

### 19.4.
Варианты упорядочи таким образом, чтобы те, которые ты считаешь лучшими — предшествовали остальным.

### 19.5.
Вариант должен быть в стиле quiet luxury: Brunello Cucinelli, Loro Piana.
Вариант должен соответствовать премиальности моего профиля.
Вариант должен быть не резким, ярким цветом, а скорее всего пастельных тонов: приглушённым, едва заметным.


