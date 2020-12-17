window.onload = function(){ 
  // your code 

var buttonRecord = document.getElementById("record");
var buttonStop = document.getElementById("stop");


// buttonStop.disabled = true;

buttonRecord.onclick = function() {
    console.log('here i am')
    var first_name = $('#first_name').val();
    var last_name = $('#last_name').val();
    var email = $('#email').val();
    var age = $('#age').val();
    var sid = $('#sid').val();
    var gender = $('#gender').val();

    console.log(first_name)
    console.log(sid)
    
    if (first_name.length < 1 && last_name.length < 1 && email.length < 1 && age.length < 1 && sid.length < 1 && gender.length < 1 ) {
        $("input[name~='first_name']").after('<span class="error">Fields are empty</span>');
        console.log('there is an error')
        return false;
    }

    console.log('im here')
    // var url = window.location.href + "record_status";
    buttonRecord.disabled = true;
    buttonStop.disabled = false;
    
    // disable download link
    var downloadLink = document.getElementById("download");
    downloadLink.text = "";
    downloadLink.href = "";

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);
        }
    }
    xhr.open("POST", "/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ status: "true" , name : sid}));
};

buttonStop.onclick = function() {
    buttonRecord.disabled = false;
    buttonStop.disabled = true;    

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);

            // enable download link
            var downloadLink = document.getElementById("download");
            downloadLink.text = "Download Video";
            downloadLink.href = "/static/video.avi";
        }
    }
    xhr.open("POST", "/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ status: "false" }));
};

};