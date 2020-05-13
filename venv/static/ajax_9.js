

$(document).ready(function() {
	
	$("#txt").change(function(){
		var x = $(this).val().length;
		var demande = $(this).val()
		var re = new RegExp("[^0-9][a-zA-Z][^0-9]","g");
		var reghex = new RegExp("<.*?>","g");
		var resultat = re.exec(demande)
		var result = reghex.exec(demande)
		console.log(result)
		
		if (x!=0){
			$("#error").empty().removeClass("error");
			if(x==0){
				$("#error").append("Ne laissez pas ce champ vide !").addClass("error");
			}else{
				$("#error").append("Il faut détailler un peu plus la demande").addClass("error");
			}
		}

		if (!resultat){
			$("#error").empty().removeClass("error");
			$("#error").append("Cette demande n'est pas valide !").addClass("error");
		}
		if (result){
			$("#error").empty().removeClass("error");
			$("#error").append("Ceci ressemble à un Hack !").addClass("error");
		}
		});

	$('form').on('submit', function(event) {
		var demande = $("#txt").val()
		//var x = $("#txt").val().length;
		var re = new RegExp("[a-zA-Z]","i");
		var reghex = new RegExp("<.*?>","g");
		var resultat = re.exec(demande)
		var result = reghex.exec(demande)
		$("#error").empty().removeClass("error");

		if((resultat) && (!result)) {
			$.ajax({
				url : '/search_api',
				data : {
					demande : $('#txt').val()
				},
				type : 'POST',
				success: function(response){console.log(response);}
			})
			.done(function(data) {
				var chaine = JSON.parse(data);
				var demande = chaine.resultat;
				var url_google = chaine.url_google;
				var localisation = chaine.localisation;
				var wiki = chaine.wiki;
				
				$('#txt').val("");
				if(demande.lenght != 0){
					$('#historique').append(demande);	
				}

				if (localisation.lenght != 0){
					$('#historique').append(localisation);	
				}
				if (jQuery.type(url_google[0]) != "object"){
					var obj = jQuery.parseJSON(url_google);
					$('#historique').append("<li class='list-group-item list-group-item-success' class='map' style='height:400px;'></li>")
					$('.corps').each(function(){
						var x = 0;
						$(this).find('li').each(function(){
							x++;
						});
					});
					mapInit = "map" + x;
					$("li").last().attr("id",mapInit)
					map = new google.maps.Map(document.getElementById(mapInit), {
						center: new google.maps.LatLng(obj.position0.lat, obj.position0.lng),
						zoom: 11,
						mapTypeId: google.maps.MapTypeId.ROADMAP,
						mapTypeControl: true,
						scrollwheel: false,
						mapTypeControlOptions: {
							style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR
						},
						navigationControl: true,
						navigationControlOptions: {
							style: google.maps.NavigationControlStyle.ZOOM_PAN
						}
					});
					$.each(JSON.parse(url_google), function(i,localisation){
						console.log(localisation)
						var marker = new google.maps.Marker({
							position: new google.maps.LatLng(localisation.lat,localisation.lng),
							map: map
						});	
					});
					
				}

				if(wiki.lenght != 0){
					$('#historique').append(wiki);	
				}	
		
			});
			event.preventDefault();	
		}else{
			$("#error").append("Cette demande est incorrect !").addClass("error");
		
	}
});

});