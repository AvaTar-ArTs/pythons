#!/usr/bin/env node
/**
 * Unified Marketplace Uploader
 * 
 * One CSV → ALL platforms (Gumroad, LemonSqueezy, Sellfy, Fiverr, Upwork, Payhip)
 * API where available, browser automation where not.
 * Dedup checking per platform. Saved sessions.
 * 
 * Usage:
 *   node src/upload-all.js [path/to/products_master.csv] [--platforms gumroad,sellfy,fiverr]
 *   node src/upload-all.js --dry-run
 */

import { readFileSync, existsSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { parse } from "csv-parse/sync";
import { chromium } from "playwright";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, "..");
const PLATFORMS_CONFIG = JSON.parse(readFileSync(resolve(root, "src/platforms.json"), "utf8"));
const DATA_DIR = resolve(root, "data");

function loadCSV(csvPath) {
  const content = readFileSync(csvPath, "utf8");
  return parse(content, { columns: true, skip_empty_lines: true, trim: true });
}

function getToken(platform) {
  const config = PLATFORMS_CONFIG.platforms[platform];
  if (!config) return null;
  if (config.browser_only) return null;
  
  const envVar = config.env_var;
  const token = process.env[envVar];
  if (token) return token;
  
  const envPath = resolve(root, ".env");
  if (existsSync(envPath)) {
    const m = readFileSync(envPath, "utf8").match(new RegExp(`${envVar}=(.+)`));
    if (m) return m[1].trim().replace(/^["']|["']$/g, "");
  }
  return null;
}

async function getExistingAPI(platform) {
  const config = PLATFORMS_CONFIG.platforms[platform];
  if (!config || config.browser_only) return [];
  
  const token = getToken(platform);
  if (!token) {
    console.log(`   ⚠️  No API token for ${config.name} — using browser fallback`);
    return null; // signals browser fallback
  }

  const headers = config.auth === "bearer"
    ? { Authorization: `Bearer ${token}` }
    : { Authorization: `Basic ${Buffer.from(token + ":").toString("base64")}` };

  const res = await fetch(`${config.api_base}${config.endpoints.list}`, { headers });
  const data = await res.json();

  if (!res.ok) {
    console.log(`   ⚠️  API error for ${config.name}: ${data.message || res.status}`);
    return null;
  }

  const products = data.products ?? data.data ?? [];
  return products;
}

function parsePlatforms(platformStr) {
  if (!platformStr) return Object.keys(PLATFORMS_CONFIG.platforms);
  return platformStr.split("|").map(p => p.trim().toLowerCase()).filter(p => PLATFORMS_CONFIG.platforms[p]);
}

function isDuplicate(product, existingNames, existingUrls, dedupFields) {
  for (const field of dedupFields) {
    const val = (product[field] || "").toLowerCase();
    if (val && (existingNames.has(val) || existingUrls.has(val))) return true;
  }
  return false;
}

async function createProductAPI(platform, product) {
  const config = PLATFORMS_CONFIG.platforms[platform];
  const token = getToken(platform);
  if (!token) return false;

  const form = new URLSearchParams();
  form.set("access_token", token);
  form.set("name", product.name);
  form.set("price_cents", String(product.price_cents || 0));
  if (product.description) form.set("description", product.description.replace(/\|/g, ", "));
  if (product.permalink) form.set("custom_permalink", product.permalink);

  const headers = { "Content-Type": "application/x-www-form-urlencoded" };
  if (config.auth === "bearer") headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${config.api_base}${config.endpoints.create}`, {
    method: "POST",
    headers,
    body: form,
  });
  const data = await res.json();
  return data.success !== false;
}

async function fillBrowserForm(page, platform, product) {
  const config = PLATFORMS_CONFIG.platforms[platform];
  const s = config.browser_fallback?.selectors || config.selectors;
  if (!s) return;

  await page.goto(config.browser_fallback?.new_url || config.new_url, { waitUntil: "domcontentloaded" }).catch(() => {});
  await page.waitForLoadState("networkidle").catch(() => {});

  // Name
  const nameSel = s.name;
  const nameInput = page.locator(nameSel).first();
  await nameInput.waitFor({ state: "visible", timeout: 10000 }).catch(() => null);
  await nameInput.fill(product.name).catch(() => {});

  // Price
  if (s.price && product.price_cents) {
    const priceStr = (product.price_cents / 100).toFixed(2);
    const priceInput = page.locator(s.price).first();
    await priceInput.fill(priceStr).catch(() => {});
  }

  // Description
  if (s.description && product.description) {
    const desc = product.description.replace(/\|/g, ", ");
    const descInput = page.locator(s.description).first();
    await descInput.fill(desc).catch(() => {});
  }

  // File upload
  if (s.file && product.file_path && existsSync(product.file_path)) {
    const fileInput = page.locator(s.file).first();
    await fileInput.waitFor({ state: "attached", timeout: 15000 }).catch(() => null);
    await fileInput.setInput(product.file_path).catch(() => {});
    await page.waitForTimeout(3000);
  }

  // Cover image
  if (s.file && product.cover_image && existsSync(product.cover_image)) {
    const fileInputs = page.locator(s.file);
    const count = await fileInputs.count();
    if (count > 1) {
      await fileInputs.nth(1).setInputFiles(product.cover_image).catch(() => {});
      await page.waitForTimeout(2000);
    }
  }

  // Click submit
  if (s.submit) {
    const btn = page.getByRole("button", { name: /create|save|publish|continue|next/i }).first();
    await btn.click().catch(() => {});
    await page.waitForTimeout(4000);
  }
}

async function uploadBrowser(platform, product, authState) {
  const config = PLATFORMS_CONFIG.platforms[platform];
  const authFile = resolve(DATA_DIR, `auth-${platform}.json`);
  const hasAuth = existsSync(authState || authFile);

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1366, height: 900 },
    storageState: hasAuth ? (authState || authFile) : undefined,
  });

  const page = await context.newPage();
  await page.goto(config.browser_fallback?.new_url || config.new_url, { waitUntil: "domcontentloaded" });

  // Check login
  const url = page.url();
  if (url.includes("/login") || url.includes("/sign_in")) {
    console.log(`   📝 Please log in to ${config.name} in the browser window.`);
    try {
      await page.waitForURL(/dashboard|products|create|new/, { timeout: 120_000 });
      await context.storageState({ path: authFile });
      console.log(`   ✅ ${config.name} login saved.`);
    } catch {
      console.log(`   ⏰ Login timed out for ${config.name}.`);
      await browser.close();
      return false;
    }
  }

  await fillBrowserForm(page, platform, product);
  
  await context.storageState({ path: authFile });
  console.log(`   ✅ ${config.name} form filled. Add images, review, and publish.`);
  
  await browser.close();
  return true;
}

async function main() {
  const csvPath = process.argv[2] || resolve(DATA_DIR, "products_master.csv");
  const dryRun = process.argv.includes("--dry-run");
  const platformFilter = process.argv.find(a => a.startsWith("--platforms="))?.split("=")[1];

  if (!existsSync(csvPath)) {
    console.error("❌ CSV not found:", csvPath);
    process.exit(1);
  }

  const products = loadCSV(csvPath);
  console.log(`=== 🚀 Unified Marketplace Uploader ===\n`);
  console.log(`📄 CSV: ${csvPath}`);
  console.log(`📦 ${products.length} product(s)\n`);

  for (let i = 0; i < products.length; i++) {
    const p = products[i];
    const platforms = parsePlatforms(p.platforms);
    if (platformFilter) {
      platforms.splice(0, platforms.length, ...platforms.filter(pl => platformFilter.includes(pl)));
    }

    console.log(`\n${"═".repeat(60)}`);
    console.log(`[${i + 1}/${products.length}] ${p.name} — $${(p.price_cents / 100).toFixed(2)}`);
    console.log(`📎 File: ${p.file_path || "(none)"}`);
    console.log(`🌐 Platforms: ${platforms.join(", ")}`);
    console.log(`${"═".repeat(60)}\n`);

    for (const platform of platforms) {
      const config = PLATFORMS_CONFIG.platforms[platform];
      if (!config) {
        console.log(`  ⚠️  Unknown platform: ${platform}`);
        continue;
      }

      console.log(`  🏪 ${config.name}...`);

      // Check existing
      const existing = await getExistingAPI(platform);
      if (existing === null) {
        // Browser fallback
        if (dryRun) {
          console.log(`    [DRY RUN] Would open browser for ${config.name}`);
          continue;
        }
        await uploadBrowser(platform, p);
        continue;
      }

      // Dedup check
      const existingNames = new Set(existing.map(x => (x.name || "").toLowerCase()));
      const existingUrls = new Set((existing.filter(x => x.url || x.permalink)).map(x => (x.url || x.permalink).toLowerCase()));
      if (isDuplicate(p, existingNames, existingUrls, config.dedup_by || ["name"])) {
        console.log(`    ⏭️  Already exists — skipping`);
        continue;
      }

      // Create via API
      if (dryRun) {
        console.log(`    [DRY RUN] Would create: ${p.name}`);
        continue;
      }

      const success = await createProductAPI(platform, p);
      if (success) {
        console.log(`    ✅ Created via API`);
      } else {
        console.log(`    ⚠️  API create failed — falling back to browser`);
        await uploadBrowser(platform, p);
      }
    }
  }

  console.log(`\n${"═".repeat(60)}`);
  console.log(`✅ Done. All platforms processed.`);
  if (dryRun) console.log(`(Dry run — nothing was uploaded)`);
}

main().catch(err => {
  console.error("❌ Error:", err);
  process.exit(1);
});
