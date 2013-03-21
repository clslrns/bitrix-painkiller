<?
/*
Возвращает параметры компонента по умолчанию на основании названия.

Пример вызова:
/bitrix/modules/painkiller/components-api.php?component=bitrix:news.list

Ответ в формате JSON: {
    status:
        found — компонент найден,
        not_found — компонент не найден,
        error — ошибка в названии или пространстве имён
    data:
        в случае ошибки — объект с вычесленным именем, пространством имён и директорией компонента;
        иначе — объект с параметрами и значениями по умолчанию
}
*/

$bitrixDir = dirname( __FILE__ ) . '/../..';
require $bitrixDir . '/modules/main/include.php';

list( $arCData['nspace'], $arCData['name'] ) = explode( ':', urldecode($_GET['component']) );

// Валидация пространства имён и названия компонента
// Не даст подключить файл .parametrs.php из директории, отличной от /bitrix/components
if( !preg_match( '/[a-zA-Z_-]+/', $arCData['nspace'] )
    || !preg_match( '/[a-zA-Z._-]+/', $arCData['name'] ) )
{
    echo json_encode(
        array(
            'status' => 'error',
            'data' => $arCData
        )
    );
    die;
}

$arCData['dir']  = $bitrixDir . '/components/'
                 . $arCData['nspace'] . '/'
                 . $arCData['name'];

$arReturn = array(
    'status' => 'not_found'
);
if( is_file( $arCData['dir'] . '/.parameters.php' ) ){
    include $arCData['dir'] . '/.parameters.php';

    ksort( $arComponentParameters['PARAMETERS'] );

    foreach( $arComponentParameters['PARAMETERS'] as $paramName => $arParam ){
        $arParams[ $paramName ] = $arParam['DEFAULT'] ? $arParam['DEFAULT'] : '';
    }
    $arReturn['status'] = 'found';
    $arReturn['data'] = $arParams;
}

echo json_encode( $arReturn );