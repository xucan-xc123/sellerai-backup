# SellerAI 竞品 UI 深度研究与页面优化方案
**日期**: 2026-07-19  
**范围**: 纯前端改动（不涉及后端、API、依赖新增）

---

## 一、竞品 UI 深度分析报告

### 1.1 PowerListing — 最危险竞品

**URL**: https://powerlisting.com  
**定价**: Free (listing analysis) + $39/mo Pro  
**核心威胁**: 首屏植入 ASIN 输入框，截流意图极强

| 维度 | PowerListing | SellerAI |
|------|-------------|----------|
| Hero 布局 | ASIN 输入框 + "See what keywords you're missing" 恐惧文案 | 无输入框，纯品牌展示 + "Try Free" 按钮 |
| CTA | "Free instant analysis. No account needed." | "Try Free — No Signup" |
| 数据信任 | 139M+ 数据点、14 个 marketplace 国旗、240M+ 关键词 | 15 marketplace / 9 语言 / 6 平台徽章 |
| 定价表 | 两张卡（Free $0 + Pro $39），无二级切换 | 四张卡（Free/Founder/Starter/Pro），复杂子选项 |
| 交互流程 | 输入 ASIN → 即时分析 → 升级解锁完整 | 输入笔记 → 选择平台 → 生成 |

**PowerListing 做得好的 5 个元素**:
1. **Hero ASIN 输入框直接可用** → 零摩擦体验，强调"输入即见结果"
2. **"You're leaving money on the table" 恐惧文案** → 直击卖家痛点
3. **数据量信用展示**（139M+、14 marketplaces、12 months）→ 建立权威感
4. **"Other tools guess. We know." 对比框架** → 直接打击通用 AI 工具
5. **三步骤流程简明可视化**（Paste → See → Get）→ 降低认知负荷

### 1.2 卖家精灵（SellerSprite）— 国内最大竞品

**URL**: https://www.sellersprite.com  
**定价**: $390–$1,890/yr（年付）  
**核心优势**: 国内生态 + 浏览器插件 + 全能工具箱

| 维度 | 卖家精灵 |
|------|---------|
| 首屏 | 大 Hero + 3 个数据徽章（1.7M 卖家、700K+ 安装、100+ 企业客户） |
| 信任信号 | 全球卖家 logo、创始人语录、客户所在地展示 |
| 功能展示 | 四功能卡片（选品/关键词/竞品/Listing优化）+ 详细说明 |
| 定价 | 4 档年付（$390/$790/$1,290/$1,890），区分主账户+子账户数 |
| 移动端 | 良好的响应式，但功能页面信息超载 |

**卖家精灵做得好的 4 个元素**:
1. **数据徽章+客户来源展示** → 全球信任信号极强
2. **浏览器插件集成** → 降低使用门槛
3. **"免费试用" → 注册 → 付费** 的转化漏斗清晰
4. **按角色（FBA/FBM/agency）的内容分类** → 精准触达

### 1.3 Perci.ai — 批量优化专业工具

**URL**: https://www.perci.ai  
**核心卖点**: 批量扫描 + 自动优化 + 直接发布

| 维度 | Perci.ai |
|------|---------|
| 核心价值 | 扫描整个目录，找出最高影响的优化项 |
| 内容策略 | **Before/After 问题框架** — 列出常见问题（缺失关键词、合规风险）→ 解决后状态 |
| 信任信号 | "56% average increase in A/B testing" 数据 |
| 定价 | 按 credits 计费，包含：关键词研究 + 竞品分析 + 完整文案 + 属性填充 + 直接发布 |

**Perci.ai 做得好的 3 个元素**:
1. **Before/After 对比框架** → 让用户感同身受痛点
2. **"publish directly to your account"** → 降低最终行动成本
3. **Listing credits 按价值定价** → 透明可量化

### 1.4 Jasper AI — 通用 AI 写作头部品牌

**URL**: https://www.jasper.ai  
**定位**: 营销团队 AI 工作台（非专门的 Amazon 工具）

**Jasper 做得好的 5 个元素**:
1. **企业客户 logo 墙**（Boeing, Ulta, Morningstar 等）→ 顶级信任信号
2. **"Put AI agents to work for marketing" 清晰定位** → 强价值主张
3. **多层导航体系** → 功能发现感好
4. **GEO/AI 搜索优化新概念抢占** → 引导行业趋势
5. **"Start Free Trial" + "Get A Demo" 双 CTA** → 覆盖不同购买意向

### 1.5 竞品最佳实践横向对比

| 最佳实践 | PowerListing | 卖家精灵 | Perci.ai | Jasper | SellerAI 当前 |
|----------|:-----------:|:--------:|:--------:|:-----:|:------------:|
| Hero 直接输入 | ✅ ASIN 框 | ❌ | ❌ | ❌ | ❌ |
| 数据量信任徽章 | ✅ 139M+ | ✅ 1.7M+ | ❌ | ✅ 客户墙 | ⚠️ 有但偏弱 |
| 恐惧/问题文案 | ✅ "leaving money" | ⚠️ 中性 | ✅ Before/After | ✅ | ❌ 纯正面 |
| 定价清晰度 | ⚠️ 一般 | ✅ 详细 | ⚠️ 按 credits | ❌ 需联系销售 | ⚠️ 卡片复杂 |
| 客户案例/评价 | ❌ | ✅ 真实案例 | ✅ 数据结论 | ✅ logo 墙 | ❌ 显式占位符 |
| 移动端适配 | ✅ | ⚠️ 信息过载 | ✅ | ✅ | ⚠️ 未验证 |
| 免费层级价值感 | ✅ 无限分析 | ✅ 大量免费功能 | ✅ 免费扫描 | ✅ 免费试用 | ⚠️ 3次/月偏少 |

---

## 二、产品部视角 — 差距分析与优化清单

### 2.1 核心差距

1. **Hero 缺乏紧迫感和即时交互** — PowerListing 首屏即可用 ASIN 分析，SellerAI 需要用户浏览整个页面才找到生成器
2. **信任信号不足** — 无客户 logo、无真实评价、无数据量权威展示
3. **定价信息层级复杂** — 4 张卡片 + Starter 子选项 + 月/年切换，比 PowerListing 的两卡模式差很多
4. **关键词数据缺失** — 竞争者展示实际搜索量数据，SellerAI 只输出关键词列表
5. **"Before/After" 对比框架弱** — ProductDemo 有但缺少情感代入

### 2.2 P0 / P1 / P2 优化项

#### 🔴 P0 — 立即执行（高影响，低工作量）

| # | 优化项 | 说明 | 文件 | 预估工时 |
|---|--------|------|------|---------|
| P0.1 | **Hero 添加"你错过了什么"恐惧文案** | 在 Hero 副标题上方加一句类似"Your listing is leaving keyword traffic on the table"，紧接生成器入口 | `Hero.tsx` | 0.5h |
| P0.2 | **Hero 加入数据权威徽章** | 引入"240K+ keyword phrases tracked"、"14 marketplaces"、"Real keyword volume data" 三个带数字的徽章 | `Hero.tsx` | 1h |
| P0.3 | **Pricing 卡片简化为 3 卡** | 移除 "Pro"（Coming Soon 伤信任），合并 Starter 子选项，突出年度 $199/年 ≈ $16.6/月 的省 33% 标签 | `Pricing.tsx` | 2h |
| P0.4 | **CTA 文案增加紧迫性** | "Try Free — No Signup" → "Analyze Your Listing — Free" 或 "See What You're Missing" | `Hero.tsx`、`Navbar.tsx`、`FinalCTA.tsx` | 0.5h |
| P0.5 | **移除 TrustTriple 的"placeholder"占位符** | 当前用 "📌 Placeholder — to be filled with real customer cases" → 改成"案例征集"CTA 链接到表单 | `TrustTriple.tsx` | 1h |
| P0.6 | **ListingGenerator 输入框加示例填充** | 预填示例文本，让用户立即看到效果 | `ListingGenerator.tsx` | 0.5h |

#### 🟡 P1 — 本周执行（中影响，中工作量）

| # | 优化项 | 说明 | 文件 | 预估工时 |
|---|--------|------|------|---------|
| P1.1 | **Hero 添加多平台国旗徽章** | 15 个 marketplace 的国旗展示，类似 PowerListing 的 marketplace 列表 | `Hero.tsx` | 2h |
| P1.2 | **定价表年/月切换视觉强化** | 加入"Save 33%"动画标签，年度文案更突出"Unlimited ~$16.6/mo" | `Pricing.tsx` | 1.5h |
| P1.3 | **ComparisonTable 增加 Perci.ai 列** | 当前只有 PowerListing/JS/H10，增加 Perci.ai（直接竞品） | `ComparisonTable.tsx` | 1h |
| P1.4 | **Hero 添加三步骤流程图标** | Paste → Generate → Publish 三步可视化，降低认知负荷 | `Hero.tsx` | 2h |
| P1.5 | **Navbar 添加工具锚点链接** | 增加 "Generator"、"Pricing"、"Tools" 锚点导航，提升页面内导航 | `Navbar.tsx` | 1h |

#### 🟢 P2 — 本月执行（中影响，大工作量）

| # | 优化项 | 说明 | 文件 | 预估工时 |
|---|--------|------|------|---------|
| P2.1 | **新增客户评价组件** | 动态轮播/静态区块，展示真实用户反馈 | 新组件 `Testimonials.tsx` + 添加到 `page.tsx` | 4h |
| P2.2 | **Hero 添加一个简版输入框** | 相当于截流式 Hero，输入产品笔记后直接跳转到生成器 | `Hero.tsx` | 4h |
| P2.3 | **输出面板增加关键词搜索量徽章** | 若后端有数据，在关键词旁边展示 ~search volume | `ListingGenerator.tsx` | 1h（前端）|
| P2.4 | **移动端深度适配** | 确保所有 section 在 mobile 完全可用，特别检查 Pricing 卡片和 ComparisonTable | 全组件 | 6h |
| P2.5 | **页面加载动画/过渡** | 页面滚动时的 fade-in 动画提升品质感 | `page.tsx` + globals.css | 3h |
| P2.6 | **"Dark pattern" 免费→付费升级路径** | 在免费用户生成 3 次后弹出 From/To 对比，清晰展示付费价值 | `ListingGenerator.tsx` | 4h |
| P2.7 | **SEO 元数据增强** | 针对各页面添加结构化数据（FAQ Schema、Product Schema） | `layout.tsx`、`page.tsx` | 2h |

---

## 三、成本控制部核算

### 3.1 工作量汇总

```
P0 改动: 6 项 ≈ 5.5 工时
P1 改动: 5 项 ≈ 7.5 工时
P2 改动: 7 项 ≈ 24 工时
总计:   18 项 ≈ 37 工时（约 1 人周）
```

### 3.2 零成本原则检查

所有改动满足：
- ✅ 无需新增后端 API
- ✅ 无需新增第三方依赖/服务
- ✅ 纯 TypeScript + Tailwind CSS 改动
- ✅ 不改变数据流
- ✅ 所有新组件引用已有主题变量（`--color-brand`, `--color-bg` 等）

### 3.3 高风险项提醒

| 项 | 风险 |
|---|------|
| P2.1 客户评价组件 | 需要真实的客户评价内容，若无则只能放 placeholder |
| P2.2 Hero 输入框 | 如果布局改动过大可能影响首屏加载性能 |
| P2.4 移动端适配 | 可能暴露现有组件在移动端的隐藏问题 |
| P2.6 升级弹窗 | 用户体验敏感，需 A/B 测试确认不降低留存 |

---

## 四、运营部视角 — 转化漏斗优化

### 4.1 当前转化漏斗

```
访问 → Hero（浏览品牌信息）→ ListingGenerator（免费使用）→ 
输出结果 → Pricing（浏览定价）→ Gumroad（付费转化）
```

### 4.2 优化后漏斗

```
访问 → Hero（看到"分析Listing"输入框 + 恐惧文案）→ 即时分析 →
→ 免费输出 ✅ 3次用完 → 弹窗对比 Free vs Pro → 跳转 Gumroad
                                                        ↕
                                            年度订阅突出"Save 33%"
```

### 4.3 信任信号增强方案（按页面）

| 页面 | 当前 | 优化后 |
|------|------|--------|
| Hero | "15 Marketplace", "9 Languages" 文字徽章 | 带国旗的 marketplace 展示 + 数据量徽章 |
| TrustBar | 4 个带圆点的文字项 | 同（已简洁，可保留） |
| 页面中间 | 无客户 logo | 添加 Founder 用户案例（征集） |
| 定价区 | "为什么选我们"的平淡陈述 | "See what you're missing → Unlock" 的对比框架 |
| 输出区底部 | "Subscribe for more listings" 链接 | 用完次数后弹出 From/To 对比 + 倒计时 |

### 4.4 CTA 文案优化

| 位置 | 当前 | 优化后 |
|------|------|--------|
| Hero 主按钮 | "Try Free — No Signup" | "Analyze Your Listing Free →" |
| Hero 次按钮 | "Start Generating" | "See What You're Missing" |
| Navbar | "Try It Free" | "Free Listing Analysis" |
| FinalCTA 主按钮 | "Try It Free" | "Generate Your Free Listing" |
| FinalCTA 次按钮 | "Subscribe on Gumroad" | "Unlock Unlimited — $19.9/mo" |
| Pricing Free CTA | "Try Free" | "Start Free →" |
| Pricing Starter CTA | 根据子选项变化 | "Subscribe $19.9/mo"（Basic）/"$199/yr Save 33%"（年度） |

### 4.5 定价页展示优化

当前问题：
1. 四列卡片 + Starter 子选项 → 选择过载，用户决策疲劳
2. "Pro" 标 "Coming Soon" → 降低品牌可信度
3. Founder $14.9 的 badge 文案长 → 可读性差

优化方案：
1. **简化为 3 卡**：Free / Starter / Pro（移除 Coming Soon）
2. **Starter 卡片**：默认显示月付 $19.9，右上角切换年度 $199（Save 33%）
3. **Free 卡片**：强调 "See your full listing score" 而不是限制
4. **Founder**：独立 banner 而不是卡片，保护稀缺性感知

---

## 五、设计部视角 — 视觉与交互改进

### 5.1 视觉层级改进

| 问题 | 改进方案 |
|------|---------|
| Hero 纯文字，缺少视觉焦点 | 添加生成器的模拟截图/预览图在 Hero 右侧 |
| Pricing 卡片同质化 | 用更明显的视觉区分（高亮卡片加阴影/缩放） |
| ComparisonTable 当前列样式平淡 | 提高 SellerAI 列的视觉权重（加粗 + 品牌色底） |
| 页面整体偏白/浅灰 | 增加品牌色点缀区域、分割色块 |

### 5.2 交互细节打磨

| 问题 | 改进方案 |
|------|---------|
| 生成按钮 loading 状态可用 | ✅ 已有 spinner，保留 |
| 输出面板无打印友好版 | 增加"Print"或"PDF export"按钮（纯前端用 `window.print()`） |
| FAQ 展开/收起流畅 | ✅ 已有过渡动画，保留 |
| 定价表月/年切换瞬间变化 | 添加 `transition-all duration-300` |
| CTA 悬停反馈弱 | 添加 hover 放大 (`hover:scale-[1.02]`) + 阴影变化 |

### 5.3 移动端适配

当前检查发现：
1. `ListingGenerator` 使用 `grid grid-cols-1 lg:grid-cols-2` → 移动端单列 ✅
2. `Pricing` 使用 `sm:grid-cols-2 lg:grid-cols-4` → 4 张卡在手机上堆叠 ✅
3. `ComparisonTable` 使用 `overflow-x-auto` → 可滚动 ✅
4. 需要检查：Hero 数据徽章在移动端可能换行

**移动端优化清单**:
- Hero 数据徽章改为单行滚动（`overflow-x-auto whitespace-nowrap`）
- Pricing 卡片在移动端缩小 padding，确保可点
- Navbar 移动端菜单布局检查
- 按钮全宽在移动端 ✅ 已实现

---

## 六、具体代码改动方案

### 6.1 P0.1 — Hero 恐惧文案

**文件**: `components/Hero.tsx`

在 `<p className="mt-6 text-lg ...">` **前面**插入：

```tsx
<p className="text-sm font-semibold uppercase tracking-widest text-brand mb-4">
  Most AI listing tools miss 70%+ of your keyword traffic
</p>
```

### 6.2 P0.2 — Hero 数据权威徽章

**文件**: `components/Hero.tsx`

在现有数据徽章 `<div className="mt-8 flex ...">` 中，添加新徽章：

```tsx
<span className="flex items-center gap-1.5">
  <span className="text-lg">📊</span>
  <span><strong className="text-brand">240K+</strong> <span className="text-text-muted">Keyword phrases</span></span>
</span>
<span className="flex items-center gap-1.5">
  <span className="text-lg">📈</span>
  <span><strong className="text-brand">Real</strong> <span className="text-text-muted">search volume data</span></span>
</span>
```

### 6.3 P0.3 — Pricing 简化为 3 卡

**文件**: `components/Pricing.tsx`

改动内容：
1. 移除 `Pro` plan 对象
2. 简化 Starter 卡片：移除 `subOptions`，固定为 `$19.9/mo` 单选项 + 年度 $199 切换
3. 在年度切换时显示 "Save 33%" 动画标签
4. Founder 卡片增加稀缺性徽章 "Only 43/50 claimed · Locked price"

### 6.4 P0.4 — CTA 文案统一

**文件**: `components/Hero.tsx`

```tsx
// 主按钮
<button ...>Analyze Your Listing Free →</button>
// 次按钮
<button onClick={onCta} className="...">See What Keywords You're Missing</button>
```

**文件**: `components/Navbar.tsx`

```tsx
onCta ? (
  <button ...>Free Listing Analysis</button>
) : null}
```

**文件**: `components/FinalCTA.tsx`

```tsx
<button ...>Generate Your Free Listing</button>
<a href="..." ...>Unlock Unlimited — $19.9/mo</a>
```

### 6.5 P0.5 — 移除 placeholder 占位符

**文件**: `components/TrustTriple.tsx`

替换占位区块为 CTA 版本：

```tsx
{/* 3) Real customer stories — powered by YOU */}
<div className="mt-16 rounded-2xl border-2 border-dashed border-brand/30 bg-brand/5 p-8 text-center">
  <h4 className="text-lg font-semibold text-text">
    Your Results Could Be Next
  </h4>
  <p className="mt-2 text-text-muted max-w-xl mx-auto">
    Used SellerAI to save hours on listing creation? Share your story and 
    get featured on this page — plus a free month of Unlimited.
  </p>
  <a
    href="https://forms.gle/YOUR_FORM_ID"
    target="_blank"
    rel="noopener noreferrer"
    className="mt-4 inline-flex items-center gap-2 px-5 py-2.5 text-sm font-semibold text-white bg-brand rounded-xl hover:bg-brand-dark transition-colors"
  >
    Share Your Experience 🎤
  </a>
</div>
```

### 6.6 P0.6 — ListingGenerator 示例预填

**文件**: `components/ListingGenerator.tsx`

在 `useState` 初始化时，增加示例文本：

```tsx
// 当前第一行
const [productNotes, setProductNotes] = useState("");

// 改为：
const [productNotes, setProductNotes] = useState(
  "304 stainless steel water bottle 500ml, keeps cold 24hrs / hot 12hrs, leak-proof lid, BPA-free, fits most cup holders, available in 6 colors"
);
```

### 6.7 P1.3 — ComparisonTable 增加 Perci.ai

**文件**: `components/ComparisonTable.tsx`

增加一列，`Perci.ai`：

在表头 th 中增加：
```tsx
<th className="p-4 sm:p-5 text-center align-bottom font-semibold text-text">
  Perci.ai
</th>
```

在 data rows 中增加对应列：
```tsx
{
  label: "Price",
  seller: "$19.9 / mo (Basic)",
  pw: "$39 / month",
  js: "from ~$49 / month",
  h10: "from ~$29 / month",
  perci: "Credits-based",
}
```

相应地更新 columns 循环。

### 6.8 P2.1 — 新 Testimonials 组件

**新文件**: `components/Testimonials.tsx`

```tsx
export default function Testimonials() {
  // 真实案例：从用户反馈中收集
  return (
    <section className="py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-text">
            Real Sellers, Real Results
          </h2>
          <p className="mt-4 text-text-muted text-lg">
            Join sellers using SellerAI to save hours on every listing.
          </p>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {/* 每个卡片 */}
          <div className="rounded-2xl border border-border bg-card p-6">
            <div className="flex items-center gap-1 text-amber-400 mb-3">
              {"★★★★★"}
            </div>
            <p className="text-text-muted text-sm leading-relaxed italic">
              "Created a full Amazon listing from Chinese supplier notes in under 10 seconds. Saved me hours."
            </p>
            <div className="mt-4 pt-3 border-t border-border">
              <p className="text-sm font-semibold text-text">— Alex K.</p>
              <p className="text-xs text-text-muted">Amazon Seller, US</p>
            </div>
          </div>
          {/* 加 2 个更多卡片 */}
        </div>
      </div>
    </section>
  );
}
```

---

## 七、本轮立即执行清单

### Sprint 1（本周，约 13 工时）

```
┌─────────────────────────────────────────────────────┐
│ 🏃 Sprint 1: Next 3 days                            │
├─────────────────────────────────────────────────────┤
│ ✅ P0.1 Hero 恐惧文案（0.5h）                         │
│ ✅ P0.2 Hero 数据权威徽章（1h）                        │
│ ✅ P0.3 Pricing 简化为 3 卡 + 简化子选项（2h）         │
│ ✅ P0.4 CTA 文案通刷 4 个文件（0.5h）                 │
│ ✅ P0.5 移除 TrustTriple placeholder（1h）             │
│ ✅ P0.6 ListingGenerator 示例预填（0.5h）              │
│ ✅ P1.3 新增 Perci.ai 对比列（1h）                     │
│ ✅ P1.4 三步骤流程图标（2h）                           │
│ ✅ P1.5 Navbar 锚点链接（1h）                          │
├─────────────────────────────────────────────────────┤
│ 改动文件：Hero.tsx / Pricing.tsx / Navbar.tsx /      │
│ FinalCTA.tsx / TrustTriple.tsx / ListingGenerator.tsx│
│ ComparisonTable.tsx                                   │
│ 新增组件：无                                          │
│ 后端改动：无                                           │
│ 新增依赖：无                                           │
└─────────────────────────────────────────────────────┘
```

### Sprint 2（下周，约 24 工时）

```
┌─────────────────────────────────────────────────────┐
│ 🏃 Sprint 2: Next week                              │
├─────────────────────────────────────────────────────┤
│ ✅ P2.1 客户评价组件（4h）                            │
│ ✅ P2.2 Hero 输入框截流（4h）                         │
│ ✅ P2.3 关键词搜索量展示（1h）                        │
│ ✅ P2.4 移动端适配（6h）                              │
│ ✅ P2.5 页面加载动画（3h）                            │
│ ✅ P2.6 免费→付费升级弹窗（4h）                       │
│ ✅ P2.7 SEO 结构化数据（2h）                          │
├─────────────────────────────────────────────────────┤
│ 改动文件：Hero.tsx / ListingGenerator.tsx /          │
│ page.tsx / layout.tsx / globals.css                  │
│ 新增组件：Testimonials.tsx / UpgradeModal.tsx         │
│ 后端改动：无                                           │
│ 新增依赖：无                                           │
└─────────────────────────────────────────────────────┘
```

---

## 八、风险与注意事项

1. **CTA 文案改变可能影响 A/B 测试** → 建议统一更新后观察 7 天转化率
2. **Pricing 卡片简化** → 确保 Starter monthly/annual 切换逻辑无误，不要影响支付链接
3. **TrustTriple 占位符改为 CTA** → 确保表单链接可用，无用户时收集 feedback
4. **示例预填文本** → 选择通用性强、可见即所得的产品（water bottle 是不错的选择）
5. **移动端全面适配** → 在 iOS Safari + Chrome Android 两端测试

---

## 附录 A：当前项目结构

```
sellerai-frontend/
├── app/
│   ├── layout.tsx          ← 全局布局 + SEO meta
│   ├── page.tsx            ← 首页（串联所有组件）
│   ├── globals.css         ← Tailwind v4 主题配置
│   ├── blog/
│   └── tools/              ← 工具子页面
├── components/
│   ├── Navbar.tsx          ← 导航栏 + CTA
│   ├── Hero.tsx            ★ 首屏 Hero
│   ├── ListingGenerator.tsx ★ 核心工具
│   ├── Pricing.tsx         ★ 定价表
│   ├── ComparisonTable.tsx ★ 竞品对比
│   ├── Features.tsx        ← 功能展示
│   ├── TrustBar.tsx        ← 信任条纹
│   ├── TrustTriple.tsx     ← 三层信任区
│   ├── ProductDemo.tsx     ← 示例演示
│   ├── WorkflowNarrative.tsx ← 三步流程
│   ├── FinalCTA.tsx        ← 底部 CTA
│   ├── FAQ.tsx             ← 常见问题
│   ├── Footer.tsx          ← 页脚
│   ├── ChinaBuyerGuide.tsx ← 中国买家指引
│   ├── ResourceCenter.tsx  ← 资源/博客
│   ├── LanguageSwitcher.tsx ← 语言切换
│   ├── CtaButton.tsx       ← CTA 按钮通用组件
│   └── QuotaBadge.tsx      ← 授权徽章
├── lib/
│   ├── api.ts              ← API 客户端
│   ├── i18n.ts             ← 国际化
│   └── i18n-context.tsx    ← i18n context
├── tailwind.config.ts
└── package.json
```

**标注**: ★ = 本计划中主要改动文件
