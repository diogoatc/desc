titulo=localStorage.getItem("categoria");
//Call all ads from the category
function showads(){
$.ajax({
    url: 'http://descontao.herokuapp.com/api/list',
    dataType: 'json',
    data: {"categoria":titulo}, 
    success: function(dados){
        var html = '';
        for(var key in dados){
            html += '<div class="flip-box flip-up col-xs-10 col-ms-10 col-md-10 col-lg-10 flipbox-size">';
            html += '<div class="object">';
            html += '<div class="front"><img class="responsiva" alt="imagem" src="http://descontao.herokuapp.com/static/img/'+dados[key].imagem +'" /> </div>'; //using the adress of server only in app version
            html += '<div class="back"><p class="p-id"> TEXTO: '+dados[key].texto + '</p></div>';
            html += '<div class="flank"></div>';
            html += "</div>";
            html += "</div>";

           
        }
        $('#title').append(titulo)
        $('.content').append(html);
      }
  });
}

//Call and populate categories list
function populate(){
$.ajax({
	type: "POST",
    url: 'http://descontao.herokuapp.com/api/categorias',
    dataType: 'json',
    success: function(data){
        var html = '';

        for(var key in data){
        	var cat = "\'categoria\'";
        	var nome = "\'"+data[key].nome+"\'";
            html += '<a href="/categoria.html" id="cat" onclick="localStorage.setItem('+cat+','+nome+')">'+data[key].nome + '</a>';
        }
    return($('.cats').append(html));
      }
  });
}
function homeads(){
    $.ajax({
    url: 'http://descontao.herokuapp.com/api/home',
    dataType: 'json',
    data: {"tipo":"1"},
    success: function(dados){
        var html = '';

        for(var key in dados){
           html += '<div class="flip-box flip-up col-xs-10 col-ms-10 col-md-10 col-lg-10 flipbox-size">';
            html += '<div class="object">';
            html += '<div class="front"><img class="responsiva" alt="imagem" src="http://descontao.herokuapp.com/static/img/'+dados[key].imagem +'" /> </div>'; //using the adress of server only in app version
            html += '<div class="back"><p class="p-id"> TEXTO: '+dados[key].texto + '</p></div>';
            html += '<div class="flank"></div>';
            html += "</div>";
            html += "</div>";
        }
        $('.gold').append(html);
      }
  });
  $.ajax({
    url: 'http://descontao.herokuapp.com/api/home',
    dataType: 'json',
    data: {"tipo":"2"},
    success: function(dados){
      var html = '';

      for(var key in dados){
        html += '<div class="flip-box flip-up col-xs-10 col-ms-10 col-md-10 col-lg-10 flipbox-size">';
            html += '<div class="object">';
            html += '<div class="front"><img class="responsiva" alt="imagem" src="http://descontao.herokuapp.com/static/img/'+dados[key].imagem +'" /> </div>'; //using the adress of server only in app version
            html += '<div class="back"><p class="p-id"> TEXTO: '+dados[key].texto + '</p></div>';
            html += '<div class="flank"></div>';
            html += "</div>";
            html += "</div>";
      }
      $('.silver').append(html);
      }
  });
}