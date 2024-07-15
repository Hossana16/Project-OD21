document.addEventListener('DOMContentLoaded', function() {
    var sidebarItems = document.querySelectorAll('.sidebar-item');
  
    // Function to remove active class from all items
    function removeActiveClasses() {
      sidebarItems.forEach(function(item) {
        item.classList.remove('-is-active');
      });
    }
  
    // Attach event listeners to each sidebar item
    sidebarItems.forEach(function(item) {
      item.addEventListener('click', function() {
        removeActiveClasses();
        this.classList.add('-is-active');
      });
    });
  });
  