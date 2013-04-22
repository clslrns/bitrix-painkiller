Bitrix Painkiller
=================

The plugin is designed to ease the development of web sites on 1C-Bitrix CMS. It allows you to convert code like `bitrix:news.list` into a full component inclusion code by <kbd>Tab</kbd>.

Плагин предназначен для облегчения разработки сайтов на 1С-Битрикс. Он позволяет преобразовывать код вида `bitrix:news.list` в полноценный код подключения компонента одним нажатием <kbd>Tab</kbd>.

![transform](http://picasion.com/pic67/6991b114c4f74ac1b1aaa89f8a456746.gif)

Особенности
-----------
* Поддерживает множественные курсоры;
* Запрашивает параметры компонентов асинхронно, не вешая редактор;
* Учитывает ваши настройки форматирования (табы или пробелы, ширину отступов);
* Работает для компонентов из неймспейсов, отличных от bitrix.

Установка
-------------------------------
### thelikers.painkiller для 1C-Битрикс
Установить модуль можно из [Маркетплейса 1С-Битрикс](http://marketplace.1c-bitrix.ru/solutions/thelikers.painkiller/index.php). Также доступен [репозиторий на Github](https://github.com/clslrns/bitrix-painkiller-module).
Модуль нужен для получения параметров разворачиваемых компонентов.

### Плагин для Sublime Text 2

Для начала, если вы этого ещё не сделали, установите [Package Control](http://wbond.net/sublime_packages/package_control). После установки сделайте Tools — Command Pallete — Package Control: Install Package — Bitrix Painkiller.

#### Готовые команды
##### OS X

    cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/
    git clone git@github.com:clslrns/bitrix-painkiller.git

##### Ubuntu Linux

    cd ~/.config/sublime-text-2/Packages/
    git clone git://github.com/clslrns/bitrix-painkiller.git

Известные проблемы
------------------
Возможен конфликт с плагином Emmet. Вы можете переназначить сочетание клавиш для Painkiller, либо отвязать Emmet от кнопри Tab, добавив в пользовательский конфиг параметр:

    "disable_tab_abbreviations": true
