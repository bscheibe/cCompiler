// Implements a loading button - don't use show b/c sets to display: block
$( '#compile' ).click(function() {
  $('#loading').css( "display", "inline-block")  
  $('#compile').hide();
});

// Leaving so I can implement shift + tabbing
// var map = []; // Or you could call it "key"
// onkeydown = onkeyup = function(e){
//     e = e || event; // to deal with IE
//     map[e.keyCode] = e.type == 'keydown';
//     /*insert conditional here*/
// }

// Allows tabbing for the user w/in the textarea
$(document).delegate('#textbox', 'keydown', function(e) {
  var keyCode = e.keyCode || e.which;

  if (keyCode == 9) {
    e.preventDefault();
    var start = $(this).get(0).selectionStart;
    var end = $(this).get(0).selectionEnd;

    // set textarea value to: text before caret + tab + text after caret
    $(this).val($(this).val().substring(0, start)
                + "\t"
                + $(this).val().substring(end));

    // put caret at right position again
    $(this).get(0).selectionStart =
    $(this).get(0).selectionEnd = start + 1;
  }
});