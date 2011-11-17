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
            this.videos = new Videos();
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
            this.videos.getYouTubeVideoDetails(id, _.bind(function(video){
                console.log(video);
                if(!video){
                    $("#video_title").html("That Video was either not found or not embedable, please try another.");
                    return;
                }
                var template =  _.template($("#createVideoTemplate").html());
                $('#video_details_container').html(template(video.toJSON()));
                $('#video_details_container .edit').editable(function(value, settings){
                    console.log(value);
                    console.log(settings);
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
                
                this.videos.add(video);
                //video.save();
            }, this));
        }
        
        
    });
    
    window.app = new App();
    
    
    
    function getVideoDetails(){
        
    }

});