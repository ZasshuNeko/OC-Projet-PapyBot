

$(document).ready(function() {

	$('form').on('submit', function(event) {
		var demande = $("#txt").val();
		var reghex = new RegExp("<.*?>","g");
		var result = reghex.exec(demande);
		var demande_util = demande.replace(/(.[^<]*>|[<>][<\/])/gm,"");
		var demande_util = demande.replace(/[^0-9]/gm,"");
		$.ajax({
			url : '/search_api',
			data : {
				demande : demande_util //$('#txt').val()
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
			var num = 0;

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
				$('#historique').each(function(){
					$(this).find('li').each(function(){
						num++;
					});
				});
				mapInit = "map" + num;
				$("li").last().attr("id",mapInit)
				map = new google.maps.Map(document.getElementById(mapInit), {
					center: new google.maps.LatLng(obj.position0.lat, obj.position0.lng),
					zoom: 8,
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

	});

});