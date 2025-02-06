---
layout: blank
title: Gallery
---

<!-- Slick CSS -->
<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick.min.css"/>
<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick-theme.min.css"/>

 <style>
    /* Ensure the body takes full height */
    body, html {
      margin: 0;
      padding: 0;
      height: 100%;
    }
    
    /* Full height slider setup */
    #slider {
      width: 100%;
      height: 100vh; /* Full viewport height */
    }

    #slider img {
      width: 100%;
      height: 100%;
      object-fit: cover; /* Make images cover the full container */
    }
  </style>

<!-- Slick JS -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick.min.js"></script>


<div id="slider">
</div>

<script>
    $().ready(function(){
        $slider = $('#slider');

        $slider.slick({
            infinite: true,
            dots: true,
            arrows: false,
            autoplay: true,
            autoplaySpeed: 3000,
            pauseOnHover: false,
            fade: true,
            speed: 1000,
        });

        $.getJSON("/museum.json", artworks => {
            console.log(artworks);
            artworks.forEach(artwork => {
                var slideHTML = '<div>';
                slideHTML += '<img src="' + artwork.image + '" alt="' + (artwork.title || 'Artwork') + '">';
                if (artwork.title) {
                    slideHTML += '<div class="slide-title">' + artwork.title + '</div>';
                }
                slideHTML += '</div>';

                // Append the slide to the slider
                // $slider.append(slideHTML);
                $slider.slick('slickAdd', slideHTML);
            });

            
        });
    });
</script>