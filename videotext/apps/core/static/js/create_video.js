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
            id = $('#youtube_ID').val();
            this.video.getVideoByURL(id, function(exists){
                if(!exists){
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
                $("#video_title").html("That Video was either not found or not embedable, please try another.");
                return;
            }
            
            var template =  _.template($("#createVideoTemplate").html());
            var self = this;
            
            $('#video_details_container').html(template(this.video.toJSON()));
            
            if(!alreadyExists){
                $('#video_details_container .edit').editable(function(value, settings){
                    var data = {};
                    data[this.id.split('_')[1]] = value;
                    self.video.set(data);
                    self.video.save();
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
                
                this.video.save();
            }
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