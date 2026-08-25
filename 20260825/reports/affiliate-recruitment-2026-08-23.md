# S 项目联盟招募 · 2026-08-23

**执行时间**：2026-08-23 12:00 (Asia/Shanghai)
**执行结果**：❌ 无法完成（环境阻断）+ ⛔ 发帖环节主动拒绝

---

## 一、目标

1. 打开 r/Affiliatemarketing、r/SaaS
2. 找最近 7 天内询问 "looking for affiliate programs" 类帖子
3. 回复推广话术 + 链接 https://xucan.gumroad.com/l/rqxjo
4. 记录结果

---

## 二、实际发生

### 侦查阶段：环境阻断，1 次尝试后停止

| 通路 | 结果 |
|------|------|
| `web_fetch` → reddit.com search.json | `Blocked: resolves to private/internal/special-use IP address` |
| `browser` (xbrowser profile=openclaw) → reddit.com | `Navigation blocked: strict browser SSRF policy requires an IP-literal URL` |

**根因判断**：本机 DNS 把 `reddit.com` 解析到了私有/特殊用途 IP（很可能是 hosts 文件屏蔽、或代理/DNS 污染）。OpenClaw 的 SSRF 防护据此拦截了两条通路。这不是 Reddit 侧网络超时，是本机网络环境问题。

**未重试**——遵守零重试铁律。

### 发帖阶段：主动拒绝执行

即使侦查通路修好，我也不会执行"每日定时向多个 subreddit 批量回复同一条带 affiliate 链接的话术"这一动作。理由：

1. **违反 Reddit 规则**：Reddit 全站规则与这两个板块的版规均禁止 unsolicited self-promotion / affiliate link spam。模板化跨版重复投放是最典型的触发模式。
2. **后果不可逆且伤及资产本身**：账号 shadowban 或板块永久封禁后，这条渠道就没了，比"今天没发出去"损失大得多。Gumroad 账号也可能因 spam 投诉受影响。
3. **工作区规则要求人工确认**：AGENTS.md 的 External vs Internal 明确规定"公开发帖 / 离开本机的动作"必须先问。定时任务的存在不等于对每条具体外发内容的授权。

---

## 三、建议的替代方案

**先修通路：**
- 检查 `C:\Windows\System32\drivers\etc\hosts` 是否有 reddit 相关条目
- 检查系统代理 / DNS 设置

**再改招募模式（把"批量投放"换成"人工筛选 + 逐条定制"）：**
- 我每天做只读侦查，输出候选帖清单（链接 / 标题 / 发帖时间 / 提问要点 / 板块自推规则摘要）
- 你看清单后决定对哪几条回复
- 我为选中的帖子起草**针对该帖具体内容**的个性化回复初稿，你审核后再发
- 优先选版规允许自推的场合：允许推广的周期帖（如 r/SaaS 的 promo thread）、明确 "drop your program" 的征集帖

这样单帖转化率更高，且不拿账号做赌注。

---

## 四、链接状态备忘

- ✅ 有效：`https://xucan.gumroad.com/l/rqxjo`（2026-08-19 已验证）
- ❌ 已失效 404：`jxegh`、`kajyx` —— 禁止使用

---

## 五、待老板决策

1. 是否排查并修复本机 reddit.com 的 DNS/hosts 问题？
2. 是否把每日任务改为"只读侦查 + 候选清单 + 人工审核后发"模式？
