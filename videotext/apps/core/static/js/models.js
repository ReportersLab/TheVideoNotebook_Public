$(function(){
    window.Video = Backbone.Model.extend({
         
         initialize: function(){
             //make a real JS date out of the date string we got in JSON.
             if(this.get('time')){
                var dt = new Date(this.get('time'));
             }else{
                var dt = new Date();
                this.set({time: dt});
             }
             var hours = dt.getHours() < 10 ? '0' + dt.getHours() : dt.getHours();
             var minutes =  dt.getMinutes() < 10 ? '0' + dt.getMinutes() : dt.getMinutes();
             var seconds = dt.getSeconds() < 10 ? '0' + dt.getSeconds() : dt.getSeconds();
             this.set({date_time: dt});
             this.set({time_component:hours + ':' + minutes + ':' + seconds, date_component: dt.getDate() + '/' + (dt.getMonth() + 1) + '/' + dt.getFullYear()})   
        
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
                        if(self.get('time'))
                           self.set({time_component:self.get('time').split('T')[1].replace('.000Z', ''), date_component:self.get('time').split('T')[0]});
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
                    //split time into date & time for editing purposes.
                    var time_component = time.split('T')[1].replace('.000Z', '');
                    var date_component = time.split('T')[0];
                    var tags = item['tags'].join(',');
                    var user_name = item['uploader'];
                    var image = item['thumbnail']['hqDefault'];
                    this.set({title: title, description:description, time:time, tags:tags, user_name: user_name,
                              icon_link:image, type:'youtube', private: false, video_url: id, embedable: embedable, resource_uri: VIDEO_API,
                              time_component:time_component, date_component:date_component});
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
    
    
    window.Source = Backbone.Model.extend({
        defaults: function(){
            return{
              type: "twitter",
              scraped: false,
              url: 'http://'
            };
        },
        url: function(){
            return this.get('resource_uri') || this.collection.url || SOURCE_API;
        }
    });
     
     
    window.Sources = Backbone.Collection.extend({
       model: Source,
       url: SOURCE_API,
       parse: function(data){
            return data.objects;
       },
       comparator: function(source){
            source.get('update_time');
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
        },
        //takes a video and adjusts all of the times / offsets of individual notes to match.
        //used on the video page after a video time is updated.
        syncToVideo: function(video){
            this.each(function(note){
                //miliseconds difference
                var diff = note.get('date_time') - video.get('date_time');
                diff = Math.round(diff / 1000);
                note.set({offset: diff});
                if(note.view){
                    note.view.render();
                }
            });            
        }
    });
     
    
}); 