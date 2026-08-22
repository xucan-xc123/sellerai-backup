# 2026-07-19 UI 六项修复 + 页面重构

## 改动清单

### 1. License 弹窗位置修复
- **文件**: `components/QuotaBadge.tsx`
- **改动**: 外层容器改为 `items-start justify-center pt-[15vh] overflow-y-auto`，弹窗始终在屏幕中上部垂直居中显示
- **之前**: `fixed inset-0 flex items-center justify-center` — 但内容超出了视口

### 2. ComparisonTable 废弃列已移除
- **文件**: `app/page.tsx`
- **改动**: 首页对比表组件已完全移除，不再展示 PowerListing/Jungle Scout/Helium 10 对比

### 3. 定价切换中文→英文
- **文件**: `components/Pricing.tsx`
- **改动**: "按月" → "Monthly"，"包年" → "Annual"，"省约 50%" → "Save ~33%"

### 4. Pro 版本移除
- **文件**: `components/Pricing.tsx`
- **改动**: 删除 Pro 卡 ($49.9 "Coming Soon") 及其类型定义 `comingSoon` 字段
- **定价 4 卡 → 3 卡**: Free / Starter(含 Basic+Unlimited子选项) / Founder
- grid 布局同步: `lg:grid-cols-4` → `lg:grid-cols-3`，max-w 收窄

### 5. 中国卖家指引取消
- **文件**: `components/Footer.tsx`
- **改动**: 完全移除折叠面板（含🇨🇳按钮 + 中文购买指引内容），Footer 恢复干净的三链接底部栏
- 不再 import `useState`（移除了唯一的 state 使用）

### 6. 页面路由重构
- **首页 `/`**（已从 51kB 瘦身至 **3.61kB**）: Navbar → Hero → TrustBar → Features → Pricing → FAQ → FinalCTA → Footer
- **工具页 `/tools`**: 独立简短 Hero → ListingGenerator → ProductDemo → WorkflowNarrative → Footer
- 所有 CTA 按钮从 `onClick toggle` 改为 `<Link href="/tools">`，纯路由跳转
- 之前塞在首页的 14 个组件压缩为 8 个核心销售组件，工具交互搬到 `/tools`

### 未改但已就绪
- Bullet Points 的单条复制 + Copy All ✅
- Description (HTML) 代码框 + Copy 按钮 ✅
- QuotaBadge 内嵌在 Navbar 工具栏 ✅
- 页面路由重构（子 Agent 完工，首页已按新结构运行）

## 部署
- Cloudflare Workers Version: `a5209812-c4b1-4d8a-9556-ee12e7cca784`
- 站点: https://sellerai.listaikit.com
