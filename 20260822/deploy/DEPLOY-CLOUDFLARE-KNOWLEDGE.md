# SellerAI Cloudflare 部署知识库（团队自主复用，禁止重复打扰创始人）

> 目的：所有部署相关凭证/权限/命令/路径集中在此，团队自主执行，不再向创始人索取。
> 最后更新：2026-07-17

## 一、账号信息（固定，不涉密）
- Cloudflare 账号：2123314331
- Account ID：9bd06de214f6c2bbd3ce3923a558f8fa
- Zone（listaikit.com）：32b180678d1998f719e306221a314240（active）
- 自定义域：sellerai.listaikit.com（国内可达，workers.dev 国内被墙必须绑自定义域）

## 二、部署命令（写死路径，团队直接跑）
前端仓库：E:\QClaw\Work-QClaw\sellerai-frontend
wrangler：E:\QClaw\Work-QClaw\sellerai-frontend\node_modules\.bin\wrangler.cmd
node：C:\Program Files\QClaw\v0.2.33.617\resources\openclaw\config\bin\node\node.cmd

标准部署流程（在 sellerai-frontend 目录）：
1. npm install --legacy-peer-deps（若 node_modules 不全）
2. npm run build:cf  （= opennextjs-cloudflare build，生成 .open-next/worker.js）
3. wrangler deploy

注意：wrangler.jsonc / wrangler.toml 已被 gitignore（含 DEEPSEEK_API_KEY），不进版本库；部署前须确认两文件在本地且 KEY 完好。

## 三、凭证管理（关键教训，写死规则）
- **规则1**：每次成功部署后，必须把有效 CLOUDFLARE_API_TOKEN 持久化为用户级环境变量：
  [Environment]::SetEnvironmentVariable("CLOUDFLARE_API_TOKEN", $token, "User")
  并存档到本知识库"当前有效 token 状态"段（⚠️ 仅团队可见，不主动外发创始人）。
- **规则2**：若 token 失效（报 9109 Invalid access token），优先用 `wrangler login` 重新授权（浏览器授权，无需填权限），不要用旧串重复试。
- **规则3**：创始人给的 token 若被 Cloudflare 拒，立即判断为失效，主动走 login 流程，不得反复拿同一串骚扰创始人。
- **规则4**：本机已生成一键授权文件：桌面 `一键Cloudflare授权.bat`（双击即弹登录页，登录2123314331点Authorize）。创始人只需点一次。

## 四、当前有效 token 状态
- 2026-07-17 12:49：创始人重新授权流程中（wrangler login 待执行）。团队等待创始人点完授权即部署，不再索要 token 字符串。

## 五、常见坑（复盘，避免重复踩）
1. worktree 部署需复制 wrangler.jsonc 进 worktree（gitignore 不含入版本库）。
2. PowerShell 管道调 wrangler 会报"CantActivateDocumentInPipeline"——改用临时文件接输出或 &直接调。
3. npm install 的 stderr warn 会让 PowerShell 误判失败，看 exitcode 不看异常。
4. 不要部署 feat/moat-multiplatform 等半成品分支，只部署 main 已验证 commit（如 dbb73bd）。
5. token 形态：真 Cloudflare token 以 Cf. 开头；cfk_ 开头多为无效/草稿串。
