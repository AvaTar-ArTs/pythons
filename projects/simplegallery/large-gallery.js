/**
 * SimpleGallery 2.1 - Large Gallery JavaScript
 * Optimized for galleries with 2,500+ images
 * Features: Lazy loading, pagination, search, virtual scrolling
 */

(function() {
    'use strict';

    const LargeGallery = {
        config: null,
        images: null,
        searchIndex: null,
        albums: null,
        currentPage: 0,
        loadedImages: new Set(),
        visibleImages: new Set(),
        searchResults: null,
        currentAlbum: null,
        isLoading: false,
        intersectionObserver: null,
        dataLoaded: false,
        
        init: function() {
            this.config = window.largeGalleryConfig;
            if (!this.config) {
                console.error('Large gallery config not found');
                return;
            }
            
            // Load data asynchronously
            this.loadData();
            
            this.setupEventListeners();
            this.setupLazyLoading();
            
            if (this.config.enableSearch) {
                this.setupSearch();
            }
            
            if (this.config.enableAlbums) {
                this.setupAlbums();
            }
        },
        
        loadData: async function() {
            try {
                // Load images data
                const imagesResponse = await fetch(this.config.imagesDataUrl);
                const imagesData = await imagesResponse.json();
                
                // Convert to array format
                this.images = Object.keys(imagesData).map(name => ({
                    ...imagesData[name],
                    name: name
                }));
                
                // Load search index if enabled
                if (this.config.enableSearch && this.config.searchIndexUrl) {
                    const searchResponse = await fetch(this.config.searchIndexUrl);
                    this.searchIndex = await searchResponse.json();
                }
                
                // Load albums if enabled
                if (this.config.enableAlbums && this.config.albumsUrl) {
                    const albumsResponse = await fetch(this.config.albumsUrl);
                    this.albums = await albumsResponse.json();
                }
                
                this.dataLoaded = true;
                this.loadInitialPage();
            } catch (error) {
                console.error('Error loading gallery data:', error);
                this.showError('Failed to load gallery data. Please refresh the page.');
            }
        },
        
        setupEventListeners: function() {
            const loadMoreBtn = document.getElementById('loadMoreBtn');
            if (loadMoreBtn) {
                loadMoreBtn.addEventListener('click', () => this.loadNextPage());
            }
            
            // Infinite scroll
            window.addEventListener('scroll', this.debounce(() => {
                if (this.isNearBottom() && !this.isLoading) {
                    this.loadNextPage();
                }
            }, 200));
        },
        
        setupLazyLoading: function() {
            // Use Intersection Observer for lazy loading
            if ('IntersectionObserver' in window) {
                this.intersectionObserver = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            if (img.dataset.src && !img.src) {
                                img.src = img.dataset.src;
                                img.removeAttribute('data-src');
                            }
                        }
                    });
                }, {
                    rootMargin: '50px'
                });
            }
        },
        
        setupSearch: function() {
            const searchInput = document.getElementById('searchInput');
            if (!searchInput) return;
            
            searchInput.addEventListener('input', this.debounce((e) => {
                const query = e.target.value.trim().toLowerCase();
                if (query.length < 2) {
                    this.clearSearch();
                    return;
                }
                this.performSearch(query);
            }, 300));
            
            searchInput.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    this.clearSearch();
                    searchInput.value = '';
                }
            });
        },
        
        setupAlbums: function() {
            const albumTabs = document.querySelectorAll('.album-tab');
            albumTabs.forEach(tab => {
                tab.addEventListener('click', () => {
                    const albumName = tab.dataset.album;
                    this.switchAlbum(albumName);
                    
                    // Update active state
                    albumTabs.forEach(t => t.classList.remove('active'));
                    tab.classList.add('active');
                });
            });
        },
        
        loadInitialPage: function() {
            if (!this.dataLoaded) return;
            this.currentPage = 0;
            const images = this.getCurrentImages();
            this.renderImages(images.slice(0, this.config.imagesPerPage));
            this.updatePageInfo();
        },
        
        loadNextPage: function() {
            if (this.isLoading || !this.dataLoaded) return;
            
            this.isLoading = true;
            this.showLoadingIndicator();
            
            // Simulate async loading
            setTimeout(() => {
                this.currentPage++;
                const images = this.getCurrentImages();
                const startIndex = this.currentPage * this.config.imagesPerPage;
                const endIndex = startIndex + this.config.imagesPerPage;
                const pageImages = images.slice(startIndex, endIndex);
                
                if (pageImages.length > 0) {
                    this.renderImages(pageImages, true);
                    this.updatePageInfo();
                } else {
                    this.hideLoadMoreButton();
                }
                
                this.isLoading = false;
                this.hideLoadingIndicator();
            }, 100);
        },
        
        getCurrentImages: function() {
            if (!this.dataLoaded || !this.images) {
                return [];
            }
            if (this.searchResults) {
                return this.searchResults;
            }
            if (this.currentAlbum && this.albums && this.albums[this.currentAlbum]) {
                const albumImageNames = this.albums[this.currentAlbum];
                return this.images.filter(img => albumImageNames.includes(img.name));
            }
            return this.images;
        },
        
        renderImages: function(images, append = false) {
            const galleryGrid = document.getElementById('gallery-grid');
            if (!galleryGrid) return;
            
            if (!append) {
                galleryGrid.innerHTML = '';
                this.loadedImages.clear();
            }
            
            const fragment = document.createDocumentFragment();
            
            images.forEach((image, index) => {
                if (this.loadedImages.has(image.name)) return;
                
                const link = document.createElement('a');
                link.href = image.src;
                link.className = 'gallery-photo';
                link.setAttribute('data-index', this.loadedImages.size);
                link.setAttribute('data-type', image.type || 'image');
                link.setAttribute('data-gallery', '0');
                link.setAttribute('data-width', image.size[0]);
                link.setAttribute('data-height', image.size[1]);
                if (image.date) {
                    link.setAttribute('data-date', image.date);
                }
                link.style.setProperty('--w', image.thumbnail_size[0]);
                link.style.setProperty('--h', image.thumbnail_size[1]);
                
                const img = document.createElement('img');
                img.className = 'thumbnail rounded';
                img.alt = image.description || image.name;
                
                // Lazy load thumbnail
                if (this.intersectionObserver) {
                    img.dataset.src = image.thumbnail;
                    img.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"%3E%3C/svg%3E';
                    this.intersectionObserver.observe(img);
                } else {
                    img.src = image.thumbnail;
                }
                
                link.appendChild(img);
                fragment.appendChild(link);
                
                this.loadedImages.add(image.name);
            });
            
            galleryGrid.appendChild(fragment);
            
            // Reinitialize PhotoSwipe if needed
            if (typeof initPhotoSwipe === 'function') {
                initPhotoSwipe();
            }
        },
        
        performSearch: function(query) {
            if (!this.searchIndex || !this.images) {
                console.warn('Search index or images not available');
                return;
            }
            
            const results = new Set();
            const queryLower = query.toLowerCase();
            
            // Search by name
            if (this.searchIndex.by_name[queryLower]) {
                this.searchIndex.by_name[queryLower].forEach(name => results.add(name));
            }
            
            // Search by description
            const words = queryLower.split(/\s+/);
            words.forEach(word => {
                if (word.length > 2 && this.searchIndex.by_description[word]) {
                    this.searchIndex.by_description[word].forEach(name => results.add(name));
                }
            });
            
            // Convert to image objects
            this.searchResults = this.images.filter(img => results.has(img.name));
            
            // Update UI
            this.currentPage = 0;
            this.renderImages(this.searchResults.slice(0, this.config.imagesPerPage));
            this.updateSearchStats(this.searchResults.length);
            this.updatePageInfo();
        },
        
        clearSearch: function() {
            this.searchResults = null;
            const searchInput = document.getElementById('searchInput');
            if (searchInput) {
                searchInput.value = '';
            }
            this.loadInitialPage();
            this.updateSearchStats(this.config.totalImages);
        },
        
        switchAlbum: function(albumName) {
            this.currentAlbum = albumName;
            this.currentPage = 0;
            const images = this.getCurrentImages();
            this.renderImages(images.slice(0, this.data.imagesPerPage));
            this.updatePageInfo();
        },
        
        updatePageInfo: function() {
            const pageInfo = document.getElementById('pageInfo');
            if (pageInfo) {
                const images = this.getCurrentImages();
                const totalPages = Math.ceil(images.length / this.config.imagesPerPage);
                const currentPage = Math.min(this.currentPage + 1, totalPages);
                pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
            }
        },
        
        showError: function(message) {
            const galleryGrid = document.getElementById('gallery-grid');
            if (galleryGrid) {
                galleryGrid.innerHTML = `<div class="alert alert-danger">${message}</div>`;
            }
        },
        
        updateSearchStats: function(count) {
            const stats = document.getElementById('searchResultsCount');
            if (stats) {
                stats.textContent = count;
            }
        },
        
        showLoadingIndicator: function() {
            const indicator = document.getElementById('loadingIndicator');
            if (indicator) {
                indicator.style.display = 'block';
            }
        },
        
        hideLoadingIndicator: function() {
            const indicator = document.getElementById('loadingIndicator');
            if (indicator) {
                indicator.style.display = 'none';
            }
        },
        
        hideLoadMoreButton: function() {
            const btn = document.getElementById('loadMoreBtn');
            if (btn) {
                btn.style.display = 'none';
            }
        },
        
        isNearBottom: function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;
            return scrollTop + windowHeight >= documentHeight - 500;
        },
        
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }
    };
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => LargeGallery.init());
    } else {
        LargeGallery.init();
    }
    
    // Export for global access
    window.LargeGallery = LargeGallery;
})();

