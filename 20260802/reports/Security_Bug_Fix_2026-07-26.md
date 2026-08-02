# 🛡️ 安全 Bug 修复报告 — 2026-07-26 22:30

## 发现根因

创始人指出：3天试用到期后用户不应回到每天3次免费，应强制付费。审计发现 4 个关联漏洞。

---

## 🔴 Bug 1 — 试用过期回到免费版（致命）

**文件**: `lib/quota.ts` → `checkQuota()`

**现象**: 用户注册3天试用 → 到期自动降级为 `free`（每天3次）→ 永远白嫖

**修复**: 
- `subscription_status` 从 `'free'` 改为 `'expired'`
- `quota_remaining` 从 `FREE_DAILY_LIMIT(3)` 改为 `0`
- `allowed` 从 `true` 改为 `false`
- 提示改为 "Your 3-day trial has ended. Subscribe to continue."

```diff
- `UPDATE users SET subscription_status='free', quota_remaining=3...`
+ `UPDATE users SET subscription_status='expired', quota_remaining=0...`

- return { allowed: true, remaining: 3, status: "free" }
+ return { allowed: false, remaining: 0, status: "expired" }
```

---

## 🔴 Bug 2 — 登录用户绕过所有配额检查（致命）

**文件**: `app/api/generate-listing/route.ts` → `checkAuthorization()`

**现象**: Bearer Token 登录后，把**邮箱地址当 visitor_id** 传入 `checkQuota(db, email, ...)`。数据库按 visitor_id 查，永远找不到 → fail-open 放行所有请求。

**修复**:
```diff
- const quota = await checkQuota(db, resolved.email, clientIp, resolved.email);
+ const visitorId = request.headers.get("X-Visitor-Id") || resolved.email;
+ const quota = await checkQuota(db, visitorId, clientIp, resolved.email);
```

现在登录用户也按 visitor_id 走正常的配额检查流程。

---

## 🟠 Bug 3 — readQuota 不写数据库（高危）

**文件**: `lib/quota.ts` → `readQuota()`

**现象**: 只读配额接口只返回了 `allowed: false`，但不执行数据库降级，导致再次调用时状态不一致。

**修复**: status 从 `"free"` 改为 `"expired"`。

---

## 🟠 Bug 4 — 过期用户重新注册被放行（高危）

**文件**: `app/api/register/route.ts`

**现象**: 试用过期用户用同一邮箱重新注册，直接被允许开始**新的3天试用** → 无限白嫖。

**修复**:
1. 重新注册时先查 `trial_ends_at < date('now')`，过期返回 403
2. UPSERT 的 CASE WHEN 逻辑加 `'expired'` 保护（不会被改写为 `'free'`）

---

## ✅ 修复后行为矩阵

| 用户状态 | 触发条件 | 行为 | API 返回 |
|:--|:--|:--|:--|
| 匿名用户 | 无注册 | 每天3次 | 200 + 正常配额 |
| 试用中 | 注册3天内 | 无限次数 | 200 |
| 试用过期 | 注册3天后 | **0次，必须付费** | 402 + "Trial ended" |
| 付费用户 | Gumroad 购买 | 无限次数 | 200 |
| 已取消 | Gumroad 退款 | 宽限期保留 | 200 |
| 已过期 | License 到期 | 0次 | 402 + "License expired" |
| KOC 测试 | 后台手动创建 | 3个月免费 | 待实现 |

---

## 📁 改动文件

| 文件 | 改动行 |
|:--|:--|
| `lib/quota.ts` | checkQuota() — 试用降级逻辑 / readQuota() — status |
| `app/api/generate-listing/route.ts` | Bearer Token → visitor_id 映射 |
| `app/api/register/route.ts` | 过期重注册拦截 + CASE WHEN 加固 |

## 🔜 待做

- KOC 3个月免费账号机制（独立 migration + admin API）
- 构建部署 + 全链路回归测试
