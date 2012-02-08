
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
            'click .source_save': 'onSaveClick',
            'change .source_type': 'onSourceTypeChange'
       },
       
       initialize: function(){
            this.container = this.options.container;
       },
       
       render: function(){
            $(this.el).html(this.template(this.model.toJSON()));
            $(this.el).fadeIn('slow');
            return this;
       },
       
       onSourceTypeChange: function(event){
            var type = $(this.el).find('.source_type').val();
            if(type == 'twitter'){
                $(this.el).find('.source_twitter').slideDown('slow');
                $(this.el).find('.source_url_container').slideUp('slow');
            }else{
                $(this.el).find('.source_twitter').slideUp('slow');
                $(this.el).find('.source_url_container').slideDown('slow');
            }
       },
       
       onSaveClick: function(event){
            status = $(this.el).find('.status');
            status.html("Saving source").show();
            var url = $(this.el).find('.source_url').val();
            var type = $(this.el).find('.source_type').val();
            var twitter_user = $(this.el).find('.source_twitter_user').val();
            var twitter_start_id = $(this.el).find('.source_twitter_start_id').val();
            var twitter_end_id = $(this.el).find('.source_twitter_end_id').val();
            var twitter_hash = $(this.el).find('.source_twitter_hash').val();
            
            if( (type == "") || ((url == "") && (twitter_user == "")) ){
                status.html("Please fill out everything.").effect("pulsate", {times:3, mode:"show"}, 500);
                return;
            }
            this.model.save(
            {
                url: url,
                type: type,
                video: app.video.get('resource_uri'),
                video_id : parseInt(app.video.get('id')),
                twitter_user : twitter_user,
                twitter_start_id : twitter_start_id,
                twitter_end_id : twitter_end_id,
                twitter_hash : twitter_hash
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
            
            $('#add_video_details').append(template(this.video.toJSON()))
            $('#add_video_details_container').slideDown('slow');
            $('#thumb_container').html('<img src="' + this.video.get('icon_link') + '" />').slideDown('slow');;
            if(!alreadyExists){
                $("#add_edit_message").show();
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
                
                $('#add_video_details .timepicker').editable(function(value, settings){
                    var stamp = $('#video_date_component').html() + 'T' + value + '.000Z';
                    self.video.set({time: stamp});
                    self.video.save(null, {wait:true, success:function(model, response){self.updateStatus("Video Details Updated!")}});
                    return value;
                },
                {
                    type: 'timepicker',
                    submit: 'Submit',
                    tooltip: 'Click to edit...'
                });
                
                $('#add_video_details .datepicker').editable(function(value, settings){
                    var vp = value.split('/');
                    value = vp[2] + '-' + vp[1] + '-' + vp[0];
                    var stamp = value + 'T' + $('#video_time_component').html() + '.000Z';
                    self.video.set({time: stamp});
                    self.video.save(null, {wait:true, success:function(model, response){self.updateStatus("Video Details Updated!")}});
                    return value;
                },
                {
                    type: 'datepicker',
                    submit: 'Submit',
                    tooltip: 'Click to edit...'
                });
                
                this.video.save(null, {wait:true, success:function(model, response){self.updateStatus("Video Added! Add sources or view the video to sync and add notes.")}});
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





/* jQuery timepicker
 * replaces a single text input with a set of pulldowns to select hour, minute, and am/pm
 *
 * Copyright (c) 2007 Jason Huck/Core Five Creative (http://www.corefive.com/)
 * Dual licensed under the MIT (http://www.opensource.org/licenses/mit-license.php) 
 * and GPL (http://www.opensource.org/licenses/gpl-license.php) licenses.
 *
 * Version 1.0
 */

(function($){
	jQuery.fn.timepicker = function(){
		this.each(function(){
			// get the ID and value of the current element
			var i = this.id;
			var v = $(this).val();
	
			// the options we need to generate
			var hrs = new Array('00', '01','02','03','04','05','06','07','08','09','10','11','12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23');
			var mins = new Array('00','01','02','03','04','05','06','07','08','09','10','11','12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59');
			
			// default to the current time
			var d = new Date;
			var h = d.getHours();
			var m = d.getMinutes();
			var s = d.getSeconds();
			
			// override with current values if applicable
			if(v.length == 8){
				h = parseInt(v.substr(0,2));
				m = parseInt(v.substr(3,2));
				s = parseInt(v.substr(6,2));
			}
		    
			// build the new DOM objects
			var output = '';
			
			output += '<select id="h_' + i + '" class="h timepicker">';				
			for(hr in hrs){
				output += '<option value="' + hrs[hr] + '"';
				if(parseInt(hrs[hr], 10) == h) output += ' selected';
				output += '>' + hrs[hr] + '</option>';
			}
			output += '</select>';
	
			output += '<select id="m_' + i + '" class="m timepicker">';				
			for(mn in mins){
				output += '<option value="' + mins[mn] + '"';
				if(parseInt(mins[mn], 10) == m) output += ' selected';
				output += '>' + mins[mn] + '</option>';
			}
			output += '</select>';				
            
            output += '<select id="s_' + i + '" class="s timepicker">';				
			for(mn in mins){
				output += '<option value="' + mins[mn] + '"';
				if(parseInt(mins[mn], 10) == s) output += ' selected';
				output += '>' + mins[mn] + '</option>';
			}
			output += '</select>';			
            
			// hide original input and append new replacement inputs
			//$(this).attr('type','hidden').after(output);
            // Fix IE crash (tuupola@appelsiini.net)
			$(this).hide().after(output);
			
		});
		
		
		$('select.timepicker').change(function(){
			var i = this.id.substr(2);
			var h = $('#h_' + i).val();
			var m = $('#m_' + i).val();
            var s = $('#s_' + i).val();
			var v = h + ':' + m + ":" + s ;
			$('#' + i).val(v);
		});
		
		return this;
	};
})(jQuery);




/*
 * Timepicker for Jeditable
 *
 * Copyright (c) 2007-2009 Mika Tuupola
 *
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Depends on Timepicker jQuery plugin by Jason Huck:
 *   http://jquery.com/plugins/project/timepicker
 *
 * Project home:
 *   http://www.appelsiini.net/projects/jeditable
 *
 * Revision: $Id$
 *
 */
var timepickerFormId = 0
$.editable.addInputType('timepicker', {
    /* This uses default hidden input field. No need for element() function. */

    /* Call before submit hook. */
    submit: function (settings, original) {
        /* Collect hour, minute and am/pm from pulldowns. Create a string from */
        /* them. Set value of hidden input field to this string.               */
        //2012-01-31T10:58:06.000Z
        var value = $('.h.timepicker').val() + ':' + $('.m.timepicker').val() + ":" + $('.s.timepicker').val();
        $('input', this).val(value);
    },
    /* Attach Timepicker plugin to the default hidden input element. */
    plugin:  function(settings, original) {
        $('input', this).filter(':hidden')
          .attr("id", "jquery_timepicker_"+(++timepickerFormId))
          .filter(':hidden').timepicker();
    }
});




/*
 * Datepicker for Jeditable (currently buggy, not for production)
 *
 * Copyright (c) 2007-2008 Mika Tuupola
 *
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Depends on Datepicker jQuery plugin by Kelvin Luck:
 *   http://kelvinluck.com/assets/jquery/datePicker/v2/demo/
 *
 * Project home:
 *   http://www.appelsiini.net/projects/jeditable
 *
 * Revision: $Id$
 *
 */
 
$.editable.addInputType('datepicker', {
    /* create input element */
    element : function(settings, original) {
        var input = $('<input>');
        $(this).append(input);
        //$(input).css('opacity', 0.01);
        return(input);
    },

    /* attach 3rd party plugin to input element */
    plugin : function(settings, original) {
        /* Workaround for missing parentNode in IE */
        var form = this;
        settings.onblur = 'cancel';
        $("input", this)
        .datePicker({createButton:false})
        .bind('click', function() {
            //$(this).blur();
            $(this).dpDisplay();
            return false;
        })
        .bind('dateSelected', function(e, selectedDate, $td) {
            $(form).submit();
        })
        .bind('dpClosed', function(e, selected) {
            /* TODO: unneseccary calls reset() */
            //$(this).blur();
        })
        .trigger('change')
        .click();
    }
});
