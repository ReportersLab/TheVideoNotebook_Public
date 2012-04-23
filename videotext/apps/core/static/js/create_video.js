
$(document).ready(function(){
    
    
    window.MainRouter = Backbone.Router.extend({
        
        initialize: function(options){
            this.app = options.app; // um, no options?
        },
        
        routes: {
            'edit/:videoID': 'editVideo'
        },
        
        editVideo: function(videoID){
            this.app.video.set({id: videoID, resource_uri:VIDEO_API+videoID+"/"});
            this.app.video.fetch({
                success: function(model, response){
                    //once data is fetched, initialize dates.
                    this.app.type = this.app.video.get("type");
                    if(this.app.type == 'youtube'){
                        $('#youtube_ID').val(this.app.video.get('video_url'));
                    }else{
                        $('#upload_url').val(this.app.video.get('video_url'));
                    }
                    $("input:radio[value=" + this.app.type + "]").attr('checked',true).trigger('change');
                    this.app.video.initialize();
                    this.app.displayVideo(true, true);
                },
                error: function(model, response){
                    this.app.updateStatus("There was an error loading that video", true);
                }
            });
        }
        
        
    });
    
    
    
    window.App = Backbone.View.extend({
        el: $("#app"),
        events: {
            "change input:radio": 'onRadioChange',
            'click .video_submit': 'onVideoSubmit',
            'keydown .video_entry' : 'onVideoEntryKeyDown'
        },
        
        initialize: function(){
            this.video = new Video();
            this.type = $('input:radio[name=video_type]:checked').val();
            this.router = new MainRouter({app:this});
            Backbone.history.start();
            //this.genUploader($('#uploader'), $('#upload_url'), true, 'Upload some video or audio', '*.mp4;*.mp3');
        },
        
        genUploader: function(targetElement, resultTarget, submitAfter, buttonText, fileExtensions, buttonLink){
            var self = this;
            this.removeUploader(targetElement);
            //$(targetElement).next().remove();
            uploader = $(targetElement).uploadify({
                   'scriptAccess': 'always',
                   'fileDataName' : 'file',
                   'uploader'  : '/site_media/static/js/uploadify-v2.1.4/uploadify.swf',
                   'script'    : 'http://media.reporterslab.org.s3.amazonaws.com/',
                   'cancelImg' : STATIC_URL + 'js/uploadify-v2.1.4/cancel.png',
                   'buttonImg' : STATIC_URL + 'img/' + buttonLink,
                   'auto'      : true,
                   'width'     : 400,
                   'height'    : 41,
                   'wmode'     : 'transparent',
                   'fileExt'   : fileExtensions, //'*.jpg;*.gif;*.png;*.mp4;*.mp3;*.jpeg',
                   'onError' : function(errorObj, q, f, err) {
                        //console.log(errorObj); console.log(q); console.log(f); console.log(err);
                         self.updateStatus("There was an error uploading that file. Please try again or pick a different file.", true);
                    },
                   'scriptData' : S3_DATA,
                   onSelect: function(event, ID, fileObj){
                        //console.log(fileObj); console.log(event); console.log(ID);
                        ext = fileObj.name.substr(fileObj.name.lastIndexOf('.') + 1).toLowerCase();
                        if(ext == 'jpg'){
                            type = 'image/jpeg';
                        }else if( (ext == 'png') || (ext == 'gif') ){
                            type = 'image/'+ext;
                        }else if( ext == 'mp4'){
                            type = 'video/mp4';
                        }else if (ext == 'mp3'){
                            type = 'audio/mpeg';
                        }else{
                            type = '';
                        }
                        //isn't working?
                        //$(targetElement).uploadifySettings("scriptData", {'Content-Type': type });
                        
                   },
                   onComplete: function(event, ID, fileObj, responseJSON, data) {
                        url = UPLOAD_URL + USER_NAME + '/' + TIMESTAMP + '-' + fileObj.name;
                        self.updateStatus("Upload complete.", true);
                        resultTarget.val(url);
                        if(submitAfter){
                            self.onVideoSubmit();
                        }
                   },
                   
                   onProgress: function(event, ID, fileObj, data) {
                       self.updateStatus("Uploading file... large files may take some time to complete.<br />" +
                                         "<div class='progress_bar_container'><div class='progress_bar' style='width:"+ data.percentage +"%;'>"+data.percentage+"%</div></div>", true, true);
                   }
               
               });
            
            
        },
        
        removeUploader: function(element){
            $(element).next().remove();
            $(element).unbind("uploadifySelect");
            $(element).next().remove();
        },
        
        onRadioChange: function(event){
            this.type = $(event.currentTarget).val();
            $('.add_box').slideUp('slow');
            $('#' + event.target.id + '_add').slideDown('slow');
            
            if(this.type == 'mp4'){
                this.genUploader($('#uploader'), $('#upload_url'), true, 'Upload a video file', '*.mp4', 'upload_mp4.png');    
            }
            if(this.type == 'mp3'){
                this.genUploader($('#uploader'), $('#upload_url'), true, 'Upload an audio file', '*.mp3', 'upload_mp3.png');
            }
            
        },
        
        onVideoEntryKeyDown: function(event){
            if(event.keyCode == 13){ //the 'enter' key
                this.onVideoSubmit();
            }
        },
        
        onVideoSubmit: function(){
            if(this.type == 'youtube'){
                this.getYouTubeDetails();
            }
            else if( (this.type == 'mp4') || (this.type == 'mp3') ){
                this.getManualDetails();
            }
        },
        
        getManualDetails : function(){
            this.video = new Video();
            this.updateStatus("Checking to see if this video already exists", true);
            id = $("#upload_url").val();
            this.video.getVideoByURL(id, function(exists){
                if(!exists){
                    this.displayVideo(false, true);
                }else{
                    this.displayVideo(true, true);
                }
                
            }, this);
        },
        
        getYouTubeDetails: function(){
            this.video = new Video();
            id = $('#youtube_ID').val();
            this.updateStatus("Checking if video exists...", true);
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
                this.updateStatus("That video was either not found, not embedable, or not listed. Please try another.", true);
                return;
            }
            
            
            if(!alreadyExists || ( alreadyExists && (LOGGED_IN_USER.toString() == this.video.get("user").id.toString())) ){
                
                if(!alreadyExists){
                    this.updateStatus("Please fill out the details for your new video.", true);
                    var dt = new Date();
                    var hours = dt.getHours() < 10 ? '0' + dt.getHours() : dt.getHours();
                    var minutes =  dt.getMinutes() < 10 ? '0' + dt.getMinutes() : dt.getMinutes();
                    var day = dt.getDate() < 10 ? '0' + dt.getDate() : dt.getDate();
                    var month = (dt.getMonth() + 1) < 10 ? '0' + (dt.getMonth() + 1) : (dt.getMonth() + 1);
                    this.video.set({time: dt});
                    this.video.set({date_time: dt});
                    this.video.set({time_component:dt.getHours() + ':' + minutes, date_component: day + '/' + month + '/' + dt.getFullYear()})
                    this.video.set({type: this.type});
                }else{
                    this.updateStatus("Edit your video.");
                }
            
            
                var template =  _.template($("#videoFormTemplate").html());
                $('#add_video_details').html(template(this.video.toJSON()));
                var self = this;
                
                $('#add_video_details_container').slideDown('slow');
                if(this.video.get('icon_link') != null){
                    $('#thumb_container').html('<img src="' + this.video.get('icon_link') + '" />').slideDown('slow');;
                }
            
                    
                
                $('#add_video_details').html(template(this.video.toJSON()))
                $('#add_video_details_container').slideDown('slow');
                
                $("#add_edit_message").show();
                $('#add_video_details .timepicker').timepicker();
                $('#add_video_details .datepicker').datePicker({createButton:true, startDate: new Date(1980, 0, 1)})
                this.genUploader($('#image_uploader'), $('#video-icon_link'), false, 'Upload an image', '*.jpg;*.gif;*.png;*.jpeg', 'upload_image.png');
                
                $("#video_save_button").click(function(){
                    var title = $("#video-title").val();
                    var description = $("#video-description").val();
                    var icon_link = $("#video-icon_link").val();
                    var private_note = $("#video-private").attr('checked');
                    var lock_notes = $("#video-lock_notes").attr('checked');
                    //'DD/MM/YYYY'
                    var dateparts = $('#video_date_component').val().split('/');
                    var timeparts = $('#video_time_component').val();
                    
                    
                    if( (title == '') || (description == '') || (dateparts.length < 3) || (timeparts == '')){
                        self.updateStatus("Please fill out all video fields.", true);
                        return;
                    }
                    
                    var dateComponent = dateparts[2] + '-' + dateparts[1] + '-' + dateparts[0];
                    var timeparts = timeparts.split(':');
                    var time = new Date(dateparts[2], dateparts[1] - 1, dateparts[0], timeparts[0], timeparts[1], timeparts[2]);
                    
                    self.video.set({title: title, description: description, icon_link: icon_link, time_component: timeparts, date_component: dateComponent,
                                    private: private_note, lock_notes: lock_notes, time: time, type:self.type});
                    self.video.save(null, {wait:true, success:function(model, response){self.updateStatus("Video Details Updated!")}});
                    if(!self.addSourceView)
                        self.addSourceView = new AddSourceView();
                });
                if(!alreadyExists && this.type == 'youtube'){
                    this.video.save(null, {wait:true, success:function(model, response){self.updateStatus("Video Added! Add sources or view the video to sync and add notes.")}});
                    if(!this.addSourceView)
                        this.addSourceView = new AddSourceView();
                }
                
            }else{
                this.updateStatus("This video already exists and you do not have permission to edit it.");
            }
        },
        
        updateStatus: function(message, noLink, noFade)
        {
            if(noLink){
                message = '<h4 id="status_message">' + message + '</h4>';
            }else{
                message = '<h4 id="status_message">' + message + ' <a href="/video/' + this.video.get('slug') + '">See the video now</a></h4>'
            }
            if(noFade){
                $("#add_status").html(message).show();
            }else{
                $("#add_status").html(message).slideDown('slow', function(){
                                    $('#status_message').effect("pulsate", {times:1, mode:"show"}, 500);
                                });
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
				h = parseInt(v.substr(0,2), 10);
                m = parseInt(v.substr(3,2), 10);
				s = parseInt(v.substr(6,2), 10);
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
        .datePicker({createButton:false, startDate: new Date(1980, 0, 1)})
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




/**
 * Usage:
 *
 * 1. Install Jeditable: http://www.appelsiini.net/projects/jeditable
 * 2. Add the code below to your javascript.
 * 3. Call it like this:
 *
 * $('p').editable('/edit', {
 *   type:   'checkbox',
 *   cancel: 'Cancel',
 *   submit: 'OK',
 *   checkbox: { trueValue: 'Yes', falseValue: 'No' }
 * });
 *
 * Upon clicking on the <p>, it's content will be replaced by a checkbox.
 * If the text within the paragraph is 'Yes', the checkbox will be checked
 * by default, otherwise it will be unchecked.
 *
 * trueValue is submitted when the checkbox is checked and falseValue otherwise.
 *
 * Have fun!
 *
 * Peter BŸcker (spam.naag@gmx.net)
 * http://www.pastie.org/893364
 */

$.editable.addInputType('checkbox', {
  element: function(settings, original) {
    $(this).append('<input type="checkbox"/>');
    var hidden = $('<input type="hidden"/>');
    $(this).append(hidden);
    return(hidden);
  },

  submit: function(settings, original) {
    settings = $.extend({ checkbox: {
      trueValue: 'true',
      falseValue: 'false'
    }}, settings);

    if ($(':checkbox', this).is(':checked')) {
      $(':hidden', this).val(settings.checkbox.trueValue);
    } else {
      $(':hidden', this).val(settings.checkbox.falseValue);
    }
  },

  content: function(data, settings, original) {
    settings = $.extend({ checkbox: {
      trueValue: '1',
      falseValue: '0'
    }}, settings);

    if (data == settings.checkbox.trueValue) {
      $(':checkbox', this).attr('checked', 'checked');
    } else {
      $(':checkbox', this).removeAttr('checked');
    }
  }
});


