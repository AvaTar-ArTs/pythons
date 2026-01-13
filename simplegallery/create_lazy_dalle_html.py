#!/usr/bin/env python3
"""
Create lazy-loading dalle.html using the 2.1 large gallery format
"""
import json
import math

# Load configuration
with open('dalle_images_data.json', 'r') as f:
    images_data = json.load(f)

total_images = len(images_data)
images_per_page = 100
total_pages = math.ceil(total_images / images_per_page)

# First image for OG meta
first_image_src = list(images_data.values())[0]['src'] if images_data else ''

html_template = '''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <meta property="og:title" content="DALL·E Gallery">
    <meta property="og:description" content="Browse through {total_images} beautiful images in this interactive gallery with search, albums, and lightbox viewing.">
    <meta property="og:image" content="{first_image}">
    <meta property="og:url" content="">
    <meta property="og:site_name" content="DALL·E Gallery">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image:alt" content="DALL·E Gallery">

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="2.1/data/public/css/photoswipe.css">
    <link rel="stylesheet" href="2.1/data/public/css/default-skin.css">
    <link rel="stylesheet" href="2.1/data/public/css/main.css">
    <link rel="stylesheet" href="2.1/data/public/css/large-gallery.css">
    <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@200;300;400;500;600;700&display=swap" rel="stylesheet">

    <title>Λ∀ʌ†ʌʀ 🦄 ∆ʀ†s - DALL·E Gallery</title>

    <style>
        /* Black nav white hover link */
        .navbar {{
            background-color: #000;
            border-bottom: 1px solid #333;
        }}

        .navbar-brand {{
            color: #fff;
        }}

        .nav-link {{
            color: #fff;
            font-weight: 600;
        }}

        .nav-link:hover {{
            color: #fff;
            background-color: #333;
            border-radius: 4px;
        }}

        /* Body styles */
        body {{
            background-color: #202020;
            font-family: 'Oswald', sans-serif;
            color: #fff;
            text-shadow: 0px 2px 2px #000;
        }}

        /* Back to top and jump down buttons */
        #myBtn,
        #jumpBtn {{
            display: none;
            position: fixed;
            left: 30px;
            z-index: 99;
            font-size: 16px;
            border: none;
            outline: none;
            background-color: black;
            color: rgb(255, 0, 0);
            cursor: pointer;
            padding: 10px;
            border-radius: 4px;
        }}

        #myBtn {{
            bottom: 60px;
        }}

        #jumpBtn {{
            bottom: 20px;
        }}

        #myBtn:hover,
        #jumpBtn:hover {{
            background-color: #555;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        .gallery-section h2 {{
            color: #fff;
            text-shadow: 0px 2px 2px #000;
        }}

        footer {{
            text-align: center;
            margin-top: 30px;
            padding: 20px 0;
        }}

        footer a {{
            text-decoration: none;
            color: #ffffff;
        }}

        footer a:hover {{
            color: #aaaaaa;
        }}
    </style>
</head>

<body>
    <button onclick="topFunction()" id="myBtn" title="Go to top" aria-label="Go to top" style="display:none;">Top</button>
    <button onclick="jumpDown()" id="jumpBtn" title="Down" aria-label="Down" style="display:none;">Jump Down</button>

    <!-- Navigation menu -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <a class="navbar-brand" href="https://avatararts.org">Λ∀ʌ†ʌʀ 🦄 ∆ʀ†s</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item active">
                    <a class="nav-link" href="https://avatararts.org/">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="https://www.avatararts.org/dalle.html">GaLLerY</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="https://www.youtube.com/@iChoake/shorts">Shorts</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="https://www.youtube.com/@iChoake">Videos</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="https://avatararts.org/form.html">Contact</a>
                </li>
            </ul>
        </div>
    </nav>

    <!-- Search and Filter Bar -->
    <div class="container-fluid search-bar-container">
        <div class="row">
            <div class="col-12">
                <div class="search-controls">
                    <input type="text" id="searchInput" class="form-control" placeholder="Search images... ({total_images} images)" autocomplete="off">
                    <div class="search-stats">
                        <span id="searchResultsCount">{total_images}</span> images
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Gallery Section -->
    <div class="container-fluid" id="gallery-container" name="gallery">
        <div class="row">
            <div class="col gallery-section">
                <h2>DALL·E Gallery</h2>
                <div class="gallery-stats">
                    <span id="galleryStats">{total_images} images in {total_pages} pages</span>
                </div>
            </div>
        </div>

        <!-- Gallery Grid (Lazy Loaded) -->
        <div class="row">
            <div class="col gallery" id="gallery-grid">
                <!-- Images will be loaded here via JavaScript -->
            </div>
        </div>

        <!-- Loading Indicator -->
        <div id="loadingIndicator" class="loading-indicator">
            <div class="spinner-border" role="status">
                <span class="sr-only">Loading...</span>
            </div>
        </div>

        <!-- Load More Button -->
        <div class="row">
            <div class="col-12 text-center">
                <button id="loadMoreBtn" class="btn btn-primary btn-lg" style="display: none;">
                    Load More Images
                </button>
            </div>
        </div>

        <!-- Pagination Info -->
        <div class="row">
            <div class="col-12 text-center">
                <div class="pagination-info">
                    <span id="pageInfo">Page 1 of {total_pages}</span>
                </div>
            </div>
        </div>
    </div>

    <!-- PhotoSwipe Container -->
    <div class="pswp" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="pswp__bg"></div>
        <div class="pswp__scroll-wrap">
            <div class="pswp__container">
                <div class="pswp__item"></div>
                <div class="pswp__item"></div>
                <div class="pswp__item"></div>
            </div>
            <div class="pswp__ui pswp__ui--hidden">
                <div class="pswp__top-bar">
                    <div class="pswp__counter"></div>
                    <button class="pswp__button pswp__button--close" title="Close (Esc)"></button>
                    <button class="pswp__button pswp__button--share" title="Share"></button>
                    <button class="pswp__button pswp__button--fs" title="Toggle fullscreen"></button>
                    <button class="pswp__button pswp__button--zoom" title="Zoom in/out"></button>
                    <div class="pswp__preloader">
                        <div class="pswp__preloader__icn">
                            <div class="pswp__preloader__cut">
                                <div class="pswp__preloader__donut"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="pswp__share-modal pswp__share-modal--hidden pswp__single-tap">
                    <div class="pswp__share-tooltip"></div>
                </div>
                <button class="pswp__button pswp__button--arrow--left" title="Previous (arrow left)"></button>
                <button class="pswp__button pswp__button--arrow--right" title="Next (arrow right)"></button>
                <div class="pswp__caption">
                    <div class="pswp__caption__center"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

    <!-- Large Gallery Data - Load from external JSON files (must be before large-gallery.js) -->
    <script>
        window.largeGalleryConfig = {{
            totalImages: {total_images},
            totalPages: {total_pages},
            imagesPerPage: {images_per_page},
            enableSearch: true,
            enableAlbums: false,
            searchIndexUrl: "dalle_search_index.json",
            albumsUrl: null,
            imagesDataUrl: "dalle_images_data.json"
        }};
    </script>

    <!-- PhotoSwipe -->
    <script src="2.1/data/public/js/photoswipe.min.js"></script>
    <script src="2.1/data/public/js/photoswipe-ui-default.min.js"></script>

    <!-- Gallery Scripts -->
    <script src="2.1/data/public/js/main.js"></script>
    <script src="2.1/data/public/js/large-gallery.js"></script>

    <!-- Initialize scroll buttons after DOM is ready -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const myBtn = document.getElementById("myBtn");
            const jumpBtn = document.getElementById("jumpBtn");

            if (myBtn && typeof topFunction === 'function') {{
                myBtn.onclick = function() {{
                    topFunction();
                }};
            }}

            if (jumpBtn && typeof jumpDown === 'function') {{
                jumpBtn.onclick = function() {{
                    jumpDown();
                }};
            }}
        }});
    </script>

    <!-- Scroll functions -->
    <script>
        window.onscroll = function() {{
            scrollFunction();
        }};

        function scrollFunction() {{
            const myBtn = document.getElementById("myBtn");
            const jumpBtn = document.getElementById("jumpBtn");
            if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {{
                myBtn.style.display = "block";
                jumpBtn.style.display = "block";
            }} else {{
                myBtn.style.display = "none";
                jumpBtn.style.display = "none";
            }}
        }}

        function topFunction() {{
            window.scrollTo({{
                top: 0,
                behavior: 'smooth'
            }});
        }}

        function jumpDown() {{
            window.scrollBy({{
                top: window.innerHeight,
                behavior: 'smooth'
            }});
        }}
    </script>

    <!-- Disable right click and save as -->
    <script>
        document.addEventListener("contextmenu", function(event) {{
            event.preventDefault();
        }});
        document.addEventListener("keydown", function(event) {{
            if (
                event.keyCode === 123 ||
                (event.ctrlKey && event.shiftKey && [73, 67, 74].includes(event.keyCode)) ||
                (event.ctrlKey && event.keyCode === 85)
            ) {{
                event.preventDefault();
            }}
        }});
    </script>

    <footer class="container-fluid text-center">
        <p>
            <a rel="noreferrer" href="https://www.avatararts.org">Λ∀ʌ†ʌʀ 🦄 ∆ʀ†s</a>
        </p>
    </footer>

</body>
</html>'''

# Generate HTML
html_output = html_template.format(
    total_images=total_images,
    total_pages=total_pages,
    images_per_page=images_per_page,
    first_image=first_image_src
)

# Write to file
with open('dalle_lazy.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print(f"Created dalle_lazy.html")
print(f"  Total images: {total_images}")
print(f"  Images per page: {images_per_page}")
print(f"  Total pages: {total_pages}")
print(f"  Features: Lazy loading, Pagination, Search")

