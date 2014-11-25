var Mustache = {};
var staches = [ 'dali', 'borat', 'sellec', 'swanson', 'burgundy' ];
var current_frame, total_frames, path, length, handle;

$('a.toggle-comments').on('click', function() {
  Mustache.toggleComments(this);
  return false;
});

$(document).ready(function() {
  
  $('nav.navigation').waypoint('sticky', {
    offset: -66
  });

  Mustache.Svg.init();
  Mustache.Svg.draw();

});
         
Mustache.Layout = {
  
  setMasthead: function(){
    $('header.masthead').addClass(staches[Math.floor(Math.random()*staches.length)]);
  },

  toggleComments: function(el){
    var commentList = $(el).parent().next().children('ul.comments-list');
    commentList.children(':nth-child(n+2)').stop().slideToggle();
  }

};

Mustache.Svg = {

  init: function(){
    current_frame = 0;
    total_frames = 120;
    path = document.querySelector('.content path');
    length = path.getTotalLength();
    path.style.strokeDasharray = length + ' ' + length;
    path.style.strokeDashoffset = length;
    handle = 0;
  },
 
  draw: function() {
     var progress = current_frame/total_frames;

     if (progress > 1) {
       window.cancelAnimationFrame(handle);
       path.style.fill = "rgba(255,255,255,1)" 
     } 
     else {
      current_frame++;
      path.style.strokeDashoffset = Math.floor(length * (1 - progress));
      handle = window.requestAnimationFrame(Mustache.Svg.draw);
     }
  }

};



