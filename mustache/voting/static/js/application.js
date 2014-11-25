var Mustache = {};
var klasses = [ 'dali', 'borat', 'sellec', 'swanson', 'burgundy' ];

$(document).on('click', 'a.toggle-comments', function() {
  Mustache.toggleComments(this);
  return false;
});

         
Mustache = {
  
  setMasthead: function(){
    $('header.masthead').addClass(klasses[Math.floor(Math.random()*klasses.length)]);
  },

  toggleComments: function(el){
    var commentList = $(el).parent().next().children('ul.comments-list');
    commentList.children(':nth-child(n+3)').stop().slideToggle();
  }

}



