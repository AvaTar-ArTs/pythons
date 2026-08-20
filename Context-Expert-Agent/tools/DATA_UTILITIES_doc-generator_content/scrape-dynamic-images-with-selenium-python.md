---
title: Scrape Dynamic Images with Selenium Python
description: Conversation transcript.
tags:
- conversation
- deepseek
date: '2025-10-07'
updated: '2025-06-10T18:56:23.610000+08:00'
toc: true
---

# Scrape Dynamic Images with Selenium Python

## Transcript

_No messages found._


<details><summary>Raw Conversation JSON</summary>

```json
{
  "id": "23375148-4a0f-4a11-ba3b-196167518c46",
  "title": "Scrape Dynamic Images with Selenium Python",
  "inserted_at": "2025-06-10T18:55:20.195000+08:00",
  "updated_at": "2025-06-10T18:56:23.610000+08:00",
  "mapping": {
    "root": {
      "id": "root",
      "parent": null,
      "children": [
        "3"
      ],
      "message": null
    },
    "3": {
      "id": "3",
      "parent": "root",
      "children": [
        "4"
      ],
      "message": {
        "files": [],
        "model": "deepseek-reasoner",
        "inserted_at": "2025-06-10T18:55:21.427000+08:00",
        "fragments": [
          {
            "type": "REQUEST",
            "content": "for https://mydesigns.io/dream {as in ALL we scroll the html to load the {<img class=\"object-cover object-center transition-all duration-500 group-hover:scale-105\" crossorigin=\"anonymous\" alt=\"Vibrant Fishing Graphic Design\" loading=\"lazy\" src=\"https://cdn.mydesigns.io/dynamic-thumbnail/7b2270617468223a22657874656e73696f6e2f647265616d65722f696d6167652f64303736323863392d343839352d346462362d616331642d3561313137313934616338632e706e67222c227769647468223a3830302c2274797065223a22696d6167652f61766966227d.avif\">} from src=\"([^\"]+) to scrape and copy to csv || https://mydesigns.io/dream?category=Art&filterBy=MOST_LIKES"
          }
        ]
      }
    },
    "4": {
      "id": "4",
      "parent": "3",
      "children": [],
      "message": {
        "files": [],
        "model": "deepseek-reasoner",
        "inserted_at": "2025-06-10T18:55:21.427000+08:00",
        "fragments": [
          {
            "type": "THINK",
            "content": "We are going to scrape the website https://mydesigns.io/dream?category=Art&filterBy=MOST_LIKES\n The images are loaded dynamically as we scroll. We'll use Selenium to simulate scrolling and wait for images to load.\n Steps:\n 1. Set up Selenium with a web driver (we'll use Chrome) and headless mode for efficiency.\n 2. Navigate to the URL.\n 3. Scroll to the bottom of the page repeatedly to load all images.\n 4. Parse the page source to extract image URLs from the `src` attribute of the <img> tags with the given class.\n 5. Write the image URLs to a CSV file.\n\n Note: The image elements have a class that includes \"object-cover\", and we are looking for the `src` attribute.\n\n However, note that the example image element uses a `src` attribute that points to a .avif image. We want to capture the actual image source.\n\n Let's look at the example: \n   <img ... src=\"https://cdn.mydesigns.io/dynamic-thumbnail/...avif\">\n\n We are going to extract all such `src` values.\n\n Since the page uses lazy loading, we need to wait for images to appear as we scroll.\n\n We'll use:\n   - WebDriverWait to wait for the presence of elements.\n   - We'll scroll in steps and wait for new content to load.\n\n Plan for scrolling:\n   - We'll scroll to the bottom, wait for new images to load, then scroll again until no new images are loaded.\n\n Let's code accordingly."
          },
          {
            "type": "RESPONSE",
            "content": "To scrape the dynamically loaded images from the infinite-scrolling page at `https://mydesigns.io/dream?category=Art&filterBy=MOST_LIKES`, follow this Python solution using Selenium and BeautifulSoup:\n\n```python\nimport csv\nfrom selenium import webdriver\nfrom selenium.webdriver.common.by import By\nfrom selenium.webdriver.support.ui import WebDriverWait\nfrom selenium.webdriver.support import expected_conditions as EC\nfrom bs4 import BeautifulSoup\nimport time\n\n# Configure Selenium WebDriver\noptions = webdriver.ChromeOptions()\noptions.add_argument(\"--headless=new\")  # Run in headless mode\ndriver = webdriver.Chrome(options=options)\n\nurl = \"https://mydesigns.io/dream?category=Art&filterBy=MOST_LIKES\"\ndriver.get(url)\n\n# Initialize variables for scrolling\nlast_height = driver.execute_script(\"return document.body.scrollHeight\")\nimage_urls = set()\nscroll_attempts = 0\nmax_attempts = 5  # Stop after 5 consecutive scrolls without new content\n\nprint(\"Starting scraping...\")\nwhile scroll_attempts < max_attempts:\n    # Scroll to bottom\n    driver.execute_script(\"window.scrollTo(0, document.body.scrollHeight);\")\n    time.sleep(2)  # Allow time for new images to load\n    \n    # Parse current page source with BeautifulSoup\n    soup = BeautifulSoup(driver.page_source, 'html.parser')\n    \n    # Find all target image elements\n    images = soup.find_all('img', {\n        'class': 'object-cover object-center transition-all duration-500 group-hover:scale-105',\n        'crossorigin': 'anonymous',\n        'loading': 'lazy'\n    })\n    \n    # Extract new image URLs\n    new_count = 0\n    for img in images:\n        src = img.get('src')\n        if src and src not in image_urls:\n            image_urls.add(src)\n            new_count += 1\n    \n    print(f\"Found {new_count} new images (Total: {len(image_urls)})\")\n    \n    # Check if reached bottom\n    new_height = driver.execute_script(\"return document.body.scrollHeight\")\n    if new_height == last_height:\n        scroll_attempts += 1\n    else:\n        scroll_attempts = 0\n    last_height = new_height\n\ndriver.quit()\n\n# Save results to CSV\nwith open('dream_images.csv', 'w', newline='') as csvfile:\n    writer = csv.writer(csvfile)\n    writer.writerow(['Image_URL'])\n    for url in image_urls:\n        writer.writerow([url])\n\nprint(f\"Scraping complete! Saved {len(image_urls)} image URLs to dream_images.csv\")\n```\n\n### Key Features:\n1. **Dynamic Scrolling**: Automatically scrolls to the bottom of the page until no new content loads\n2. **Headless Browser**: Uses Chrome in headless mode for efficiency\n3. **Duplicate Prevention**: Tracks unique image URLs using a set\n4. **Failure Safeguard**: Stops after 5 consecutive scrolls without new content\n5. **CSV Output**: Saves all image URLs in a clean CSV format\n\n### Requirements:\n- Install required packages:\n  ```bash\n  pip install selenium beautifulsoup4 webdriver-manager\n  ```\n- Chrome browser must be installed\n\n### Output:\nThe script generates a `dream_images.csv` file containing all scraped image URLs in this format:\n```\nImage_URL\nhttps://cdn.mydesigns.io/dynamic-thumbnail/...1.avif\nhttps://cdn.mydesigns.io/dynamic-thumbnail/...2.avif\n...\n```\n\n### Customization Options:\n1. **Adjust scrolling behavior**:\n   - Modify `time.sleep(2)` to change loading wait time\n   - Change `max_attempts` to alter scroll termination sensitivity\n2. **Add explicit waits** (if needed):\n   ```python\n   WebDriverWait(driver, 10).until(\n       EC.presence_of_element_located((By.CSS_SELECTOR, \"img[loading='lazy']\"))\n   )\n   ```\n3. **Filter specific URLs**:\n   ```python\n   # Add inside the image extraction loop:\n   if \".avif\" in src:  # Only keep AVIF format\n   ```\n\nThis solution handles the dynamic loading of images through infinite scrolling and efficiently captures all target image URLs while avoiding duplicates."
          }
        ]
      }
    }
  }
}
```
</details>
