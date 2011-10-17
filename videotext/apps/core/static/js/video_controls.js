player = null;

function embed_youtube(url)
{
    var params = { allowScriptAccess: "always" };
    var attrs  = { id: "player" };
    swfobject.embedSWF( url , "player_container", "640", "390", "8", null, null, params, attrs);
}

function onYouTubePlayerReady(playerId){
    player = document.getElementById("player");
}

