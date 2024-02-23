document.addEventListener('DOMContentLoaded', function() {
    // var images = document.querySelectorAll('img[id^="sourceImage_"]');
    // images.forEach(function(img) {
    //     var canvasId = 'brandCanvas_' + img.id.split('_')[1];
    //     var canvas = document.getElementById(canvasId);
    //     if (canvas) {
    //         var context = canvas.getContext('2d');
    //         var image = new Image();
    //         image.src = img.src;
    //         image.onload = function() {
    //             canvas.width = image.width;
    //             context.drawImage(image, 0, 0);
    //         };
    //     }
    // });

    var categoriesLists = document.querySelectorAll('.categories-ul');
    categoriesLists.forEach(function(list) {
        list.style.display = 'none';
    });

    var brandListItems = document.querySelectorAll('.brand-li');

    brandListItems.forEach(function(brandListItem) {
        brandListItem.addEventListener('click', function(event) {
            if (event.target === this || event.target.classList.contains('brand-li-header')) {
                event.preventDefault();
                var targetList = this.querySelector('.categories-ul');

                if (targetList) {
                    targetList.style.display = targetList.style.display === 'none' ? 'block' : 'none';
                    event.target.classList.toggle('open');
                }
            }
        });
    });
});

// document.addEventListener('DOMContentLoaded', () => {
//   document.querySelector('.brand-li').addEventListener('click', () => {
//     console.log('Clicked!');
//   });
// });

if (window.innerWidth >= 775) {
    const collapseLinks = document.querySelectorAll('[data-toggle="collapse"]');
    collapseLinks.forEach(function (link) {
        const targetId = link.getAttribute('data-target');
        const collapseElement = document.querySelector(targetId);
        link.classList.remove('collapsed');
        link.setAttribute('aria-expanded', 'true');
        collapseElement.classList.add('show');
    });
}
