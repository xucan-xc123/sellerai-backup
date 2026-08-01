# SellerAI 部署上线战报 — Cloudflare Workers 路线

**日期**: 2026-07-16 22:30 GMT+8
**状态**: ✅ 官网正式上线,全链路验证通过

## 最终架构
- 前端: Next.js 15.5.4 + OpenNext 适配器
- 运行时: Cloudflare Workers(非 Vercel/Netlify,避开 team 权限墙)
- 生产域名: **https://sellerai.listaikit.com** (HTTP 200, 国内可达)
- API: /api/generate-listing → DeepSeek (实测返回真实 Amazon Listing)
- 环境变量: DEEPSEEK_API_KEY 通过 wrangler.jsonc [vars] 注入

## 踩坑与解决
1. Vercel / Netlify 均因个人 token 无 team 写入权限 BLOCKED → 换 Cloudflare Pages
2. Cloudflare Pages 404(OpenNext 产物目录错) → 改 Workers 路线
3. Workers 路线需 Workers Scripts=Edit 权限 → token 补全
4. workers.dev 国内被墙(HTTP 000) → 绑自定义域 listaikit.com
5. 自定义域 530 / 10000 / 403(权限粒度不足) → token 补 SSL and Certificates=Edit
6. wrangler 经代理时 domains/records 子请求 fetch failed(网络抖动) → 重试通过
7. DNSSEC 已确认 disabled(满足 Cloudflare 前置检查)

## Token 最终权限集(已验证可用)
Account: Cloudflare Pages=Edit, Workers Scripts=Edit, Account Settings=Read, Workers KV Storage=Edit
Zone: DNS=Edit, SSL and Certificates=Edit, Zone=Edit
User: User Details=Read, Memberships=Read
End Date: Never

## 配置文件
- wrangler.jsonc: name/compatibility_flags(nodejs_compat)/main(.open-next/worker.js)/assets/.open-next/assets/routes[sellerai.listaikit.com custom_domain]/vars[DEEPSEEK_API_KEY]
- open-next.config.ts: 已配置
- build 命令: opennextjs-cloudflare build → wrangler deploy

## Cloudflare 资源
- Account ID: 9bd06de214f6c2bbd3ce3923a558f8fa
- Zone listaikit.com: 32b180678d1998f719e306221a314240 (status: active)
- Worker: sellerai-frontend (version 282d5ab2...)
- NS: buck.ns.cloudflare.com / evelyn.ns.cloudflare.com

## 域名与落地结果 (2026-07-16 22:45)
- ✅ 子域 **sellerai.listaikit.com** 正式上线(Worker custom domain, HTTP 200, 国内可达)
- ✅ 根域 **listaikit.com** 经 Cloudflare Page Rule 301 跳转到子域(rule id: 37aef3f47cf30b4b733c839170bb5b20)
  - 注意: 根域未走 Worker custom domain( wrangler domains/records 子请求被代理干扰 fetch failed, 直连 API 端点仅支持 405/403),改用 Page Rule 301 跳转, 效果等价
  - 若未来要把根域直接承载 Worker(不做跳转), 需在 Cloudflare Dashboard 网页手动加 custom domain(网页登录权限高于 token)
- ✅ Gumroad 购买页官网链接: 创始人确认已手动完成指向官网(我方代理/浏览器/抓取均无法外部核验 Gumroad 页面, 采信创始人陈述)

## 待执行(团队自转)
- [ ] SEO 博客 3 篇重新部署上线(部署链路已通, 内容早班恢复自动发版)
- [ ] 引流获客(SEO + Gumroad 发现流量)
