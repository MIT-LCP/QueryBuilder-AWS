$(document).ready(function(){
  tab_list = ['q_home']
	
    $("#Export").click(function(){
    $("#loading").show();

    x = document.getElementById("query").value;
    if(x != null){
      $.ajax({
        url : "/download_random_query",
        type : "POST", 
        data : {Query : x}, 
        success : function(File) {

	  $("#loading").hide();
	  var NewFile = new Blob([File], {type: "text/csv;charset='utf-8'"});
          saveAs(NewFile, "Result.csv");

	}
      });
    }
  });

  $("#Execute").click(function(){

    $('#result-content').html('');
    $('#result-content2').html('');
    $('#result-error').html('');	
    x = document.getElementById("query").value;
    $("#loading").show();

    if(x != null){
      var query = $.ajax({
        url : "/random_query",
        type : "POST", 
        data : {Query : x}, 
        success : function(response) {
          $("#loading").hide();
	  Content = response['result'];
          if (Content.length > 2){
            result  = Content[0];
            content2 = Content[1];
            write = Content[2];
            $('#result-content').html(result);
            $('#result-content2').html(content2);
            $('#result-error').html('');
          }
          else{
            Error_Query = Content[0];
            $('#result-error').html(Error_Query);
            $('#result-content').html('');
            $('#result-content2').html('');
          }
        }
      });
    }
  });
});

function Get_File(filename, TabName){
  $.ajax({
    url : "get_file",
     type : "POST", 
     data : { Filename : filename }, 
     success : function(File) {        
      if ( $.inArray(TabName, tab_list) == -1 ) {
        $("#page-content-wrapper").append(File);
        tab_list.push(TabName);
        $('#TabManager').append("<li id='LI_"+TabName+"' class='nav-item'><a class='nav-link' data-toggle='tab' href='#"+TabName+"'>"+TabName+"  <i class='far fa-times-circle' onclick='Remove_Tab(\""+TabName+ "\", event);' aria-hidden='true'></i></a></li>");
      }
    }
  });
}

function eventFire(el, etype){
  if (el.fireEvent) {
    el.fireEvent('on' + etype);
  } else {
    var evObj = document.createEvent('Events');
    evObj.initEvent(etype, true, false);
    el.dispatchEvent(evObj);
  }
}

function Remove_Tab(ID, event){

  var index = tab_list.indexOf(ID);

  if (index > -1) {
     tab_list.splice(index, 1);
  }
  document.getElementById("LI_"+ID).remove();
  document.getElementById(ID).remove();
  eventFire(document.getElementById('Query_tab'), 'click');
  $('#q_home').addClass(' active');
  if ( !document.getElementById("q_home").classList.contains('active') ){
    document.getElementById("q_home").classList.add('active');
  }

  event.stopPropagation();
}
