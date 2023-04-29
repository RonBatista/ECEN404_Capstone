<?php
// File containing System Variables
define("LOCAL_PATH_ROOT", $_SERVER["DOCUMENT_ROOT"]);
require LOCAL_PATH_ROOT . '/uas_tools/system_management/centralized_management.php';

function SetTempFolderLocalPath()
{
    //return '/var/www/html/wordpress/temp/';
    return '/var/www/html/temp/';
}

function SetVisualizationFolderLocalPath()
{
    //return '/var/www/html/wordpress/uas_tools/visualization/';
    return '/var/www/html/uas_tools/visualization/';
}

function SetFolderLocalPath()
{
    //return '/var/www/html/wordpress/uas_data/uploads/products/';
    return '/var/www/html/uas_data/uploads/products/';
}

function SetFolderHTMLPath()
{
    //return 'https://uashub.tamucc.edu/uas_data/uploads/products/';
    //return 'http://basfhub.gdslab.org/uas_data/uploads/products/';
    //return 'http://bhub.gdslab.org/uas_data/uploads/products/';
    return $header_location . '/uas_data/uploads/products/';
}

function SetDisplayHTMLPath()
{
    //return 'https://uashub.tamucc.edu/uas_data/uploads/products/';
    //return 'http://basfhub.gdslab.org/uas_data/uploads/products/';
    //return 'http://bhub.gdslab.org/uas_data/uploads/products/';
    return $header_location . '/uas_data/uploads/products/';
}

// Added
function SetTempFolderLocalPathMobile()
{
    return '/var/www/html/temp/mobile/';
}

function SetVisualizationFolderLocalPathMobile()
{
    return '/var/www/html/uas_tools/visualization/mobile/';
}

function SetFolderLocalPathMobile()
{
    return '/var/www/html/uas_data/uploads/products/mobile/';
}

function SetFolderHTMLPathMobile()
{
    return $header_location . '/uas_data/uploads/products/mobile/';
}

function SetDisplayHTMLPathMobile()
{
    return $header_location . '/uas_data/uploads/products/mobile/';
}

//

?>
