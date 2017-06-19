<?php
    $languageFromSettings = "none";
    $language = "none";

    // get language from Browser.
    switch(substr($_SERVER['HTTP_ACCEPT_LANGUAGE'], 0, 2))
    {
        case "en":
            $languageFromBrowser = "english";
            break;
        case "ja":
            $languageFromBrowser = "japanese";
            break;
        default:
            $languageFromBrowser = "english";
            break;
    }

    // get language from settings.
    if (file_exists("/var/lib/crystal-signal/Settings.json"))
    {
        $json = file_get_contents("/var/lib/crystal-signal/Settings.json");
        $json_data = json_decode($json, true);
        if(array_key_exists("language", $json_data))
        {
            $languageFromSettings = $json_data["language"];
        }
    }

    // set language
    if($languageFromSettings == "none")
    {
        $language = $languageFromBrowser;
    }
    else
    {
        $language = $languageFromSettings;
    }

    // include language files
    switch($language)
    {
        case "english": 
            include_once("./languageFiles/english.php");
            break;
        case "japanese":
            include_once("./languageFiles/japanese.php");
            break;
        default:
            include_once("./languageFiles/english.php");
            break;
    }
?>
