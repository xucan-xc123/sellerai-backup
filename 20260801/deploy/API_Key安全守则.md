# SellerAI API Key 安全守则

> 最后更新：2026-07-15

---

## 🔐 Key 存储位置

| Key | 存放位置 | 是否上传 GitHub |
|------|------|:--:|
| DeepSeek `sk-a29e99...` | `sellerai-backend\.env`（本地） | ❌ 已在 `.gitignore` |
| DeepSeek `sk-a29e99...` | Vercel → Settings → Environment Variables | ✅ Vercel 加密存储 |

- `.env` 文件不会进入 GitHub（`.gitignore` 已排除）
- 发给 AI 助手的聊天记录中有 Key 片段，但**当前会话结束后 Key 不会泄漏到其他对话**

---

## 🚫 绝对不要做的事

| 禁止 | 原因 |
|------|------|
| ❌ 把 Key 发到微信群/朋友圈 | 任何人都能用扣你的钱 |
| ❌ 把 `.env` 文件上传到 GitHub | 爬虫扫描 30 秒就能发现 |
| ❌ 在公开论坛（知乎/Reddit）贴 Key | 永久留痕 + 被滥用 |
| ❌ 把 Key 交给陌生人 | 等于把钱包密码给人 |

---

## ✅ 安全操作清单

| 场景 | 正确操作 |
|------|------|
| 需要换 Key | 在 DeepSeek 后台「删除旧 Key → 创建新 Key」→ 更新 `.env` |
| 怀疑 Key 泄漏 | 立刻在 `platform.deepseek.com` → API Keys → Delete → 重新创建 |
| 部署到 Vercel | 在 Vercel Dashboard → Settings → Environment Variables 填入（加密存储） |
| 本地开发 | 只用 `.env` 文件，确保 `.gitignore` 排除它 |

---

## 💰 余额监控

- **每日自动检查**：每天早上 9:00，脚本 `check_balance.py` 自动运行
- **告警阈值**：
  - ⚠️ 余额 < ¥5 → 提醒充值（粉色预警）
  - 🚨 余额 < ¥1 → 紧急告警（红色预警）
- **异常检测**：如果单日消耗超过 ¥10（正常应 < ¥0.1），AI 会主动报警
- **充值地址**：https://platform.deepseek.com/top_up

---

## 🔑 DeepSeek 后台操作

| 操作 | 路径 |
|------|------|
| 查看余额 | https://platform.deepseek.com → 首页即可看到 |
| 查看 API 用量 | https://platform.deepseek.com/usage |
| 创建/删除 Key | https://platform.deepseek.com/api_keys |
| 充值 | https://platform.deepseek.com/top_up |
| 设置消费限额 | https://platform.deepseek.com → 设置 → 消费上限 |
| 查看账单 | https://platform.deepseek.com/billing |

> ⚠️ **强烈建议**：在 DeepSeek 后台设置「月度消费上限」¥50，防止 Key 泄漏后被疯狂调用导致大额损失。
