<?php
    include_once("./setupLanguage.php");
?>
<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta charset="UTF-8">
        <title><?php echo LABEL_TITLE ?></title>

        <!-- jQuery -->
        <Script src="./js/jquery-3.1.1.min.js"></script> 

        <!-- bootstrap -->
        <link rel="stylesheet" href="./css/bootstrap-3.3.7.min.css">
        <script src="./js/bootstrap-3.3.7.min.js"></script> 

        <!-- bootstrap slider -->
        <link rel="stylesheet" href="./css/bootstrap-slider-9.5.1.min.css">
        <script src="./js/bootstrap-slider-9.5.1.min.js"></script>

        <!-- stylesheet -->
        <link rel="stylesheet" href="./css/status.css">

        <!-- Fonts -->
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">
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
                        $.get("ctrl/simpleController.py" + queryString, function(data, status){
                            $("#statusText").html(data); 
                        });
                    }
                };
                SenderObj.send();
            });
        </script>
    </body>
</html>
