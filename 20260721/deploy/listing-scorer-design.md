# SellerAI - Amazon Listing 诊断评分系统设计

> 对标 Jungle Scout LQS、Helium 10 Listing Analyzer、ZonGuru Listing Optimizer 4.0

---

## 一、竞品调研摘要

### 1.1 Jungle Scout — Listing Quality Score (LQS)

| 维度 | 竞品做法 |
|------|---------|
| **评分输出** | 实时动态评分（输入时即时反馈），总分 0-100 |
| **检测维度** | 标题（Title）、五点描述（Bullet Points）、关键词（Keywords）、图片（Images） |
| **关键词** | 从 Keyword Bank 导入关键词列表，自动检测关键词嵌入率和排名 |
| **AI 能力** | AI Assist 一键生成标题/五点/描述；AI 驱动评分 |
| **差异化** | 与 JS 的 Keyword Scout 深度集成，可一键同步到 Seller Central |
| **不足** | 维度较少（仅4个），无 A+ 内容检测，无 Review 维度，无竞品对比 |

### 1.2 Helium 10 — Listing Analyzer

| 维度 | 竞品做法 |
|------|---------|
| **评分输出** | 总分 0-10 分制，支持最多 10 个 ASIN 批量对比 |
| **检测维度** | 标题 ≥150 字符、图片 ≥7 张 + 主图白色背景 1000×1000+、5条 Bullet Points 填满、描述 ≥1000 字符、Review ≥10 条 + 均分 ≥4.0 |
| **关键词** | KPS（Keyword Performance Score）+ KPR（Keyword Performance Rank），按精确/词组/广泛匹配评估 SEO 潜力 |
| **AI 能力** | AI Listing Builder 集成、Scribbles 关键词嵌入检测 |
| **差异化** | 最强竞品对比能力（批量 10 ASIN），市场分析模块（vs 类目均值） |
| **不足** | 无 A+ 内容 / EBC 检测，判定标准偏机械（只看字数/数量），不做语义质量判断 |

### 1.3 ZonGuru — Listing Optimizer 4.0

| 维度 | 竞品做法 |
|------|---------|
| **评分输出** | AI-Readiness Score（针对 COSMO / Rufus 的 AI 可读性评分） |
| **检测维度** | Semantic Gap Audit（语义缺口分析）、Rufus Question Coverage（问答覆盖）、Trust & Authority Signals（信任信号） |
| **关键词** | 关键词映射到 Listing 各板块，跟踪关键词嵌入 |
| **AI 能力** | Helix™ Agentic AI（基于 ChatGPT），全自动 Listing 工程 |
| **差异化** | 唯一关注 COSMO/Alexa AI 搜索优化的工具；Semantic Gap 分析 |
| **不足** | 更偏向 AI-Ready 概念营销，传统硬指标（字数/图片/Review）覆盖不足 |

### 1.4 竞品空白点（我们的切入点）

| 空白点 | SellerAI 机会 |
|--------|--------------|
| **语义质量** | 竞品多为"长度够了没"，我们做"写得好不好"——AI 判断文案吸引力、可读性、信息密度 |
| **A+ Content** | 三家竞品均未做 A+ 内容质量检测 |
| **Review 无质量分析** | H10 只看"≥10条+4.0分"，不做 Review 内容语义分析（差评揭示什么痛点？Listing 是否回应了这些？） |
| **竞品对比** | H10 有批量对比但无"相对短板"诊断（你 vs Top 10 中位数的差距） |
| **可操作的单一诊断句** | 竞品给分数但不给"一句话告诉你怎么改" |

---

## 二、SellerAI Listing 诊断系统设计

### 2.1 系统概述

**输入：** ASIN 或 Listing 各字段文本（标题、Bullet Points、描述、图片数、A+ 内容、Backend Search Terms、Review 数据 + 竞品 Top 10 数据可选）

**输出：** JSON，包含 overall_score (0-100) + 8 个维度子分数 + 各维度改进建议

**核心理念：** 不只看「合规了没」，更看「写得好不好」和「比竞品差在哪」

---

### 2.2 评分维度总览（8 个维度）

| # | 维度 | 权重 | 满分 | 竞品来源参考 |
|---|------|------|------|-------------|
| 1 | Title Quality（标题质量） | 20% | 20 | JS LQS + H10 150字符检测 |
| 2 | Image Completeness（图片完整度） | 15% | 15 | H10 7张图片 + 主图规范 |
| 3 | Bullet Points Quality（五点描述质量） | 15% | 15 | JS LQS + H10 5条完整检测 |
| 4 | Product Description Richness（产品描述丰富度） | 10% | 10 | H10 1000字符检测 |
| 5 | Keyword Optimization（关键词优化） | 15% | 15 | JS Keyword Bank + H10 KPS |
| 6 | A+ Content / EBC（A+内容质量） | 10% | 10 | **竞品空白点** |
| 7 | Review & Social Proof（评论与社会证明） | 10% | 10 | H10 Review 检测 + **语义增强** |
| 8 | Backend Search Terms（后台搜索词） | 5% | 5 | JS / H10 均有但不深入 |
| **总计** | | **100%** | **100** | |

---

### 2.3 各维度详细计分规则

---

#### 维度 1：Title Quality（标题质量）— 满分 20 分

| 子项 | 分值 | 计分规则 |
|------|------|---------|
| 1-1 长度达标 | 4 | ≥150 字符得 4；100-149 得 2；<100 得 0 |
| 1-2 核心关键词前置 | 5 | 主要搜索词在前 80 字符内得 5；在前 120 字符得 3；在后面得 1；未出现得 0 |
| 1-3 品牌名开头 | 2 | 以品牌名开头得 2；品牌在标题中得 1；无品牌得 0 |
| 1-4 关键信息完整性 | 4 | 标题包含：材质/尺寸/数量/颜色/核心功能（AI 判断覆盖 3+ 得 4；2 项得 2；<2 得 1） |
| 1-5 语法与可读性 | 3 | AI 判断：语法正确+流畅得 3；有轻微问题得 1；有拼写错误或堆砌关键词得 0 |
| 1-6 无违规 | 2 | 无全大写、无促销词（Best/Cheapest/100% Guarantee）、无特殊符号得 2；否则得 0 |

**AI 检测 Prompt（英文）：**
```
You are an Amazon listing quality auditor. Analyze the following product title for an Amazon listing.

Title: "{title}"

Score each sub-dimension and provide the result as JSON:
1. length_score (0-4): Check character count. score 4 if >=150 chars, 2 if 100-149, 0 if <100.
2. keyword_placement_score (0-5): Identify the main product keyword. score 5 if it appears in the first 80 characters, 3 if in first 120, 1 if present but later, 0 if missing.
3. brand_score (0-2): Check if brand name starts the title. score 2 if title starts with brand name, 1 if brand appears elsewhere, 0 if no brand.
4. info_completeness_score (0-4): Does the title mention material, size/dimensions, quantity, color, and core function? score 4 for 4+ of these, 2 for 2-3, 1 for 1, 0 for none.
5. readability_score (0-3): Evaluate grammar, flow, and whether it reads like a human wrote it (not keyword-stuffed). score 3 for excellent, 1 for minor issues, 0 for spammy/stuffed.
6. compliance_score (0-2): Check for prohibited content: ALL CAPS, promotional words (Best, Cheapest, 100% Guarantee), special characters (™, ©, !!, **). score 2 if clean, 0 if any violation.

Return ONLY valid JSON: {"length_score": N, "keyword_placement_score": N, "brand_score": N, "info_completeness_score": N, "readability_score": N, "compliance_score": N, "total": N, "issues": ["issue1", "issue2"], "suggestion": "One-sentence actionable fix"}
```

---

#### 维度 2：Image Completeness（图片完整度）— 满分 15 分

| 子项 | 分值 | 计分规则 |
|------|------|---------|
| 2-1 图片数量 | 5 | ≥7 张得 5；5-6 张得 3；3-4 张得 1；<3 得 0 |
| 2-2 主图白底 | 3 | 主图为纯白底+仅产品得 3；白底但有杂物得 1；非白底得 0 |
| 2-3 主图分辨率 | 2 | ≥1000×1000 得 2；500-999 得 1；<500 得 0 |
| 2-4 图片类型多样性 | 5 | 包含：展示图/细节图/尺寸图/场景图/对比图。AI 判断有 4+ 类型得 5；2-3 类得 3；1 类得 1 |

**AI 检测 Prompt（英文）：**
```
You are an Amazon image quality auditor. Given the following image metadata for an Amazon listing:

Images: {image_list_json}
Main image background: {main_image_bg_type}
Main image dimensions: {width}x{height}

Score each sub-dimension and return JSON:
1. count_score (0-5): score 5 if >=7 images, 3 if 5-6, 1 if 3-4, 0 if <3.
2. main_image_bg_score (0-3): score 3 for pure white background with only product, 1 for white background with props/distractions, 0 for non-white or lifestyle.
3. resolution_score (0-2): score 2 if width>=1000 AND height>=1000, 1 if 500-999, 0 if <500.
4. diversity_score (0-5): Identify image types from descriptions: hero shot, detail/close-up, dimension/size chart, lifestyle/scene, infographic/comparison, packaging, video. score 5 if 4+ types present, 3 if 2-3, 1 if 1, 0 if all same type.

Return ONLY valid JSON: {"count_score": N, "main_image_bg_score": N, "resolution_score": N, "diversity_score": N, "total": N, "missing_types": ["type1"], "suggestion": "One-sentence actionable fix"}
```

---

#### 维度 3：Bullet Points Quality（五点描述质量）— 满分 15 分

| 子项 | 分值 | 计分规则 |
|------|------|---------|
| 3-1 数量完整性 | 3 | 5条全填得 3；3-4条得 1；<3得 0 |
| 3-2 每条长度合理 | 3 | 平均每条 ≥80 字符得 3；50-79得 2；<50得 0 |
| 3-3 首词大写+格式化 | 2 | 每条首字母大写且格式统一得 2；部分统一得 1；混乱得 0 |
| 3-4 卖点优先级排序 | 4 | AI 判断：第1-2条是最核心卖点（功能/效果），而非次要信息，得 4；一般得 2；顺序混乱得 0 |
| 3-5 关键词嵌入 | 3 | 核心关键词至少出现在 3 条 bullet 中得 3；1-2条得 1；0条得 0（但不堆砌） |

**AI 检测 Prompt（英文）：**
```
You are an Amazon listing quality auditor. Analyze the following bullet points for an Amazon listing:

Bullet Points:
{bullet_points_array}

Target Keywords: {target_keywords}

Score each sub-dimension and return JSON:
1. completeness_score (0-3): score 3 if 5 bullets filled, 1 if 3-4, 0 if <3.
2. length_score (0-3): Calculate average character count per bullet. score 3 if avg >=80, 2 if 50-79, 0 if <50.
3. formatting_score (0-2): Check if each bullet starts with a capitalized first word and format is consistent. score 2 for perfect, 1 for partial, 0 for messy.
4. priority_score (0-4): Evaluate whether bullets 1-2 highlight the MOST important selling points (features, benefits, what problem it solves) — NOT warranty, packaging, or secondary info. score 4 for excellent prioritization, 2 for average, 0 for poor/random order.
5. keyword_embedding_score (0-3): Count how many bullets contain at least one target keyword. score 3 if 3+ bullets contain keywords, 1 if 1-2, 0 if none. Penalize if keywords are obviously stuffed.

Return ONLY valid JSON: {"completeness_score": N, "length_score": N, "formatting_score": N, "priority_score": N, "keyword_embedding_score": N, "total": N, "issues": ["issue1"], "suggestion": "One-sentence actionable fix"}
```

---

#### 维度 4：Product Description Richness（产品描述丰富度）— 满分 10 分

| 子项 | 分值 | 计分规则 |
|------|------|---------|
| 4-1 长度达标 | 3 | ≥1000 字符得 3；500-999得 2；200-499得 1；<200得 0 |
| 4-2 HTML 格式化 | 2 | 使用 `<p>` / `<br>` / `<b>` 分段排版得 2；纯文本无格式得 0 |
| 4-3 信息完整度 | 3 | 包含：产品描述/规格/使用场景/售后保障。AI 判断覆盖 4 项得 3；2-3项得 2；1项得 1 |
| 4-4 关键词自然嵌入 | 2 | 核心关键词自然出现在描述中得 2；无关键词或堆砌得 0 |

**AI 检测 Prompt（英文）：**
```
You are an Amazon listing quality auditor. Analyze the following product description for an Amazon listing:

Description: "{description}"

Target Keywords: {target_keywords}

Score each sub-dimension and return JSON:
1. length_score (0-3): Check character count. score 3 if >=1000, 2 if 500-999, 1 if 200-499, 0 if <200.
2. formatting_score (0-2): Check for HTML formatting (paragraphs, line breaks, bold). score 2 if well-formatted with <p>/<br>/<b>, 0 if plain text only.
3. completeness_score (0-3): Does the description cover: product overview, specifications/parameters, use cases, after-sales/warranty? score 3 for 4/4, 2 for 2-3, 1 for 1, 0 for none.
4. keyword_natural_score (0-2): Are target keywords naturally embedded (not stuffed)? score 2 for natural use, 1 for mechanical insertion, 0 for no keywords or obvious stuffing.

Return ONLY valid JSON: {"length_score": N, "formatting_score": N, "completeness_score": N, "keyword_natural_score": N, "total": N, "issues": ["issue1"], "suggestion": "One-sentence actionable fix"}
```

---

#### 维度 5：Keyword Optimization（关键词优化）— 满分 15 分

| 子项 | 分值 | 计分规则 |
|------|------|---------|
| 5-1 标题关键词覆盖率 | 5 | Top 5 目标关键词出现在标题中：5个全有得 5；3-4个得 3；1-2个得 1；0得 0 |
| 5-2 全字段关键词分布 | 4 | 关键词合理分布（标题/Bullet/描述各有一部分），而非全部堆在标题，得 4；集中在 1-2 字段得 2 |
| 5-3 长尾关键词覆盖 | 3 | 至少包含 3+ 长尾词（3+ 词短语）在 listing 任意字段，得 3；1-2 个得 1；0得 0 |
| 5-4 Search Term 不被浪费 | 3 | Backend search terms 不重复标题/五点已有词、不包含品牌/ASIN、不重复填词得 3；部分冗余得 1；严重浪费得 0 |

**AI 检测 Prompt（英文）：**
```
You are an Amazon SEO auditor. Analyze keyword optimization for this listing:

Title: "{title}"
Bullet Points: {bullets_array}
Description: "{description}"
Backend Search Terms: "{backend_terms}"
Target Keywords (ranked by importance): {keywords_array}

Score each sub-dimension and return JSON:
1. title_keyword_coverage (0-5): How many of the top 5 target keywords appear in the title? score 5 for 5/5, 3 for 3-4, 1 for 1-2, 0 for 0.
2. field_distribution_score (0-4): Are keywords well-distributed across title/bullets/description, or crammed into one field? score 4 for balanced across all, 2 for concentrated in 1-2, 0 for all in one place.
3. longtail_coverage (0-3): Count unique long-tail keywords (3+ word phrases) used anywhere in the listing. score 3 for 3+, 1 for 1-2, 0 for none.
4. backend_efficiency_score (0-3): Are backend search terms efficient? Penalize if they repeat title/bullet words, include brand names, competitor ASINs, or are redundant. score 3 for clean and efficient, 1 for moderate waste, 0 for completely wasted.

Return ONLY valid JSON: {"title_keyword_coverage": N, "field_distribution_score": N, "longtail_coverage": N, "backend_efficiency_score": N, "total": N, "missing_top_keywords": ["kw1"], "suggestion": "One-sentence actionable fix"}
```

---

#### 维度 6：A+ Content / EBC（A+内容质量）— 满分 10 分（竞品空白点）

| 子项 | 分值 | 计分规则 |
|------|------|---------|
| 6-1 A+ 是否存在 | 2 | 有 A+ 内容得 2；无得 0 |
| 6-2 模块丰富度 | 3 | ≥5 个 A+ 模块（如品牌故事/对比图/技术规格/产品矩阵等）得 3；3-4个得 2；1-2个得 1 |
| 6-3 视觉质量 | 3 | A+ 使用高质量定制图片（非普通产品图重复利用），有信息图表/对比表得 3；一般得 1 |
| 6-4 品牌叙事 | 2 | A+ 讲述品牌故事/价值主张，而非仅贴图，得 2；纯产品图堆砌得 0 |

**AI 检测 Prompt（英文）：**
```
You are an Amazon A+ Content auditor. Analyze the A+ Content / Enhanced Brand Content for this listing:

A+ Modules: {aplus_modules_json}
  (each module has: type, image_count, text_content)

Score each sub-dimension and return JSON:
1. has_aplus_score (0-2): score 2 if A+ content exists, 0 if absent.
2. module_richness_score (0-3): Count distinct module types. score 3 for 5+ modules, 2 for 3-4, 1 for 1-2.
3. visual_quality_score (0-3): Are images high-quality, custom-designed (not reused product images), and include infographics/comparison tables? score 3 for professional custom visuals, 1 for basic/reused images.
4. brand_storytelling_score (0-2): Does the A+ content tell a brand story, present value proposition, or build trust — not just show product images? score 2 for narrative/branding, 0 for image-only dump.

Return ONLY valid JSON: {"has_aplus_score": N, "module_richness_score": N, "visual_quality_score": N, "brand_storytelling_score": N, "total": N, "issues": ["issue1"], "suggestion": "One-sentence actionable fix"}
```

---

#### 维度 7：Review & Social Proof（评论与社会证明）— 满分 10 分

| 子项 | 分值 | 计分规则 |
|------|------|---------|
| 7-1 评论数量 | 3 | ≥50条得 3；10-49得 2；1-9得 1；0得 0 |
| 7-2 评论均分 | 3 | ≥4.3得 3；4.0-4.29得 2；3.5-3.99得 1；<3.5得 0 |
| 7-3 差评语义分析 | 4 | AI 分析 Top 最近的 1-3 星差评，总结高频痛点，检测 Listing 是否已在描述/Bullet/A+ 中回应这些痛点。回应了 ≥80% 痛点得 4；回应 50-79% 得 2；<50% 得 0 |

**AI 检测 Prompt（英文）：**
```
You are a review analysis auditor for Amazon listings. Analyze reviews for this product:

Review Count: {review_count}
Average Rating: {avg_rating}
Recent Negative Reviews (1-3 stars, last 20): {negative_reviews_json}
Listing Bullet Points: {bullets_array}
Listing Description: "{description}"
A+ Content: {aplus_text}

Score each sub-dimension and return JSON:
1. quantity_score (0-3): score 3 for 50+ reviews, 2 for 10-49, 1 for 1-9, 0 for 0.
2. rating_score (0-3): score 3 for avg >=4.3, 2 for 4.0-4.29, 1 for 3.5-3.99, 0 for <3.5.
3. pain_point_coverage_score (0-4): Extract the top 5 recurring pain points from negative reviews. Then check whether the listing content (bullets, description, A+) addresses or preemptively answers these concerns. score 4 if 4-5 pain points are addressed, 2 if 2-3, 0 if 0-1.

Return ONLY valid JSON: {"quantity_score": N, "rating_score": N, "pain_point_coverage_score": N, "total": N, "top_pain_points": ["point1", "point2"], "unaddressed_pain_points": ["point3"], "suggestion": "One-sentence actionable fix"}
```

---

#### 维度 8：Backend Search Terms（后台搜索词）— 满分 5 分

| 子项 | 分值 | 计分规则 |
|------|------|---------|
| 8-1 字符利用率 | 2 | 使用 200-249 字符（接近250上限）得 2；100-199得 1；<100得 0 |
| 8-2 质量检测 | 3 | 不含品牌名/ASIN/重复词/标点符号/标题已有词，语言为小写+空格分隔，得 3；轻微违规得 1；严重浪费得 0 |

**AI 检测 Prompt（英文）：**
```
You are an Amazon backend search terms auditor. Analyze the backend keywords:

Backend Search Terms: "{backend_search_terms}"
Title (for dedup check): "{title}"
Bullet Points (for dedup check): {bullets_array}
Brand Name: "{brand}"

Score each sub-dimension and return JSON:
1. utilization_score (0-2): Amazon allows ~250 bytes. score 2 if 200-249 chars used, 1 if 100-199, 0 if <100 or >249.
2. quality_score (0-3): Check for violations: brand names, ASINs, competitor brand names, duplicate words, punctuation, words already in title/bullets, NOT in lowercase, NOT space-separated. score 3 for perfectly clean, 1 for 1-2 minor violations, 0 for 3+ violations.

Return ONLY valid JSON: {"utilization_score": N, "quality_score": N, "total": N, "violations": ["violation1"], "suggestion": "One-sentence actionable fix"}
```

---

## 三、最终输出 JSON Schema

```json
{
  "asin": "B0XXXXXXXXX",
  "timestamp": "2026-07-15T22:22:00Z",
  "overall_score": 72,
  "grade": "B",
  "grade_meaning": "Good foundation, but 3 dimensions need attention",
  "one_line_diagnosis": "Your listing scores 72/100 — you lost points on missing A+ Content (0/10), weak keyword distribution (8/15), and bullet points need better prioritization (8/15).",
  "dimensions": [
    {
      "name": "Title Quality",
      "score": 18,
      "max": 20,
      "weight": "20%",
      "sub_scores": {
        "length": { "score": 4, "max": 4, "status": "good" },
        "keyword_placement": { "score": 5, "max": 5, "status": "good" },
        "brand_prefix": { "score": 2, "max": 2, "status": "good" },
        "info_completeness": { "score": 3, "max": 4, "status": "warning" },
        "readability": { "score": 2, "max": 3, "status": "warning" },
        "compliance": { "score": 2, "max": 2, "status": "good" }
      },
      "issues": [
        "Title is missing material type and size dimensions",
        "Title reads slightly keyword-stuffed — consider rewording for natural flow"
      ],
      "fix_suggestion": "Add material and size info to title, e.g. '...Stainless Steel, 12-inch...' and smooth out the keyword density"
    },
    {
      "name": "Image Completeness",
      "score": 13,
      "max": 15,
      "weight": "15%",
      "sub_scores": { /* ... */ },
      "issues": ["Only 5 images — add at least 2 more (lifestyle + size chart)"],
      "fix_suggestion": "Upload a lifestyle/use-case image and an infographic size-comparison chart to reach 7 images"
    },
    {
      "name": "Bullet Points Quality",
      "score": 12,
      "max": 15,
      "weight": "15%",
      "sub_scores": { /* ... */ },
      "issues": ["Bullet #1 talks about warranty — move core feature/benefit to top position"],
      "fix_suggestion": "Reorder bullets: put the strongest product benefit in position 1, move warranty to position 5"
    },
    {
      "name": "Product Description",
      "score": 8,
      "max": 10,
      "weight": "10%",
      "sub_scores": { /* ... */ },
      "issues": ["Description is only 340 characters — expand to 1000+ with use cases and specs"],
      "fix_suggestion": "Add a specifications section, 2-3 use case scenarios, and care instructions to reach 1000+ characters"
    },
    {
      "name": "Keyword Optimization",
      "score": 10,
      "max": 15,
      "weight": "15%",
      "sub_scores": { /* ... */ },
      "issues": [
        "Top keyword 'portable blender USB-C' not in title",
        "Backend search terms repeat title words — wasting 60% of space"
      ],
      "fix_suggestion": "Include 'USB-C rechargeable' in title; clean backend terms to remove duplicates and add unique synonyms"
    },
    {
      "name": "A+ Content",
      "score": 0,
      "max": 10,
      "weight": "10%",
      "sub_scores": { /* ... */ },
      "issues": ["No A+ Content / EBC exists for this ASIN"],
      "fix_suggestion": "Create A+ Content with brand story module, comparison chart, and detailed feature modules — single biggest scoring opportunity"
    },
    {
      "name": "Review & Social Proof",
      "score": 7,
      "max": 10,
      "weight": "10%",
      "sub_scores": { /* ... */ },
      "issues": [
        "Only 8 reviews (need 50+ for full score)",
        "Top complaint 'battery dies fast' not addressed anywhere in listing"
      ],
      "fix_suggestion": "Add battery life specifications prominently in bullet #2 and description; address longevity concerns proactively"
    },
    {
      "name": "Backend Search Terms",
      "score": 4,
      "max": 5,
      "weight": "5%",
      "sub_scores": { /* ... */ },
      "issues": ["Using only 87/250 characters — add relevant synonyms and alternate spellings"],
      "fix_suggestion": "Fill backend terms to ~240 characters with unique synonyms (e.g. 'travel blender', 'blender bottle', 'smoothie maker', etc.)"
    }
  ],
  "quick_wins": [
    "Add A+ Content → +10 points instantly (biggest gap)",
    "Reorder bullet points → +3 points",
    "Expand description to 1000+ characters → +2 points",
    "Fill backend search terms → +1 point"
  ]
}
```

---

## 四、Grade 等级对照表

| 分数区间 | Grade | 含义 |
|---------|-------|------|
| 90-100 | A+ | Excellent — nearly optimized; minor polish only |
| 80-89 | A | Strong listing; 1-2 dimensions could improve |
| 70-79 | B | Good foundation; 3-4 dimensions need attention |
| 60-69 | C | Below average; multiple critical gaps |
| 40-59 | D | Poor; significant rework needed |
| 0-39 | F | Not competitive; requires complete rewrite |

---

## 五、一句话诊断生成规则

系统必须能生成以下格式的一句诊断：

> **"Your listing scores {overall}/100 — you lost points on {top2_missing_dims} ({lost_score1+lost_score2} points), and {weakest_sub_item}."**

Examples:
- "Your listing scores 72/100 — you lost points on missing A+ Content (10 points) and weak keyword distribution (5 points); fix these first."
- "Your listing scores 85/100 — you lost points on low review count (3 points) and bullet point prioritization (3 points); add 2 more images for a quick win."
- "Your listing scores 58/100 — you lost points on title keyword placement (5 points), image count (4 points), and missing description (3 points); start by reworking the title."

---

## 六、相比竞品的差异化优势

| 能力 | JS LQS | H10 | ZonGuru | **SellerAI** |
|------|--------|-----|---------|-------------|
| 标题长度检测 | ✅ | ✅ | ✅ | ✅ + 语义质量 |
| 图片数量检测 | ✅ | ✅ | ❌ | ✅ + 类型多样性 |
| Bullet 数量检测 | ✅ | ✅ | ❌ | ✅ + 优先级排序 |
| 描述长度检测 | ❌ | ✅ | ❌ | ✅ + HTML 格式 |
| 关键词覆盖率 | ✅ | ✅ ✅(KPS) | ✅ | ✅ + 分布均衡性 |
| A+ 内容检测 | ❌ | ❌ | ❌ | ✅ **独有** |
| 差评语义分析 | ❌ | ❌ | ❌ | ✅ **独有** |
| Backend Search Term | ❌ | ❌ | ❌ | ✅ |
| 一句话诊断 | ❌ | ❌ | ❌ | ✅ **独有** |
| Quick Wins 清单 | ❌ | ❌ | ❌ | ✅ **独有** |
| COSMO/Rufus Ready | ❌ | ❌ | ✅ | 后续版本 |
| 竞品对比模式 | ❌ | ✅ | ❌ | 后续版本 |

---

## 七、实施建议

1. **Phase 1 (MVP)：** 实现 8 个维度的规则检测（纯编程判断子项 80%），AI 仅处理语义判断子项（标题可读性、Bullets 优先级、A+ 视觉质量、差评语义分析）
2. **Phase 2：** 接入竞品 Top 10 数据，增加「相对评分」——不只告诉你得分，还告诉你 vs 类目中位数/前10均值的差距
3. **Phase 3：** 增加 COSMO/Rufus AI-Ready 检测（对标 ZonGuru 差异化），检测 listing 是否包含 AI 购物助手可提取的结构化信息
4. **Phase 4：** AI 一键优化——根据诊断结果直接在 Listing 编辑器中应用修改建议

---

> **文档版本：** v1.0 | **作者：** SellerAI Product Design Team | **日期：** 2026-07-15
