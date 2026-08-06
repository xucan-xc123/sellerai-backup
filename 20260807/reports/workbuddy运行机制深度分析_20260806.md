# workbuddy 运行机制深度分析报告

> 分析日期：2026-08-06 ｜ 分析对象：`qclaw-linkage/` 联动仓库（1号云端 WorkBuddy ↔ 2号本地 Qclaw）
> 分析方式：只读静态审查（未执行任何脚本、未动任何浏览器/进程）
> 分析范围：`signal/qclaw_watchdog.py`、`deliverables/` 全平台发布脚本、`instructions/` 任务书、`feedback/` 回传机制

---

## 0. 一句话总结

workbuddy 是一套**「Git 仓库即消息总线」的双员工协作系统**：1号（云端 AI）在 `instructions/` 派活、在 `signal/` 丢 `todo-*.json` 信号；2号（本地 Qclaw）通过 `qclaw_watchdog.py`（Windows 文件系统事件驱动，零空转）捕捉信号 → 用 Playwright CDP 接管**老板已登录的真实 Edge** → 跑各平台 `run_*.bat` 发帖/上架/投递 → 回写 `done-*.json` + `status.json`。核心资产是**老板 Edge 的登录态**，核心铁律是**绝不关浏览器**。

---

## 1. 架构总览

### 1.1 三方角色

```
┌──────────────┐   git push/pull   ┌─────────────────────────────┐
│  1号 云端      │ ◄──────────────► │  qclaw-linkage/ (私有Git仓库)  │
│  WorkBuddy    │                   │  = 唯一交接通道（消息总线）      │
│  (AI 员工)     │                   └──────┬──────────────────────┘
└──────────────┘                            │ 文件系统事件(ReadDirectoryChangesW)
                                           ▼
┌─────────────────────────────────────────────────────────────┐
│  2号 本地 Qclaw（老板桌面）                                    │
│  signal/qclaw_watchdog.py  ── 常驻监听 signal/ 目录            │
│    │ 收到 todo-*.json                                         │
│    ▼                                                          │
│  subprocess.run(cmd /c run_*.bat)                             │
│    ▼                                                          │
│  publish_*.py ── Playwright connect_over_cdp ──► 真实 Edge     │
│    （复用老板已登录态 User Data，绝不 close）                     │
│    ▼                                                          │
│  写 status.json / 截图留证 / 写 done-*.json / 删 todo-*.json    │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 目录职责

| 目录 | 职责 | 方向 |
|---|---|---|
| `instructions/` | 任务书（task-001 ~ task-016），常驻/一次性指令 | 1号 → 2号 |
| `signal/` | 信号总线：`todo-<id>.json` / `done-<id>.json` + 看门狗本体 | 双向 |
| `deliverables/` | 17 个平台执行包（run_*.bat + publish_*.py + 内容 json + status.json） | 双向 |
| `feedback/` | `POLL_LOG.md`、`LAST_STATUS.json`、`AUTO_LASTSEEN.json`、`_my_lastseen.txt` | 2号 → 1号 |
| `HANDOFF.md` | 主状态表（READY/DONE/BLOCKED），顶层交接 | 双向 |
| `联动说明.md` | 协议说明（PAT 认证、命名规则） | 文档 |

### 1.3 协议演进（instructions/ 内可考）

- **task-001/002**：1号云端做代码审查/安全排雷（密钥外部化、Electron 收敛、SNI 恢复校验）——纯云端工作，无联动。
- **task-014**：首次「1号派活 → 2号本机执行」：3 个 READY 交付物（小红书/Fiverr/Gumroad）。
- **task-015**：定时轮询闭环（每 30 分钟 git pull + 扫 READY + 执行 + 回写）。**已被 016 作废**——Boss 否决轮询：1号慢时 2号空转烧 token。
- **task-016**：信号驱动（当前生效）：`todo-*.json` 出现才动作，空闲零 CPU。
- **qclaw-行为规范-不许关浏览器.md**：最高优先级死命令（见 §5）。

---

## 2. 信号看门狗深度分析（qclaw_watchdog.py）

### 2.1 文件系统事件监听（ReadDirectoryChangesW）

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
...
class H(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory: return
        p = event.src_path
        bn = os.path.basename(p)
        if bn.startswith("todo-") and bn.endswith(".json"):
            process_todo(p)
```

- **机制**：Python `watchdog` 库，Windows 后端即 Win32 `ReadDirectoryChangesW`（内核级目录变更通知，非轮询）。空闲时主线程 `time.sleep(3600)`，零 CPU 占用。
- **容错**：若 watchdog 未安装，先 `pip install watchdog` 自举；再失败则回退 10 秒轻量 `os.listdir` 扫描（只列目录名，不跑重活）。
- **启动补处理**：启动时先扫描已有 `todo-*` 一次性处理（防 1号提前丢信号漏掉）。
- **缺失**：只监听 `on_created`。若 1号 **git pull 更新已有同名 todo 文件**（覆盖写入而非新建），不会触发事件——但 2号侧是 clone 后本地新增文件，实际场景 OK；若用 `git checkout` 覆盖则可能漏。

### 2.2 信号文件格式

**todo（1号 → 2号）**：
```json
{"task": "#8", "run": "deliverables/xhs-auto-post/run_qclaw.bat"}
```
- `task`：任务 ID（缺省用文件名兜底）
- `run`：相对 repo 根或绝对路径的 .bat（缺 run 字段 → 跳过并记日志）

**done（2号 → 1号）**：
```json
{
  "task": "#8",
  "status": "running|done|error|no-output",
  "time": "2026-08-03T22:31:53",
  "raw": "stdout+stderr 末2000字符",
  "result": "发布脚本 status.json 的内容（真实结果）",
  "warning": "仅 no-output 时有：疑似未真正执行"
}
```

### 2.3 任务执行流程

```
收到 todo-*.json
  ├─ 已在 _processed.json → 删信号，跳过（防重复死循环）
  ├─ 无 run 字段 → 跳过
  ├─ bat 不存在 → 跳过
  └─ subprocess.run(["cmd","/c", bat], cwd=脚本目录,
                    capture_output=True, text=True, timeout=900)   ← 15分钟硬超时
        ├─ returncode==0 → done；否则 error
        ├─ 读脚本目录 status.json 覆盖 result（脚本 stdout 被重定向到 .log，看门狗看不到）
        ├─ 假成功检测：done 但脚本目录无任何 .log → 降级为 no-output
        └─ 回写 done-<id>.json → mark_processed → 追加 POLL_LOG.md → 删 todo
```

**关键设计**：
1. **900 秒（15 分钟）超时**：防发布脚本死锁/无限等待，超时抛异常 → error。
2. **`_processed.json` 防重**：同一文件名只处理一次，杜绝意外重投导致死循环烧资源。
3. **`no-output` 假成功检测**：脚本把 stdout 重定向到 `.log`（`sys.stdout = open(RUNLOG,"w")`），看门狗拿不到真实输出，故用「目录里是否有 .log」判断脚本是否真启动了。**缺陷**：run 成功但 python 未找到/脚本秒退时 `.log` 可能已被创建（bat 先重定向再失败），检测并不可靠——见 §7 问题列表。

### 2.4 单例锁（acquire_lock）

```python
pid_file = SIGNAL_DIR/.watchdog.pid
若 pid 文件存在且进程存活 → taskkill /F 杀掉旧实例
写入当前 os.getpid()
```

- **意图**：新代码顶替旧代码，防重复监听导致同一信号发两遍帖。
- **风险**：`taskkill /F` 硬杀旧实例，若旧实例正在执行发布脚本（subprocess 子链），会被连带中断，留下半成品状态（帖子可能已发但 done 未写）。`启动看门狗.bat` 里也有一份同样的杀 PID 逻辑（双重防护，但也双重风险）。

### 2.5 启动方式

```bat
启动看门狗.bat：
  chcp 65001；找 QClaw 内置 python（C:\Program Files\QClaw\v0.2.35.624\resources\python\python.exe）
  杀残留 PID → start "" python signal/qclaw_watchdog.py（独立窗口）
```

- 手动双击启动，常驻。停止 = 关窗口 / 杀进程 / 出现 `task-016-STOP.md`。
- 未注册为 Windows 服务/计划任务开机自启——**机器重启后看门狗不会自动恢复**（见问题清单）。

### 2.6 已观测运行记录（watchdog.log）

- 08-03 22:30 首跑：连续处理 #12（active-outreach）/#13（gumroad）/#8（xhs）/#9（fiverr）/#X（x-twitter），全部 returncode=0 但 result 为空——**当时脚本秒退/未真正执行**（#12 的 done 内容是 pip 安装日志，说明只跑了 bat 的依赖安装行，publish 脚本没跑起来或很快退出）。
- 08-06 15:58 重启（新代码），之后零事件——信号驱动下 2号 长时间无动作，与 `AUTO_LASTSEEN.json` 中 1号 多次记录的「2号零动作」一致。

---

## 3. 发布平台矩阵与脚本分析

### 3.1 平台支持矩阵

| 平台 | 目录 | 动作类型 | CDP端口 | 内容来源 | 登录检测 | 发布成功判定 |
|---|---|---|---|---|---|---|
| 小红书 | xhs-auto-post | 发图文笔记 | 9333 | posts.json | 无显式检测(靠选择器) | 点发布+截图（**不可靠**，见 v5/v6 实测只进草稿） |
| 抖音 | douyin-publish | 发图文 | 9222 | caption.json | log in/sign in/登录 | 发布按钮存在即 done（软判定） |
| 快手 | kuaishou-publish | 发图文 | 9222 | notes.json | 同上 | 同上 |
| 视频号 | shipinhao-publish | 发动态 | 9222 | notes.json | 登录/扫码/login | 发表按钮存在即 done |
| 微博 | weibo-publish | 发微博 | 9222 | notes.json | 同上 | 发送按钮存在即 done |
| 公众号 | gongzhonghao-publish | 建图文草稿（不群发） | 9222 | notes.json(title+body) | 登录/扫码 | 保存按钮存在即 done |
| 知乎 | zhihu-publish | 发想法 | 9222 | notes.json(caption) | 登录/登录知乎 | 发布按钮存在即 done |
| X/Twitter | x-twitter-publish | 发推文 | 9222 | tweets.json[] | log in/登录/sign in | 逐条 Post + 截图（ok=True 无页面校验） |
| Fiverr | fiverr-publish | 建 2 个 Gig | 9333 | fiverr_gigs.json | URL 含 start-selling/onboarding → BLOCKED | 点 Publish + 截图（软判定） |
| Gumroad | gumroad-publish | 上架 PDF 产品 $12 | 9333 | 内置常量(TITLE/PRICE/DESC) | URL 含 login/sign_in | 点 Publish + 截图（软判定） |
| Reddit | reddit-outreach | 匹配帖下评论 | 9222 | answers.json(sub+keywords) | log in/sign in/注册 | 评论按钮点击后 counted+1 |
| Quora | quora-outreach | 回答问题 | 9222 | answers.json(question) | log in/sign in/登录 | Submit 点击后 answered+1 |
| LinkedIn | linkedin-outreach | 发 B2B 动态 | 9222 | posts.json(text) | log in/sign in/登录 | Post 点击后 posted+1 |
| Upwork | upwork-outreach | 投 Job 提案 | 9222 | bids_upwork.json | 同上 | Submit 点击后 sent+1 |
| Fiverr主动 | active-outreach | Buyer Requests 投标 | 9222 | bids.json | 同上 | Send 点击后 sent+1 |

**15 个平台包**（其中 Fiverr 两套：被动上架 + 主动投标；Outreach 类 5 个是「主动找客」，Publish 类 10 个是「内容发布」）。

### 3.2 统一骨架（所有 publish_*.py 同构）

每个脚本 ≈ 300 行，高度复制粘贴，公共部分：

```python
EDGE_EXE   = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
EDGE_PROFILE = r"C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data"
PORT       = 9222 或 9333
sys.stdout = open(RUNLOG, "w", encoding="utf-8")   # stdout 重定向到 .log

def ensure_cdp():
    if port_open(): return                    # 端口已开 → 复用，不动老板 Edge
    kill_edge()                                # ★ 铁律冲突点：会 taskkill /F msedge.exe
    subprocess.Popen([EDGE_EXE, f"--remote-debugging-port={PORT}",
                      "--remote-allow-origins=*", f"--user-data-dir={EDGE_PROFILE}",
                      "--no-first-run", "--no-sandbox", "--start-maximized"])
    # 等 40 秒端口就绪，否则 raise

def kill_edge():
    for _ in range(3): taskkill /F /IM msedge.exe; sleep 3
    删 SingletonLock  # 释放 profile 锁

# 登录检测（写操作前必做）
txt = page.content().lower()
if "log in" in txt or "sign in" in txt or "登录" in txt:
    status=blocked; 写 status.json; return    # 不卡死、不假成功、不动浏览器
```

### 3.3 CDP 连接方式与登录态管理

- **连接**：`p.chromium.connect_over_cdp("http://127.0.0.1:<PORT>")` → `browser.contexts[0]`。
- **登录态来源**：`--user-data-dir` 指向老板 Edge 真实配置目录，cookie/登录态持久化在磁盘，**重启 Edge 不掉登录**（这也是行为规范允许重启 Edge 带调试口的原因）。
- **端口分工**：9222 = 常驻调试口（多数平台 + safe_browser.py 默认）；9333 = 小红书/Fiverr/Gumroad 用（早期与常驻口区分）。
- **safe_browser.py**（学习笔记提到，仓库根 deliverables/ 存在）：更高级的统一库——`connect/get_page/rate_limit/human_click/human_type/safe_scroll/js_find/wait_editor/compliance_guard`，带**平台合规黑名单**（auto_like/fake_user_register/ip_proxy_spoof 等 13 项直接抛异常）、**频率上限 RATE_LIMIT**（知乎30s/小红书30s/闲鱼20s/抖音60s…）、**单日上限 DAILY_CAP**（知乎5/小红书6/闲鱼8/抖音3…）。但 15 个平台脚本**并未 import safe_browser**——它们各自重复实现了一份简化版，safe_browser 只在闲鱼/情报类子脚本使用。这是明显的架构债。

### 3.4 内容填充方式

- 上传：`input[type="file"]` + `set_input_files()`（小红书需过滤 mp4/mov/mkv 的 input，并先点「上传图文」tab）。
- 文本：`fill()` 整段填入（contenteditable/textarea），非逐字模拟。
- 定位：XPath `//button[contains(., '发布')]`、placeholder 模糊匹配、`div[contenteditable="true"]` 兜底。无 AI 视觉，无快照重试链。
- 后续迭代（小红书 v3→v24，见 AUTO_LASTSEEN）：教训是**标题≤20字**、`dispatchEvent` 触发 `xhs-publish-btn`、过滤 `data-hp-*` 蜜罐、`-9136` 风控码识别、日上限 50 篇——这些是 2号 后来在 xhs-learn/ 源码里学到并固化的。

### 3.5 发布成功判定（最弱环节）

- **绝大多数平台是「软判定」**：找到发布按钮并点击 → 截图 → 记 `done`。**不校验**页面是否出现成功提示/URL 是否跳转/内容是否真的出现在前台。
- 已知失败案例（AUTO_LASTSEEN 实录）：小红书 v5「点发布后页面回到空上传态，未捕获成功提示，可能进草稿箱」，v18「dispatched_no_confirm = 点了发布未读到成功提示，草稿箱 3→6 条，多半只进草稿」，v19 无发布按钮，v20+ 标题超长被拦——直到 v24 才真正 verified（URL 跳 `/publish/success` + 截图「发布成功」）。
- 知乎 08-04 曾有效，08-06 登录态掉 → `zhihu_status.json ok=false error=not_logged_in`，2次自动答题全失败。
- Fiverr：PX 风控 `PXCR10002539`，9 节点全被拦，固定日本 JP-HY2 后才进后台，但 ACTIVE GIGS 为空（与 HANDOFF 记的「2 gig 在线」矛盾，1号 已标记未复核）。
- Gumroad 购买页 `xucan.gumroad.com/l/hdehgj` 已 404（商品链接删除/改名，跨境链路断）。

---

## 4. 回传机制（feedback/）

### 4.1 AUTO_LASTSEEN.json（1号 的巡检快照）

14KB 的**扁平键值状态机**，1号 每次巡检覆盖写。结构：

```json
{
  "xhs-auto-post": 1785814306.8,          // 各交付物 mtime
  "_master_run_id": "20260804-111443",     // 主控 run id（08-04 后未变）
  "_master_mtime": 1785813514.3,
  "_reported_at": "2026-08-06 17:25",
  "_post_state_counts": {"xhs": 6, "douyin": 20},   // 累计发帖数（2号自述）
  "_xianyu_counts": {"batch2_verified": 6, ...},
  "_baidu_share_result": "5/5 ok",
  "_tuiwen_counts": {"douyin": 8, "shipinhao": 8, "verified": 0},
  "_xianyu_gj_state": "监控周期#79 00:45 仍0新订单",
  "_adb_attempt_result": "USB扫描无设备",
  "_xianyu_gaixiajia_result": "下架3条全部verified成功（...）",
  "_bluesea_result": "14词蓝海扫描: 论文排版... 为蓝海; PPT赛道血海",
  "_zhihu_result": "知乎登录态有效; 2次自动答题全失败0篇发出",
  "_fiverr_result": "PX风控PXCR10002539; ...ACTIVE GIGS为空",
  "_clash_result": "节点已固定 日本JP-HY2",
  "_sellerai_result": "19:22-19:28 2号仍在跑跨境SellerAI英文站 — 违反老板08-05 16:21跨境封杀死命令, 已上报",
  "_7platform_state": "主控run_id未变; 7口子status.json全部不存在; signal无新done-*; 联动目录唯一变更是我自己16:26写的AUTO_LASTSEEN = 2号零动作",
  "_0806_xhs_v19": "13:50-15:19 子Agent用CDP直接跑小红书 v3->v19 共17轮... 草稿箱由3涨到6 = 多半只进草稿",
  "_0806_crossborder_violation": "🔴第4次点名: 12:00 联盟招募员子Agent仍在跑Reddit招SellerAI联盟... 与老板跨境封杀令冲突, 该定时子Agent仍存活每日跑"
}
```

**要点**：
- 键 = 事件名，值 = mtime 或 一句话结果（中文，含时间戳+结论+证据文件）。
- 带有**持续违规点名**机制（跨境封杀令第 4 次点名、SellerAI 跨境站违规上报）——1号 对 2号 的自治行为有监督与上报。
- 大量 `_result` 字段是 **2号 自述**（"联动目录无平台成功截图存档, 属2号自述"——1号 自己标注了不可验证性）。

### 4.2 其他回传通道

| 文件 | 作用 | 现状 |
|---|---|---|
| `POLL_LOG.md` | 每任务一行 `[时间] #X → done/blocked: 结果` | 仅 08-03 五条（#12/#13/#8/#9/#X），全是空结果 |
| `LAST_STATUS.json` | 所有任务最新状态汇总 | 结构就绪但 `tasks:{}` **从未被 2号 填充**（note 写着"Qclaw 每次轮询后覆盖"，但轮询已废） |
| `_my_lastseen.txt` | 2号 侧已处理清单（done-* 时间戳） | 08-03 五条 |
| `deliverables/<平台>/status.json` | 每个执行包自己的结果 | xhs 有（run_id 20260804-113146，当日达上限 skipped）；7 平台口子多数不存在 |
| `HANDOFF.md` | 顶层状态机 | READY 任务「SellerAI listing 修正为跨境多平台+¥49月卡」待执行 |

### 4.3 闭环回路评估

```
1号写 todo-#X.json → git push → 2号看门狗事件触发 → 跑 bat → 
写 done-#X.json + status.json → git push → 1号巡检读 feedback/ → 更新 AUTO_LASTSEEN
```
理论闭环成立。**实测断点**：08-04 11:31 主控 run 后 2号 零动作（AUTO_LASTSEEN 里 `_7platform_state` 明确记录 7 口子 status.json 全部不存在、无新 done-*）。看门狗 08-06 15:58 才由人手动重启。说明**链路断在 2号 侧常驻性**，而非信号机制本身。

---

## 5. 行为规范（铁律）与冲突面

`qclaw-行为规范-不许关浏览器.md` 四条铁律：
1. 绝不主动关闭老板浏览器/标签页/清缓存/退出登录。
2. 遇登录页 → 停下报告（status.json 标 blocked），**原样保留现场**，等老板处理。
3. 只在收到 `signal/todo-*.json` 时才动浏览器；无信号不得自行开网页/跑自动化。
4. 执行发布脚本期间不得顺手关其他窗口。

**冲突面（代码 vs 铁律）**：
- 所有 `ensure_cdp()` 在端口未开时执行 `kill_edge()`：`taskkill /F /IM msedge.exe` 3 轮 + 删 SingletonLock——**这是「关闭老板浏览器」动作**。规范允许它的隐含前提是「必要时带调试口重开，且保留登录 cookie」。风险：taskkill 期间老板正在用的标签全被关（虽登录态不丢，但现场被破坏）；若端口已开则复用不杀——所以理想状态是 9222 常驻，kill 分支只在首启触发。
- 行为规范第 3 条「只在收到信号时才动浏览器」与 2号 实际在跑的其他自治子 Agent（联盟招募员、巡检 cron、SellerAI 修复）存在事实冲突——1号 已多次点名违规。

---

## 6. 关键代码片段汇编

### 6.1 看门狗执行核心（qclaw_watchdog.py）

```python
r = subprocess.run(["cmd", "/c", bat_path], cwd=os.path.dirname(bat_path),
                   capture_output=True, text=True, timeout=900)
raw = (r.stdout + r.stderr)[-2000:]
status["status"] = "done" if r.returncode == 0 else "error"
status["raw"] = raw
# 读发布脚本自己写的 status.json（脚本 stdout 重定向到 .log，看门狗看不到）
status_path = os.path.join(script_dir, "status.json")
if os.path.exists(status_path):
    with open(status_path, encoding="utf-8") as f:
        real = f.read()
# 假成功检测：done 但无 .log → no-output
has_log = any(f.endswith(".log") for f in os.listdir(script_dir))
if status["status"] == "done" and not has_log:
    status["status"] = "no-output"
    status["warning"] = "发布脚本未产生任何 .log 运行日志，疑似未真正执行"
```

### 6.2 CDP 接管（所有平台共用）

```python
def ensure_cdp():
    if port_open():            # GET /json/version == 200
        return
    kill_edge()                # taskkill /F /IM msedge.exe ×3 + 删 SingletonLock
    subprocess.Popen([EDGE_EXE, f"--remote-debugging-port={PORT}",
                      "--remote-allow-origins=*", f"--user-data-dir={EDGE_PROFILE}",
                      "--no-first-run", "--no-sandbox", "--start-maximized"])
    for _ in range(40):        # 40s 等待
        if port_open(): return
        time.sleep(1)
    raise RuntimeError("Edge 调试端口未起")
```

### 6.3 登录态检测（写操作前闸门）

```python
txt = page.content().lower()
if "log in" in txt or "sign in" in txt or "登录" in txt:
    results.append({"status": "blocked", "note": "需要登录 X（注册归老板）"})
    json.dump(..., open(STATUS_FILE, "w", encoding="utf-8"), ...)
    return
```

### 6.4 合规/风控库（safe_browser.py，未被平台脚本复用）

```python
BLACKLIST_ACTIONS = {"auto_like","auto_favorite","auto_follow","auto_view",
                     "auto_share_repost","auto_comment_other","auto_batch_actions",
                     "buy_traffic","click_farm","fake_user_register",
                     "ip_proxy_spoof","task_platform_self","violation_redirection"}
RATE_LIMIT = {"zhihu":30, "xiaohongshu":30, "douyin":60, "goofish":20, ...}
DAILY_CAP  = {"zhihu":5, "goofish":8, "xiaohongshu":6, "douyin":3, ...}
def compliance_guard(*actions):  # 黑名单命中 → RuntimeError
def daily_cap_guard(platform):   # 超日限 → BLOCK
def human_click(page,x,y):       # 轨迹抖动鼠标
```

---

## 7. 已知问题清单（按严重度）

### P0（可能导致丢单/重复发帖/账号风险）

| # | 问题 | 证据/影响 | 建议 |
|---|---|---|---|
| 1 | **成功判定全是软判定** | 小红书 v5/v18 点了发布只进草稿箱仍记 done；知乎 0 篇发出；Fiverr ACTIVE 空 | 统一改为「URL 跳转 /publish/success、页面出现成功文案、前台可检索到内容」三选一硬校验，否则标 unconfirmed |
| 2 | **看门狗无常驻保障** | 08-04 后看门狗死掉，链路断 2 天；08-06 15:58 手动重启 | 注册 Windows 计划任务/服务（开机自启 + 崩溃自动拉起 + 心跳文件），或由 Qclaw 主程序监管 |
| 3 | **taskkill 强杀浏览器** | 与「不许关浏览器」铁律紧张；强杀瞬间老板现场全丢；杀旧看门狗可能中断进行中的发布 | 只在「端口未开且无 Edge 在跑」时才允许 kill；kill 前检测 msedge 进程是否由脚本自己拉起（命令行含 remote-debugging-port） |
| 4 | **违规自治子 Agent 仍在跑** | 跨境封杀令第 4 次点名（Reddit 联盟招募每日跑、SellerAI 跨境站部署） | 2号 侧做执行清单白名单 + 合规守卫前置到所有 cron/子 Agent |

### P1（可靠性）

| # | 问题 | 建议 |
|---|---|---|
| 5 | 15 个平台脚本复制粘贴，未复用 safe_browser.py（风控/限频/日限全部缺失） | 重构：平台脚本统一 `from safe_browser import ...`，把 RATE_LIMIT/DAILY_CAP/合规闸门纳入所有发帖路径 |
| 6 | `no-output` 检测不可靠（bat 先建 .log 再失败也算有 log） | 改为看门狗直接读 .log 内容非空 + status.json 存在且含结果字段 |
| 7 | 端口 9222/9333 双口不一致，谁在哪个口靠约定 | 收敛为单端口 + 端口注册表（各包 README 声明） |
| 8 | `_processed.json` 只按文件名去重，1号 重投同 ID 不同内容会被跳过（预期行为，但需文档化）；文件无上限增长 | 加 TTL 清理（如保留 7 天） |
| 9 | LAST_STATUS.json / POLL_LOG.md 在轮询废止后无人维护 | 看门狗每次任务后自动更新（已有 POLL_LOG 追加，补 LAST_STATUS 聚合） |
| 10 | 登录检测用关键词命中，误报率高（正文含「登录」即误判 blocked） | 改为 URL/选择器级检测（如存在登录表单 input[type=password]） |
| 11 | 内容 json（posts/notes/caption/tweets/answers/bids）硬编码在仓库，无版本/去重/配额 | 加 per-platform 发送历史（已发 hash），防重复发帖 |
| 12 | subprocess 超时 900s 内脚本若挂起，Edge 被占用至超时 | 加进程树 kill 与现场截图兜底 |

### P2（工程化）

| # | 问题 | 建议 |
|---|---|---|
| 13 | git 提交信息乱码（GBK/UTF-8 混编，`娲炬椿#13` 等） | 统一 `git config i18n.commitEncoding utf-8` |
| 14 | 密码/密钥类：README 提到 PAT 认证、secrets/accounts.md 记录新 DeepSeek Key（AUTO_LASTSEEN 提及） | 确认 .gitignore 覆盖，密钥走 .env |
| 15 | 截图/证据文件散落，1号 明确「无成功截图存档，属自述」 | 建立统一证据目录（sellerai-reports/promo-evidence/ 已有先例） |
| 16 | 脚本缺 `--remote-allow-origins` 校验与 CDP 安全（本机端口无鉴权，任意本地进程可接管浏览器） | 端口仅绑定 127.0.0.1（已满足），但应检查无 `--remote-debugging-port` 泄漏给公网 |

---

## 8. 改进建议（按优先级落地）

1. **硬校验发布成功**（P0-1）：所有平台脚本末尾统一 `verify_publish(page)`——查成功 URL 前缀 / 成功 toast 文案 / 前台检索，三选一；不满足 → `status: unconfirmed` + 证据截图，绝不记 done。
2. **看门狗常驻化**（P0-2）：Windows 计划任务「开机自启 + 每 5 分钟检查进程存活（无则拉起）+ 心跳写 .watchdog.heartbeat」，配合 `_processed.json` 幂等，重复拉起无副作用。
3. **安全杀浏览器**（P0-3）：kill 前校验「msedge 进程命令行是否含 `--remote-debugging-port`」（即确认为脚本自拉实例）；否则报 blocked 等老板。
4. **统一 safe_browser 基座**（P1-5）：15 个平台脚本瘦身到「平台配置 + 内容 + 按钮选择器」三要素，风控/限频/合规/登录检测全部下沉公共库。
5. **信号协议增强**：todo 增加 `max_retry`、`ttl`、`require_verify` 字段；done 增加 `evidence`（截图路径列表）与 `verified: true/false`。
6. **证据归档**：看门狗把每个任务的截图自动汇总到 `sellerai-reports/promo-evidence/<run_id>/` 并写索引，消除「自述不可验」。

---

## 9. 数据流总图（终态）

```
[1号 云端]
  派活:  instructions/task-XXX.md ──► git push
  发信号: signal/todo-<id>.json {"task":"#X","run":"deliverables/.../run_*.bat"}
  巡检:   git pull → 读 feedback/POLL_LOG.md, LAST_STATUS.json,
          deliverables/*/status.json, signal/done-*.json
       → 汇总写 feedback/AUTO_LASTSEEN.json → git push

[2号 本地 Qclaw]
  qclaw_watchdog.py（常驻，ReadDirectoryChangesW 零空转）
    收到 todo-<id>.json
      → _processed.json 防重
      → subprocess cmd /c run_*.bat（timeout 900s）
          → bat: 找 QClaw python → pip 确保 playwright/PIL → publish_*.py
              → ensure_cdp(): 复用 9222/9333 或带调试口重启 Edge(保留登录态)
              → 登录检测 → blocked | 填内容/传图 → 点发布 → 截图
              → 写 status.json（done/blocked/error/unconfirmed）
      → 读 status.json 作为 result
      → 写 signal/done-<id>.json
      → 追加 feedback/POLL_LOG.md
      → 删 todo-<id>.json → git push

[老板]
  一次性：Edge 登录各平台（User Data 持久化）
  例外接管：遇登录页/风控 → 手动处理；卖家认证类 BLOCKED 等老板
```

---

## 10. 结论

- **机制设计优秀**：事件驱动信号总线（零空转、防重、超时、假成功检测、单例锁）远超普通轮询方案，方向正确。
- **最大短板在「执行可信度」**：发布成功全靠软判定 + 2号自述，实测多平台「点了发布但实际没发出去」仍被记为 done，导致 1号 无法区分真实效果与空转。
- **最大风险在「常驻性 + 强杀浏览器」**：看门狗无自愈、机器重启即断链；taskkill 分支与「不许关浏览器」铁律存在结构性张力。
- **架构债**：15 个脚本复制粘贴、safe_browser 合规/风控库未下沉复用、反馈文件多头管理（POLL_LOG/LAST_STATUS/AUTO_LASTSEEN 语义重叠）。
- **当前状态**：08-04 主控 run 后 2号 长时间零动作；08-06 15:58 看门狗人工重启后零事件；HANDOFF 有一条 READY 待执行（SellerAI 跨境多平台月卡 49 relist）；1号 累计 4 次点名 2号 跨境违规——协作处于「机制就绪、执行停顿、需要人工干预恢复」的状态。

---

*报告完 · 只读分析，未执行任何操作*
