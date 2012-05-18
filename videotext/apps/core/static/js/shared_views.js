
$(document).ready(function(){
    
    
    window.AddSourceView = Backbone.View.extend({
        el: $('#add_source_container'),
        
        events: {
            'click #add_source_link' : 'onAddSourceClick',
            'click .close_link': 'onCloseClick'
        },
        
        initialize: function(){
            this.sources = new Sources();
            this.loadAFterSave = false;
            this.notes = null;
            if(this.options && this.options.loadAfterSave){
                this.loadAfterSave = this.options.loadAfterSave;
                this.notes = this.options.notes;
            }
            this.addSource();
            $(this.el).slideDown('slow');
        },
        
        onAddSourceClick: function(event){
            this.addSource();
        },
        
        addSource: function(){
            source = new Source();
            var view = new SourceView({model:source, container:this, loadAfterSave: this.loadAfterSave, notes:this.notes});
            $("#sources").append(view.render().el);
            $(view.el).fadeIn('slow');
            source.view = view;
            this.sources.add(source);
        },
        
        onCloseClick: function(event){
            $(this.el).slideUp("slow");
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
            this.loadAfterSave = this.options.loadAfterSave;
            this.notes = this.options.notes;
            this.container = this.options.container;
        },
       
        render: function(){
            $(this.el).html(this.template(this.model.toJSON()));
            //$(this.el).fadeIn('slow');
            return this;
        },
       
        onSourceTypeChange: function(event){
            var type = $(this.el).find('.source_type').val();
            
            if( (type == "twitter") || (type == "csv") || (type == "srt") ){
                $(this.el).find('.source_url_container').slideUp('slow');                
            }else{
                $(this.el).find('.source_url_container').slideDown('slow');                
            }
            
            if(type == 'twitter'){
                $(this.el).find('.source_twitter').slideDown('slow');
            }else{
                $(this.el).find('.source_twitter').slideUp('slow');
            }
            
            if(type == "csv"){
                $(this.el).find('.source_csv').slideDown('slow');
            }else{
                $(this.el).find('.source_csv').slideUp('slow');
            }
            
            if(type == "srt"){
                $(this.el).find('.source_srt').slideDown('slow');
            }else{
                $(this.el).find('.source_srt').slideUp('slow');
            }
            
            if(type =="granicus"){
                $(this.el).find('.source_granicus').slideDown('slow');
            }else{
                $(this.el).find('.source_granicus').slideUp('slow');
            }
            
        },
       
        onSaveClick: function(event){
            var self = this;
            var status = $(this.el).find('.status');
            status.html("Saving source").show();
            var name = $(this.el).find('.source_name').val();
            var url = $(this.el).find('.source_url').val();
            var type = $(this.el).find('.source_type').val();
            var twitter_user = $(this.el).find('.source_twitter_user').val();
            var twitter_start_id = $(this.el).find('.source_twitter_start_id').val();
            var twitter_end_id = $(this.el).find('.source_twitter_end_id').val();
            var twitter_hash = $(this.el).find('.source_twitter_hash').val();
            var csv_data = $(this.el).find('.source_csv_data').val();
            var srt_data = $(this.el).find('.source_srt_data').val();
            
            if( (type == "") || ((url == "") && (twitter_user == "") && ( csv_data == "") && (srt_data == "")) ){
                status.html("Please fill out everything.").effect("pulsate", {times:3, mode:"show"}, 500);
                return;
            }
            this.model.save(
            {
                name: name,
                url: url,
                type: type,
                video: app.video.get('resource_uri'),
                video_id : parseInt(app.video.get('id')),
                twitter_user : twitter_user,
                twitter_start_id : twitter_start_id,
                twitter_end_id : twitter_end_id,
                twitter_hash : twitter_hash,
                csv_data : csv_data,
                srt_data : srt_data
            },
            {
                success: function(){
                    status.html("Source Saved");
                    status.effect("pulsate", {times:3, mode:"show"}, 500);
                    if(self.loadAfterSave){
                        self.mergeNotes();
                    }
                }
            });
        },
       
        
        
        mergeNotes: function(){
            if(this.notes == null){
                return;
            }
            var self = this;
            //model should now have an id.
            var newNotes = new Notes();
            newNotes.url = NOTE_API + "?limit=2000&import_source=" + this.model.get("id");
            newNotes.fetch({
                success: function(collection, response){
                    self.notes = self.notes.add(collection.models);
                    self.notes.sort();
                },
                error: function(collection, response){
                    //do nothing?
                }
            })
            
            
            
            
        }
       
       
    });

});



