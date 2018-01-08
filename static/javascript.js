window.onload = function() {
  $("#submitb>input").click(function(){
    setTimeout(()=>{
      $('#loading').show();
    }, 500);
  });
}
