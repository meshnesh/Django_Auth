$(window).load(function() {
    setTimeout(function(){
      $("html, body").animate({ scrollTop: $(document).height() }, 1000);
    }, 2000);
});



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
        

        if(data.message && !data.message.trim()==""){
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
        } else if(data.image){
            ele.append(
                $("<td></td>").text(data.timestamp)
            );
            ele.append(
                $("<td></td>").text(data.handle)
            );
            ele.append(
                $("<td></td>").html($('<img>').attr('src', data.image).css({
                'width': '100px'
            }))
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


   $(".pic_form").submit(function(event) {
    event.preventDefault();
    var file = $('#id_picture').get(0).files[0];
    if (file.type.match('image.*')) {
     var reader = new FileReader();
     reader.readAsDataURL(file);
     reader.onloadend = function() {
        var picture = {
        image: reader.result,
        filename: file.name,
       }
       chatsock.send(JSON.stringify(picture));
        $('#id_picture').val('');
       return false;
      //  success: function(data) {
      //   console.log("Success");
      //   $('#id_picture').val('');
      //   var chat = $("#chat");
      //   var ele = $('<tr></tr>');

      //   ele.append(
      //    $("<td></td>").text(data.timestamp)
      //   );
      //   ele.append(
      //    $("<td></td>").text(data.handle)
      //   );
      //   ele.append(
      //    $("<td></td>").html($('<img>').attr('src', data.image).css({
      //     'width': '100px'
      //    }))
      //   );

      //   chat.append(ele);

      //  },
      //  error: function(error) {
      //   console.log("error");
      //   console.log(error);
      //   console.log(error.responseText)
      //  }
      // });
     }
    } else {
     alert("You tried to uploaded a file which is not an image.");
     $('#id_picture').val('');
    }
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