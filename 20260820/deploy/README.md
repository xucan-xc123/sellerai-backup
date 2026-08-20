# 🚀 SellerAI 部署操作手册

> 这是一份写给「电脑小白」看的操作手册。跟着做，30 分钟就能把你的 AI 聊天网站搞上线。

---

## 这个项目是什么？

**SellerAI** 是一个电商运营 AI 助手网站。卖家输入问题（比如"帮我写个产品标题"），AI 帮你出主意。我们把它做成一个网站，任何人都能用浏览器访问。

本项目分成两块：

| 部分 | 技术 | 干什么的 |
|------|------|---------|
| `sellerai-frontend` | Next.js | 网页界面，负责显示聊天框、发送消息、接收回复 |
| `sellerai-backend` | Python Flask | 后端大脑，负责接收消息、调 AI 模型、返回结果 |

两个都部署在 **Vercel**（一个免费托管平台），不需要自己买服务器。

---

## 部署前需要准备什么？

在开始之前，请先准备好以下 3 样东西：

| 序号 | 需要什么 | 去哪搞 | 要不要钱 |
|------|---------|--------|---------|
| 1 | **DeepSeek API Key** | https://platform.deepseek.com/api_keys | 充值 5 块钱就够用很久 |
| 2 | **GitHub 账号** | https://github.com （点右上角 Sign Up 注册） | 免费 |
| 3 | **域名**（可有可无） | Namecheap / 阿里云 / 腾讯云 | 一年几十块 |

> 如果暂时没有域名，可以先用 Vercel 送的免费域名（`xxx.vercel.app`），后面再绑自己的域名也行。

---

## 📋 10 步部署清单

每步最多一句话，跟着做就完事了。

### 第 1 步：把所有代码上传到 GitHub

把整个项目文件夹推到 GitHub 上，新建一个仓库叫 `sellerai`。

- 打开 GitHub → 左上角绿色按钮「New」→ 仓库名填 `sellerai` → 点「Create repository」
- 把你的项目代码推上去。不会用 git？去下载 GitHub Desktop（https://desktop.github.com），拖拽文件夹进去，点 Publish 就行。

---

### 第 2 步：注册 / 登录 Vercel

打开 https://vercel.com → 点右上角「Sign Up」→ 选「Continue with GitHub」→ 授权登录。

> 用 GitHub 账号一键登录，不用另外注册。

---

### 第 3 步：在 Vercel 创建前端项目

登录后看到 Dashboard 页面 → 点「Add New...」→ 选「Project」→ 在列表里找到你的 `sellerai` 仓库 → 点「Import」。

---

### 第 4 步：配置前端

Vercel 会自动识别出这是个 Next.js 项目，不用改任何东西。

- **Root Directory** → 点「Edit」→ 改成 `sellerai-frontend`
- 其他配置保持默认
- 点「Deploy」

等 1-2 分钟，部署完成。Vercel 会给你一个地址，类似 `https://sellerai-xxxxx.vercel.app`。恭喜！你的前端已经上线了 🎉

---

### 第 5 步：在 Vercel 创建后端项目

回到 Dashboard → «Add New...» → «Project» → 再次导入同一个 `sellerai` 仓库。

- **Root Directory** → 点「Edit」→ 改成 `sellerai-backend`
- **Framework Preset** → 选「Other」
- 点「Deploy」

部署完成后你会得到后端的地址，类似 `https://sellerai-backend-xxxxx.vercel.app`。

---

### 第 6 步：配置环境变量（重要！）

这是最关键的一步，不配环境变量，AI 就不会回复你。

**在前端项目里配：**

1. 进入前端项目 → 点顶部菜单「Settings」→ 左侧选「Environment Variables」
2. 添加以下变量：

| 变量名 | 值填什么 |
|--------|---------|
| `NEXT_PUBLIC_API_URL` | 你后端项目的地址，比如 `https://sellerai-backend-xxxxx.vercel.app` |

3. 点「Save」
4. 点顶部菜单「Deployments」→ 找到最新的那条 → 点右侧「⋯」→ 点「Redeploy」→ 再点一次「Redeploy」确认

**在后端项目里配：**

同操作，进入后端项目 Settings → Environment Variables，添加：

| 变量名 | 值填什么 |
|--------|---------|
| `DEEPSEEK_API_KEY` | 你的 DeepSeek API Key（长这样：`sk-xxxxxxxxxxxxxxxx`） |
| `SILICONFLOW_API_KEY` | 你的 SiliconFlow API Key（可选，不用就留空） |

保存后同样 Redeploy 一次。

---

### 第 7 步：测试网站能不能用

打开前端的网址（`https://sellerai-xxxxx.vercel.app`）→ 在聊天框里输入「你好」→ 点发送。

如果能收到 AI 回复，恭喜你部署成功 ✅

如果没收到回复 → 看下面的常见问题。

---

### 第 8 步：绑自己的域名（可选）

详细步骤见 `域名绑定指南.md`。

简单说就三步：
1. 在 Vercel 项目里进入 Settings → Domains → 输入你的域名 → 点 Add
2. Vercel 会告诉你需要加的 DNS 记录，照抄到域名管理后台
3. 等几分钟到 48 小时，域名就生效了

---

### 第 9 步：关闭自动部署（可选）

如果你不想每次改代码 Vercel 都自动部署：

1. 进入项目 → Settings → Git → 找到「Auto Deploy on Push」
2. 关掉它

---

### 第 10 步：收工，把它发给别人用！

把网址（你自己的域名或 `xxx.vercel.app`）发给你的同事、朋友、客户。

他们打开浏览器就能用，不需要安装任何东西。

---

## 🆘 常见问题

### Q1：部署失败了怎么办？

1. 先看 Vercel 给你的报错信息（红色警告框里写的啥）
2. 常见原因一：`Root Directory` 没改对。确认前端项目填了 `sellerai-frontend`，后端填了 `sellerai-backend`
3. 常见原因二：仓库名拼错了。确认 GitHub 仓库确实叫 `sellerai`
4. 还是不行？去 GitHub 仓库看一眼代码是不是全推上去了（别漏了 `package.json`、`requirements.txt`）
5. 终极办法：删掉 Vercel 里的项目，重新 Import 一次

---

### Q2：网站能打开，但发消息没反应？

> 这种情况下，AI 接口没通。

1. **检查环境变量**：进入 Vercel Settings → Environment Variables，确认 `DEEPSEEK_API_KEY` 填了而且没填错（别前后多了空格）
2. **检查后端地址**：确认前端的 `NEXT_PUBLIC_API_URL` 填的是后端地址，不是前端地址
3. **确认 Redploy 了**：改完环境变量后必须 Redeploy！光保存不够
4. **确认 API Key 有钱**：去 https://platform.deepseek.com 看一下余额是不是 0
5. **打开浏览器 F12**：看 Console 里有没有红色报错，截图发给懂技术的朋友

---

### Q3：网站打不开（白屏 / 404 / 加载不出来）？

1. 等 30 秒再刷新一次。Vercel 刚部署完可能有延迟
2. 换个浏览器试试（用 Chrome）
3. 检查是不是被墙了——让朋友用手机流量试一下
4. 确认 Vercel 部署状态：进项目看 Deployments 页面，状态是不是「Ready」→ 如果不是，点进去看错误日志
5. 绑了域名的：等 DNS 生效（最长 48 小时，一般几分钟就好）

---

### Q4：怎么更新代码？

1. 在你电脑上改代码
2. 提交（commit）并推送（push）到 GitHub
3. Vercel 会自动检测到新代码，自动部署
4. 1-2 分钟后刷新网站就能看到更新

> 不想要自动部署？看第 9 步。

---

### Q5：这玩意儿花钱吗？

| 项目 | 费用 |
|------|------|
| Vercel 托管前端 | 免费（个人项目够用） |
| Vercel 托管后端 | 免费（每月 100GB 流量，够几千人用） |
| DeepSeek API | 按量付费，大概 1 块钱能问答几百次 |
| 域名 | 一年几十块 |

**总结：除了 API 调用和域名费，基本不花钱。**

---

### Q6：怎么保证别人不乱用我的 API？

你可以在后端加一个简单的密码验证。或者在 DeepSeek 后台设置 API 调用额度上限，防止刷爆余额。去 https://platform.deepseek.com → 左侧「Usage Limits」设置。

---

有问题？把报错信息截图发给你身边懂技术的朋友，或者去 Vercel 官方文档：https://vercel.com/docs

祝你部署顺利！🎉
