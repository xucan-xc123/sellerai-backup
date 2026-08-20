# 定价页更新部署日志

**日期：** 2026-07-18  
**执行者：** Subagent  
**状态：** ✅ 构建通过（EXIT 0）

---

## 任务清单

### 1. 定价页组件更新 (`components/Pricing.tsx`)

| 项目 | 旧值 | 新值 |
|------|------|------|
| Free Trial | $0 / 3天 | $0 / 7天 |
| Starter 月付 | $19.9 | **$14.9** |
| Starter 年付总计 | $119/年 (原$119，名义未变但实际月付降为$9.9/mo) | **$119/年** (Save 33%) |
| Starter badge | 无 | **"Most Popular"** |
| Growth 月付 | $24.9（不变） | $24.9 |
| Growth 年付总计 | $199/年 | **$189/年** (Save 37%) |
| Pro 月付 | $39.9（不变） | $39.9 |
| Pro 年付总计 | $299/年（不变） | $299/年 (Save 38%) |
| Pro 权益 | 含"Priortiy queue" | 改为 "Rufus-optimized content" + "Priority generation queue" |
| "Coming Soon" 标签 | ✅ 已移除 | — |
| 所有购买按钮 | Gumroad | ✅ 保持 `xucan.gumroad.com/l/sellerai` |
| 高亮层 | Growth（旧） | **Starter**（新，Most Popular） |

### 2. Listing Scorer CTA 按钮 (`tools/listing-scorer/ListingScorer.tsx`)

- 原 `<a>` 标签 → 改为 `<Link>` 组件（修复 eslint 规则 `@next/next/no-html-link-for-pages`）
- CTA 文字：**"Generate AI-Optimized Listing →"**
- 跳转目标：`/?open=generator`

### 3. 构建结果

- **命令：** `npm run build`
- **编译：** ✅ Compiled successfully（1854ms）
- **页面生成：** ✅ 14/14 静态页面全部生成
- **ESLint:** 仅 2 个 warning（Pre-existing: custom font warning + listingScorer.ts L206 unused-expression — 均为已有 issue，非本次引入）
- **退出码：** `0`

### 4. 构建产出路由表

| 路由 | Size | 类型 |
|------|------|------|
| `/` | 12.9 kB | Static |
| `/tools/listing-scorer` | 5.71 kB | Static |
| `/tools/keyword-tool` | 3.51 kB | Static |
| `/blog` | 1.04 kB | Static |
| + 其他 10 条路由 | — | Static/Dynamic |

### 5. 未完成/限制

- 未 `git push`（按约束要求，部署链路堵塞）
- 未触及 `DEEPSEEK_API_KEY`
- 锁文件警告（`sellerai-frontend/package-lock.json` vs workspace root `package-lock.json`）由项目结构造成，不影响构建

---

## 附件

- 修改文件：`E:\QClaw\Work-QClaw\sellerai-frontend\components\Pricing.tsx`
- 修改文件：`E:\QClaw\Work-QClaw\sellerai-frontend\app\tools\listing-scorer\ListingScorer.tsx`
