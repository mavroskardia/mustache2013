var Mustache = {};
var klasses = [ 'dali', 'borat', 'sellec', 'swanson', 'burgundy' ];
         
Mustache.Layout = {
  setMasthead: function(){
    $('header.masthead').addClass(klasses[Math.floor(Math.random()*klasses.length)]);
  }
}



