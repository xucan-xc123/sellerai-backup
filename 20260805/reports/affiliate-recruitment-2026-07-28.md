# SellerAI 联盟招募报告 - 2026-07-28

## 执行状态：❌ 失败

- **执行时间：** 2026-07-28 12:00 (UTC+8)
- **目标：** Reddit r/Affiliatemarketing + r/SaaS，搜索最近7天内 "looking for affiliate programs" 相关帖子
- **结果：** ❌ 无法完成
- **原因：** Reddit 域名被安全策略拦截（SSRF保护：解析至内网/特殊IP），浏览器和 WebFetch 均无法访问

## 失败详情

- 浏览器打开：被 strict browser SSRF policy 拦截（需 IP 字面地址）
- WebFetch：Blocked - resolves to private/internal/special-use IP address
- 兜底尝试：均告失败

## 后续建议

- 检查网络代理配置或添加 Reddit 域名白名单
- 或改用其他平台（如 Twitter/X、LinkedIn）进行联盟招募
