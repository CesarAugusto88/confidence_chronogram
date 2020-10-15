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
//imagens
var jumboHeight=$(".jumbotron").outerHeight();function parallax(){var o=$(window).scrollTop();$(".jumbotron").css("background-position","center "+-.2*o+"px"),console.log(jumboHeight-o)}$(window).scroll((function(o){parallax()}));
$(document).ready((function(){$("[data-bs-hover-animate]").mouseenter((function(){var a=$(this);a.addClass("animated "+a.attr("data-bs-hover-animate"))})).mouseleave((function(){var a=$(this);a.removeClass("animated "+a.attr("data-bs-hover-animate"))}))}));
var jumboHeight=$(".jumbotron").outerHeight();function parallax(){var a=$(window).scrollTop();$(".jumbotron").css("background-position","center "+-.2*a+"px"),console.log(jumboHeight-a)}$(window).scroll((function(a){parallax()}));