Bitrix Painkiller
=================

Плагин предназначен для облегчения разработки сайтов на 1С-Битрикс. Он позволяет преобразовывать код вида bitrix:news.list в полноценный код подключения компонента одним нажатием <kbd>Tab</kbd>. Для использования необходимо установить вспомогательный модуль `thelikers.painkiller` на сайт (доступен в Bitrix Marketplace и на [https://github.com/clslrns/bitrix-painkiller-module](Github)).

Установка модуля для 1С-Битрикс
-------------------------------
### Получение модуля ###
Если вы хотите использовать Painkiller в качестве субмодуля, то:
    cd site_root;
    git submodule add git://github.com/clslrns/bitrix-painkiller-module.git bitrix/modules/thelikers.painkiller

Иначе, скачивайте [https://nodeload.github.com/clslrns/bitrix-painkiller-module/zip/master](последнюю версию в архиве) и кладите файлы из корня репозитория в директорию `site_root/bitrix/modules/thelikers.painkiller`.

### Установка ###
В панели управления сайта перейдите в раздел Marketplace — Установленные решения. В контекстном меню напротив модуля Bitrix Painkiller (thelikers.painkiller) выберите «Установить»:
!(http://puu.sh/2nGyS)

Установка плагина для Sublime Text 2
------------------------------------
OS X
    cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/;
    git clone git@github.com:clslrns/bitrix-painkiller.git
