# Index.html Analysis & Issues Found

**File:** `/Users/steven/simplegallery/index.html`  
**Date:** 2024-11-25

---

## 🐛 Critical Issues Found

### 1. **Incorrect CSS Paths** 🔴 CRITICAL
**Lines 18-20:**
```html
<link rel="stylesheet" href="data/public/css/photoswipe.css">
<link rel="stylesheet" href="data/public/css/default-skin.css">
<link rel="stylesheet" href="data/public/css/main.css">
```

**Problem:** Paths should be relative to `public/` directory, not include `data/public/`

**Expected:**
```html
<link rel="stylesheet" href="css/photoswipe.css">
<link rel="stylesheet" href="css/default-skin.css">
<link rel="stylesheet" href="css/main.css">
```

---

### 2. **Incorrect HTML Structure** 🔴 CRITICAL
**Lines 58-75:**
```html
<div class="container-fluid">
    <div class="row">
        <div class="col gallery-section">
            <div class="container-fluid">  <!-- ❌ NESTED - WRONG -->
                <div class="row">          <!-- ❌ NESTED - WRONG -->
                    <div class="col gallery-section">  <!-- ❌ NESTED - WRONG -->
                        <h2>DiScO</h2>
                        <p></p>  <!-- ❌ EMPTY DESCRIPTION -->
                    </div>
                </div>
                <div class="row">
                    <div class="col gallery">
                        <!-- Only ONE image shown -->
                    </div>
                </div>
            </div>
            <!-- PhotoSwipe and footer nested inside - WRONG -->
```

**Problem:** 
- Double-nested container-fluid and row
- Gallery section macro is creating nested structure
- PhotoSwipe and footer should be at body level, not inside gallery-section

**Expected Structure:**
```html
<div class="container-fluid">
    <div class="row">
        <div class="col gallery-section">
            <h2>Title</h2>
            <!-- Gallery images here -->
        </div>
    </div>
</div>
<!-- PhotoSwipe at body level -->
<!-- Footer at body level -->
```

---

### 3. **Empty Description** 🟡 MEDIUM
**Line 65:**
```html
<p></p>
```

**Problem:** Description is empty. Should show parent folder name (e.g., `01_ideogram_designs`)

**Expected:**
```html
<p>01_ideogram_designs</p>
```

---

### 4. **Only One Image Displayed** 🟡 MEDIUM
**Lines 68-74:**
```html
<div class="row">
    <div class="col gallery">
        <a href="images/photos/02.jpg" ...>
            <!-- Only one image -->
        </a>
    </div>
</div>
```

**Problem:** Only showing one image instead of all images in the gallery

**Possible Causes:**
- Only one image in `images_data.json`
- Gallery macro not iterating correctly
- Template rendering issue

---

### 5. **PhotoSwipe & Footer Nested Incorrectly** 🔴 CRITICAL
**Lines 78-117:**
```html
<div class="col gallery-section">
    <!-- ... gallery content ... -->
    <div class="pswp">...</div>  <!-- ❌ Should be at body level -->
    <footer>...</footer>          <!-- ❌ Should be at body level -->
</div>
```

**Problem:** PhotoSwipe container and footer are nested inside gallery-section instead of being siblings at body level

---

### 6. **Scripts Nested Incorrectly** 🔴 CRITICAL
**Lines 119-173:**
```html
<div class="col gallery-section">
    <!-- ... -->
    <script>...</script>  <!-- ❌ Should be at body level -->
</div>
```

**Problem:** Scripts are inside gallery-section div instead of at body level before closing `</body>`

---

## ✅ Template vs Generated HTML

### Template (Correct)
```jinja
<div class="container-fluid">
    <div class="row">
        <div class="col gallery-section">
            <h2>{{ gallery_config.title }}</h2>
            {{ gallery_macros.section(...) }}
        </div>
    </div>
</div>
<!-- PhotoSwipe at body level -->
<!-- Footer at body level -->
<!-- Scripts at body level -->
```

### Generated HTML (Incorrect)
- Has nested structure
- PhotoSwipe/footer/scripts inside gallery-section
- CSS paths wrong

---

## 🔧 Root Cause Analysis

The `gallery_macros.section()` macro creates its own `container-fluid` and `row`, which causes nesting when called from within another container-fluid/row structure.

**Current Macro:**
```jinja
{% macro section(...) -%}
  <div class="container-fluid">  <!-- Creates nesting -->
    <div class="row">
      ...
    </div>
  </div>
{%- endmacro %}
```

**Template calls it inside:**
```jinja
<div class="container-fluid">  <!-- Already has container -->
    <div class="row">
        <div class="col gallery-section">
            {{ gallery_macros.section(...) }}  <!-- Creates nested container -->
        </div>
    </div>
</div>
```

---

## 💡 Solutions

### Option 1: Fix the Macro (Recommended)
Create a version that doesn't add container-fluid if already in one.

### Option 2: Fix the Template
Remove the outer container-fluid/row and let the macro handle it.

### Option 3: Create New Macro
Create `section_inline()` that doesn't add container structure.

---

## 🎯 Recommended Fix

Update the template to not nest containers, or update the macro to detect nesting.

**Best Solution:** Update template to match the macro's structure:

```jinja
{# Let the macro handle the container structure #}
{{ gallery_macros.section(0, images|length, gallery_config['title'], gallery_config.get('description', ''), images) }}
```

And remove the outer container-fluid/row wrapper.

---

*End of Analysis*

