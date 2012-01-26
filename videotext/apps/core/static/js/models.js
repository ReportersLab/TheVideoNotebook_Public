$(function(){
    window.Video = Backbone.Model.extend({
         
         initialize: function(){
             //make a real JS date out of the date string we got in JSON.
             this.set({date_time: new Date(this.get('time')) });
             if(this.get('end_time')){
                 this.set({end_date_time: new Date(this.get('end_time'))});
             }
         },
         
        url: function(){
            return this.get('resource_uri') || this.collection.url;     
        },
        
        getVideoByURL: function(url, callback, object){
            this.clear();
            this.set({video_url: url, resource_uri: VIDEO_API + "?video_url=" + url});
            var self = this;
            this.fetch({
                success: function(model, response){
                    if(response.objects && response.objects.length == 1){
                        self.set(response.objects[0]);
                        if(callback)
                            callback.call(object, true);
                        return;
                    }
                    if(callback)
                        callback.call(object, false);
                },
                failure: function(model, response){
                    if(callback)
                        callback.call(object, false);
                }
            });
        
        },
        
        getYouTubeVideoDetails: function(id, callback, object){
            
            $.getJSON('http://gdata.youtube.com/feeds/api/videos?v=2&alt=jsonc&q='+ id +'&callback=?', _.bind(function(data) { 
                try{
                    var item = data.data.items[0];
                    var embedable = item['accessControl']['embed'] == 'allowed';
                    //if we can't embed the video, there's really no point in going any further.
                    if(!embedable){
                        if(callback)
                            callback.call(object, false);
                    }
                    var title = item['title'];
                    var description = item['description'];
                    var time = item['uploaded'];
                    var tags = item['tags'].join(',');
                    var user_name = item['uploader'];
                    var image = item['thumbnail']['hqDefault'];
                    this.set({title: title, description:description, time:time, tags:tags, user_name: user_name,
                              icon_link:image, type:'youtube', private: false, video_url: id, embedable: embedable, resource_uri: VIDEO_API });
                    if(callback)
                        callback.call(object, true);
                }catch (e){
                    if(callback)
                        callback.call(object, false);
                }
            }, this));
        }
        
    });
    
    window.Videos = Backbone.Collection.extend({
         model: Video,
         url: VIDEO_API,
         parse: function(data){
             return data.objects;
         },
         comparator: function(video){
             return video.get('end_date_time');
         }
    });
     
    window.Note = Backbone.Model.extend({
        
         defaults: function(){
           return {
             text: "",
             video: VIDEO_ID || -1,
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
     
    
}); 