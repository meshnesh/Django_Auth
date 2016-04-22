$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";

    // For running on localhost
    // var chatsock = new WebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);

    // For running on heroku
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);


    console.log(ws_scheme + '://' + window.location.host  + window.location.pathname);

    console.log("Start sending messages");


    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        console.log("Receiving message");
        console.log(data)
        var chat = $("#chat");
        var ele = $('<tr></tr>');
        

        if(!data.message.trim()==""){
            ele.append(
                $("<td></td>").text(data.timestamp)
            );
            ele.append(
                $("<td></td>").text(data.handle)
            );
            ele.append(
                $("<td></td>").text(data.message)
            );
            chat.append(ele);
        }
        
    };
    $("#chatform").on("submit", function(event) {
        
        var message = {
            handle: $('#handle').text(),
            message: splitString($('#message').val(), 80),
        }
        console.log("Sending message");
        console.log(message);
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });
    
    function splitString (string, size) {
    	var re = new RegExp('.{1,' + size + '}', 'g');
    	var newString = "";
        var strArray = string.match(re);
        
        if(strArray != null){
            for(var count = 0; count < strArray.length; count++){
                newString += strArray[count] + "\n";
            }
            return newString.trim();
        } else{
            return null;
        }
    }
    
});