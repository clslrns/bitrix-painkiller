Bitrix Painkiller
=================

Плагин предназначен для облегчения разработки сайтов на 1С-Битрикс. Он позволяет преобразовывать код вида bitrix:news.list в полноценный код подключения компонента одним нажатием <kbd>Tab</kbd>. Для использования необходимо установить вспомогательный модуль `thelikers.painkiller` на сайт (доступен на [Github](https://github.com/clslrns/bitrix-painkiller-module/)).

Установка
-------------------------------
### Модуль для Битрикса
Нужен для получения параметров компонентов по умолчанию. Если эта функция не нужна, модуль можно не устанавливать.

Для использования Painkiller в качестве субмодуля выполните команды:

    cd site_root
    git submodule add git://github.com/clslrns/bitrix-painkiller-module.git bitrix/modules/thelikers.painkiller

Иначе, скачайте [https://nodeload.github.com/clslrns/bitrix-painkiller-module/zip/master](последнюю версию в архиве) и положите файлы из корня репозитория в директорию `site_root/bitrix/modules/thelikers.painkiller`.

Затем, в панели управления сайта перейдите в раздел Marketplace — Установленные решения. В контекстном меню напротив модуля Bitrix Painkiller (thelikers.painkiller) выберите «Установить».

### Плагин для Sublime Text 2

#### OS X

    cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/;
    git clone git@github.com:clslrns/bitrix-painkiller.git

#### Ubuntu Linux

    cd ~/.config/sublime-text-2/Packages/
    git clone git://github.com/clslrns/bitrix-painkiller.git
