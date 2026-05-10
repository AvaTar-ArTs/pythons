/**
 * Enhanced Main JavaScript for SimpleGallery with Content Awareness
 * Provides advanced filtering, search, and content analysis features
 */

class EnhancedGallery {
    constructor() {
        this.images = [];
        this.filteredImages = [];
        this.currentFilters = {
            search: '',
            type: '',
            quality: '',
            faces: '',
            sort: 'date-desc'
        };
        this.isLoading = false;
        this.viewMode = 'grid'; // 'grid' or 'list'
        
        this.init();
    }
    
    init() {
        this.loadImages();
        this.setupEventListeners();
        this.setupPhotoSwipe();
        this.analyzeContent();
        this.setupScrollEffects();
    }
    
    loadImages() {
        // Extract images from gallery items
        const galleryItems = document.querySelectorAll('.gallery-item');
        this.images = Array.from(galleryItems).map((item, index) => ({
            element: item,
            type: item.dataset.type,
            date: new Date(item.dataset.date),
            quality: parseFloat(item.dataset.quality) || 0,
            faces: item.dataset.faces === 'true',
            tags: item.dataset.tags ? item.dataset.tags.split(',') : [],
            description: item.dataset.description || '',
            src: item.dataset.src,
            width: parseInt(item.dataset.width),
            height: parseInt(item.dataset.height),
            thumbnail: item.dataset.thumbnail,
            thumbnailWidth: parseInt(item.dataset.thumbnailWidth),
            thumbnailHeight: parseInt(item.dataset.thumbnailHeight),
            index: index
        }));
        
        this.filteredImages = [...this.images];
        this.updateStats();
    }
    
    setupEventListeners() {
        // Search input
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.currentFilters.search = e.target.value.toLowerCase();
                this.applyFilters();
            });
        }
        
        // Filter selects
        const filterSelects = ['typeFilter', 'qualityFilter', 'faceFilter', 'sortFilter'];
        filterSelects.forEach(filterId => {
            const select = document.getElementById(filterId);
            if (select) {
                select.addEventListener('change', (e) => {
                    const filterKey = filterId.replace('Filter', '');
                    this.currentFilters[filterKey] = e.target.value;
                    this.applyFilters();
                });
            }
        });
        
        // Clear filters button
        const clearFiltersBtn = document.getElementById('clearFilters');
        if (clearFiltersBtn) {
            clearFiltersBtn.addEventListener('click', () => {
                this.clearFilters();
            });
        }
        
        // Floating action buttons
        const scrollToTopBtn = document.getElementById('scrollToTop');
        if (scrollToTopBtn) {
            scrollToTopBtn.addEventListener('click', () => {
                this.scrollToTop();
            });
        }
        
        const toggleFiltersBtn = document.getElementById('toggleFilters');
        if (toggleFiltersBtn) {
            toggleFiltersBtn.addEventListener('click', () => {
                this.toggleFilters();
            });
        }
        
        const toggleViewBtn = document.getElementById('toggleView');
        if (toggleViewBtn) {
            toggleViewBtn.addEventListener('click', () => {
                this.toggleView();
            });
        }
        
        // Gallery item clicks
        document.addEventListener('click', (e) => {
            const galleryItem = e.target.closest('.gallery-item');
            if (galleryItem) {
                e.preventDefault();
                this.openPhotoSwipe(galleryItem);
            }
        });
    }
    
    applyFilters() {
        this.showLoading();
        
        // Filter images based on current criteria
        this.filteredImages = this.images.filter(image => {
            // Search filter
            if (this.currentFilters.search) {
                const searchTerm = this.currentFilters.search.toLowerCase();
                const matchesSearch = 
                    image.description.toLowerCase().includes(searchTerm) ||
                    image.tags.some(tag => tag.toLowerCase().includes(searchTerm)) ||
                    image.element.textContent.toLowerCase().includes(searchTerm);
                if (!matchesSearch) return false;
            }
            
            // Type filter
            if (this.currentFilters.type && image.type !== this.currentFilters.type) {
                return false;
            }
            
            // Quality filter
            if (this.currentFilters.quality) {
                const qualityGrade = this.getQualityGrade(image.quality);
                if (this.currentFilters.quality === 'high' && !['A', 'B'].includes(qualityGrade)) {
                    return false;
                }
                if (this.currentFilters.quality === 'medium' && qualityGrade !== 'C') {
                    return false;
                }
                if (this.currentFilters.quality === 'low' && qualityGrade !== 'D') {
                    return false;
                }
            }
            
            // Face filter
            if (this.currentFilters.faces === 'with-faces' && !image.faces) {
                return false;
            }
            if (this.currentFilters.faces === 'no-faces' && image.faces) {
                return false;
            }
            
            return true;
        });
        
        // Sort images
        this.sortImages();
        
        // Update display
        this.updateDisplay();
        this.hideLoading();
    }
    
    sortImages() {
        const sortBy = this.currentFilters.sort;
        
        this.filteredImages.sort((a, b) => {
            switch (sortBy) {
                case 'date-desc':
                    return b.date - a.date;
                case 'date-asc':
                    return a.date - b.date;
                case 'quality-desc':
                    return b.quality - a.quality;
                case 'quality-asc':
                    return a.quality - b.quality;
                case 'name-asc':
                    return a.description.localeCompare(b.description);
                case 'name-desc':
                    return b.description.localeCompare(a.description);
                default:
                    return 0;
            }
        });
    }
    
    updateDisplay() {
        const galleryContainer = document.getElementById('galleryContainer');
        const noResults = document.getElementById('noResults');
        
        if (!galleryContainer) return;
        
        // Hide all images
        this.images.forEach(image => {
            image.element.style.display = 'none';
        });
        
        // Show filtered images
        this.filteredImages.forEach((image, index) => {
            image.element.style.display = 'block';
            image.element.style.order = index;
        });
        
        // Show/hide no results message
        if (noResults) {
            noResults.style.display = this.filteredImages.length === 0 ? 'block' : 'none';
        }
        
        // Update gallery container class for view mode
        if (this.viewMode === 'list') {
            galleryContainer.classList.add('list-view');
        } else {
            galleryContainer.classList.remove('list-view');
        }
    }
    
    updateStats() {
        // Update statistics in the header
        const totalImages = this.images.length;
        const photos = this.images.filter(img => img.type === 'image').length;
        const videos = this.images.filter(img => img.type === 'video').length;
        const withFaces = this.images.filter(img => img.faces).length;
        
        // Update stat numbers (if elements exist)
        this.updateStatNumber('total-images', totalImages);
        this.updateStatNumber('total-photos', photos);
        this.updateStatNumber('total-videos', videos);
        this.updateStatNumber('total-faces', withFaces);
    }
    
    updateStatNumber(statId, value) {
        const statElement = document.querySelector(`[data-stat="${statId}"]`);
        if (statElement) {
            statElement.textContent = value;
        }
    }
    
    clearFilters() {
        // Reset all filter inputs
        const searchInput = document.getElementById('searchInput');
        if (searchInput) searchInput.value = '';
        
        const filterSelects = ['typeFilter', 'qualityFilter', 'faceFilter', 'sortFilter'];
        filterSelects.forEach(filterId => {
            const select = document.getElementById(filterId);
            if (select) select.value = '';
        });
        
        // Reset filter state
        this.currentFilters = {
            search: '',
            type: '',
            quality: '',
            faces: '',
            sort: 'date-desc'
        };
        
        // Apply filters
        this.applyFilters();
    }
    
    toggleFilters() {
        const filterControls = document.querySelector('.filter-controls');
        if (filterControls) {
            filterControls.style.display = filterControls.style.display === 'none' ? 'block' : 'none';
        }
    }
    
    toggleView() {
        this.viewMode = this.viewMode === 'grid' ? 'list' : 'grid';
        this.updateDisplay();
        
        // Update button icon
        const toggleViewBtn = document.getElementById('toggleView');
        if (toggleViewBtn) {
            const icon = toggleViewBtn.querySelector('i');
            if (icon) {
                icon.className = this.viewMode === 'grid' ? 'fas fa-list' : 'fas fa-th';
            }
        }
    }
    
    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
    
    showLoading() {
        this.isLoading = true;
        const loadingSpinner = document.getElementById('loadingSpinner');
        if (loadingSpinner) {
            loadingSpinner.style.display = 'block';
        }
    }
    
    hideLoading() {
        this.isLoading = false;
        const loadingSpinner = document.getElementById('loadingSpinner');
        if (loadingSpinner) {
            loadingSpinner.style.display = 'none';
        }
    }
    
    getQualityGrade(score) {
        if (score >= 0.8) return 'A';
        if (score >= 0.6) return 'B';
        if (score >= 0.4) return 'C';
        return 'D';
    }
    
    analyzeContent() {
        // Analyze color palette
        this.analyzeColorPalette();
        
        // Analyze camera information
        this.analyzeCameraInfo();
        
        // Update content analysis sections
        this.updateContentAnalysis();
    }
    
    analyzeColorPalette() {
        const colorPalette = document.getElementById('colorPalette');
        if (!colorPalette) return;
        
        // Extract dominant colors from all images
        const allColors = [];
        this.images.forEach(image => {
            // This would normally come from the enhanced metadata
            // For now, we'll generate some sample colors
            const sampleColors = [
                { hex: '#3B82F6', percentage: 25 },
                { hex: '#10B981', percentage: 20 },
                { hex: '#F59E0B', percentage: 15 },
                { hex: '#EF4444', percentage: 12 },
                { hex: '#8B5CF6', percentage: 10 }
            ];
            allColors.push(...sampleColors);
        });
        
        // Sort by percentage and take top 5
        const topColors = allColors
            .sort((a, b) => b.percentage - a.percentage)
            .slice(0, 5);
        
        // Create color swatches
        colorPalette.innerHTML = topColors.map(color => 
            `<div class="color-swatch" style="background-color: ${color.hex};" title="${color.hex} (${color.percentage}%)"></div>`
        ).join('');
    }
    
    analyzeCameraInfo() {
        const cameraInfo = document.getElementById('cameraInfo');
        if (!cameraInfo) return;
        
        // Sample camera information
        const cameraData = [
            'iPhone 13 Pro: 45%',
            'Canon EOS R5: 25%',
            'Sony A7R IV: 15%',
            'Samsung Galaxy S21: 10%',
            'Other: 5%'
        ];
        
        cameraInfo.innerHTML = cameraData.map(info => `<li>${info}</li>`).join('');
    }
    
    updateContentAnalysis() {
        // Update various content analysis sections
        this.updateFaceAnalysis();
        this.updateQualityDistribution();
        this.updateSceneAnalysis();
    }
    
    updateFaceAnalysis() {
        const faceCount = this.images.filter(img => img.faces).length;
        const totalFaces = this.images.reduce((sum, img) => sum + (img.faces ? 1 : 0), 0);
        const facePercentage = this.images.length > 0 ? (faceCount / this.images.length * 100).toFixed(1) : 0;
        
        // Update face analysis display
        const faceElements = document.querySelectorAll('[data-face-count]');
        faceElements.forEach(el => {
            el.textContent = faceCount;
        });
        
        const facePercentageElements = document.querySelectorAll('[data-face-percentage]');
        facePercentageElements.forEach(el => {
            el.textContent = `${facePercentage}%`;
        });
    }
    
    updateQualityDistribution() {
        const qualityGrades = { A: 0, B: 0, C: 0, D: 0 };
        
        this.images.forEach(image => {
            const grade = this.getQualityGrade(image.quality);
            qualityGrades[grade]++;
        });
        
        // Update quality distribution display
        Object.entries(qualityGrades).forEach(([grade, count]) => {
            const percentage = this.images.length > 0 ? (count / this.images.length * 100).toFixed(1) : 0;
            const elements = document.querySelectorAll(`[data-quality-${grade.toLowerCase()}]`);
            elements.forEach(el => {
                el.textContent = `${count} (${percentage}%)`;
            });
        });
    }
    
    updateSceneAnalysis() {
        // Analyze scene categories
        const sceneCategories = {};
        this.images.forEach(image => {
            image.tags.forEach(tag => {
                sceneCategories[tag] = (sceneCategories[tag] || 0) + 1;
            });
        });
        
        // Update scene analysis display
        const topScenes = Object.entries(sceneCategories)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 5);
        
        const sceneElements = document.querySelectorAll('[data-scene-analysis]');
        sceneElements.forEach(el => {
            el.innerHTML = topScenes.map(([scene, count]) => 
                `<li>${scene}: ${count} images</li>`
            ).join('');
        });
    }
    
    setupPhotoSwipe() {
        // Initialize PhotoSwipe
        this.slides = {};
        this.createSlides();
        
        // Bind click events
        document.addEventListener('click', (e) => {
            const galleryItem = e.target.closest('.gallery-item');
            if (galleryItem) {
                e.preventDefault();
                this.openPhotoSwipe(galleryItem);
            }
        });
    }
    
    createSlides() {
        this.images.forEach((image, photoId) => {
            const slide = {
                w: image.width,
                h: image.height,
                msrc: image.thumbnail,
                title: image.description,
                date: image.date.toLocaleDateString(),
            };

            if (image.type === 'image') {
                slide.src = image.src;
            } else {
                slide.html = `<video style="margin: 0px auto; height: 100%; max-width: 100%; max-height: 100%; display: block" 
                    data-index="${photoId}" controls>
                    <source src="${image.src}" type="video/mp4">
                </video>`;
            }

            const galleryId = 0; // Single gallery
            if (!(galleryId in this.slides)) {
                this.slides[galleryId] = [];
            }

            this.slides[galleryId].push(slide);
        });
    }
    
    openPhotoSwipe(galleryItem) {
        const index = parseInt(galleryItem.dataset.index) || 0;
        const galleryId = 0;
        
        const options = {
            index: index,
            getThumbBoundsFn: (id) => this.getThumbBounds(galleryId, id),
            addCaptionHTMLFn: this.addCaptionHTML,
            preload: [2, 5],
            zoomEl: false,
            shareEl: true,
            barsSize: { top: 0, bottom: 0 },
            bgOpacity: 1,
            loop: false,
            mainClass: 'pswp--minimal--dark',
            shareButtons: [
                { id: 'download', label: 'Download image', url: '{{raw_image_url}}', download: true }
            ],
        };

        const gallery = new PhotoSwipe(document.querySelector('.pswp'), PhotoSwipeUI_Default, this.slides[galleryId], options);

        gallery.listen('initialZoomOut', function() {
            if (this.currItem.html) {
                const videos = document.querySelectorAll(`div.pswp__item video[data-index=${this.getCurrentIndex()}]`);
                if (videos.length > 0) {
                    videos[0].pause();
                }
            }
        });

        gallery.listen('afterChange', function() {
            const videos = document.querySelectorAll('div.pswp__item video');
            for (let i = 0; i < videos.length; ++i) {
                videos[i].pause();
            }

            if (this.currItem.html) {
                const videos = document.querySelectorAll(`div.pswp__item video[data-index=${this.getCurrentIndex()}]`);
                if (videos.length > 0) {
                    videos[0].play();
                }
            }
        });

        gallery.init();
    }
    
    getThumbBounds(gallery, index) {
        const thumbnail = document.querySelector(`div.gallery-item[data-index="${index}"]`);
        if (!thumbnail) return { x: 0, y: 0, w: 0 };
        
        const pageYScroll = window.pageYOffset || document.documentElement.scrollTop;
        const rect = thumbnail.getBoundingClientRect();
        return { x: rect.left, y: rect.top + pageYScroll, w: rect.width };
    }
    
    addCaptionHTML(item, captionEl, isFake) {
        if (!item.title && !item.date) {
            captionEl.children[0].innerText = '';
            return false;
        }
        captionEl.children[0].innerHTML = item.title;
        if (item.date) {
            captionEl.children[0].innerHTML += `<p class="caption-date">${item.date}</p>`;
        }
        return true;
    }
    
    setupScrollEffects() {
        // Navbar scroll effect
        let lastScrollTop = 0;
        const navbar = document.querySelector('.enhanced-navbar');
        
        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (navbar) {
                if (scrollTop > 100) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
            }
            
            // Show/hide floating buttons
            const floatingActions = document.querySelector('.floating-actions');
            if (floatingActions) {
                if (scrollTop > 300) {
                    floatingActions.style.opacity = '1';
                    floatingActions.style.visibility = 'visible';
                } else {
                    floatingActions.style.opacity = '0';
                    floatingActions.style.visibility = 'hidden';
                }
            }
            
            lastScrollTop = scrollTop;
        });
        
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
}

// Initialize the enhanced gallery when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EnhancedGallery();
});

// Additional utility functions
function debounce(func, wait) {
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

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = EnhancedGallery;
}