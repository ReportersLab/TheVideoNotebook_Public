
//time we should seek before a note before playing the video.
NOTE_SEEK_BEFORE_TIME = 30;

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
        initialize: function(){
            this.player = null;  
        },
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
            //console.log("New Video Time: " + this.videoTime);
            app.notesView.showNoteAtTime(this.videoTime);
            
       },
       
       seekToNote: function(note, exact){
            var seconds = note.get('offset');
            //subtract some time so that we're slightly before the note
            if(!exact)
                seconds = seconds - NOTE_SEEK_BEFORE_TIME;
            
            if(this.model.get('type') == 'youtube'){
                if(this.player == null){
                    $.later(500, this, 'seekToNote', [note, exact], false);
                    return;
                }
                if(seconds < 0) seconds = 0; // if pre-event, just go to beginning.
                if(seconds > this.player.getDuration()) return; //need graceful way to indicate note is after video ends.
                this.seekToOffset(seconds);
            }
       },
       
       seekToOffset: function(offset){
            this.player.seekTo(offset, true);
            this.player.playVideo();
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
       }
    });
    
    
    
    
    window.NotesView = Backbone.View.extend({
       initialize: function(){
            this.app = this.options.app;
            this.notes = this.options.notes;
            this.autoScroll = true;
            this.autoHighlight = true;
            //then load the notes
            this.notes.bind('add', this.addNote, this);
            this.notes.bind('reset', this.refreshNotes, this);
            this.notes.bind('all', this.render, this);
            //bootstrap the notes
            this.notes.reset(NOTES_DATA);
            
            this.notesSearch = new NoteSearchView({el: $('#note_search'), app:this.app, notesView:this, notes:this.notes });
       },
       
       events: {
            'click #auto_scroll': 'toggleAutoScroll'
       },
       
       render: function(){
            return this;
       },
       
       addNote: function(note){
            var view = new NoteView({model:note, id:'note_'+ note.id, container:this});
            $("#notes").append(view.render().el);
            note.view = view;
        },
        
        refreshNotes: function(){
            this.notes.each(this.addNote, this);
        },
       
       
       toggleAutoScroll: function(){
            //console.log("Scrolling: " + this.autoScroll);
            if(this.autoScroll){
                this.autoScroll = false;
                $("#auto_scroll").html("<span>Enable Auto-Scroll</span>");
            }else{
                this.autoScroll = true;
                $("#auto_scroll").html("<span>Disable Auto-Scroll</span>");
            }
       },
       
       scrollToTop: function(){
            $("#notes").scrollTo("0", 200);
        },
        
        scrollToNote: function(note){
            if((this.autoScroll == false) || (!$(note.view.el).is(":visible")))
                return;
            $("#notes").scrollTo($(note.view.el), 200, {offset:{top:-70}});
        },
        
        showNote: function(note){
            this.selectNote(note);
            this.scrollToNote(note);
            this.autoHighlight = false;
            this.app.videoView.seekToNote(note, false);
        },
        
        
        showNoteById: function(noteId){
            note = this.notes.get(noteId);
            this.showNote(note);
       },
       
        selectNote: function(new_note){
            //not sure if in a search situation we should change highlighting if new-note is invisible?
            if((this.autoHighlight == false) || (!$(new_note.view.el).is(":visible")))
                return;
            
             if(this.selectedNote)
                this.selectedNote.view.removeNoteHighlight();
             this.selectedNote = new_note;
             this.selectedNote.view.highlightNote();
        },
       
        
        showNoteAtTime: function(time){
            //first, find the note we're looking for
            new_note = this.notes.find(function(note){
                return note.get('offset') > time;
            }, this);
            
            //if the user has jumped ahead manually, we want to give them time to watch video
            //before moving, so we set the autoHighlight property to false.
            if( (this.selectedNote != null) && (new_note.get('offset') < this.selectedNote.get('offset')) && (this.autoHighlight == false) )
                return;
            
            if(this.selectedNote == new_note)
                return
            else{
                this.autoHighlight = true;
                this.selectNote(new_note);
            }
            
            //then get a note a few before, that's where we're going to scroll.
            //var index = this.notes.indexOf(this.selectedNote)-2;
            //if(index < 0) index = 0;
            //if(index > this.notes.length - 1) index = this.notes.length - 1; //not possible. I think.
            //var top_note = this.notes.at(index);
            //scroll to the note.
            this.scrollToNote(this.selectedNote);
            
       }
       
    });
    
    
    
    
    window.NoteSearchView = Backbone.View.extend({
        initialize: function(){
            this.app = this.options.app;
            this.notesView = this.options.notesView;
            this.notes = this.options.notes;
            this.render();
        },
        events: {
            'click #note_search_button': 'onSearchPress',
            'keyup #note_search_text': 'onSearchKeyUp',
            'blur #note_search_text': 'onSearchBlur'
        },
        
        render: function(){
            if(this.resultCount == null)
                this.resultCount = this.app.notes.length;
            var html = "<span>" + this.resultCount + " results</span>";
            $("#search_results_count").html(html);
            this.notesView.scrollToTop();
            return this;
        },
        
        onSearchPress: function(){
            this.search();
        },
        
        onSearchKeyUp: function(element){
            text = $("#note_search_text").val();
            if(text.length > 2)
                this.search();
            if(text.length == 0)
                this.resetNotes();
        },
        
        onSearchBlur: function(){
            this.app.router.navigate("search/" + searchText);
        },
        
        makeSearch: function(searchText){
          $("#note_search_text").val(searchText);
          this.search();
        },
        
        search: function(){
            searchText = $("#note_search_text").val();
            //this.notes = app.notes;
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
            this.render();
        },
        
        resetNotes: function(){
            this.notes.each(function(note){
               _.defer(function(){$(note.view.el).show()}); 
            });
            this.resultCount = app.notes.length;
            this.render();
        }
        
        
        
    })
    
    window.NoteView = Backbone.View.extend({
       tagName: 'div',
       className: 'note',
       template: _.template($("#noteTemplate").html()),
       
       initialize: function(){
            //this.model.set({'time_formatted': this.model.get('time').format("mm/dd/yy h:MM:ss TT")});
            this.container = this.options.container;
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
            this.container.selectNote(this.model);
            this.container.scrollToNote(this.model);
            this.container.autoHighlight = false;
            //this.container.autoScroll = false;
            app.videoView.seekToNote(this.model, false);
            //save history
            app.router.navigate("note/" + this.model.id);
       },
       
       
       
       highlightNote: function(){
            $(this.el).addClass('highlighted');
       },
       
       removeNoteHighlight: function(){
            $(this.el).removeClass('highlighted');
       }
       
       
    });
    
    window.MainRouter = Backbone.Router.extend({
        
        initialize: function(options){
            this.app = options.app; // um, no options?
        },
        
        routes: {
            'offset/:offset': 'videoOffset',
            'note/:noteId': 'note',
            'takeNotes': 'takeNotes',
            'notes': 'showNotes',
            'search/:search' : 'search'
        },
        
        videoOffset: function(offset){
            this.app.videoView.seekToOffset(offset);
        },
        
        note: function(noteId){
            this.app.notesView.showNoteById(noteId);  
        },
        
        search: function(search){
            this.app.notesView.notesSearch.makeSearch(search);
        },
        
        takeNotes: function(){
            //TODO: Show Note Taking Panel.
        },
        
        showNotes: function(){
            //TODO: Show Note Panel.
        }
        
    })
    
    
    
    
    window.App = Backbone.View.extend({
        
        el: $("app"),
        
        events: {
            
        },
        
        initialize: function(){
            //first bootstrap the video data.
            this.video = new Video(VIDEO_DATA);
            //and add it to the view
            this.videoView = new VideoView({model:this.video});
            $("#video").append(this.videoView.render().el);
            
            
            this.notes = new Notes();
            
            //Add search view
            this.notesView = new NotesView({el: $('#notes_container'), app:this, notes:this.notes });
            
            this.router = new MainRouter({app:this});
            Backbone.history.start();
        }
        
    })
    
    
    window.app = new App();
    
});






