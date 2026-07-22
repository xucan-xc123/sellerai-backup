# SellerAI · HR 招聘记录

---

## 2026-07-16（周三例行·实际执行于 07-16 17:48）

### 一、编制盘点
- 专家角色库：266 个 / 18 部门
- 常驻员工：13 名
- 挂载技能：9 个

现有 13 员工部门分布：
| 部门 | 常驻员工 |
|---|---|
| engineering | 产品工程师(每4h) |
| marketing | 内容引擎-早(11:00)、内容引擎-晚(20:00)、增长优化师(13:30) |
| specialized | 技能雷达员(每3h) |
| sales | 竞品情报员(15:00) |
| finance | 财务管家(09:30)、消耗飙升检测(每1h) |
| security | 运维巡检(每1h) |
| product | 市场雷达(周一10:00) |
| project-management | 备份员(00:30)、角色库同步(08:10)、HR招聘官(周三10:00) |

### 二、缺口判断
「有专家库但无常驻员工」的部门：**support(6专家)、design(9)、testing(9)、paid-media(7)、game-development、gis、spatial-computing、academic、healthcare、video-production**。

按护栏优先级（support > design > testing > paid-media > 其他）逐条核验：
- **support 客服部**：无常驻员工 ✅；对跨境电商主业务价值极高（差评响应/客诉/FAQ/退换货）✅；与现有 13 岗职责无重叠 ✅ → **三条件全满足，判定需补员**。

### 三、补员决策
- 拟建岗位：**员工-智能客服官**（support 部门）
- 频率：每日 16:00（低频，满足 CPU 硬护栏）
- 职责：差评/客诉痛点分析、多语种客服话术库与 FAQ 维护、每日客服简报
- 产出文件：`sellerai-deploy\客服简报.md`、`sellerai-deploy\客服话术库.md`

### 四、执行状态 ⚠️ 阻塞
- 本次运行为**隔离 cron 环境**，cron 工具被限制为「仅可操作当前任务」，返回 `Cron tool is restricted to the current cron job.`，**无法在本轮自动新建岗位 cron 任务**。
- 为避免"注册假员工"（有编制无任务），本轮**未执行 org-register 入编**。
- **待办**：需在主会话（非隔离）中执行以下两步完成补员：
  1. `cron add`：员工-智能客服官，sessionTarget=isolated，payload.kind=agentTurn，delivery.mode=none，每日16:00
  2. `node E:\QClaw\Work-QClaw\agency-agents-lib\org-register.cjs staff 智能客服官 support 每日16:00`

### 五、护栏合规
- 单次拟建 ≤1 岗 ✅
- 建成后总员工 14 < 18 上限 ✅
- 频率每日1次 < 每2小时 ✅
- 与保命级监控（运维巡检/消耗飙升检测）无重复 ✅
