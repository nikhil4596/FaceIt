/**
 * Created by nikhil on 11/27/2016.
 */

var imageBlob;
function take_snapshot() {
    Webcam.snap( function(data_uri) {
        imageBlob = dataURItoBlob(data_uri);
    } );
    var file = new File([imageBlob], "image.jpg", {type: "image/jpeg"});
    console.log(file);
    var form = document.getElementById('myForm');
    var img_name = document.getElementById("helperp").value;
    console.log(img_name);
    var formData = new FormData(form);
    formData.append("file", file);
    formData.append("img_name", img_name);
    var xmlhttp = new XMLHttpRequest();
    var url = "/compute?img=" + img_name;
    xmlhttp.open("POST", url);
    xmlhttp.onreadystatechange = function() {

    if(this.readyState == 4 && this.status == 200) {
        alert(typeof this.responseText);
        var score = this.responseText["total"];
        var escore = this.responseText["escore"];
        var fscore = this.responseText["fscore"];
        window.location = "/end?score=" + score + "&escore=" + escore + "&fscore=" +fscore;
    }
    };

    xmlhttp.send(formData);
    console.log(formData.get('file'));
}

function waitSeconds(iMilliSeconds) {
    var counter= 0
        , start = new Date().getTime()
        , end = 0;
    while (counter < iMilliSeconds) {
        end = new Date().getTime();
        counter = end - start;
    }
}
