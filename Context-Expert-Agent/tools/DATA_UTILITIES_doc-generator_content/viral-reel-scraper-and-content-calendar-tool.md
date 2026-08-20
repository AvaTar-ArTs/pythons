---
title: Viral Reel Scraper and Content Calendar Tool
description: Conversation transcript.
tags:
- conversation
- deepseek
date: '2025-10-07'
updated: '2025-03-10T05:49:50.522000+08:00'
toc: true
---

# Viral Reel Scraper and Content Calendar Tool

## Transcript

_No messages found._


<details><summary>Raw Conversation JSON</summary>

```json
{
  "id": "b7e56948-a1b5-4ae5-aa23-526e371759d0",
  "title": "Viral Reel Scraper and Content Calendar Tool",
  "inserted_at": "2025-03-10T05:48:48.629000+08:00",
  "updated_at": "2025-03-10T05:49:50.522000+08:00",
  "mapping": {
    "root": {
      "id": "root",
      "parent": null,
      "children": [
        "1"
      ],
      "message": null
    },
    "1": {
      "id": "1",
      "parent": "root",
      "children": [
        "2"
      ],
      "message": {
        "files": [],
        "model": "deepseek-reasoner",
        "inserted_at": "2025-03-10T05:48:49.129000+08:00",
        "fragments": [
          {
            "type": "REQUEST",
            "content": "do some deep seo/keyword/tag researcg on tiktok/youtube/instagram so i can find the top rising trend hashtags and keys..\n\nAlso, if possible:\n I need to create a tool that pulls the top reels on Instagram for a certain search keyword, analyzes them, and creates a content calendar based on the insights from those reels.\n\nDetails blow\n\nPulling Viral Reels\n\nINPUT:\nSearch instagram keyword\nPull top 100 Reels based on views and engagement. These reels must be at least 90% organic views.\n\nCriteria for viral reels (this needs to be able to be changed)\n\nViews: 100K+\nLikes: 1K+\nShares: 100+\nComments: 100+\nViews geo: 75%+ US, CA, AUS, UK\nViews timeframe: 50% of views from last 30 days\nOUTPUT: Spreadsheet with this data in columns:\n\n(A) Video link\n\n(B) Views from last 30 days\n(C) Total Views\n(D) Total Likes\n(E) Total Shares\n(F) Total Comments\n\n(G) Video hook - you will use an OCR tool to pull the text that is visible during the first 1 seconds of the reel (e.g. text overlay). This the the ‘hook’\n\n(H) Reel style (b-roll, talking head, green screen, comedy, meme, reaction)\n\n(I) Screenshot of first 1s of video\n\n(J) Caption\n\nAnalyzing Viral Reels\n\nINPUT\nThen I will give input and tell you my brand and my audience and my instagram handle.  \nANALYZE From there I want you to use insights from the viral reels and recreate reels for me baed on the insights.\n\nAnalyze:\n\nHook\nCaption\nReel style (b-roll, talking head, green screen, comedy, meme, reaction)\nThematic video elements\nGeneral analysis of why this worked\nOUTPUT\nCreate 30 days of viral reels for my content based on the analysis.\n\n(A) Video link that was the inspiration\n(B) Reel Style\n(C)Video Hook\n(D) Entire Video Text overlay (if broll style)\n(C) Video Text Script (if talking head)\n\nI would like this for IG first, then we can re-hire for TikTok and other platforms. My goal is to build this + build a relationship with a developer for multiple projects!"
          }
        ]
      }
    },
    "2": {
      "id": "2",
      "parent": "1",
      "children": [],
      "message": {
        "files": [],
        "model": "deepseek-reasoner",
        "inserted_at": "2025-03-10T05:48:49.129000+08:00",
        "fragments": [
          {
            "type": "THINK",
            "content": "Okay, let's break down what the user is asking for. They want to do deep SEO/keyword/hashtag research on platforms like TikTok, YouTube, and Instagram to find rising trends. Then, they want a tool that pulls top Instagram Reels based on specific criteria and generates a content calendar from that analysis. \n\nFirst, I need to outline the steps for the SEO and keyword research part. For each platform, the methods might differ. For Instagram, hashtag research is crucial, while YouTube relies more on keywords and tags. TikTok uses trending sounds and challenges. I should mention tools like Instagram's native search, Keyword Tool, and third-party platforms like Hootsuite or Later for hashtag tracking. Also, TikTok's Creative Center and YouTube's Keyword Planner could be useful.\n\nNext, the tool development part. The user wants to scrape Instagram Reels with certain viral criteria. But Instagram's API is limited, so maybe using a third-party service or web scraping with Python libraries like Selenium or BeautifulSoup. However, they need to ensure the views are 90% organic, which complicates things. Maybe look into engagement metrics versus follower count to estimate organic reach. \n\nThe criteria for viral Reels are strict: views over 100K, likes 1K+, etc. The tool needs to filter based on these, which can be adjusted. The output is a spreadsheet with video links and various metrics. Then, using OCR for the video hook. Tesseract OCR with Python could work here, but processing the first second of the video would require frame extraction, maybe with OpenCV. \n\nFor the analysis part, once the data is collected, they need to analyze hooks, styles, captions, etc. Then, generating a content calendar based on these insights. The user wants 30 days of content ideas inspired by the top Reels. \n\nChallenges: Instagram's API limitations and data privacy issues. Web scraping might be against Instagram's terms, so they might need to use approved third-party tools. Also, ensuring the views are mostly organic could be tricky. Maybe checking if the account has a high follower count vs. views ratio. If a Reel has 100K views but the account only has 1K followers, it's more likely organic. \n\nThe tool would need to process each Reel, extract metadata, run OCR on the first frame, classify the style (maybe using a simple dropdown or ML model if possible), and compile everything into a spreadsheet. For the content calendar, the analysis would involve identifying common elements in successful Reels and adapting them to the user's brand. \n\nPotential developers would need expertise in Python, API integration, web scraping, OCR, and maybe frontend for a UI. They should also be aware of legal aspects regarding data scraping. \n\nI should also mention alternatives if building the tool is too complex, like using existing platforms like Hootsuite or Sprout Social for analytics, and Later for content calendaring. Maybe a hybrid approach using existing tools and custom scripts for specific tasks. \n\nFinally, the user wants a relationship with a developer for multiple projects, so scalability and maintainability of the tool are important. They might need a backend with a database to store scraped data, a frontend for inputting keywords and adjusting criteria, and automated reporting features."
          },
          {
            "type": "RESPONSE",
            "content": "Here's a structured plan to achieve your goals, including technical requirements, tools, and developer considerations:\n\n---\n\n### **Phase 1: Keyword/Hashtag Research for TikTok/YouTube/Instagram**\n#### **Tools & Methods**\n1. **Instagram**:\n   - Use Instagram’s native search (autocomplete suggestions for keywords/hashtags).\n   - Tools: Later, Hootsuite, Meta Business Suite, Keyword Tool (keywordtool.io), Display Purposes.\n   - Track rising hashtags with *RiteTag* or *Hashtagify*.\n\n2. **TikTok**:\n   - TikTok Creative Center (official trending data).\n   - Tools: Pentos, TrendTok, VidIQ, Exploding Topics.\n   - Analyze trending sounds/challenges in your niche.\n\n3. **YouTube**:\n   - YouTube Search Autocomplete & Trending Page.\n   - Tools: TubeBuddy, VidIQ, Google Trends, Ahrefs.\n   - Filter by \"Last 30 days\" to find rising trends.\n\n#### **Action Steps**:\n- Export keyword/hashtag lists and prioritize by search volume/competition.\n- Focus on hashtags with growing usage (e.g., #BookTok → #BookReviewTok).\n\n---\n\n### **Phase 2: Viral Reel Scraper & Analysis Tool**\n#### **Core Features**\n1. **Data Scraping**:\n   - Use **Python + Instagram API** (limited) or third-party tools like *Phantombuster* or *Apify*.\n   - Filter reels by:\n     - Views (100k+), likes (1k+), shares (100+), comments (100+).\n     - Geo-location (US/CA/AUS/UK) via proxy/IP filtering.\n     - 50%+ views from the last 30 days (use timestamp analysis).\n\n2. **OCR for Video Hooks**:\n   - Use **Tesseract OCR** (Python) or AWS Rekognition to extract text from the first 1 second of reels.\n   - Integrate with *OpenCV* for frame extraction.\n\n3. **Reel Style Classification**:\n   - Train a simple ML model (TensorFlow/PyTorch) to categorize styles (b-roll, talking head, etc.) or use manual tagging.\n\n4. **Output Spreadsheet**:\n   - Automate with Python libraries like *Pandas* and *OpenPyXL*.\n\n#### **Developer Requirements**:\n- Backend: Python (scraping, data analysis), API integration.\n- Frontend: Optional dashboard (React.js/Django).\n- Budget: $5k–$15k+ depending on complexity.\n\n---\n\n### **Phase 3: Content Calendar Generator**\n#### **Workflow**\n1. **Input Brand Details**:\n   - Audience demographics, brand voice, Instagram handle.\n\n2. **Analysis Engine**:\n   - Identify patterns in hooks, captions, and styles from scraped reels.\n   - Use NLP (e.g., spaCy) to analyze caption sentiment/CTAs.\n\n3. **Content Scripting**:\n   - Generate 30-day calendar with:\n     - Video concepts inspired by top reels.\n     - Customized hooks/scripts (e.g., \"5 Secrets to...\" if trending).\n     - Recommended posting times based on audience activity.\n\n#### **Output**:\n- Spreadsheet/PDF with daily reel ideas, scripts, and inspiration links.\n\n---\n\n### **Phase 4: Developer Hiring & Execution**\n#### **Hiring Tips**\n1. **Skills Needed**:\n   - Python (scraping, OCR, data analysis).\n   - Experience with Instagram API/TikTok API.\n   - Frontend (if building a dashboard).\n\n2. **Platforms**:\n   - Upwork, Toptal, or GitHub to find developers with portfolio projects in social media analytics.\n\n3. **MVP Approach**:\n   - Start with a basic scraper (proof of concept), then add OCR/ML features.\n\n#### **Cost-Saving Alternatives**:\n- Use no-code tools like *Zapier* + *Airtable* for manual analysis.\n- Leverage existing tools like Hootsuite (analytics) and Canva (content creation).\n\n---\n\n### **Example Output (Content Calendar)**\n| Day | Reel Style      | Hook Text             | Script Idea                          | Inspiration Link       |\n|-----|-----------------|-----------------------|--------------------------------------|------------------------|\n| 1   | B-Roll          | \"You’re doing it WRONG!\" | Show quick cuts of common mistakes + solutions. | [Link]                |\n| 2   | Talking Head    | \"I quit my 9-5 for this\" | Share a personal story with cuts to b-roll.     | [Link]                |\n\n---\n\n### **Next Steps**\n1. Start with Instagram scraper development.\n2. Hire a Python developer (post a job on Upwork with this spec).\n3. Test the MVP with 1-2 keywords before scaling.\n\nLet me know if you need help drafting a job post or evaluating developers!"
          }
        ]
      }
    }
  }
}
```
</details>
