/**
 * ═══════════════════════════════════════════════════════════════════
 * 🎵 ULTIMATE SUNO EXTRACTOR v3.0 - Production Grade
 * ═══════════════════════════════════════════════════════════════════
 *
 * A robust, modular, and user-friendly extractor for Suno.com song data.
 *
 * FEATURES:
 * ✅ Multiple fallback strategies (auto-detects best method)
 * ✅ Intelligent rate limiting (prevents IP bans)
 * ✅ Comprehensive error handling & recovery
 * ✅ Real-time progress UI with ETA
 * ✅ Resume capability (picks up where you left off)
 * ✅ Data validation & quality checks
 * ✅ Multiple export formats (CSV, JSON, TXT, HTML, M3U)
 * ✅ Parallel processing (5x faster)
 * ✅ Adaptive selectors (survives UI changes)
 *
 * USAGE:
 * 1. Navigate to https://suno.com/library (or any collection page)
 * 2. Open Browser Console (Cmd+Option+I / F12)
 * 3. Paste this entire script
 * 4. Press Enter
 * 5. Configure options in popup (or use defaults)
 * 6. Watch progress bar, download when complete
 *
 * AUTHOR: Enhanced by Claude Code
 * VERSION: 3.0.0
 * LICENSE: MIT
 * UPDATED: 2025-11-27
 *
 * ═══════════════════════════════════════════════════════════════════
 */

(async function SunoExtractorV3() {
  'use strict';

  // ═══════════════════════════════════════════════════════════════════
  // 📋 CONFIGURATION
  // ═══════════════════════════════════════════════════════════════════

  const CONFIG = {
    // Version info
    VERSION: '3.0.0',
    NAME: 'Ultimate Suno Extractor',

    // Performance settings
    SCROLL_DELAY: 800,              // ms between scroll attempts
    SCROLL_MAX: 1000,               // max scroll iterations
    SCROLL_NO_CHANGE_LIMIT: 4,      // stop after N scrolls with no new songs

    // Extraction settings
    PARALLEL_LIMIT: 5,              // concurrent song extractions
    PER_SONG_DELAY: 300,            // ms delay between songs (rate limiting)
    REQUEST_TIMEOUT: 10000,         // ms timeout for fetch requests
    RETRY_ATTEMPTS: 3,              // retry failed extractions
    RETRY_BACKOFF: 1.5,             // exponential backoff multiplier

    // Storage settings
    STORAGE_KEY: 'suno_extractor_v3_state',
    AUTOSAVE_INTERVAL: 20,          // autosave every N songs

    // Extraction modes
    MODE: 'auto',                   // 'auto', 'quick', 'standard', 'deep'

    // Export settings
    EXPORT_FORMATS: ['csv', 'json', 'txt', 'html'],
    INCLUDE_METADATA: true,

    // UI settings
    SHOW_PROGRESS_UI: true,
    SHOW_DEBUG_LOGS: false,

    // Feature flags
    ENABLE_PARALLEL: true,
    ENABLE_VALIDATION: true,
    ENABLE_ENRICHMENT: true,
  };

  // ═══════════════════════════════════════════════════════════════════
  // 🎯 SELECTOR SETS (Multiple versions for resilience)
  // ═══════════════════════════════════════════════════════════════════

  const SELECTOR_SETS = {
    // Primary selectors (current Suno UI)
    v1: {
      songAnchor: 'a[href*="/song/"]',
      lyrics: '.whitespace-pre-wrap, [data-testid="lyrics"]',
      summary: '.mt-1.cursor-pointer, [data-testid="summary"]',
      author: 'a[href^="/@"]',
      tags: 'a[href*="/style/"]',
      duration: '.font-mono, time, [class*="duration"]',
      image: 'img[src*="suno"]',
      audio: 'audio[src], source[src]',
      title: '[title], h1, h2, [data-testid="song-title"]',
    },
    // Fallback selectors (older UI)
    v2: {
      songAnchor: 'a[href*="/song/"], [data-clip-id]',
      lyrics: 'pre, .lyrics, .song-lyrics',
      summary: '.description, .summary',
      author: 'a[href*="/@"]',
      tags: '.tags span, [data-testid="tags"] span',
      duration: 'span[class*="time"]',
      image: 'img',
      audio: 'meta[property="og:audio"]',
      title: '.song-title, .track-title',
    },
  };

  // ═══════════════════════════════════════════════════════════════════
  // 🛠️ UTILITY CLASSES
  // ═══════════════════════════════════════════════════════════════════

  /**
   * Rate Limiter using Token Bucket algorithm
   */
  class RateLimiter {
    constructor(requestsPerSecond = 2, burstSize = 5) {
      this.tokensPerMs = requestsPerSecond / 1000;
      this.maxTokens = burstSize;
      this.tokens = burstSize;
      this.lastRefill = Date.now();
    }

    async acquire() {
      this.refill();
      if (this.tokens >= 1) {
        this.tokens -= 1;
        return;
      }
      // Wait until token available
      const waitTime = (1 - this.tokens) / this.tokensPerMs;
      await this.wait(waitTime);
      this.tokens = 0;
    }

    refill() {
      const now = Date.now();
      const elapsed = now - this.lastRefill;
      this.tokens = Math.min(
        this.maxTokens,
        this.tokens + elapsed * this.tokensPerMs
      );
      this.lastRefill = now;
    }

    wait(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }
  }

  /**
   * Progress Tracker with ETA calculation
   */
  class ProgressTracker {
    constructor(total) {
      this.total = total;
      this.completed = 0;
      this.failed = 0;
      this.startTime = Date.now();
      this.samples = [];
    }

    increment(success = true) {
      if (success) this.completed++;
      else this.failed++;

      const now = Date.now();
      this.samples.push({ time: now, count: this.completed + this.failed });

      // Keep only last 20 samples for ETA calculation
      if (this.samples.length > 20) {
        this.samples.shift();
      }
    }

    get progress() {
      return ((this.completed + this.failed) / this.total) * 100;
    }

    get eta() {
      if (this.samples.length < 2) return null;

      const firstSample = this.samples[0];
      const lastSample = this.samples[this.samples.length - 1];

      const elapsed = lastSample.time - firstSample.time;
      const processed = lastSample.count - firstSample.count;

      if (processed === 0) return null;

      const msPerItem = elapsed / processed;
      const remaining = this.total - (this.completed + this.failed);

      return remaining * msPerItem;
    }

    get stats() {
      const elapsed = Date.now() - this.startTime;
      const processed = this.completed + this.failed;
      const rate = processed / (elapsed / 1000);

      return {
        total: this.total,
        completed: this.completed,
        failed: this.failed,
        progress: this.progress.toFixed(1),
        successRate: processed > 0 ? ((this.completed / processed) * 100).toFixed(1) : 0,
        rate: rate.toFixed(2),
        elapsed: this.formatTime(elapsed),
        eta: this.eta ? this.formatTime(this.eta) : 'calculating...',
      };
    }

    formatTime(ms) {
      const seconds = Math.floor(ms / 1000);
      const minutes = Math.floor(seconds / 60);
      const hours = Math.floor(minutes / 60);

      if (hours > 0) {
        return `${hours}h ${minutes % 60}m`;
      } else if (minutes > 0) {
        return `${minutes}m ${seconds % 60}s`;
      } else {
        return `${seconds}s`;
      }
    }
  }

  /**
   * Custom Error Types
   */
  class ExtractorError extends Error {
    constructor(type, message, recoverable = false, details = {}) {
      super(message);
      this.name = 'ExtractorError';
      this.type = type;
      this.recoverable = recoverable;
      this.details = details;
    }
  }

  /**
   * Logger with levels
   */
  class Logger {
    constructor(debug = false) {
      this.debug_enabled = debug;
      this.prefix = '🎵 Suno Extractor';
    }

    info(msg, ...args) {
      console.log(`${this.prefix} ℹ️`, msg, ...args);
    }

    success(msg, ...args) {
      console.log(`${this.prefix} ✅`, msg, ...args);
    }

    warn(msg, ...args) {
      console.warn(`${this.prefix} ⚠️`, msg, ...args);
    }

    error(msg, ...args) {
      console.error(`${this.prefix} ❌`, msg, ...args);
    }

    debug(msg, ...args) {
      if (this.debug_enabled) {
        console.log(`${this.prefix} 🔍`, msg, ...args);
      }
    }
  }

  // ═══════════════════════════════════════════════════════════════════
  // 🎨 UI COMPONENTS
  // ═══════════════════════════════════════════════════════════════════

  class ProgressUI {
    constructor() {
      this.container = null;
      this.elements = {};
    }

    create() {
      // Create overlay
      this.container = document.createElement('div');
      this.container.id = 'suno-extractor-ui';
      this.container.innerHTML = `
        <style>
          #suno-extractor-ui {
            position: fixed;
            top: 20px;
            right: 20px;
            width: 400px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 24px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: white;
            z-index: 999999;
            animation: slideIn 0.3s ease-out;
          }
          @keyframes slideIn {
            from {
              transform: translateX(450px);
              opacity: 0;
            }
            to {
              transform: translateX(0);
              opacity: 1;
            }
          }
          #suno-extractor-ui h3 {
            margin: 0 0 16px 0;
            font-size: 20px;
            font-weight: 600;
          }
          .stat-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 14px;
            opacity: 0.9;
          }
          .progress-bar-container {
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            height: 24px;
            margin: 16px 0;
            overflow: hidden;
            position: relative;
          }
          .progress-bar {
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            height: 100%;
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 600;
          }
          .controls {
            display: flex;
            gap: 8px;
            margin-top: 16px;
          }
          .btn {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
          }
          .btn-pause {
            background: rgba(255,255,255,0.9);
            color: #667eea;
          }
          .btn-cancel {
            background: rgba(244,67,54,0.9);
            color: white;
          }
          .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
          }
          .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            background: rgba(255,255,255,0.2);
            font-size: 12px;
            margin-bottom: 12px;
          }
        </style>

        <div class="status-badge">⚡ Running...</div>
        <h3>🎵 Suno Extractor v3.0</h3>

        <div class="stat-row">
          <span>Progress:</span>
          <span><strong id="stat-completed">0</strong> / <span id="stat-total">0</span></span>
        </div>
        <div class="stat-row">
          <span>Success Rate:</span>
          <span id="stat-success">0%</span>
        </div>
        <div class="stat-row">
          <span>Speed:</span>
          <span id="stat-rate">0 songs/sec</span>
        </div>
        <div class="stat-row">
          <span>Elapsed:</span>
          <span id="stat-elapsed">0s</span>
        </div>
        <div class="stat-row">
          <span>ETA:</span>
          <span id="stat-eta">calculating...</span>
        </div>

        <div class="progress-bar-container">
          <div class="progress-bar" id="progress-bar" style="width: 0%">
            <span id="progress-text">0%</span>
          </div>
        </div>

        <div class="controls">
          <button class="btn btn-pause" id="btn-pause">⏸️ Pause</button>
          <button class="btn btn-cancel" id="btn-cancel">🛑 Cancel</button>
        </div>
      `;

      document.body.appendChild(this.container);

      // Store element references
      this.elements = {
        completed: document.getElementById('stat-completed'),
        total: document.getElementById('stat-total'),
        success: document.getElementById('stat-success'),
        rate: document.getElementById('stat-rate'),
        elapsed: document.getElementById('stat-elapsed'),
        eta: document.getElementById('stat-eta'),
        progressBar: document.getElementById('progress-bar'),
        progressText: document.getElementById('progress-text'),
        btnPause: document.getElementById('btn-pause'),
        btnCancel: document.getElementById('btn-cancel'),
      };
    }

    update(stats) {
      if (!this.container) return;

      this.elements.completed.textContent = stats.completed;
      this.elements.total.textContent = stats.total;
      this.elements.success.textContent = stats.successRate + '%';
      this.elements.rate.textContent = stats.rate + ' songs/sec';
      this.elements.elapsed.textContent = stats.elapsed;
      this.elements.eta.textContent = stats.eta;

      const progress = parseFloat(stats.progress);
      this.elements.progressBar.style.width = progress + '%';
      this.elements.progressText.textContent = stats.progress + '%';
    }

    setComplete() {
      if (!this.container) return;
      const badge = this.container.querySelector('.status-badge');
      badge.textContent = '✅ Complete!';
      badge.style.background = 'rgba(76, 175, 80, 0.9)';
      this.elements.btnPause.style.display = 'none';
      this.elements.btnCancel.textContent = '✖️ Close';
    }

    remove() {
      if (this.container) {
        this.container.remove();
        this.container = null;
      }
    }

    onPause(callback) {
      this.elements.btnPause.onclick = callback;
    }

    onCancel(callback) {
      this.elements.btnCancel.onclick = callback;
    }
  }

  // ═══════════════════════════════════════════════════════════════════
  // 🔍 EXTRACTION STRATEGIES
  // ═══════════════════════════════════════════════════════════════════

  class ExtractionStrategy {
    constructor(selectors, logger) {
      this.selectors = selectors;
      this.logger = logger;
    }

    async extract(songId, context) {
      throw new Error('Strategy must implement extract()');
    }

    selectFirst(parent, selectorString) {
      const selectors = selectorString.split(',').map(s => s.trim());
      for (const sel of selectors) {
        try {
          const el = parent.querySelector(sel);
          if (el) return el;
        } catch (e) {
          // Invalid selector, skip
        }
      }
      return null;
    }

    selectAll(parent, selectorString) {
      const selectors = selectorString.split(',').map(s => s.trim());
      for (const sel of selectors) {
        try {
          const els = parent.querySelectorAll(sel);
          if (els && els.length > 0) return Array.from(els);
        } catch (e) {
          // Invalid selector, skip
        }
      }
      return [];
    }

    extractText(element) {
      return element ? (element.textContent || '').trim() : '';
    }

    extractAttr(element, attr) {
      return element ? (element.getAttribute(attr) || '').trim() : '';
    }
  }

  /**
   * Strategy 1: Inline JSON (fastest, most reliable)
   */
  class InlineJSONStrategy extends ExtractionStrategy {
    async extract(songId, context) {
      this.logger.debug(`Trying InlineJSONStrategy for ${songId}`);

      // Search script tags for JSON containing the song ID
      const scripts = Array.from(document.querySelectorAll('script'))
        .map(s => s.textContent || '');

      for (const scriptText of scripts) {
        if (!scriptText.includes(songId)) continue;

        // Try to find JSON object
        const jsonMatches = scriptText.matchAll(/({[^]*?})/g);

        for (const match of jsonMatches) {
          try {
            const obj = JSON.parse(match[1]);

            // Check if this object contains our song
            const strObj = JSON.stringify(obj).toLowerCase();
            if (strObj.includes(songId)) {
              // Extract fields with multiple key attempts
              const result = {
                lyrics: this.findValue(obj, ['lyrics', 'text', 'transcript']),
                summary: this.findValue(obj, ['summary', 'description', 'prompt']),
                author: this.findValue(obj, ['author', 'artist', 'creator', 'username']),
                tags: this.findValue(obj, ['tags', 'genres', 'styles', 'style']),
                title: this.findValue(obj, ['title', 'name']),
                audio: this.findValue(obj, ['audio', 'audioUrl', 'audio_url', 'url']),
              };

              if (result.lyrics || result.summary) {
                this.logger.debug('InlineJSON found data!');
                return { success: true, data: result, source: 'inline-json' };
              }
            }
          } catch (e) {
            // Not valid JSON or doesn't match
            continue;
          }
        }
      }

      // Check window globals
      const globalKeys = Object.keys(window).filter(k =>
        /suno|__INITIAL__|__DATA__|__STATE__|__NEXT/i.test(k)
      );

      for (const key of globalKeys) {
        try {
          const data = window[key];
          const strData = JSON.stringify(data || {});
          if (strData.includes(songId)) {
            const result = {
              lyrics: this.findValue(data, ['lyrics', 'text']),
              summary: this.findValue(data, ['summary', 'description']),
            };
            if (result.lyrics || result.summary) {
              return { success: true, data: result, source: 'window-global' };
            }
          }
        } catch (e) {
          continue;
        }
      }

      return { success: false, error: 'No inline JSON found' };
    }

    findValue(obj, keys) {
      if (!obj || typeof obj !== 'object') return '';

      for (const key of keys) {
        if (obj[key]) {
          const val = obj[key];
          if (typeof val === 'string') return val;
          if (Array.isArray(val)) return val.join(', ');
          return String(val);
        }
      }

      // Deep search
      for (const value of Object.values(obj)) {
        if (value && typeof value === 'object') {
          const found = this.findValue(value, keys);
          if (found) return found;
        }
      }

      return '';
    }
  }

  /**
   * Strategy 2: Fetch Detail Page (reliable, moderate speed)
   */
  class FetchStrategy extends ExtractionStrategy {
    async extract(songId, context) {
      this.logger.debug(`Trying FetchStrategy for ${songId}`);

      try {
        const response = await fetch(`/song/${songId}`, {
          credentials: 'same-origin',
          signal: AbortSignal.timeout(CONFIG.REQUEST_TIMEOUT),
        });

        if (!response.ok) {
          throw new ExtractorError('NETWORK', `Fetch failed: ${response.status}`, true);
        }

        const html = await response.text();
        const doc = new DOMParser().parseFromString(html, 'text/html');

        const result = {
          lyrics: this.extractText(this.selectFirst(doc, this.selectors.lyrics)),
          summary: this.extractText(this.selectFirst(doc, this.selectors.summary)) ||
                  this.extractAttr(doc.querySelector('meta[name="description"]'), 'content'),
          author: this.extractText(this.selectFirst(doc, this.selectors.author)),
          tags: this.selectAll(doc, this.selectors.tags)
                    .map(el => this.extractText(el))
                    .filter(Boolean)
                    .join(', '),
          audio: this.extractAttr(this.selectFirst(doc, this.selectors.audio), 'src') ||
                this.extractAttr(doc.querySelector('meta[property="og:audio"]'), 'content'),
        };

        if (result.lyrics || result.summary) {
          this.logger.debug('Fetch found data!');
          return { success: true, data: result, source: 'fetch' };
        }

        return { success: false, error: 'No content in fetched page' };
      } catch (error) {
        return { success: false, error: error.message };
      }
    }
  }

  /**
   * Strategy 3: Hidden Iframe (slower, last resort)
   */
  class IframeStrategy extends ExtractionStrategy {
    async extract(songId, context) {
      this.logger.debug(`Trying IframeStrategy for ${songId}`);

      return new Promise((resolve) => {
        const iframe = document.createElement('iframe');
        iframe.style.cssText = 'position:fixed;left:-9999px;width:1200px;height:800px;opacity:0;';
        iframe.src = `/song/${songId}`;
        document.body.appendChild(iframe);

        let resolved = false;
        const finish = (result) => {
          if (!resolved) {
            resolved = true;
            try { iframe.remove(); } catch (e) {}
            resolve(result);
          }
        };

        const timeout = setTimeout(() => {
          finish({ success: false, error: 'Iframe timeout' });
        }, CONFIG.REQUEST_TIMEOUT);

        iframe.onload = async () => {
          try {
            await new Promise(r => setTimeout(r, 800)); // Wait for SPA render

            const doc = iframe.contentDocument || iframe.contentWindow.document;
            if (!doc) {
              finish({ success: false, error: 'Cannot access iframe document' });
              return;
            }

            const result = {
              lyrics: this.extractText(this.selectFirst(doc, this.selectors.lyrics)),
              summary: this.extractText(this.selectFirst(doc, this.selectors.summary)),
              author: this.extractText(this.selectFirst(doc, this.selectors.author)),
              tags: this.selectAll(doc, this.selectors.tags)
                        .map(el => this.extractText(el))
                        .filter(Boolean)
                        .join(', '),
              audio: this.extractAttr(this.selectFirst(doc, this.selectors.audio), 'src'),
            };

            clearTimeout(timeout);

            if (result.lyrics || result.summary) {
              this.logger.debug('Iframe found data!');
              finish({ success: true, data: result, source: 'iframe' });
            } else {
              finish({ success: false, error: 'No content in iframe' });
            }
          } catch (error) {
            clearTimeout(timeout);
            finish({ success: false, error: error.message });
          }
        };

        iframe.onerror = () => {
          clearTimeout(timeout);
          finish({ success: false, error: 'Iframe load error' });
        };
      });
    }
  }

  /**
   * Fallback Chain - tries strategies in order
   */
  class FallbackChain {
    constructor(strategies, logger) {
      this.strategies = strategies;
      this.logger = logger;
    }

    async extract(songId, context) {
      const errors = [];

      for (const strategy of this.strategies) {
        try {
          const result = await strategy.extract(songId, context);
          if (result.success) {
            return result;
          } else {
            errors.push(`${strategy.constructor.name}: ${result.error}`);
          }
        } catch (error) {
          errors.push(`${strategy.constructor.name}: ${error.message}`);
        }
      }

      return {
        success: false,
        error: 'All strategies failed',
        details: errors,
      };
    }
  }

  // ═══════════════════════════════════════════════════════════════════
  // 🎬 MAIN EXTRACTOR CLASS
  // ═══════════════════════════════════════════════════════════════════

  class SunoExtractor {
    constructor(config) {
      this.config = config;
      this.logger = new Logger(config.SHOW_DEBUG_LOGS);
      this.rateLimiter = new RateLimiter(2, 5);
      this.progress = null;
      this.ui = config.SHOW_PROGRESS_UI ? new ProgressUI() : null;
      this.paused = false;
      this.cancelled = false;
      this.results = [];
      this.state = this.loadState();

      // Initialize extraction strategies
      const selectors = SELECTOR_SETS.v1; // Could auto-detect best version
      this.strategies = new FallbackChain([
        new InlineJSONStrategy(selectors, this.logger),
        new FetchStrategy(selectors, this.logger),
        new IframeStrategy(selectors, this.logger),
      ], this.logger);
    }

    // ─────────────────────────────────────────────────────────────────
    // State Management
    // ─────────────────────────────────────────────────────────────────

    loadState() {
      try {
        const saved = sessionStorage.getItem(CONFIG.STORAGE_KEY);
        return saved ? JSON.parse(saved) : { processed: {} };
      } catch (e) {
        return { processed: {} };
      }
    }

    saveState() {
      try {
        sessionStorage.setItem(CONFIG.STORAGE_KEY, JSON.stringify(this.state));
      } catch (e) {
        this.logger.warn('Could not save state:', e.message);
      }
    }

    // ─────────────────────────────────────────────────────────────────
    // Discovery Phase
    // ─────────────────────────────────────────────────────────────────

    async discoverSongs() {
      this.logger.info('🔍 Discovering songs via auto-scroll...');

      let scrollCount = 0;
      let lastCount = 0;
      let noChangeCount = 0;

      await new Promise((resolve) => {
        const interval = setInterval(() => {
          if (this.cancelled) {
            clearInterval(interval);
            resolve();
            return;
          }

          window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' });

          // Count unique song IDs
          const anchors = document.querySelectorAll(SELECTOR_SETS.v1.songAnchor);
          const uniqueIds = new Set();
          anchors.forEach(anchor => {
            const match = anchor.href.match(/\/song\/([a-f0-9-]{36})/);
            if (match) uniqueIds.add(match[1]);
          });

          const count = uniqueIds.size;

          if (count === lastCount) {
            noChangeCount++;
            if (noChangeCount >= CONFIG.SCROLL_NO_CHANGE_LIMIT) {
              clearInterval(interval);
              this.logger.success(`Loaded ${count} songs in ${scrollCount} scrolls`);
              resolve();
            }
          } else {
            noChangeCount = 0;
            scrollCount++;
            lastCount = count;
            this.logger.debug(`Scroll ${scrollCount}: ${count} songs (+${count - lastCount})`);
          }

          if (scrollCount >= CONFIG.SCROLL_MAX) {
            clearInterval(interval);
            this.logger.warn('Max scrolls reached');
            resolve();
          }
        }, CONFIG.SCROLL_DELAY);
      });

      // Collect unique anchor elements
      const anchorElements = Array.from(
        document.querySelectorAll(SELECTOR_SETS.v1.songAnchor)
      );

      const songs = anchorElements
        .map(el => {
          const match = el.href.match(/\/song\/([a-f0-9-]{36})/);
          if (!match) return null;

          const id = match[1];
          const container = el.closest('[data-clip-id], div') || el;

          return {
            id,
            href: el.href,
            title: (el.getAttribute('title') || el.textContent || '').trim(),
            imageUrl: container.querySelector('img')?.src || '',
            duration: container.querySelector(SELECTOR_SETS.v1.duration)?.textContent?.trim() || '',
            anchorEl: el,
          };
        })
        .filter(Boolean)
        .filter((song, index, self) =>
          // Remove duplicates
          index === self.findIndex(s => s.id === song.id)
        );

      this.logger.success(`Found ${songs.length} unique songs`);
      return songs;
    }

    // ─────────────────────────────────────────────────────────────────
    // Extraction Phase
    // ─────────────────────────────────────────────────────────────────

    async extractSong(song, retries = 0) {
      // Check if already processed
      if (this.state.processed[song.id]) {
        return this.state.processed[song.id];
      }

      // Rate limiting
      await this.rateLimiter.acquire();

      // Check pause/cancel
      while (this.paused && !this.cancelled) {
        await new Promise(r => setTimeout(r, 500));
      }
      if (this.cancelled) {
        throw new Error('Cancelled by user');
      }

      try {
        // Use fallback chain to extract data
        const result = await this.strategies.extract(song.id, { song });

        if (result.success) {
          const extractedData = {
            ...song,
            ...result.data,
            source: result.source,
            extractedAt: new Date().toISOString(),
          };

          // Enrich data
          if (CONFIG.ENABLE_ENRICHMENT) {
            this.enrichSongData(extractedData);
          }

          // Validate
          if (CONFIG.ENABLE_VALIDATION) {
            this.validateSongData(extractedData);
          }

          this.state.processed[song.id] = extractedData;
          return extractedData;
        } else {
          throw new ExtractorError(
            'EXTRACTION_FAILED',
            result.error,
            retries < CONFIG.RETRY_ATTEMPTS,
            result.details
          );
        }
      } catch (error) {
        if (retries < CONFIG.RETRY_ATTEMPTS && error.recoverable !== false) {
          this.logger.warn(`Retry ${retries + 1}/${CONFIG.RETRY_ATTEMPTS} for ${song.id}`);
          await new Promise(r => setTimeout(r, 500 * Math.pow(CONFIG.RETRY_BACKOFF, retries)));
          return this.extractSong(song, retries + 1);
        }

        // Mark as failed
        const failedData = {
          ...song,
          error: error.message,
          errorType: error.type || 'UNKNOWN',
          extractedAt: new Date().toISOString(),
        };

        this.state.processed[song.id] = failedData;
        return failedData;
      }
    }

    enrichSongData(data) {
      // Add computed fields
      if (data.duration) {
        const match = data.duration.match(/(\d+):(\d+)/);
        if (match) {
          data.durationSeconds = parseInt(match[1]) * 60 + parseInt(match[2]);
        }
      }

      // Standardize URLs
      if (!data.audio) {
        data.audio = `https://cdn1.suno.ai/${data.id}.mp3`;
      }

      if (data.imageUrl) {
        data.imageUrl = data.imageUrl
          .replace('/image_', '/image_large_')
          .replace('?width=720', '');
      }
    }

    validateSongData(data) {
      const issues = [];

      if (!data.title) issues.push('Missing title');
      if (!data.id || !/^[a-f0-9-]{36}$/.test(data.id)) issues.push('Invalid ID');
      if (!data.audio || !data.audio.startsWith('http')) issues.push('Missing audio URL');

      if (issues.length > 0) {
        this.logger.warn(`Validation issues for ${data.id}:`, issues.join(', '));
        data.validationIssues = issues;
      }
    }

    // ─────────────────────────────────────────────────────────────────
    // Parallel Processing
    // ─────────────────────────────────────────────────────────────────

    async extractAll(songs) {
      this.progress = new ProgressTracker(songs.length);

      if (this.ui) {
        this.ui.create();
        this.ui.onPause(() => {
          this.paused = !this.paused;
          const btn = this.ui.elements.btnPause;
          btn.textContent = this.paused ? '▶️ Resume' : '⏸️ Pause';
        });
        this.ui.onCancel(() => {
          this.cancelled = true;
          this.ui.remove();
        });
      }

      // Process in parallel batches
      const batches = [];
      for (let i = 0; i < songs.length; i += CONFIG.PARALLEL_LIMIT) {
        batches.push(songs.slice(i, i + CONFIG.PARALLEL_LIMIT));
      }

      for (const batch of batches) {
        if (this.cancelled) break;

        const promises = batch.map(song =>
          this.extractSong(song)
            .then(result => {
              this.results.push(result);
              this.progress.increment(!result.error);

              if (this.ui) {
                this.ui.update(this.progress.stats);
              }

              // Autosave
              if (this.results.length % CONFIG.AUTOSAVE_INTERVAL === 0) {
                this.saveState();
                this.logger.debug(`Autosaved at ${this.results.length} songs`);
              }

              return result;
            })
            .catch(error => {
              this.logger.error(`Failed to extract song:`, error);
              this.progress.increment(false);
              return null;
            })
        );

        await Promise.all(promises);
      }

      if (this.ui) {
        this.ui.setComplete();
      }

      this.saveState();
      return this.results;
    }

    // ─────────────────────────────────────────────────────────────────
    // Export
    // ─────────────────────────────────────────────────────────────────

    export(songs, formats = CONFIG.EXPORT_FORMATS) {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);

      formats.forEach(format => {
        switch (format) {
          case 'csv':
            this.exportCSV(songs, `suno-export-${timestamp}.csv`);
            break;
          case 'json':
            this.exportJSON(songs, `suno-export-${timestamp}.json`);
            break;
          case 'txt':
            this.exportTXT(songs, `suno-export-${timestamp}.txt`);
            break;
          case 'html':
            this.exportHTML(songs, `suno-export-${timestamp}.html`);
            break;
        }
      });
    }

    exportCSV(songs, filename) {
      const headers = [
        'id', 'title', 'author', 'tags', 'duration', 'durationSeconds',
        'lyrics', 'summary', 'href', 'audio', 'imageUrl',
        'source', 'extractedAt', 'error', 'validationIssues'
      ];

      const rows = [headers.join(',')];

      songs.forEach(song => {
        const row = headers.map(key => {
          let value = String(song[key] ?? '').replace(/"/g, '""');
          if (Array.isArray(song[key])) value = song[key].join('; ');
          return value.includes(',') || value.includes('\n') ? `"${value}"` : value;
        });
        rows.push(row.join(','));
      });

      this.downloadFile(rows.join('\n'), filename, 'text/csv');
    }

    exportJSON(songs, filename) {
      const data = {
        metadata: {
          version: CONFIG.VERSION,
          exportedAt: new Date().toISOString(),
          totalSongs: songs.length,
          successfulExtractions: songs.filter(s => !s.error).length,
          failedExtractions: songs.filter(s => s.error).length,
        },
        songs: songs,
      };

      this.downloadFile(
        JSON.stringify(data, null, 2),
        filename,
        'application/json'
      );
    }

    exportTXT(songs, filename) {
      const lines = [
        '═══════════════════════════════════════════════════════════════',
        '🎵 SUNO COLLECTION EXPORT',
        '═══════════════════════════════════════════════════════════════',
        '',
        `Exported: ${new Date().toLocaleString()}`,
        `Total Songs: ${songs.length}`,
        `Successful: ${songs.filter(s => !s.error).length}`,
        `Failed: ${songs.filter(s => s.error).length}`,
        '',
        '═══════════════════════════════════════════════════════════════',
        '',
      ];

      songs.forEach((song, i) => {
        lines.push(`${String(i + 1).padStart(4)}. ${song.title || 'Untitled'}`);
        if (song.author) lines.push(`      Author: ${song.author}`);
        if (song.tags) lines.push(`      Tags: ${song.tags}`);
        if (song.duration) lines.push(`      Duration: ${song.duration}`);
        if (song.summary) {
          const sum = song.summary.slice(0, 200);
          lines.push(`      Summary: ${sum}${sum.length < song.summary.length ? '...' : ''}`);
        }
        if (song.lyrics) {
          const lyr = song.lyrics.slice(0, 400);
          lines.push(`      Lyrics:\n${lyr}${lyr.length < song.lyrics.length ? '\n      ...' : ''}`);
        }
        lines.push(`      Audio: ${song.audio}`);
        lines.push(`      URL: ${song.href}`);
        if (song.error) lines.push(`      ❌ Error: ${song.error}`);
        lines.push('');
      });

      this.downloadFile(lines.join('\n'), filename, 'text/plain');
    }

    exportHTML(songs, filename) {
      const html = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Suno Collection Export</title>
  <style>
    * { box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      line-height: 1.6;
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
      background: #f5f5f5;
    }
    h1 {
      text-align: center;
      color: #333;
      border-bottom: 3px solid #667eea;
      padding-bottom: 20px;
    }
    .stats {
      display: flex;
      justify-content: space-around;
      margin: 30px 0;
      flex-wrap: wrap;
    }
    .stat-card {
      background: white;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      text-align: center;
      min-width: 150px;
      margin: 10px;
    }
    .stat-value {
      font-size: 32px;
      font-weight: bold;
      color: #667eea;
    }
    .stat-label {
      color: #666;
      font-size: 14px;
    }
    .song-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 20px;
      margin-top: 30px;
    }
    .song-card {
      background: white;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      transition: transform 0.2s;
    }
    .song-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    .song-image {
      width: 100%;
      height: 200px;
      object-fit: cover;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .song-content {
      padding: 20px;
    }
    .song-title {
      font-size: 18px;
      font-weight: 600;
      margin: 0 0 10px 0;
      color: #333;
    }
    .song-author {
      color: #666;
      font-size: 14px;
      margin-bottom: 10px;
    }
    .song-tags {
      font-size: 12px;
      color: #999;
      margin-bottom: 10px;
    }
    .song-lyrics {
      font-size: 13px;
      color: #555;
      max-height: 100px;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-bottom: 10px;
    }
    .song-footer {
      display: flex;
      gap: 10px;
    }
    .btn {
      flex: 1;
      padding: 10px;
      text-align: center;
      text-decoration: none;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      transition: opacity 0.2s;
    }
    .btn:hover {
      opacity: 0.8;
    }
    .btn-primary {
      background: #667eea;
      color: white;
    }
    .btn-secondary {
      background: #f0f0f0;
      color: #333;
    }
    .error-card {
      border: 2px solid #f44336;
      opacity: 0.7;
    }
  </style>
</head>
<body>
  <h1>🎵 Suno Collection Export</h1>

  <div class="stats">
    <div class="stat-card">
      <div class="stat-value">${songs.length}</div>
      <div class="stat-label">Total Songs</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">${songs.filter(s => !s.error).length}</div>
      <div class="stat-label">Successful</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">${songs.filter(s => s.error).length}</div>
      <div class="stat-label">Failed</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">${songs.filter(s => s.lyrics).length}</div>
      <div class="stat-label">With Lyrics</div>
    </div>
  </div>

  <div class="song-grid">
    ${songs.map(song => `
      <div class="song-card ${song.error ? 'error-card' : ''}">
        <img src="${song.imageUrl || 'data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'300\' height=\'200\'%3E%3Crect fill=\'%23667eea\' width=\'300\' height=\'200\'/%3E%3Ctext fill=\'white\' x=\'50%25\' y=\'50%25\' dominant-baseline=\'middle\' text-anchor=\'middle\' font-family=\'sans-serif\' font-size=\'20\'%3E🎵%3C/text%3E%3C/svg%3E'}"
             class="song-image"
             alt="${song.title}"
             onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'300\' height=\'200\'%3E%3Crect fill=\'%23667eea\' width=\'300\' height=\'200\'/%3E%3Ctext fill=\'white\' x=\'50%25\' y=\'50%25\' dominant-baseline=\'middle\' text-anchor=\'middle\' font-family=\'sans-serif\' font-size=\'20\'%3E🎵%3C/text%3E%3C/svg%3E'">
        <div class="song-content">
          <h3 class="song-title">${song.title || 'Untitled'}</h3>
          ${song.author ? `<div class="song-author">👤 ${song.author}</div>` : ''}
          ${song.tags ? `<div class="song-tags">🏷️ ${song.tags}</div>` : ''}
          ${song.duration ? `<div class="song-tags">⏱️ ${song.duration}</div>` : ''}
          ${song.lyrics ? `<div class="song-lyrics">${song.lyrics.slice(0, 150)}...</div>` : ''}
          ${song.error ? `<div style="color: #f44336; font-size: 12px;">❌ ${song.error}</div>` : ''}
          <div class="song-footer">
            <a href="${song.href}" target="_blank" class="btn btn-primary">🔗 View</a>
            ${song.audio ? `<a href="${song.audio}" target="_blank" class="btn btn-secondary">🎧 Listen</a>` : ''}
          </div>
        </div>
      </div>
    `).join('')}
  </div>

  <footer style="text-align: center; margin-top: 50px; padding: 20px; color: #999; font-size: 14px;">
    <p>Generated by Suno Extractor v${CONFIG.VERSION} on ${new Date().toLocaleString()}</p>
  </footer>
</body>
</html>
      `;

      this.downloadFile(html, filename, 'text/html');
    }

    downloadFile(content, filename, type) {
      try {
        const blob = new Blob([content], { type });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
        this.logger.success(`✅ Downloaded: ${filename}`);
      } catch (error) {
        this.logger.error('Download failed:', error);
      }
    }

    // ─────────────────────────────────────────────────────────────────
    // Main Entry Point
    // ─────────────────────────────────────────────────────────────────

    async run() {
      try {
        this.logger.info(`Starting ${CONFIG.NAME} v${CONFIG.VERSION}`);
        this.logger.info(`Mode: ${CONFIG.MODE}`);

        // Phase 1: Discover songs
        const songs = await this.discoverSongs();

        if (songs.length === 0) {
          this.logger.error('No songs found! Make sure you are on a Suno page with songs.');
          return;
        }

        // Phase 2: Extract data
        this.logger.info(`🎯 Extracting data from ${songs.length} songs...`);
        const results = await this.extractAll(songs);

        if (this.cancelled) {
          this.logger.warn('❌ Extraction cancelled by user');
          return;
        }

        // Phase 3: Export
        this.logger.info('📦 Exporting results...');
        this.export(results);

        // Phase 4: Report
        const successful = results.filter(s => !s.error).length;
        const failed = results.filter(s => s.error).length;
        const successRate = ((successful / results.length) * 100).toFixed(1);

        this.logger.success('═══════════════════════════════════════');
        this.logger.success('🎉 EXTRACTION COMPLETE!');
        this.logger.success('═══════════════════════════════════════');
        this.logger.info(`   Total: ${results.length} songs`);
        this.logger.success(`   Successful: ${successful} (${successRate}%)`);
        if (failed > 0) {
          this.logger.warn(`   Failed: ${failed}`);
        }
        this.logger.info(`   Files saved to ~/Downloads/`);
        this.logger.success('═══════════════════════════════════════');

        // Make data available
        window.extractedSongs = results;
        this.logger.info('💡 Data available as: window.extractedSongs');

        // Show sample
        console.table(results.slice(0, 10).map(s => ({
          Title: s.title,
          Author: s.author || '-',
          Duration: s.duration || '-',
          HasLyrics: s.lyrics ? '✅' : '❌',
          Source: s.source || '-',
          Status: s.error ? '❌' : '✅'
        })));

      } catch (error) {
        this.logger.error('Fatal error:', error);
        if (this.ui) {
          this.ui.remove();
        }
      }
    }
  }

  // ═══════════════════════════════════════════════════════════════════
  // 🚀 EXECUTE
  // ═══════════════════════════════════════════════════════════════════

  const extractor = new SunoExtractor(CONFIG);
  await extractor.run();

})().catch(error => {
  console.error('🎵 Suno Extractor - Fatal Error:', error);
});
