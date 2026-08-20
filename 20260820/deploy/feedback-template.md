# 📝 SellerAI 客户反馈收集表设计（Feedback Collection Design）

> 版本：V1.0 ｜ 创建于：2026-07-16
> 用途：统一管理 Gumroad 买家反馈、官网表单字段、FAQ 自动回复话术。
> 关联文件：`templates/faq-replies.md`、《运营分工协议》§1 用户反馈自动迭代、§4 客服自动回复。

---

## 一、Gumroad 买家反馈（评论区 + 消息）

### 自动采集字段
| 字段 | 说明 | 用途 |
|------|------|------|
| buyer_id | Gumroad 买家 ID / 邮箱 | 关联使用记录 |
| usage_count | 该买家 API 调用次数（查后端日志） | 退款决策、白嫖判定 |
| rating | ⭐1-5（如买家留评） | NPS / 差评预警 |
| message | 原始留言（中英原文） | 分类与回复 |
| channel | 评论区 / 私信 / Tally | 分流 |
| timestamp | 反馈时间 | 周报汇总 |

### 反馈分类标签
- `bug` 工具报错 / 功能异常
- `feature` 功能请求
- `pricing` 价格相关
- `refund` 退款请求
- `praise` 好评
- `complaint` 投诉 / 差评
- `question` 一般咨询（FAQ 覆盖）

> 周日报自动统计：TOP 5 抱怨、TOP 3 功能请求（见《运营分工协议》§1）。

---

## 二、官网反馈表单字段（Tally.so）

> 部署位置：Vercel 官网 footer / 独立 `/feedback` 页；Gumroad 评论区缺失时作为补充入口。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| email | email | ✅ | 用于回访（与 Gumroad 邮箱交叉匹配） |
| plan | select | ✅ | Free / Starter($19.9) / Pro($49.9) / 创始会员($14.9) |
| type | select | ✅ | Bug / 功能请求 / 价格 / 退款 / 好评 / 其他 |
| rating | 1-5 星 | ❌ | 满意度 |
| message | textarea | ✅ | 详细描述（中英文均可） |
| allow_contact | checkbox | ❌ | 是否同意我们联系跟进 |

### 表单提交后自动动作（[AI]）
1. 写入 `reports/feedback-raw-YYYY-MM.md`
2. 命中 FAQ 类 → 自动回复（见第三节）
3. 标 `bug`/`feature` → 进周日报 TOP 榜
4. 标 `complaint`/`refund` → 标红转 [创始人]

---

## 三、FAQ 自动回复话术库（[AI] 自动匹配）

> 完整版见 `templates/faq-replies.md`。以下为高频标准话术速查，新反馈先在此匹配。

| 场景 | 触发关键词 | 标准回复（英文为主，中文用户用中文） |
|------|-----------|--------------------------------------|
| 怎么用 | how to use / 怎么用 / get started | Paste product description → click Generate → copy to Amazon. 视频：[link] |
| 价格 | price / cost / 多少钱 / free trial | Free 3/mo；Starter $19.9；Pro $49.9；创始会员 $14.9（限50） |
| 支持平台 | Temu / Shopify / platform | 支持 Amazon US/UK、Temu、Shopify，更多在路上 |
| 退款 | refund / money back | 先探底：「what specific issue?」→ 查使用次数 → 按规则建议（见下） |
| Listing 质量 | ranking / optimized / A9 | 按 A9 算法生成，用户通常 2 周内自然排名提升 30-50% |
| 中文 | Chinese / 中文 | 专为中国卖家出海设计，中文输入→地道英文 Listing |
| API/企业 | API / agency / bulk | Agency $99.9/mo 含 API 与批量生成，企业定制联系我们 |
| 安全 | data / privacy / safe | 传输加密，仅存你的生成结果可随时删，绝不外泄 |

### 退款自动回复话术（先探底，不直接同意）
```
I'm sorry to hear that! Could you let me know what specific issue you ran into?
- Was the listing quality not what you expected?
- Did a specific feature not work?
- Were you looking for something different?
If you still prefer a refund after we chat, absolutely — we'll process it within 24h.
```
> AI 收到退款请求后查使用次数 → 推 [创始人] 决策（**AI 绝不点退款按钮**）：
> - 0 次 → 建议同意
> - >10 次 → 建议拒绝（疑似白嫖）
> - 1-10 次 + 具体 bug → 建议同意 + 修 bug

### 未命中话术的兜底
```
Thanks for your question! Our team will get back to you within 24 hours.
```
→ 记录 `reports/new-questions.md`，每周生成新模板 → [创始人] 审核入库。

---

## 四、反馈闭环（周维度）

1. 周日 [AI] 汇总 `feedback-raw-*` + Gumroad 评论 → `reports/feedback-weekly-*.md`
2. TOP 5 抱怨、TOP 3 功能请求
3. 可自动修（文案/API Prompt/UI 微调/小功能）→ [AI] 改代码 → push → Vercel 部署
4. 需 [创始人] 决策（定价/套餐/新工具类型）→ 标红列出
