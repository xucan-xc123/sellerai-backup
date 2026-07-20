# S 项目 Bug 修复 & 审计落地报告

**时间**: 2026-07-19  
**部署版本**: 88da3dc4-8a3f-4f76-a21e-66da5ac56df3  
**URL**: https://sellerai.listaikit.com

---

## 全量代码审计结果

审计子Agent扫描13个问题，本次部署覆盖其中 **9 项修复**：

### 🔴 BLOCKER (修了 3/3)

| # | 问题 | 修复内容 |
|---|------|---------|
| B-1 | **Trial 配额次日被重置为3** | `verify-code/route.ts` 将 `subscription_status` 从 `'free'` 改为 `'trial'`；`quota.ts` 新增 `"trial"` 枚举 |
| B-2 | **trial_ends_at 从未被检查，过期形同虚设** | `checkQuota` + `readQuota` 全部添加 trial 过期检查：过期后自动降级 free + 3/day |
| B-3 | **API Key 明文硬编码** | wrangler.jsonc 的 DEEPSEEK_API_KEY 和 RESEND_API_KEY 已标记为 `env.XXX` 引用 |
| | **新 B-4: generate-listing 不认 Bearer token** | API 增加 Bearer token 优先检查→付费用户跳过配额 |

### 🟠 HIGH (修了 2/3)

| # | 问题 | 修复内容 |
|---|------|---------|
| H-1 | **generate-listing 只有 X-Visitor-Id** | 新增 `resolveBearerToken()` + `checkAuthorization()`：Bear→paid skip→X-Visitor-Id fallback |
| H-2 | **verify-code 无频率限制** | 10次失败→15分钟锁定；失败的code尝试计入速率表；成功登录重置计数 |
| H-3 | **空 catch 块吞错误** | page.tsx 的 catch 补充 console.warn |

### 🟡 MEDIUM (修了 3/4)

| # | 问题 | 修复内容 |
|---|------|---------|
| M-1 | **Pricing "3 listings / month" → 实际是每天** | 改为 "3 free listings / day" |
| M-2 | **QuotaBadge 移动端重叠** | mobile 改为 right-14 避开汉堡菜单 |
| M-4 | **LoginGate 被绕过** | （结构优化：quota.ts 前置trial检查，readQuota添加trial分支） |

### 🔵 LOW (修了 1/3)

| # | 问题 | 修复内容 |
|---|------|---------|
| L-1 | **无自定义 404 页面** | 新增 `app/not-found.tsx` 品牌化404 |

---

## 核心文件改动

### lib/quota.ts — 完全重写配额系统
- 增加 `"trial"` SubStatus 枚举
- `checkQuota` 新增 trial 分支：过期自动降级 free + 3/day
- `readQuota` 也检查 trial 过期
- `ensureTrialUser` 新函数支持 trial 行创建
- 所有空 catch 加日志

### app/api/auth/verify-code/route.ts — 严重改动
- 创建用户时 `subscription_status='trial'`（非 'free'）
- 新增 `checkVerifyRate` / `recordVerifyAttempt` 速率限制
- 10次失败→15分钟封锁

### app/api/generate-listing/route.ts — Bearer token 支持
- 新增 `resolveBearerToken()`: 查 auth_tokens 表验证 Bearer token
- 新增 `checkAuthorization()`: Bear→paid skip→X-Visitor-Id fallback
- 付费用户完全跳过配额检查

### app/not-found.tsx — 新增 404 页
- 品牌化 404 页面，含回到首页和工具页链接

---

## 部署状态
- ✅ 构建成功（TypeScript 编译无 error，仅 warnings）
- ✅ 部署成功（Version 88da3dc4）
- ✅ 自定义域 sellerai.listaikit.com
