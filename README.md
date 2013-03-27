Bitrix Painkiller
=================

The plugin is designed to ease the development of web sites on 1C-Bitrix CMS. It allows you to convert code like `bitrix:news.list` into a full component inclusion code by <kbd>Tab</kbd>.

Плагин предназначен для облегчения разработки сайтов на 1С-Битрикс. Он позволяет преобразовывать код вида `bitrix:news.list` в полноценный код подключения компонента одним нажатием <kbd>Tab</kbd>.

![transform](http://picasion.com/pic67/6991b114c4f74ac1b1aaa89f8a456746.gif)

Установка
-------------------------------
### Модуль thelikers.painkiller для 1C-Битрикс
Модуль доступен на Github в [отдельном репозитории](https://github.com/clslrns/bitrix-painkiller-module). Он необходим для получения параметров разворачиваемых компонентов. Без установки модуля компоненты будут разворачиваться в такой код:

    <?$APPLICATION->IncludeComponent(
        'bitrix:menu',
        '',
        array(
        )
    )?>

Можно использовать bitrix-painkiller-module в качестве git-субмодуля:

    cd site_root
    git submodule add git://github.com/clslrns/bitrix-painkiller-module.git bitrix/modules/thelikers.painkiller

Или скачать [последнюю версию модуля в архиве](https://nodeload.github.com/clslrns/bitrix-painkiller-module/zip/master) и положить файлы из архива в директорию `site_root/bitrix/modules/thelikers.painkiller`.

Затем, в панели управления сайта перейдите в раздел Marketplace — Установленные решения. В контекстном меню напротив модуля Bitrix Painkiller (thelikers.painkiller) выберите «Установить».

### Плагин для Sublime Text 2

В данный момент плагин недоступен в репозитории Package Control. Для установки скопируйте или склонируйте содержимое репозитория в директорию с плагинами Sublime Text 2. Узнать её можно в меню Preferences — Browse Packages.

#### Готовые команды
##### OS X

    cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/
    git clone git@github.com:clslrns/bitrix-painkiller.git

##### Ubuntu Linux

    cd ~/.config/sublime-text-2/Packages/
    git clone git://github.com/clslrns/bitrix-painkiller.git

