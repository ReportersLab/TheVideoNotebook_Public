$(document).ready(function(){
    
    
    window.AddNoteView = Backbone.View.extend({
        
    });
    
    window.App = Backbone.View.extend({
        el: $("#app"),
        events: {
            "change input:radio": 'onRadioChange',
            'click #youtube_submit': 'onYouTubeSubmit',
            'keydown #youtube_ID' : 'onYouTubeIDKeyDown'
        },
        
        initialize: function(){
            this.video = new Video();
        },
        
        onRadioChange: function(event){
            $('.add_box').hide();
            $('#' + event.target.id + '_add').show();
        },
        
        onYouTubeIDKeyDown: function(event){
            if(event.keyCode == 13){ //the 'enter' key
                this.getYouTubeDetails();
            }
        },
        
        onYouTubeSubmit: function(){
            this.getYouTubeDetails();
        },
        
        getYouTubeDetails: function(){
            this.video = new Video();
            id = $('#youtube_ID').val();
            this.video.getVideoByURL(id, function(exists){
                if(!exists){
                    this.updateStatus("Getting data from YouTube...");
                    this.video.getYouTubeVideoDetails(id, function(success){
                        this.displayVideo(false, success);
                    }, this);
                }else{
                    this.displayVideo(true, true);
                }
                
            }, this);
        },
        
        displayVideo: function(alreadyExists, canEmbed){
            if(!alreadyExists && !canEmbed){
                //$("#video_title").html("That Video was either not found or not embedable, please try another.");
                this.updateStatus("That video was either not found, or not embedable. Please try another.", true);
                return;
            }
            
            var template =  _.template($("#createVideoTemplate").html());
            var self = this;
            
            $('#add_video_details').html(template(this.video.toJSON()))
            $('#add_video_details_container').slideDown('slow');
            $('#thumb_container').html('<img src="' + this.video.get('icon_link') + '" />').slideDown('slow');;
            if(!alreadyExists){
                $('#add_video_details .edit').editable(function(value, settings){
                    var data = {};
                    data[this.id.split('_')[1]] = value;
                    self.video.set(data);
                    self.video.save(null, {wait:true, success:function(model, response){self.updateStatus("Video Details Updated!")}});
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
                
                this.video.save(null, {wait:true, success:function(model, response){self.updateStatus("Video Added! Click on details to edit.")}});
            }else{
                this.updateStatus("This video already exists!")
            }
        },
        
        updateStatus: function(message, noLink)
        {
            if(noLink){
                message = '<h4 id="status_message">' + message + '</h4>';
            }else{
                message = '<h4 id="status_message">' + message + ' <a href="/video/' + this.video.get('slug') + '">See the video now</a></h4>'
            }
            
            $("#add_status").html(message).slideDown('slow', function(){
                                    $('#status_message').effect("pulsate", {times:2, mode:"show"}, 500);
                                });
        },
        
        submitVideo: function(){
            //get new values.
            //this.video.set({ title:$("#video_title").html(), description:$("#video_description").html(), time:$("#video_time").html() })
            //this.video.save();
        }
        
        
    });
    
    window.app = new App();
    
    
    
    function getVideoDetails(){
        
    }

});