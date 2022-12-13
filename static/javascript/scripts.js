function itemLink() {
        console.log('here');
    }

var elements = document.getElementsByClassName("item-row");

Array.from(elements).forEach(function(element) {
      element.addEventListener('click', itemLink);
    });