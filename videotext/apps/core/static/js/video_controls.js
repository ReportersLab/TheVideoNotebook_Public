//backbone to tastypie override
var oldSync = Backbone.sync;
 
Backbone.sync = function(method, model, options){
    success = options['success'];
    error = options['error'];
    var newSuccess = function(resp, status, xhr){
        if(xhr.statusText === "success"){
            var location = xhr.getResponseHeader('Location');
            
            return $.ajax({
                       url: location,
                       success: success
                   });
        }
        return success(resp);
    };
    return oldSync(method, model, {success: newSuccess, error: error});
};

//found: http://stackoverflow.com/questions/1353684/detecting-an-invalid-date-date-instance-in-javascript
function isValidDate(d) {
  if ( Object.prototype.toString.call(d) !== "[object Date]" )
    return false;
  return !isNaN(d.getTime());
}


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
            this.videoTime = 0;
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
            var url = "http://www.youtube.com/v/" + this.model.get('video_url') + "?version=3&enablejsapi=1&feature=player_embedded"; 
            swfobject.embedSWF( url, "player_container", "540", "350", "8", null, null, params, attrs);
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
       
       pauseVideo: function(){
            if(this.player != null)
                this.player.pauseVideo();
       },
       
       playVideo: function(){
            if(this.player != null)
                this.player.playVideo();
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
            type: "note",
            source:"tv",
            source_link: PATH,
            offset: -1
          }
        },
        
        initialize: function(){
            //make a real JS date out of the date string we got in JSON.
            //now done in the view, because this fails on newly added notes.
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
            this.addingNotes = false;
            this.autoHighlight = true;
            //then load the notes
            this.notes.bind('add', this.addNote, this);
            this.notes.bind('reset', this.refreshNotes, this);
            this.notes.bind('all', this.render, this);
            //bootstrap the notes
            this.notes.reset(NOTES_DATA);
            
            this.notesSearch = new NoteSearchView({el: $('#note_search'), app:this.app, notesView:this, notes:this.notes });
            this.addNoteView = new AddNoteView({el: $('#add_note_container'), notesView: this, notes: this.notes });
       },
       
       events: {
            'click #auto_scroll': 'toggleAutoScroll',
            'click .add_note_link': 'toggleAddNotes'
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
            $("#notes").html('');
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
       
       toggleAddNotes: function(){
            if(this.addingNotes){
                this.addingNotes = false;
                $("#add_note_link").html("<span>Add Notes</span>");
                $(this.addNoteView.el).slideUp(1000);
                this.refreshNotes();
            }else{
                this.addingNotes = true;
                $("#add_note_link").html("<span>View notes</span>");
                $(this.addNoteView.el).slideDown(1000);
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
            
            //if no new note, we've reached the end of notes, so just return.
            if(new_note === undefined)
                return;
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
            if(this.searchText)
                this.app.router.navigate("search/" + this.searchText);
        },
        
        makeSearch: function(searchText){
          $("#note_search_text").val(searchText);
          this.search();
        },
        
        search: function(){
            this.searchText = $("#note_search_text").val();
            //this.notes = app.notes;
            //search the notes collection for matches.
            
            toHide = this.notes.select(function(note){
                return note.get('text').toLowerCase().indexOf(this.searchText.toLowerCase()) == -1
            }, this);
             
            toShow = this.notes.select(function(note){
                return note.get('text').toLowerCase().indexOf(this.searchText.toLowerCase()) != -1
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
            this.model.set({date_time: new Date(this.model.get('time')) });
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
       },
       
       onNoteClicked: function(event){
            //console.log(this.model.get('id'));
            this.container.autoHighlight = true;
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
    
    
    
    window.AddNoteView = Backbone.View.extend({
       tagName: 'div',
       className: 'add_note',
       id:'add_note_container',
       template: _.template($("#addNoteTemplate").html()),
       
       initialize: function(){
            this.notes = this.options.notes;
       },
       
       events: {
            'click #new_note_submit': 'onNoteAdd',
            'keyup #new_note_text': 'onNoteKeyUp'
       },
       
       render: function(){
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
       },
       
       onNoteKeyUp: function(event){
            if($("#new_note_text").val().length > 0){
                app.videoView.pauseVideo();
            }else{
                app.videoView.playVideo();
            }
            if(event.keyCode == 13){ //the 'enter' key
                this.addNote();
            }
       },
       
       onNoteAdd: function(){
            this.addNote();
       },
       
       addNote: function(){
            text = $("#new_note_text").val();
            private_note = $("#new_note_private").val();
            if(text.length < 10){
                //too short? Do nothing. Should we send a warning?
                return;
            }
            
            var status = $("#add_note_status");
            status.html("<span>Saving Note...</span>")
            status.show();
            
            this.notes.create({
                    text: text,
                    offset: app.videoView.videoTime,
                    private_note: !private_note
                }, {
                    success: function(){
                        status.html("<span>Note Saved</span>");
                        status.effect("pulsate", {times:3, mode:"hide"}, 500);
                    }
                    });
            
            $("#new_note_text").val(''); //empties the note to start over.
            app.videoView.playVideo();
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






