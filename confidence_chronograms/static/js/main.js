function days(){
    document.getElementById("day").innerHTML = gantt.change_view_mode('Day');
    //alert("Days");

}
function weeks(){
    document.getElementById("week").innerHTML = gantt.change_view_mode('Week');
    //alert("Weeks");

}
function months(){
    document.getElementById("month").innerHTML = gantt.change_view_mode('Month');
    //alert("Months");

}
function years(){
    document.getElementById("year").innerHTML = gantt.change_view_mode('Year');
    //alert("Years");

}

 
function myFunction() {/*pega id=myInput em password*/
    var x = document.getElementById("myInput");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }
