
$(document).ready(function(){
    
    
    window.AddSourceView = Backbone.View.extend({
        el: $('#add_source_container'),
        events: {
            'click #add_source_link' : 'onAddSourceClick'
        },
        initialize: function(){
            this.sources = new Sources();
            this.addSource();
            $(this.el).slideDown('slow');
        },
        onAddSourceClick: function(event){
            this.addSource();
        },
        addSource: function(){
            source = new Source();
            var view = new SourceView({model:source, container:this});
            $("#sources").append(view.render().el);
            source.view = view;
            this.sources.add(source);
        }
        
    });
    
    window.SourceView = Backbone.View.extend({
       tagName: 'div',
       className: 'add_source',
       template: _.template($("#sourceTemplate").html()),
       events: {
            'click .source_save': 'onSaveClick'
       },
       
       initialize: function(){
            this.container = this.options.container;
       },
       
       render: function(){
            $(this.el).html(this.template(this.model.toJSON()));
            $(this.el).fadeIn('slow');
            return this;
       },
       
       onSaveClick: function(event){
            status = $(this.el).find('.status');
            status.html("Saving source").show();
            var url = $(this.el).find('.source_url').val();
            var type = $(this.el).find('.source_type').val();
            if( (type == "") || (url == "") ){
                status.html("Please fill out everything.").effect("pulsate", {times:3, mode:"show"}, 500);
                return;
            }
            this.model.save(
            {
                url: url,
                type: type,
                video: app.video.get('resource_uri'),
                video_id : parseInt(app.video.get('id'))
            },
            {
                success: function(){
                    status.html("Source Saved");
                    status.effect("pulsate", {times:3, mode:"show"}, 500);
                }
            });
       }
       
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
            this.updateStatus("Checking if video exists...");
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
                //and allow the adding of sources...
                this.addSourceView = new AddSourceView();
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
                                    $('#status_message').effect("pulsate", {times:1, mode:"show"}, 500);
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