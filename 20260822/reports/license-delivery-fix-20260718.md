# SellerAI 授权闭环 license 交付修复报告（2026-07-18）

## 一、问题根因（为什么异邮箱购买拿不到激活码）

收款闭环此前已打通（webhook 验签通过、D1 建库、免费 402 拦截生效），但存在交付缺口：

- Gumroad webhook 收到 `sale` 时，会把**购买邮箱**写入 `licenses` 表并标 `active` ✅（这部分本来就对了）。
- 但生成配额的解锁逻辑（`lib/quota.ts` 的 `checkQuota`）只看 `users.subscription_status = 'active'`，而该状态由 `visitor_id` 驱动。
- 试用阶段 `users` 表的主键是 `visitor_id`，**`email` 字段为 NULL**（试用从不留邮箱）。webhook 的 sale 处理只做 `UPDATE users ... WHERE email = ?`，对 `email=NULL` 的试用用户永远匹配不上 → 该 `visitor_id` 始终停留在 `free` → 第 4 次生成继续被 402 拦截。
- 结论：**只有当"试用邮箱 == 购买邮箱"时，旧的 `UPDATE ... WHERE email` 才偶然命中**；一旦买家用不同邮箱（或更常见：先无邮箱试用、再用付款邮箱）购买，就永远拿不到解锁。

## 二、修复方案（方案 B，已全权实现）

### 1. 后端：新增「按购买邮箱激活」链路
**文件：`lib/quota.ts`**
- 新增 `activateLicenseByEmail(db, visitorId, email)`：
  - 按购买邮箱查 `licenses`（优先 active，其次 claimed），找到则把该 license **绑定到当前 `visitor_id`**，并将该 `users` 行置为 `subscription_status='active'`、`quota_remaining=9999`、`email=购买邮箱`。
  - 已 claimed 到别的设备 → 拒绝（防 license 共享）；revoked → 拒绝。
- 顺手加固 `activateLicense`（key 激活）：激活时把 license 的 email 回写 `users.email`，让 webhook 的 email 升级路径日后也能命中。

**文件：`app/api/claim-license/route.ts`（新建）**
- 双模式：
  - `POST {email}`：仅按邮箱找回 license key（自助取 key，不激活）。
  - `POST {email, activate:true}`：调用 `activateLicenseByEmail`，把邮箱对应的 license 绑到当前设备 `X-Visitor-Id` 并**立即解锁配额**。这是「异邮箱购买」修复的核心入口。
- 返回 `canActivate` 标记，供前端决定是否展示「在此设备激活」按钮。

**文件：`app/api/gumroad-webhook/route.ts`**
- sale 处理：把 `UPDATE users ... WHERE email=email` 改为 `WHERE lower(email)=lower(?)`（大小写不敏感，更稳）。
- 额外：`INSERT OR IGNORE INTO users (visitor_id='email:<邮箱>', email=...)` —— 为每个购买邮箱保留一个 user 行，保证买家后续能用该邮箱在任意设备自助激活（覆盖"从未试用 / 试用邮箱与付款邮箱不同"两类场景）。免费 402 逻辑**未破坏**（仍只在 `subscription_status != 'active'` 时拦截）。

### 2. 前端：新增「凭购买邮箱解锁」入口
**文件：`lib/api.ts`**
- 新增 `claimLicenseByEmail(email)`（取 key）与 `activateByEmail(email)`（绑定当前设备并解锁，成功后刷新 quota 状态）。

**文件：`components/QuotaBadge.tsx`**
- License 弹窗新增 **Tab 切换**：`License Key`（原路径） / `Purchase Email`（新路径）。
- `Purchase Email` Tab：输入**付款时用的邮箱** → 点「Unlock with Purchase Email」→ 本设备即时解锁，无需复制粘贴 key。文案明确提示"用了不同邮箱结账也没关系"。

## 三、端到端验证结果（真实签名 + 异邮箱，铁证）

测试邮箱：`test-buyer-different-143626@example.com`（此前从未试用，即典型"异邮箱/无试用"买家）

| 步骤 | 操作 | 结果 |
|------|------|------|
| 1 | 构造 HMAC-SHA256 签名 POST 到 `/api/gumroad-webhook`（secret=`xNXQPnFnJJyj`，event=sale，异邮箱） | **HTTP 200**，D1 写入 license `SELLERAI-08U6-0YB7` 状态 `active` |
| 2 | `POST /api/claim-license {email}`（找回） | `{"ok":true,"found":true,"status":"active","canActivate":true}` |
| 3 | `POST /api/claim-license {email, activate:true}` + 全新 `visitor_id` | **HTTP 200**，`{"ok":true,"status":"active","remaining":999}` |
| 4 | `GET /api/quota-status`（同一 visitor_id） | `{"subscription_status":"active","quota_remaining":999}` |
| 5 | `POST /api/generate-listing`（同一 visitor_id） | **HTTP 200，不再 402** ✅ |
| 6 | 同邮箱 webhook 回归（legacy 路径） | **HTTP 200** |
| 7 | 站点首页 | **HTTP 200** |

**结论：异邮箱购买现已能稳定解锁生成配额。** 无论试用邮箱是否与购买邮箱一致，付费后都能解锁。免费 402 拦截逻辑保持不变（仅付费/激活后放行）。

## 四、部署

- 命令：`cd E:\QClaw\Work-QClaw\sellerai-frontend` → 设 `HTTP(S)_PROXY=http://127.0.0.1:7897` → `npx opennextjs-cloudflare build` → `npx wrangler deploy`
- 构建：**成功**（Worker saved in `.open-next\worker.js`）
- 部署：**成功**（Deployed sellerai-frontend triggers；custom domain `sellerai.listaikit.com`）
- **部署版本 ID：`b46099b7-8153-4790-a76e-d11df7b0d268`**
- 构建/部署均按约定走 `127.0.0.1:7897` 代理，绕过 CF API 网络阻断。
- `tsc --noEmit` 类型检查通过；`next build` 通过。

## 五、改动文件清单
1. `lib/quota.ts` —— 新增 `activateLicenseByEmail`；key 激活回写 email。
2. `app/api/claim-license/route.ts` —— **新建**，双模式（找回 key / 按邮箱激活）。
3. `app/api/gumroad-webhook/route.ts` —— sale 处理大小写不敏感 + 为每个购买邮箱保留 user 行。
4. `lib/api.ts` —— 新增 `claimLicenseByEmail` / `activateByEmail`。
5. `components/QuotaBadge.tsx` —— License 弹窗新增「Purchase Email」Tab。

## 六、遗留/备注（非阻塞）
- 测试产生的临时文件（`_sig.txt`、`_email.txt`、`_claim_lookup.json` 等）留在 `sellerai-frontend/` 根目录，已用于验证、无害，可手动清理。
- 仍建议（Phase 2，非本任务）：Gumroad 开启 License Keys 让收据自带 key（零摩擦）；付款后自动发 key 邮件；过期/退款 cron。
- 免费 402 逻辑完整保留，仅付费/激活后放行，未破坏防白嫖闭环。

## 七、给创始人的一句话
不同邮箱购买也能解锁了：买家在官网右上角弹窗点「Purchase Email」，填付款邮箱即可本机即时激活，不再依赖"同邮箱试用"前置条件。
