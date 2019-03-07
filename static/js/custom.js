  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-87592301-2', 'auto');
  ga('send', 'pageview');

function addTab(evt, TabName) {//TAB_Content
    var oInput = document.getElementById('TabManager'),oChild;
    for(i = 0; i < oInput.childNodes.length; i++){
        oInput.childNodes[i].className = "";
    }
  document.getElementById(TabName.toLowerCase()).style.display = 'block';
  document.getElementById(TabName.toLowerCase()).className = 'active';
  document.getElementById('Query_tab1').className = '';

    var coInput = document.getElementById('TAB_Content'),oChild;
    for(i = 0; i < coInput.childNodes.length; i++){
        coInput.childNodes[i].className = 'tab-pane fade';
    }
  document.getElementById(TabName.toUpperCase()).className = 'tab-pane fade in active';
//
}

function Remove_Tab(ID, event){
  $('#'+ID.toLowerCase()).removeClass('active');
  $('#'+ID.toLowerCase()).hide();
  $('#'+ID.toUpperCase()).removeClass('in');
  $('#'+ID.toUpperCase()).removeClass('active');
  var oInput = document.getElementById('TabManager'),oChild;
  for(i = 0; i < oInput.childNodes.length; i++){
      oInput.childNodes[i].className = "";
  }
  var coInput = document.getElementById('TAB_Content'),oChild;
  for(i = 0; i < coInput.childNodes.length; i++){
      coInput.childNodes[i].className = 'tab-pane fade';
  }
  $('#Query_tab1').addClass('active');
  $('#QUERY_TAB').addClass('in active');
  event.stopPropagation();
}
