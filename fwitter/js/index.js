/**
 * Created by arosi on 3/25/2017.
 */

actionUrl = "";

$('#registerBtn').click(function () {
    $('form').hide();
    $('#responseDiv').hide();
    $('#registerForm').show();
    actionUrl = '/adduser';
});
$('#verifyBtn').click(function () {
    $('form').hide();
    $('#responseDiv').hide();
    $('#verifyForm').show();
    actionUrl = '/verify';
});
$('#loginBtn').click(function () {
    $('form').hide();
    $('#responseDiv').hide();
    $('#loginForm').show();
    actionUrl = '/login';
});
$('#postTweetBtn').click(function () {
    $('form').hide();
    $('#responseDiv').hide();
    $('#postTweetForm').show();
    actionUrl = '/additem';
});
$('#viewTweetBtn').click(function () {
    $('form').hide();
    $('#responseDiv').hide();
    $('#viewTweetForm').show();
    actionUrl = "";
});
$('#searchTweetsBtn').click(function () {
    $('form').hide();
    $('#responseDiv').hide();
    $('#searchTweetsForm').show();
    actionUrl = "";
});

$('.cancelBtn').click(function () {
    $('form').hide();
});

$('form').submit(function (){
    event.preventDefault();
    performApiCall($(this).serializeArray());
    return false;
});

function objectifyForm(formArray) {//serialize data function

  var returnArray = {};
  for (var i = 0; i < formArray.length; i++){
    returnArray[formArray[i]['name']] = formArray[i]['value'];
  }
  return returnArray;
}

function performApiCall(form) {
    jsonObj = objectifyForm(form);
    jsonStr = JSON.stringify(jsonObj);
    $.ajax({
        type: 'POST',
        url: actionUrl,
        data: jsonStr,
        contentType: 'application/json',
        dataType: 'json',
        success: function (data) {
            $('form').hide();
            $('#responseDiv').show();
            $('#response').html(JSON.stringify(data));
        }
    });
}