
//time we should seek before a note before playing the video.
NOTE_SEEK_BEFORE_TIME = 10;

PLAYER_STATES = {
    '-1':'unstarted',
    '0': 'ended',
    '1': 'playing',
    '2': 'paused',
    '3': 'buffering',
    '5': 'cued'
}


/**
 * YouTube API requires you to put things on the global level.
 * There also isn't an event fired while the video is playing. You get notified
 * when the video starts being played or paused or whatever, but not periodically
 * while playing. So, to get where it is, you have to set up a timer and check
 * periodically.
 *
 * ref: http://code.google.com/apis/youtube/js_api_reference.html
 * 
 **/

function onYouTubePlayerReady(playerId){
    app.videoView.player = document.getElementById("player");
    app.videoView.player.addEventListener("onStateChange", "onYouTubeStateChange");
    app.videoView.addYouTubeVideoEvents();
}

function onYouTubeStateChange(newState)
{
    app.videoView.videoState = newState;
    //if it's not playing, stop our timer
    if(newState != 1){
        app.videoView.videoStatusChecker.cancel();
    //otherwise, check away.
    }else{
        app.videoView.addYouTubeVideoEvents();
    }
    //Not sure if we'll be doing anything else.
}




$(function(){
    
    
    window.Video = Backbone.Model.extend({
        url: VIDEO_API + VIDEO_ID + "/",
        initialize: function(){
            //make a real JS date out of the date string we got in JSON.
            this.set({date_time: new Date(this.get('time')) });
            if(this.get('end_time')){
                this.set({end_date_time: new Date(this.get('end_time'))});
            }
        }
    })
    
    window.VideoView = Backbone.View.extend({
        tagName: 'div',
        className: 'video',
        template: _.template($("#videoTemplate").html()),
        render: function(){
            $(this.el).html(this.template(this.model.toJSON()));
            
            if(this.model.get('type') == "youtube"){
                //doing this immediately caused trouble.
                //using this: http://sudarmuthu.com/blog/jquery-later-a-settimeout-wrapper-in-jquery
                //time-to-execution, context, function, parameters, recur
                //NOTE: Didn't know about _.defer or _.delay
                $.later(100, this, 'embedYouTube', [], false);
            }
            return this;
       },
       
       embedYouTube: function(){
            var params = { allowScriptAccess: "always" };
            var attrs  = { id: "player" };
            swfobject.embedSWF( this.model.get('video_url') , "player_container", "540", "350", "8", null, null, params, attrs);
            //video loaded, onYouTubePlayeReady(id) is called when video loaded,
            //then 'this.player' available and 'addYouTubeVideoEvents' called
       },
       
       addYouTubeVideoEvents: function(){
            this.videoStatusChecker = $.later(1000, this, 'checkYouTubeStatus', [], true);
       },
       
       checkYouTubeStatus: function(){
            this.videoTime = this.player.getCurrentTime(); //seconds into video.
            //update the notes scrolling.
            console.log("New Video Time: " + this.videoTime);
            app.notes.showNoteAtTime(this.videoTime);
            
       },
       
       seekToNote: function(note, exact){
            var seconds = note.get('offset');
            //subtract some time so that we're slightly before the note
            if(!exact)
                seconds = seconds - NOTE_SEEK_BEFORE_TIME;
            
            if(this.model.get('type') == 'youtube'){
                if(seconds < 0) seconds = 0; // if pre-event, just go to beginning.
                if(seconds > this.player.getDuration()) return; //need graceful way to indicate note is after video ends.
                this.player.seekTo(seconds, true); //time, allow-seek-ahead
                this.player.playVideo();
            }
       }
       
       
       
       
    })
    
    
    
    
    window.Note = Backbone.Model.extend({
       
        defaults: function(){
          return {
            text: "",
            video: VIDEO_ID,
            link: "LINK_TO_SELF_GOES_HERE",
            user: "USER_ID_GOES_HERE",
            type: "note",
            source:"us",
            source_link: "LINK_TO_VIDEO_GOES_HERE"
          }
        },
        
        initialize: function(){
            //make a real JS date out of the date string we got in JSON.
            this.set({date_time: new Date(this.get('time')) });
        },
        
        url: function(){
            return this.get('resource_uri') || this.collection.url;
        }
        
    });
    
    
    window.Notes = Backbone.Collection.extend({
       model: Note,
       url: NOTE_API,
       parse: function(data){
            return data.objects;
       },
       comparator: function(note){
            return parseInt(note.get('offset'));
       },
       
       selectNote: function(new_note){
            if(this.selected_note)
               this.selected_note.view.removeNoteHighlight();
            this.selected_note = new_note;
            this.selected_note.view.highlightNote();
       },
       
       showNoteAtTime: function(time){
            //remove highlight from selected note if it exists.
            
                
            //first, find the note we're looking for
            new_note = this.find(function(note){
                return note.get('offset') > time;
            }, this);
            
            if(this.selected_note == new_note)
                return
            else{
                this.selectNote(new_note);
            }
            
            //then get a note a few before, that's where we're going to scroll.
            var index = this.indexOf(this.selected_note)-2;
            if(index < 0) index = 0;
            if(index > this.length - 1) index = this.length - 1; //not possible. I think.
            var top_note = this.at(index);
            //scroll to the note.
            top_note.view.scrollToNote();
            
       }
       
    });
    
    
    
    window.NoteSearchView = Backbone.View.extend({
        initialize: function(){
            this.app = this.options.app;
            this.render();
        },
        events: {
            'click #note_search_button': 'searchPress',
            'keyup #note_search_text': 'searchKeyUp'
        },
        
        render: function(){
            if(this.resultCount == null)
                this.resultCount = this.app.notes.length;
            var html = "<span>" + this.resultCount + " results</span>";
            $("#search_results_count").html(html);
            this.scrollToTop();
            return this;
        },
        
        searchPress: function(){
            this.search();
        },
        
        searchKeyUp: function(element){
            text = $("#note_search_text").val();
            if(text.length > 2)
                this.search();
            if(text.length == 0)
                this.resetNotes();
        },
        
        search: function(){
            searchText = $("#note_search_text").val();
            this.notes = app.notes;
            //search the notes collection for matches.
            
            toHide = this.notes.select(function(note){
                return note.get('text').toLowerCase().indexOf(searchText.toLowerCase()) == -1
            }, this);
             
            toShow = this.notes.select(function(note){
                return note.get('text').toLowerCase().indexOf(searchText.toLowerCase()) != -1
            }, this);
            
            
            _.each(toHide, function(note){
               $(note.view.el).hide(); 
            });
            
            _.each(toShow, function(note){
               $(note.view.el).show(); 
            });
            
            this.resultCount = toShow.length || 0;
            console.log(this.resultCount);
            this.render();
        },
        
        resetNotes: function(){
            this.notes.each(function(note){
               _.defer(function(){$(note.view.el).show()}); 
            });
            this.resultCount = app.notes.length;
            this.render();
        },
        
        scrollToTop: function(){
            $("#notes").scrollTo("0", 200);
        }
        
    })
    
    window.NoteView = Backbone.View.extend({
       tagName: 'div',
       className: 'note',
       template: _.template($("#noteTemplate").html()),
       
       initialize: function(){
            //this.model.set({'time_formatted': this.model.get('time').format("mm/dd/yy h:MM:ss TT")});
       },
       
       events: {
            'click .note_text': 'onNoteClicked'
       },
       
       render: function(){
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
       },
       
       onNoteClicked: function(event){
            //console.log(this.model.get('id'));
            this.model.collection.selectNote(this.model);
            app.videoView.seekToNote(this.model, true);
       },
       
       scrollToNote: function(){
            $("#notes").scrollTo($(this.el), 200);
       },
       
       highlightNote: function(){
            $(this.el).addClass('highlighted');
       },
       
       removeNoteHighlight: function(){
            $(this.el).removeClass('highlighted');
       }
       
       
    });
    
    
    
    
    window.App = Backbone.View.extend({
        
        el: $("app"),
        
        events: {
            
        },
        
        initialize: function(){
            _.bindAll(this, 'refreshNotes');
            //first bootstrap the video data.
            this.video = new Video(VIDEO_DATA);
            //and add it to the view
            this.videoView = new VideoView({model:this.video});
            $("#video").append(this.videoView.render().el);
            
            //then load the notes
            this.notes = new Notes();
            this.notes.bind('add', this.addNote);
            this.notes.bind('reset', this.refreshNotes);
            this.notes.bind('all', this.render);
            //bootstrap the notes
            this.notes.reset(NOTES_DATA)
            
            //Add search view
            this.notesSearch = new NoteSearchView({el: $('#notes_search'), app:this});
        },
        
        addNote: function(note){
            var view = new NoteView({model:note, id:'note_'+ note.id});
            $("#notes").append(view.render().el);
            note.view = view;
        },
        
        refreshNotes: function(){
            this.notes.each(this.addNote);
        }
        
        
    })
    
    
    window.app = new App();
    
});






