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
        }
    });
    
    window.Videos = Backbone.Collection.extend({
         model: Video,
         url: VIDEO_API,
         parse: function(data){
             return data.objects;
         },
         comparator: function(video){
             return this.get('end_date_time');
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