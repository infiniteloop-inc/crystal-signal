<?php
    include_once("./setupLanguage.php");
?>
<!DOCTYPE html>
<html>
    <title>Crystal Signal Pi</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta charset="UTF-8">

    <head>
        <!-- jQuery -->
        <Script src="./js/jquery-3.1.1.min.js"></script> 

        <!-- bootstrap -->
        <link rel="stylesheet" href="./css/bootstrap-3.3.7.min.css">
        <script src="./js/bootstrap-3.3.7.min.js"></script> 

        <!-- bootstrap slider -->
        <link rel="stylesheet" href="./css/bootstrap-slider-9.5.1.min.css">
        <script src="./js/bootstrap-slider-9.5.1.min.js"></script>

        <!-- Fonts -->
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">

        <style>
            html,body,h1,h2,h3,h4,h5,h6 {font-family: "Roboto", sans-serif}

            .dropdown-toggle{
                width: 150px !important;
            }

            #SliderBrightness .slider-selection {
                background: #BABABA;
            }

            .slider-handle {
                background-image: -webkit-linear-gradient(top, #dfdfdf 0%, #bebebe 100%);
                background-image: -o-linear-gradient(top, #dfdfdf 0%, #bebebe 100%);
                background-image: linear-gradient(to bottom, #dfdfdf 0%, #bebebe 100%);
                background-repeat: repeat-x;
                filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffdfdfdf', endColorstr='#ffbebebe', GradientType=0);
            }

            .DropDownSpan { display: table-cell; vertical-align: middle; }
            .block1 { float: left; width: 600px; margin-left: 10px; }
            .block2 { float: left; width: 600px; margin-left: 10px; }
            .horizontalSpacer { margin-top:15px;}
            .buttonBox {float: left; width: 290px; margin-left:10px; }
            .boxLeft {margin-left:10px; float: left; width: 350px; display: table; }
            .boxRight {float: left; width: 290px; margin-left:10px; }
        </style>
    </head>

    <body>

        <!-- Navbar -->
        <nav class="navbar navbar-default" >
            <div class="container">
                <div class="navbar-header">
                    <a class="navbar-brand" href="./"><?php echo LABEL_TITLE;?></a>
                </div>
                <ul class="nav navbar-nav">
                    <li><a href="./"><?php echo LABEL_NAVBAR_ALARM_CREATION;?></a></li>
                    <li><a href="./log.php"><?php echo LABEL_NAVBAR_LOG;?></a></li>
                    <li class="active"><a href="./settings.php"><?php echo LABEL_NAVBAR_SETTINGS;?></a></li>
                    <li><a href="./status.php"><?php echo LABEL_NAVBAR_STATUS;?></a></li> 
                </ul>
            </div>
        </nav>

        <!-- Main content -->
        <div class="container">
            <div class="row">
                <div class="block1"> 
                    <div class="panel panel-info">
                        <div class="panel-heading">
                            <h4><?php echo LABEL_BUTTON_SETTINGS;?></h4>
                        </div>
                        <div class="panel-body">

                            <!-- dropdown menus! -->
                            </br>
                            <div class="boxLeft"> 
                                <div style="width: 100%; height: 12px; border-bottom: 1px solid black; text-align: center">
                                    <span style="font-size: 15px; background-color: #FFFFFF; padding: 0 10px;">
                                        <?php echo LABEL_WITH_ALL_ALERTS_ACKNOWLEDGED;?>
                                    </span>
                                </div>
                            </div>
                            <br>
                            <br>
                            <div class="boxLeft"> 
                                <span class="DropDownSpan"><?php echo LABEL_NORMAL_BUTTON_PRESS;?></span>
                                <div id="dropdown1" style="float: right">
                                    <div class="dropdown">
                                        <button class="btn btn-default dropdown-toggle" type="button" style="width= 400px" data-toggle="dropdown" name="dropDown1">
                                            <?php echo LABEL_LOADING;?>
                                        <span class="caret"></span></button>
                                        <ul class="dropdown-menu">
                                            <li><a href="#"></a></li>'
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            </br>
                            </br>
                            <div class="boxLeft"> 
                                <span class="DropDownSpan"><?php echo LABEL_LONG_BUTTON_PRESS;?></span>
                                <div id="dropdown3" style="float: right">
                                    <div class="dropdown">
                                        <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" name="dropDown1">
                                            <?php echo LABEL_LOADING;?>
                                        <span class="caret"></span></button>
                                        <ul class="dropdown-menu">
                                            <li><a href="#"></a></li>'
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            </br>
                            </br>
                            </br>
                            <div class="boxLeft"> 
                                <div style="width: 100%; height: 12px; border-bottom: 1px solid black; text-align: center">
                                    <span style="font-size: 15px; background-color: #FFFFFF; padding: 0 10px;">
                                        <?php echo LABEL_WITH_PENDING_ALERT;?>
                                    </span>
                                </div>
                            </div>
                            <br>
                            <br>
                            <div class="boxLeft"> 
                                <span class="DropDownSpan"><?php echo LABEL_NORMAL_BUTTON_PRESS;?></span>
                                <div id="dropdown2" style="float: right">
                                    <div class="dropdown">
                                        <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" name="dropDown1">
                                            <?php echo LABEL_LOADING;?>
                                        <span class="caret"></span></button>
                                        <ul class="dropdown-menu">
                                            <li><a href="#"></a></li>'
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            </br>
                            </br>
                            <div class="boxLeft"> 
                                <span class="DropDownSpan"><?php echo LABEL_LONG_BUTTON_PRESS;?></span>
                                <div id="dropdown4" style="float: right">
                                    <div class="dropdown">
                                        <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" name="dropDown1">
                                            <?php echo LABEL_LOADING;?>
                                        <span class="caret"></span></button>
                                        <ul class="dropdown-menu">
                                            <li><a href="#"></a></li>'
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            </br>
                        </div>
                    </div>
                </div>
                <div class="block2"> 
                    <div class="panel panel-success">
                        <div class="panel-heading">
                            <h4><?php echo LABEL_GENERAL_SETTINGS;?></h4>
                        </div>
                        <br>
                        <div class="panel-body">
                            <div class="boxLeft">
                                <span class="DropDownSpan"><?php echo LABEL_BRIGHTNESS;?></span>
                                <div id="BSlider" style="float: right">
                                    <input id="sldrBrightness" data-slider-id='SliderBrightness' type="text" data-slider-min="40" data-slider-max="100" data-slider-step="1" data-slider-value="40"/>
                                </div>
                            </div>
                            </br>
                            </br>
                            <div class="boxLeft"> 
                                <span class="DropDownSpan"><?php echo LABEL_EXECUTED_AFTER_ALERT;?></span>
                                <div id="dropdown5" style="float: right">
                                    <div class="dropdown">
                                        <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" name="dropDown1">
                                            <?php echo LABEL_LOADING;?>
                                        <span class="caret"></span></button>
                                        <ul class="dropdown-menu">
                                            <li><a href="#"></a></li>'
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            </br>
                            </br>
                            <div class="boxLeft"> 
                                <span class="DropDownSpan"><?php echo LABEL_LANGUAGE_SETTING;?></span>
                                <div id="dropdown6" style="float: right">
                                    <div class="dropdown">
                                        <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" name="dropDown1">
                                            <?php echo LABEL_LOADING;?>
                                        <span class="caret"></span></button>
                                        <ul class="dropdown-menu">
                                            <li><a href="#"></a></li>'
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            </br>
                            </br>
                            <div class="boxLeft"> 
                                <span class="DropDownSpan"><?php echo LABEL_VOICE_SETTING;?></span>
                                <div id="dropdown7" style="float: right">
                                    <div class="dropdown">
                                        <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" name="dropDown1">
                                            <?php echo LABEL_LOADING;?>
                                        <span class="caret"></span></button>
                                        <ul class="dropdown-menu">
                                            <li><a href="#"></a></li>'
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            </br>
                            </br>
                            </br>
                            </br>
                            </br>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Main content end-->

        <script>
            function getHTML(){
                $.get('ctrl/controller.py?getdropdowndata=1', function(data, status){
                    //console.log(data);
                    parsedData = JSON.parse(data);
                    $("#dropdown1").html(parsedData[0]); 
                    $("#dropdown2").html(parsedData[1]); 
                    $("#dropdown3").html(parsedData[2]); 
                    $("#dropdown4").html(parsedData[3]); 
                    $("#dropdown5").html(parsedData[4]); 
                    $("#dropdown6").html(parsedData[5]); 
                    $("#dropdown7").html(parsedData[6]); 
                    $("#BSlider").html(parsedData[7]);
                    // reinit 
                    var sldrBrightness = $('#sldrBrightness').slider({
                        formatter: function(value) {
                            return 'Brightness: ' + value + '%';
                        }
                    });
                });
            } 

            function reloadCurrentPage() 
            {
                window.location.href = "";
            }

            $(document).ready(function(){
                getHTML();

                $(this).on("click","#dropdown1 a", function(e){ 
                    tmpText = $(this).text();
                    console.log("test");
                    $("#dropdown1").find('button[name=dropDown1]').text(tmpText);
                    $("#dropdown1").find('button[name=dropDown1]').append('<span class="caret"></span>')
                    $.get('ctrl/controller.py?settingupbuttons=1&dropdown1=' + tmpText, function(data, status){
                    });
                });
                $(this).on("click","#dropdown2 a", function(e){ 
                    tmpText = $(this).text();
                    $("#dropdown2").find('button[name=dropDown1]').text(tmpText);
                    $("#dropdown2").find('button[name=dropDown1]').append('<span class="caret"></span>')
                    $.get('ctrl/controller.py?settingupbuttons=1&dropdown2=' + tmpText, function(data, status){
                    });
                });
                $(this).on("click","#dropdown3 a", function(e){ 
                    tmpText = $(this).text();
                    $("#dropdown3").find('button[name=dropDown1]').text(tmpText);
                    $("#dropdown3").find('button[name=dropDown1]').append('<span class="caret"></span>')
                    $.get('ctrl/controller.py?settingupbuttons=1&dropdown3=' + tmpText, function(data, status){
                    });
                });
                $(this).on("click","#dropdown4 a", function(e){ 
                    tmpText = $(this).text();
                    $("#dropdown4").find('button[name=dropDown1]').text(tmpText);
                    $("#dropdown4").find('button[name=dropDown1]').append('<span class="caret"></span>')
                    $.get('ctrl/controller.py?settingupbuttons=1&dropdown4=' + tmpText, function(data, status){
                    });
                });
                $(this).on("click","#dropdown5 a", function(e){ 
                    tmpText = $(this).text();
                    $("#dropdown5").find('button[name=dropDown1]').text(tmpText);
                    $("#dropdown5").find('button[name=dropDown1]').append('<span class="caret"></span>')
                    $.get('ctrl/controller.py?settingupbuttons=1&dropdown5=' + tmpText, function(data, status){
                    });
                });
                $(this).on("click","#dropdown6 a", function(e){ 
                    tmpText = $(this).text();
                    $("#dropdown6").find('button[name=dropDown1]').text(tmpText);
                    $("#dropdown6").find('button[name=dropDown1]').append('<span class="caret"></span>')
                    $.get('ctrl/controller.py?settingupsettings=1&language=' + tmpText, function(data, status){
                    });
                    window.setTimeout(reloadCurrentPage, 500);
                });
                $(this).on("click","#dropdown7 a", function(e){ 
                    tmpText = $(this).text();
                    $("#dropdown7").find('button[name=dropDown1]').text(tmpText);
                    $("#dropdown7").find('button[name=dropDown1]').append('<span class="caret"></span>')
                    $.get('ctrl/controller.py?settingupsettings=1&voice=' + tmpText, function(data, status){
                    });
                });

                // SLIDERS
                var sldrBrightness = $('#sldrBrightness').slider({
                    formatter: function(value) {
                        return 'Brightness: ' + value + '%';
                    }
                });
                $(this).on("slideStop", "#sldrBrightness", function(e){
                    tmp = Math.round((e.value - 40)*(255/60))
                    console.log(tmp)
                    $.get('ctrl/controller.py?settingupsettings=1&brightness=' + tmp, function(data, status){
                    });
                });
            });
        </script>
        <!-- 日本語をたくさん書けばvimがエンコーダーを正しく選んでくれる。
            そのためのコメントにすぎない。-->
    </body>
</html>

