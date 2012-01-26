//overrides the basic Backbone.js sync command to work better with TastyPie.
//Seems that always_return_data fixes the need for this.
/*
var oldSync = Backbone.sync;
Backbone.sync = function(method, model, options){
    success = options['success'];
    error = options['error'];
    var newSuccess = function(resp, status, xhr){
        if(xhr.statusText === "success"){
            var location = xhr.getResponseHeader('Location');
            
            return $.ajax({
                       url: location,
                       success: success
                   });
        }
        return success(resp);
    };
    return oldSync(method, model, {success: newSuccess, error: error});
};
*/


//found: http://stackoverflow.com/questions/1353684/detecting-an-invalid-date-date-instance-in-javascript
//checks to see if a date is valid.
function isValidDate(d) {
  if ( Object.prototype.toString.call(d) !== "[object Date]" )
    return false;
  return !isNaN(d.getTime());
}