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
                echo "<script> $.get('ctrl/controller.py?settingupsettings=1&language=english', function(data, status){});</script>"; 
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
                    <li><a href="./"><?php echo LABEL_NAVBAR_ALARM_CREATION;?></a></li>
                    <li><a href="./log.php"><?php echo LABEL_NAVBAR_LOG;?></a></li>
                    <li><a href="./settings.php"><?php echo LABEL_NAVBAR_SETTINGS;?></a></li>
                    <li class="active"><a href="./status.php"><?php echo LABEL_NAVBAR_STATUS;?></a></li> 
                </ul>
            </div>
        </nav>
        <!-- Main content -->
        <div class="container">
            <div class="row">
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
                    send: function(){
                        queryString = '';
                        $.get("ctrl/controller.py" + queryString, function(data, status){
                            $("#statusText").html(data); 
                        });
                    }
                };
                SenderObj.send();
            });
        </script>
    </body>
</html>
