



//time we should seek before a note before playing the video.
//this is probably a matter of personal preference, so maybe we want to make it user adjustable.
NOTE_SEEK_BEFORE_TIME = 7;

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
    app.videoView.addVideoEvents();
}

function onYouTubeStateChange(newState)
{
    app.videoView.videoState = newState;
    //if it's not playing, stop our timer
    if(newState != 1){
        if(app.videoView.videoStatusChecker)
            app.videoView.videoStatusChecker.cancel();
    //otherwise, check away.
    }else{
        app.videoView.addVideoEvents();
    }
    //Not sure if we'll be doing anything else.
}




$(function(){
    
    
    
    
    window.VideoView = Backbone.View.extend({
        tagName: 'div',
        className: 'video',
        template: _.template($("#videoTemplate").html()),
        events: {
            'click #sync_notes_link': 'onSyncNotesClick'
        },
        initialize: function(){
            this.player = null;
            this.syncingNotes = false;
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
            }else{
                $.later(100, this, 'embedVideoJS', [], false);
            }
            //if the logged in user is the owner of this video, let them edit the content.
            if (this.model.get("user") && parseInt(this.model.get('user').id, 10) == LOGGED_IN_USER){
                var self = this;
                $(this.el).find('.edit').editable(function(value, settings){
                    var data = {};
                    data[this.id.split('_')[1]] = value;
                    self.model.set(data);
                    app.showMessage("<h4>Updating Video Details</h4>");
                    self.model.save(null, {wait:true, success:function(model, response){app.showMessage("<h4>Video Details Updated!</h4>")}});
                    return value;
                },
                {
                    type: 'textarea',
                    cancel: 'Cancel',
                    submit: 'Submit',
                    select: true,
                    tooltip: 'Click to edit...',
                    onblur: 'submit'
                });
            }
            
            return this;
       },
       
       embedYouTube: function(){
            var params = { allowScriptAccess: "always" };
            var attrs  = { id: "player" };
            var url = "http://www.youtube.com/v/" + this.model.get('video_url') + "?version=3&enablejsapi=1&feature=player_embedded"; 
            swfobject.embedSWF( url, "player_container", "550", "350", "8", null, null, params, attrs);
            //video loaded, onYouTubePlayeReady(id) is called when video loaded,
            //then 'this.player' available and 'addYouTubeVideoEvents' called
       },
       
       embedVideoJS: function(){
            var self = this;
            //videojs api to create a video
            _V_("video_tag").ready(function(){
                self.player = this;
                self.addVideoEvents();
            });
       },
       
       addVideoEvents: function(){
            if(this.model.get('type') == "youtube"){
                this.videoStatusChecker = $.later(1000, this, 'checkVideoStatus', [], true);
            }
            if(this.model.get('type') == "mp4"){
                var listener = _.bind(this.checkVideoStatus, this);
                this.player.addEvent("timeupdate", listener);
            }
       },
       
       checkVideoStatus: function(){
            this.videoTime = this.getCurrentOffset(); //seconds into video.
            //update the notes scrolling.
            app.notesView.showNoteAtTime(this.videoTime);
            
       },
       
       pauseVideo: function(){
            if(this.player != null){
                if(this.model.get('type') == "youtube"){
                    this.player.pauseVideo();
                }
                if(this.model.get('type') == "mp4"){
                    this.player.pause();
                }
            }
       },
       
       playVideo: function(){
            if(this.player != null){
                if(this.model.get('type') == "youtube"){
                    this.player.playVideo();
                }
                if(this.model.get('type') == "mp4"){
                    this.player.play();
                }
            }
       },
       
       getCurrentOffset: function(){
            if(this.player != null){
                if(this.model.get('type') == "youtube")
                    this.videoTime = this.player.getCurrentTime();
                if(this.model.get('type') == "mp4")
                    this.videoTime = this.player.currentTime();
            }
            return this.videoTime;
       },
       
       getDuration: function(){
            if(this.player != null){
                if(this.model.get('type') == "youtube")
                    this.videoDuration = this.player.getDuration();
                if(this.model.get('type') == "mp4")
                    this.videoDuration = this.player.duration();
            }
            return this.videoDuration;
       },
       
       awaitDurationChange: function(){
            //remove the duration listener
            this.player.removeEvent("durationchange", this.durationListener);
            this.durationListener = null;
            //and redo our note seek with the last note that attempted seek. Defered because the player isn't aware of duration until next frame.
            _.defer(_.bind(function(){this.seekToNote(this.lastNote, false)}, this));
       },
       
       seekToNote: function(note, exact){
            if(this.syncingNotes)
                return;
            var seconds = note.get('offset');
            this.lastNote = note;
            //subtract some time so that we're slightly before the note
            if(!exact)
                seconds = seconds - NOTE_SEEK_BEFORE_TIME;
            
            if(this.player == null){
                $.later(500, this, 'seekToNote', [note, exact], false);
                return;
            }
            
            var duration = this.getDuration();
            //unfortunately, Flash player doesn't prefetch, so you have to play the video to get things moving, if only for an instant.
            if(duration == 0){
                this.durationListener = _.bind(this.awaitDurationChange, this)
                //once we have an actual duration, this triggers an event.
                this.player.addEvent('durationchange', this.durationListener);
                this.playVideo();
                this.pauseVideo();
            }
            
            
            if(seconds < 0) seconds = 0; // if pre-event, just go to beginning.
            if(seconds > this.getDuration()) return; //need graceful way to indicate note is after video ends.
            this.seekToOffset(seconds);
            
       },
       
       seekToOffset: function(offset){
            if(this.player != null){
                if(this.model.get('type') == "youtube"){
                   this.player.seekTo(offset, true);
                }
                if(this.model.get('type') == "mp4"){
                    this.player.currentTime(offset);
                }
                this.playVideo();
            }
       },
       
       onSyncNotesClick: function(event){
            app.startSyncNotes();
       },
       
       syncNotes: function(note){
            //first get the note's time
            var noteTime = note.get("date_time");
            //and how many seconds earlier the start of the video is
            var offset = this.getCurrentOffset(); 
            //and create a new date based on that.
            var newTime = new Date(noteTime - offset * 1000);
            this.model.set({time: newTime, sync_notes:true});
            var video = this.model;
            this.model.save(null, {
                success: function(model, response){
                    video.set({date_time: new Date(newTime)});
                    app.notes.syncToVideo(video);
                    app.endSyncNotes();     
                },
                error: function(model, response){
                    app.endSyncNotes('There was an error syncing your notes')
                }
            });
       }
       
       
    })
    
  
    
    window.NotesView = Backbone.View.extend({
       initialize: function(){
            this.app = this.options.app;
            this.notes = this.options.notes;
            this.autoScroll = true;
            this.addingNotes = false;
            this.autoHighlight = true;
            this.syncNotes = false;
            //then load the notes
            this.notes.bind('add', this.addNote, this);
            this.notes.bind('reset', this.refreshNotes, this);
            this.notes.bind('all', this.render, this);
            //bootstrap the notes
            this.notes.reset(NOTES_DATA);
            
            this.notesSearch = new NoteSearchView({el: $('#note_search'), app:this.app, notesView:this, notes:this.notes });
            this.addNoteView = new AddNoteView({el: $('#add_note_container'), notesView: this, notes: this.notes });
            this.noteDetailsView = new NoteDetailsView({el:$('#note_details_container'), notesView: this});  
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
       
       showNoteDetails: function(note){
          this.noteDetailsView.note = note;
          this.noteDetailsView.render();
       },
       
       scrollToTop: function(){
            $("#notes").scrollTo("0", 200);
       },
        
       scrollToNote: function(note){
            if(note == undefined)
                return;
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
            //if we're in the "note sync" mode, just tell the app to do the syncing.
            if(this.syncNotes){
                this.app.syncNotes(new_note);
                return;
            }
            
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
            if(text.length > 0)
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
                //if(note.view.visible)
                    $(note.view.el).addClass("hidden");
                note.view.visible = false;
            });
            
            _.each(toShow, function(note){
                //if(!note.view.visible)
                    $(note.view.el).removeClass("hidden");
                note.view.visible = true;
            });
            
            this.resultCount = toShow.length || 0;
            this.render();
        },
        
        resetNotes: function(){
            this.notes.each(function(note){
                //if(!note.view.visible)
                    $(note.view.el).removeClass("hidden");
               //_.defer(function(){$(note.view.el).show()}); 
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
            this.visible = true;
       },
       
       events: {
            'click .note_text': 'onNoteClicked',
            'mouseenter': 'onNoteEnter',
            'mouseleave': 'onNoteLeave',
            'click .show_details_link': 'onDetailsLinkClicked'
       },
       
       render: function(){
            this.model.set({date_time: new Date(this.model.get('time')) });
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
       },
       
       onNoteEnter: function(event){
            var details = $(this.el).find('.details');
            $(this.el).animate({
                height: '+=' + details.height() + 'px'
            }, 100, function() {
                details.fadeIn(100);
            });
       },
       
       onNoteLeave: function(event){
            var details = $(this.el).find('.details');
            var el = this.el;
            details.fadeOut(100, function(){
                $(el).animate({
                    height: '-=' + details.height() + 'px'
                }, 100)    
            });
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
       
       onDetailsLinkClicked: function(event){
            this.container.showNoteDetails(this.model);
       },
       
       highlightNote: function(){
            $(this.el).addClass('highlighted');
       },
       
       removeNoteHighlight: function(){
            $(this.el).removeClass('highlighted');
       }
       
       
    });
    
    
    window.NoteDetailsView = Backbone.View.extend({
        tagName: 'div',
        className: 'noteDetails',
        template: _.template($("#noteDetailsTemplate").html()),
        initialize: function(){
            this.note = this.options.note;
            this.notesView = this.options.notesView;
        },
        
        events: {
            'click .closeLink': 'onCloseClick',
            'click .sync_note_link': 'onSyncNoteClick',
            'click .delete_note_link': 'onDeleteClick'
        },
        
        render: function(){
            $(this.el).html(this.template(this.note.toJSON()));
            $(this.el).slideDown('slow');
            
            //if the logged in user is the owner of this note, let them edit the content.
            //if there is no user for this note (as in, it was imported), the video owner can edit.
            if(    (this.note.get("user") && (this.note.get("user").id == LOGGED_IN_USER.toString()) )  ||
                   ( !this.note.get("user") && app.video.get('user') && (app.video.get('user').id == LOGGED_IN_USER.toString()) )
              ){
                
                var self = this;
                $(this.el).find('.edit').editable(function(value, settings){
                    var data = {};
                    //pattern is note_detail_VAR
                    data[this.id.split('_')[2]] = value;
                    self.note.set(data);
                    app.showMessage("<h4>Updating Note Details</h4>");
                    self.note.save(null, {wait:true, success:function(model, response){app.showMessage("<h4>Note Details Updated!</h4>")}});
                    return value;
                },
                {
                    type: 'textarea',
                    cancel: 'Cancel',
                    submit: 'Submit',
                    select: true,
                    tooltip: 'Click to edit...',
                    onblur: 'submit'
                });
            }
            return this;
        },
        
        onCloseClick: function(event){
            $(this.el).slideUp('slow');
            
        },
        
        onSyncNoteClick: function(event){
            this.note.set({offset: app.videoView.getCurrentOffset(), time:null});
            app.showMessage("<h4>Updating Note...</h4>");
            var self = this;
            this.note.save(null, {
                success: function(){
                    app.showMessage("<h4>Note Saved</h4>");
                    self.notesView.notes.sort();
                },
                failure: function(){
                    app.showMessage("<h4>There was an error saving</h4>");
                }
            });
        },
        
        onDeleteClick: function(event){
            if(confirm("Are you sure you wish to delete this note?")){
                this.notesView.notes.remove(this.note);
                this.note.destroy();
                this.notesView.notes.sort();
                this.onCloseClick();
            }
        }
        
    });
    
    
    window.AddNoteView = Backbone.View.extend({
       tagName: 'div',
       className: 'add_note',
       id:'add_note_container',
       
       initialize: function(){
            this.notes = this.options.notes;
       },
       
       events: {
            'click #new_note_submit': 'onNoteAdd',
            'keyup #new_note_text': 'onNoteKeyUp'
       },
       
       render: function(){
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
            private_note = $("#new_note_private").is(":checked");
            if(text.length < 10){
                //too short? Do nothing. Should we send a warning?
                return;
            }
            
            var status = $("#add_note_status");
            status.html("<span>Saving Note...</span>")
            status.show();
            
            var newNote = this.notes.create({
                    text: text,
                    offset: app.videoView.videoTime,
                    private: private_note
                }, {
                    success: function(model, response){
                        var newNoteTemplate = _.template($("#addNoteTemplate").html());
                        $("#add_note_display").append(newNoteTemplate(model.toJSON()));
                        status.html("<span>Note Saved</span>");
                        status.effect("pulsate", {times:3, mode:"hide"}, 500);
                        $("#add_note_display").animate({ scrollTop: $("#add_note_display").prop("scrollHeight") }, 1000);
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
        
        el: $("#app"),
        
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
        },
        
        startSyncNotes: function(){
            this.notesView.syncNotes = this.videoView.syncingNotes = true;
            this.oldAutoScroll = this.notesView.autoScroll;
            this.notesView.autoScroll = false;
            this.showMessage("<h4>Click on a note to sync the video with imported notes.</h4>");
        },
        
        syncNotes: function(note){
            this.showMessage('<h4>Syncing Notes... (this may take some time if there are a lot of notes)</h4>');
            this.videoView.syncNotes(note);
        },
        
        endSyncNotes: function(message){
            this.notesView.syncNotes = this.videoView.syncingNotes = false;
            this.notesView.autoScroll = this.oldAutoScroll;
            this.videoView.playVideo();
            if(!message){
                this.showMessage('<h4>Notes Synced.</h4>');                
            }else{
                this.showMessage('<h4>' + message + '</h4>');
            }
        },
        
        showMessage: function(message){
            $("#message_container").slideDown('slow', function(){
                $('#message').html(message).effect("pulsate", {times:1, mode:"show"}, 500);
            })
            
        }
        
    })
    
    
    window.app = new App();
    
});






