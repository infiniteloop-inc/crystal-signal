<?php
    include_once("./setupLanguage.php");
?>

<!DOCTYPE html>
<html>
    <title><?php echo LABEL_TITLE ?></title>
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

        
        <!-- set the language. This is only done when there's no language setting -->
        <?php
            if($languageFromSettings == "none"){
                echo "<script> $.get('ctrl/simpleController.py?settingupsettings=1&language=" . $language . "', function(data, status){});</script>"; 
            }
        ?>

        <style>
            html,body,h1,h2,h3,h4,h5,h6 {font-family: "Roboto", sans-serif}

            #SliderRed .slider-selection {
                background: red;
            }

            #SliderGreen .slider-selection {
                background: green;
            }

            #SliderBlue .slider-selection {
                background: blue;
            }

            #SliderPeriod .slider-selection {
                background: #BABABA;
            }

            #SliderRepeat .slider-selection {
                background: #BABABA;
            }

            .slider-handle {
                background-image: -webkit-linear-gradient(top, #dfdfdf 0%, #bebebe 100%);
                background-image: -o-linear-gradient(top, #dfdfdf 0%, #bebebe 100%);
                background-image: linear-gradient(to bottom, #dfdfdf 0%, #bebebe 100%);
                background-repeat: repeat-x;
                filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffdfdfdf', endColorstr='#ffbebebe', GradientType=0);
            }

            .block1 { float: left; width: 600px; margin-left: 10px; }
            .block2 { float: left; width: 600px; margin-left: 10px; }
            .block3 { float: left; width: 600px; margin-left: 10px; }

            .sliderBox {margin-left:10px; float: left; width: 250px; }
            .buttonBox {float: left; width: 290px; margin-left:10px; }

            .innerButtonBox1 {margin: 0 auto; width: 300px}
            .innerButtonBox2 {margin: 0 auto; width: 202px}
            .innerInputBox {width: 480px}
            .horizontalSpacer { margin-top:15px;}

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
                    <li class="active"><a href="./"><?php echo LABEL_NAVBAR_ALARM_CREATION;?></a></li>
                    <li><a href="./log.php"><?php echo LABEL_NAVBAR_LOG;?></a></li>
                    <li><a href="./settings.php"><?php echo LABEL_NAVBAR_SETTINGS;?></a></li>
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
                            <h4><?php echo LABEL_BOX_ALERT_SETTINGS?></h4>
                        </div>
                        <div class="panel-body">
                            <div class="sliderBox">
                                <br>
                                <input id="sldrRed" data-slider-id='SliderRed' type="text" data-slider-min="0" data-slider-max="255" data-slider-step="1" data-slider-value="100"/>
                                <br><br><br>
                                <input id="sldrGreen" data-slider-id='SliderGreen' type="text" data-slider-min="0" data-slider-max="255" data-slider-step="1" data-slider-value="80"/>
                                <br><br><br>
                                <input id="sldrBlue" data-slider-id='SliderBlue' type="text" data-slider-min="0" data-slider-max="255" data-slider-step="1" data-slider-value="0"/>
                            </div>
                            <div class="buttonBox">
                                <br>
                                <input id="sldrPeriod" data-slider-id='SliderPeriod' type="text" data-slider-min="10" data-slider-max="3000" data-slider-step="1" data-slider-value="1000"/>
                                <br><br><br>
                                <input id="sldrRepeat" data-slider-id='SliderRepeat' type="text" data-slider-min="0" data-slider-max="20" data-slider-step="1" data-slider-value="0"/>
                                <br>
                                <div class="innerButtonBox1">
                                    <div class="btn-group">
                                        <button type="button" class="btn btn-default horizontalSpacer" name="btnOn"><?php echo LABEL_ON;?></button>
                                        <button type="button" class="btn btn-default horizontalSpacer" name="btnBlink"><?php echo LABEL_FLASHING;?></button>
                                        <button type="button" class="btn btn-default horizontalSpacer" name="btnAsynchBlink"><?php echo LABEL_ASYNCH_FLASHING;?></button><br>
                                    </div>
                                </div>
                                <div class="innerButtonBox2">
                                    <div class="btn-group">
                                        <button type="button" class="btn btn-default horizontalSpacer" name="btnHtml">Html</button>
                                        <button type="button" class="btn btn-default horizontalSpacer" name="btnJson">Json</button>
                                    </div>
                                </div>
                            </div>
                            <div class="innerInputBox">
                                <div class="form-group">
                                    <label for="usr"><?php echo LABEL_INFO_TEXT?></label>
                                    <input type="text" class="form-control" id="infoText"> 
                                </div>
                                <div class="form-group">
                                    <label for="usr"><?php echo LABEL_SPEAK_TEXT?></label>
                                    <input type="text" class="form-control" id="speakText"> 
                                </div>

                                <div class="form-group">
                                    <label for="usr"><?php echo LABEL_ALERT_STRING?></label>
                                    <input type="text" class="form-control" id="showQueryString"> 
                                </div>
                            </div>
                            <button type="button" class="btn btn-warning horizontalSpacer" name="btnAckAlarm">
                                <?php echo LABEL_ACK?>
                            </button>
                            <button type="button" class="btn btn-default horizontalSpacer" name="btnSend"><?php echo LABEL_SEND;?></button>
                        </div>
                    </div>
                </div>

                <div class="block2">
                    <div class="panel panel-success">
                        <div class="panel-heading">
                            <h4><?php echo LABEL_STATUS_RESPONSE;?></h4>
                        </div>
                        <div class="panel-body">
                            <div id="statusText">
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
        <!-- Main content end-->

        <script>
            $(document).ready(function(){
                var SenderObj = {
                    color:  [100,80,0],
                    mode: 0,
                    period: 1000,
                    repeat: 0,
                    json: 0,
                    info: "",
                    speak: "",
                    updateMode: function(val){
                        this.mode = val
                        this.send();
                    },
                    updatePeriod: function(val){
                        this.period = val; 
                        this.send();
                    },
                    updateRepeat: function(val){
                        this.repeat = val;          
                        this.send();
                    },
                    updateJson: function(val){
                        this.json = val; 
                        this.send();
                    },
                    init: function(){
                        $('button[name=btnOn]').addClass("btn-success");
                        $('button[name=btnHtml]').addClass("btn-success");
                    },
                    updateRed: function(val){
                        this.color[0] = val;
                        this.send();
                    },
                    updateGreen: function(val){
                        this.color[1] = val;
                        this.send();
                    },
                    updateBlue: function(val){
                        this.color[2] = val;
                        this.send();
                    },
                    updateInfo: function(val){
                        this.info = val;
                        this.send();
                    },
                    updateSpeak: function(val){
                        this.speak = val;
                        this.send();
                    },
                    send: function(){
                        queryString = '?color=' + this.color[0] + ',' + this.color[1] + ',' + this.color[2] +
                            '&mode=' + this.mode + '&repeat=' + this.repeat + '&period=' + this.period + 
                            '&json=' + this.json
                            if (this.info !== ""){
                                queryString += '&info=' + this.info;
                            }
                            if (this.speak !== ""){
                                queryString += '&speak=' + this.speak;
                            }
                        $("#showQueryString").val(window.location.href + "ctrl/" + queryString);
                        $.get("ctrl/simpleController.py" + queryString, function(data, status){
                            $("#statusText").html(data); 
                        });
                    }
                };

                // Text field
                $("#infoText").change(infoTextChange);
                $("#speakText").change(speakTextChange);

                function speakTextChange(){
                    SenderObj.updateSpeak($("#speakText").val());
                }

                function infoTextChange(){
                    SenderObj.updateInfo($("#infoText").val());
                }

                // SLIDERS
                var sldrRed = $('#sldrRed').slider({
                    formatter: function(value) {
                        return 'red: ' + value;
                    }
                });

                var sldrGreen = $('#sldrGreen').slider({
                    formatter: function(value) {
                        return 'green: ' + value;
                    }
                });

                var sldrBlue = $('#sldrBlue').slider({
                    formatter: function(value) {
                        return 'blue: ' + value;
                    }
                });

                var sldrRepeat = $('#sldrRepeat').slider({
                    formatter: function(value) {
                        return 'Repeat: ' + value;
                    }
                });
                var sldrPeriod = $('#sldrPeriod').slider({
                    formatter: function(value) {
                        return 'Period: ' + value;
                    }
                });

                sldrRed.on("slideStop", function(slideEvt) {
                    SenderObj.updateRed(slideEvt.value);
                });

                sldrGreen.on("slideStop", function(slideEvt) {
                    SenderObj.updateGreen(slideEvt.value);
                });

                sldrBlue.on("slideStop", function(slideEvt) {
                    SenderObj.updateBlue(slideEvt.value);
                });

                sldrRepeat.on("slideStop", function(slideEvt) {
                    SenderObj.updateRepeat(slideEvt.value);
                });
                sldrPeriod.on("slideStop", function(slideEvt) {
                    SenderObj.updatePeriod(slideEvt.value);
                });

                    // BUTTONS
                $('button[name=btnAckAlarm]').click(function(){
                    $("#showQueryString").val(window.location.href + "ctrl/" + "?ack=1");
                    $.get('ctrl/simpleController.py?ack=1', function(data, status){
                        $("#statusText").html(data); 
                    });
                });
                $('button[name=btnSend]').click(function(){
                    SenderObj.send();
                });
                $('button[name=btnOn]').click(function(){
                    $('button[name=btnAsynchBlink]').removeClass("btn-success");
                    $('button[name=btnBlink]').removeClass("btn-success");
                    $('button[name=btnOn]').addClass("btn-success");
                    SenderObj.updateMode(0);
                });
                $('button[name=btnBlink]').click(function(){
                    $('button[name=btnAsynchBlink]').removeClass("btn-success");
                    $('button[name=btnBlink]').addClass("btn-success");
                    $('button[name=btnOn]').removeClass("btn-success");
                    SenderObj.updateMode(1);
                });
                $('button[name=btnAsynchBlink]').click(function(){
                    $('button[name=btnAsynchBlink]').addClass("btn-success");
                    $('button[name=btnBlink]').removeClass("btn-success");
                    $('button[name=btnOn]').removeClass("btn-success");
                    SenderObj.updateMode(2);
                });
                $('button[name=btnHtml]').click(function(){
                    $('button[name=btnJson]').removeClass("btn-success")
                        $('button[name=btnHtml]').addClass("btn-success")
                        SenderObj.updateJson(0);
                });
                $('button[name=btnJson]').click(function(){
                    $('button[name=btnJson]').addClass("btn-success")
                        $('button[name=btnHtml]').removeClass("btn-success")
                        SenderObj.updateJson(1);
                });
                SenderObj.init();
            });
        </script>
    </body>
</html>
