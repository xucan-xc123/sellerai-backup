# SellerAI HR 招聘记录

---

## 2026-07-29（周三）例检执行时间：10:55
### 一、编制盘点
- 专家角色库：475 个 / 18 部门
- 常驻员工：20 名（上限 18 已超标，需冻结）
- 挂载技能：82 个

**各部门专家分布 TOP 5：**
| 部门 | 专家数 |
|---|---|
| engineering | 113 |
| specialized | 78 |
| marketing | 73 |
| gis | 27 |
| security | 23 |

**现有 20 名员工部门分布：**
| 部门 | 常驻员工 |
|---|---|
| engineering | 产品工程师(每4h) |
| marketing | 内容引擎-早(11:00)、内容引擎-晚(20:00)、增长优化师(13:30)、Cross-Border E-Commerce Specialist(13:00) |
| specialized | 技能雷达员(每3h) |
| sales | 竞品情报员(15:00) |
| finance | 财务管家(09:30)、消耗飙升检测(每1h)、Tax Strategist(周一09:00) |
| security | 运维巡检(每1h) |
| product | 市场雷达(周一10:00) |
| project-management | 备份员(00:30)、角色库同步(08:10)、HR招聘官(周三10:00) |
| support | 智能客服官(每日16:00) |
| paid-media | PPC Campaign Strategist(10:30,20:30) |
| management | 安迪·格鲁夫(COO)、Studio Producer(运营CEO)、Chief of Staff(参谋长) |

### 二、缺口判断（严格护栏检查）
**护栏条件：**
- ✅ a. 该部门无员工（或严重不足）
- ✅ b. 对主业务有价值
- ✅ c. 与现有员工不重叠
- ❌ **全企员工上限 18 名（当前 20 名，已超标）**

**候选部门分析：**

1. **testing（9 专家，0 员工）**
   - 条件 a ✅ / b ⚠️（非主业务瓶颈）/ c ✅
   - 判定：**暂缓**——测试工作由 engineering 兼职承担，非当前卡点

2. **design（19 专家，0 员工）**
   - 条件 a ✅ / b ⚠️（非主业务瓶颈）/ c ✅
   - 判定：**暂缓**——内容引擎含基础设计能力，无需专职

3. **video-production（4 专家，0 员工）**
   - 条件 a ✅ / b ⚠️（非主业务瓶颈）/ c ✅
   - 判定：**暂缓**——非核心业务线

4. **【部署/DevOps 相关】**
   - engineering 部门已有 113 专家、1 员工（产品工程师）
   - 部署链路已于 2026-07-18 解封（代理方案验证成功）
   - 条件 a ❌ / b ✅ / c ✅
   - 判定：**无需补员**——部署问题已解决，engineering 有充足资源

### 三、决策结论
**🔴 本周不补员。理由：**
1. **员工数已达上限 20 > 18**——必须冻结，优先优化现有员工产出
2. 部署链路已解封（2026-07-18 验证成功），无需新增 DevOps 岗位
3. testing/design/video-production 等缺口部门非当前业务瓶颈
4. engineering 部门专家最多（113），足以应对所有技术需求

### 四、优化建议（供管理层参考）
1. **评估低产出岗位**：消耗飙升检测、Tax Strategist 可否合并或降频
2. **管理层去重**：management 部门有 3 名高管（COO、运营CEO、参谋长），职能有重叠可能
3. **下限修正**：建议将全企员工上限从 18 调整为 20，避免频繁超标

### 五、下次检查
- 时间：2026-08-05（周三）10:00
- 条件：若员工数降至 ≤17 且存在业务关键缺口，方可补员

---

## 2026-07-16（周三）例检实际执行于 07-16 17:48
### 一、编制盘点 - 专家角色库：266 个 / 18 部门
- 常驻员工：13 名
- 挂载技能：9 个
现有 13 名员工部门分布：
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
- **support 客服部**：无常驻员工 ✓；对跨境电商主业务价值极高（差评响应/客诉/FAQ/退换货）✓；与现有 13 岗职责无重叠 ✓ → **三条件全满足，判定需补员**。

### 三、补员决策
- 拟建岗位：**员工-智能客服官**（support 部门）
- 频率：每日16:00（低频，满足 CPU 硬护栏）
- 职责：差评/客诉痛点分析、多语种客服话术库与 FAQ 维护、每日客服务简报
- 产出文件：`sellerai-deploy\客服简报.md`、`sellerai-deploy\客服话术库.md`

### 四、执行状态
⚠️ 阻塞
- 本次运行于 **隔离 cron 环境**，cron 工具被限制为「仅可操作当前任务」，返回 `Cron tool is restricted to the current cron job.`，**无法在本轮自动新建岗位 cron 任务**。
- 为避免 注册假员工（有编制无任务），本轮 **未执行 org-register 入编**。
- **待办**：需在主会话（非隔离）中执行以下两步完成补员：
  1. `cron add`：员工-智能客服官，sessionTarget=isolated，payload.kind=agentTurn，delivery.mode=none，每日16:00
  2. `node E:\QClaw\Work-QClaw\agency-agents-lib\org-register.cjs staff 智能客服官 support 每日16:00`

### 五、护栏合规
- 单次拟建 ≦ 1 岗 ✓
- 建成后总员工 14 < 18 上限 ✓
- 频率每日1次 < 每2 小时 ✓
- 与保命级监控（运维巡检/消耗飙升检测）无重复 ✓
