# Gumroad 商品描述评审报告 — SellerAI

**评审日期**：2026-07-18 16:16 (GMT+8)
**评审方式**：只读（curl 抓线上 JSON + 读本地产品代码/文档，未修改任何线上内容、未操作浏览器）
**线上商品**：https://xucan.gumroad.com/l/sellerai （product id `NE3LE-vBgB4E513rnkojXQ==`，updated_at 2026-07-15）

---

## 一、结论（给主 agent）

**是否需要更新：是（必须更新）。**

主要过期/错误点：
1. **退款政策写成 30 天** → 实际为 **14 天**（MEMORY / 前端 Pricing 一致）。
2. **免费额度写成「10 条/月」** → 实际前端是 **3 条/月**（Pricing.tsx Free plan）。
3. **全站只讲 Amazon** → 产品已扩展为 **6 平台（Amazon·eBay·Walmart·Shopify·TikTok Shop·Etsy）+ 15 个 Amazon 站点**，名称与文案严重过时。
4. **只提 A9，缺 Rufus & COSMO** → 2026 搜索趋势核心叙事，前端 TrustTriple 已落地。
5. **多语言只写「中/日/韩」** → 实际 **9 种语言**。
6. **批量 CSV 标「Coming」** → 实际已是上线功能（Bulk CSV export）。
7. **「Upgrade to Pro for unlimited」误导** → Pro（$49.9）目前 **Coming Soon / 未开放**。
8. **受众框死「中国卖家 / Temu→Amazon」** → 创始人口径为 **全球卖家**，非仅中国。
9. **夸张/不实措辞**：「1 listing = 1 sale」「Save $100+/month」应删除或弱化。
10. **⚠ 结构性错配（非纯文案）**：Gumroad 商品当前配置为 **一次性 $19.90 购买**（`is_recurring_billing:false`），但文案通篇讲「月订阅 / $19.90/month / $119/year」。后台编辑会话需一并修正商品类型为订阅，否则文案与结算逻辑矛盾。
11. **BYOK 未纳入**：任务 brief 提及 BYOK，但**全代码库无 BYOK 引用**，属尚未上线的能力 → 本报告起草文案**已省略 BYOK**，避免编造。

**新文案是否已备好：是**（见第三节，英文，可直接粘贴到后台）。

---

## 二、现有线上文案摘录（如实抓取）

### 2.1 name
> SellerAI — Amazon Listing Generator

### 2.2 summary（商品卡/短描述）
> Stop wasting hours writing Amazon listings in broken English. SellerAI turns your Chinese product info into A9-optimized, native-English Amazon listings — in 60 seconds.
> 🔥 What You Get: • AI-generated Title + 5 Bullet Points + Search Terms • A9 algorithm optimized for higher rankings • Chinese → native English, no translation gibberish • 10 FREE listings for new users
> 🎯 Built for Chinese cross-border sellers who want listings that actually convert.
> 💡 1 listing = 1 sale. Start now.

### 2.3 description（长描述 / meta description 同源）
> Turn Your Chinese Product Notes into Ready-to-Publish Amazon Listings in 60 Seconds.
> Paste your product description in Chinese → Get a complete, A9-optimized Amazon listing in English: title, 5 bullet points, HTML product description, and backend search terms.
> Why Amazon Sellers Love SellerAI: ⚡ 60-second listing generation / 🎯 A9 optimized / 🧠 AI-powered quality scoring / 💰 Save $100+/month
> Works for any category — Home & Kitchen, Electronics, Sports & Outdoors, Beauty, Pet Supplies, and more.
> 3 Steps: Paste your Chinese product description → Click "Generate" → Copy and paste to Amazon Seller Central
> Start with 10 free listings per month. Upgrade to Pro for unlimited access.

### 2.4 attributes（卖点勾选表，节选）
- One-Click Listing Generation / AI Title Generation / 5 Bullet Points / Backend Search Terms
- Native American English / Auto Keyword Extraction / Mobile-Optimized Format / Multi-Category Support
- Product Description Paragraph / No Prompt Engineering / Copy-Paste Ready / **Unlimited Generations — no per-listing cap with Pro plan**
- Lightning Fast — average 3 seconds per listing / **Built for Temu → Amazon Pipeline** / **Competitor-Aware — input competitor ASINs**
- Tone Control / **Batch Mode (Coming) — upload CSV, get 100 listings at once**
- Multi-Language Input — accepts Chinese, Japanese, Korean / **10 Free Listings — no credit card**

### 2.5 refund_policy
- title: **"30-day money back guarantee"**
- fine_print: "SellerAI is a digital subscription service. You will be charged $19.90/month starting from your subscription date. • 30-day money-back guarantee — no questions asked • Cancel anytime from your Gumroad library …"

### 2.6 价格/商品类型（抓取）
- `price_cents: 1990`（$19.90）
- `is_recurring_billing: false` ← **一次性购买，非订阅**
- `free_trial: null` ← 未配置试用
- `buyer_currency: hkd`（对港币买家显示 HK$156.02）

---

## 三、过期项清单（逐项）

| # | 字段 | 线上现状 | 真实产品状态 | 严重度 |
|---|------|----------|--------------|--------|
| 1 | 退款政策 | 30 天 | 14 天（MEMORY + Pricing.tsx） | 🔴 高（与承诺不符，有争议风险） |
| 2 | 免费额度 | 10 条/月 | 3 条/月（Pricing.tsx Free plan） | 🔴 高（虚假承诺） |
| 3 | 平台范围 | 仅 Amazon | 6 平台 + 15 Amazon 站点 | 🔴 高（严重低估产品） |
| 4 | 优化引擎 | 仅 A9 | A9 + Rufus & COSMO-ready | 🟠 中 |
| 5 | 多语言 | 中/日/韩 | 9 种语言 | 🟠 中 |
| 6 | 批量 CSV | 「Batch Mode (Coming)」 | 已上线（Bulk CSV export） | 🟠 中 |
| 7 | Pro 计划 | 「Upgrade to Pro for unlimited」 | Pro $49.9 Coming Soon，未开放 | 🟠 中（误导） |
| 8 | 受众定位 | 中国跨境 / Temu→Amazon | 全球卖家（创始人 2026-07-17 口径） | 🟠 中 |
| 9 | 不实措辞 | 「1 listing = 1 sale」「Save $100+/month」 | 无依据 | 🟡 低（建议删/弱化） |
| 10 | 商品类型 | 一次性 $19.90 购买 | 应为订阅（$19.9/月、$119/年） | 🔴 高（配置错配，需后台改） |
| 11 | 3 天试用 | 未配置 | MEMORY 口径有 3 天试用（待与前端「3条/月」核对） | 🟡 低（见备注） |
| 12 | BYOK | （brief 提及） | 代码无实现 → 非真实能力 | ⚪ 已省略 |

**备注（11）**：前端 Pricing.tsx 的 Free plan 写「3 listings / month」，未显式出现「3 天试用」；MEMORY 定价口径写「3 天试用」。两者口径需创始人确认后统一。本报告在草稿中采用「3 天免费试用」表述（依任务指示对齐 MEMORY），但**请后台编辑会话落地前与前端 Free plan 文案二次核对**。

---

## 四、建议新文案（英文，可直接粘贴后台）

> 说明：以下文案严格基于已验证的真实能力（Pricing.tsx / TrustTriple.tsx / WorkflowNarrative.tsx / ops 日志），未夸大、未编造。价格、退款、免费额度与前端及 MEMORY 一致。

### 4.1 Name（商品名）
```
SellerAI — AI Listing Generator for Amazon, eBay, Walmart & more
```

### 4.2 Short description / Summary（短描述，用于商品卡与 meta）
```
Turn product notes in any language into publish-ready, search-optimized listings for Amazon, eBay, Walmart, Shopify, TikTok Shop & Etsy — in about a minute. Get a complete listing: title, 5 bullets, description, and backend search terms, optimized for Amazon's A9 and AI search (Rufus & COSMO). Start free with 3 listings per month.
```

### 4.3 Long description（长描述，Gumroad 后台 description 字段，Markdown）
```markdown
## Write listings that actually get found — in any language, on any platform

Paste your product notes (in your own language) and get a complete, marketplace-ready listing: **title, 5 bullet points, product description, and backend search terms** — optimized for how each marketplace really ranks.

### Built for how selling works in 2026
- 🌍 **9 listing languages** — English, Deutsch, Français, Español, Italiano, 日本語, Nederlands and more. Paste notes in your language, get native copy.
- 🛒 **6 platforms** — Amazon, eBay, Walmart, Shopify, TikTok Shop, Etsy.
- 🏷️ **15 Amazon marketplaces** — US, UK, DE, FR, ES, IT, JP, KR, BR and more.
- 🤖 **A9 + Rufus & COSMO-ready** — copy is built to rank in Amazon's classic search and answer Amazon's AI shopping assistant (Rufus) and the COSMO model.

### What you get with every listing
- ⚡ **~60-second generation** — from rough notes to publish-ready copy.
- 🎯 **Search-optimized** — keyword placement tuned for each marketplace's algorithm.
- 🧠 **Quality scoring** — see exactly where your listing can improve (8-dimension scorer).
- 🔑 **Keyword tool** — pull high-volume search terms your product should target.
- 📤 **Bulk CSV export** — generate at scale and export your whole catalog (Pro).

### Pricing
- **Free** — 3 listings / month, full AI generation. No credit card.
- **Starter** — **$19.9/mo**, or **$119/year** (save ~50%). 100 listings / month, priority generation, cancel anytime.
- **Founder** — **$14.9/mo** with code `FOUNDER50` (first 50 sellers, price locked for life).
- **Pro** — $49.9/mo with bulk generation & competitor analysis — *coming soon*.

### Try it risk-free
Start with 3 free listings. Paid plans include a **3-day free trial** and a **14-day money-back guarantee** — no questions asked. Cancel anytime from your Gumroad library.

*SellerAI is a writing assistant. You are responsible for reviewing output before publishing to any marketplace.*
```

### 4.4 Refund policy（退款政策，对齐 14 天）
- **title**: `14-day money-back guarantee`
- **fine_print** (建议):
```
SellerAI is a subscription service billed through Gumroad.
• 14-day money-back guarantee — no questions asked
• Cancel anytime from your Gumroad library; you keep access until the period ends
• All generated content is yours to use commercially
• We do not store your product data after generation
• Support: email sellerai@proton.me

Starter: $19.9/month or $119/year. Founder: $14.9/month (code FOUNDER50). Pro: coming soon.
```

### 4.5 后台需同步修正的配置（非文案，但必须改）
1. **商品类型**：由「一次性 $19.90 购买」改为**订阅**（月度 $19.9 / 年付 $119），否则与文案/结算矛盾。
2. **免费试用**：如采用「3 天试用」口径，在 Gumroad 配置 `free_trial`（需后台编辑会话操作）。
3. **custom button text**「Download Your SellerAI Too」语义不清，建议改为「Get SellerAI」或「Start free」。

---

## 五、给后台编辑隔离会话的交接提示
- 本评审**只读**，未做任何线上改动。
- 落地时请以第四节文案为准，重点先修：**退款 30→14 天**、**免费 10→3 条/月**、**平台范围扩到 6 平台**、**商品类型改订阅**。
- **BYOK 暂不写**（无代码支撑）；如后续上线再补。
- 「3 天试用」口径请先与前端 Pricing.tsx（写「3 listings/month」）核对一致后再发布。
