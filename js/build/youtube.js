var players = {};

function onYouTubeIframeAPIReady() {
    $('.youtube-container').each(function () {
	var id = $(this).find('img').attr('id');
	var player = new YT.Player(id, {
	    height: '390',
	    width: '640',
	    videoId: $(this).data('youtube-id'),
	    events: {
		//'onReady': onPlayerReady,
		//'onStateChange': onPlayerStateChange
	    }
	});

	players[id] = player;
    });
}

function onPlayerReady(event) {
    event.target.playVideo();
}

var done = false;
function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING && !done) {
        setTimeout(stopVideo, 6000);
        done = true;
    }
}
function stopVideo() {
    player.stopVideo();
}


$(document).ready(function() {
    if ($('.youtube-container').length === 0) {
	return;
    }

    var tag = document.createElement('script');

    tag.src = "https://www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    /*
    $('.cycle-slideshow').on('cycle-update-view', function(event, optionHash, slideOptionsHash, currentSlideEl) {
	var id = $(this).attr('id');
	$('.youtube-container').each(function () {
	    if (players.hasOwnProperty(id)) {
		console.log(players[id]);
		players[id].stopVideo();	
	    }
	});
	//players[$(this).attr('id')].playVideo();
    });*/
});
