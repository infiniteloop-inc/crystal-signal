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

        <!-- stylesheet -->
        <link rel="stylesheet" href="./css/log.css">

        <!-- Fonts -->
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">
    </head>
    <body>

        <!-- Navbar -->
        <nav class="navbar navbar-default" >
            <div class="container">
                <div class="navbar-header">
                    <a class="navbar-brand" href="./"><?php echo LABEL_TITLE ?></a>
                </div>
                <ul class="nav navbar-nav">
                    <li><a href="./"><?php echo LABEL_NAVBAR_ALARM_CREATION;?></a></li>
                    <li class="active"><a href="./log.php"><?php echo LABEL_NAVBAR_LOG;?></a></li>
                    <li><a href="./settings.php"><?php echo LABEL_NAVBAR_SETTINGS;?></a></li>
                    <li><a href="./status.php"><?php echo LABEL_NAVBAR_STATUS;?></a></li> 
                </ul>
            </div>
        </nav>

        <!-- Main content -->
        <div class="container">
            <div class="row">

                <div class="block1"> 

                    <!-- buttons! -->
                    <button type="button" class="btn btn-warning horizontalSpacer" name="btnAckAlarm"><?php echo LABEL_ACK ?> </button>
                    <button type="button" class="btn btn-success horizontalSpacer" name="btnUpdateLog"><?php echo LABEL_UPDATE_LOG ?></button>
                    <button type="button" class="btn btn-danger horizontalSpacer" name="btnDeleteLog"><?php echo LABEL_DELETE_LOG ?></button>
                    <div id="tableData"></div>
                </div>

            </div>
        </div>
        <!-- Main content end-->

        <script>
            function getTable(){
                $.get('ctrl/controller.py?getlogdata=1', function(data, status){
                    $("#tableData").html(data); 
                });
            } 
            $(document).ready(function(){
                // BUTTONS
                $('button[name=btnAckAlarm]').click(function(){
                    $.get('ctrl/controller.py?ack=1', function(data, status){
                    });
                    setTimeout(function(){
                        getTable();
                    }, 200);
                });
                $('button[name=btnUpdateLog]').click(function(){
                    getTable();
                });
                $('button[name=btnDeleteLog]').click(function(){
                    $.get('ctrl/controller.py?getlogdata=1&deletelog=1', function(data, status){
                        $("#tableData").html(data); 
                    });
                });
                // POPOVER
                $('[data-toggle="popover"]').popover();
                // show Table
                getTable();
            });
        </script>
        <!-- 日本語をたくさん書けばvimがエンコーダーを正しく選んでくれる。
            そのためのコメントにすぎない。-->
    </body>
</html>

