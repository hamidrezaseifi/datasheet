

function getCookie(name) {
		 var cookieValue = null;
		 if (document.cookie && document.cookie != '') {
			 var cookies = document.cookie.split(';');
			 for (var i = 0; i < cookies.length; i++) {
				 var cookie = jQuery.trim(cookies[i]);
				  //Does this cookie string begin with the name we want?
				 if (cookie.substring(0, name.length + 1) == (name + '=')) {
					 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					 break;
				 }
			 }
		 }
		 return cookieValue;
	 }

function deleteItem(deleteUrl, pk, itemName){

    $("#idToDelete").val(pk);
    $("#urlToDelete").val(deleteUrl);

    $("#deleteModelBody").text("Möchten Sie diesen Artikel (" + itemName + ":" + pk + ") wirklich löschen?");
    $("#deleteModel").modal();

    /*if (confirm("Möchten Sie diesen Artikel (" + itemName + ":" + pk + ") wirklich löschen?") == false) {
      return;
    }

    $.post(deleteUrl, {key: pk, csrfmiddlewaretoken: getCookie('csrftoken')},
    function(data, status){
        alert("Das Artikel (" + itemName + ":" + pk + ") ist gelöscht.");
        location.replace(location.pathname);
    }).fail(function(data) {
    alert("Error in in delete: " + JSON.stringify(data.responseText));
  });*/
}

function doDeleteItem(){

    var pk = $("#idToDelete").val();
    var deleteUrl = $("#urlToDelete").val();
    var itemName = $("#nameToDelete").val();

    $.post(deleteUrl, {key: pk, csrfmiddlewaretoken: getCookie('csrftoken')},
    function(data, status){

        location.replace(location.pathname);
    }).fail(function(data) {
    alert("Error in in delete: " + JSON.stringify(data.responseText));
  })
}


function closeDeleteModal(){

    $("#deleteModel").modal("hide");

}
