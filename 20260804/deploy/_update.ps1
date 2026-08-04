$path = 'E:\QClaw\Work-QClaw\sellerai-deploy\竞品档案.md'
$content = Get-Content $path -Raw -Encoding UTF8

$old = '> 自动更新于 2026-07-29 15:00 GMT+8（周三）· SellerAI 竞品情报 Agent'
$new = "| 2026-07-30 15:00（周四） | **15:00 自驱复核（英文+中文双通道）**：JS 中文官网（junglescout.cn/freemium，07-19 快照）确认 插件套餐 `$197/年、创业版 `$399/年，与基线一致；英文官网 Catalyst/Cobalt 双线结构维持——Catalyst 三档（Starter `$29/mo / Growth Accelerator `$49/mo / Brand Owner `$129/mo）及「Save up to `$360 on annual plans」标语同前，Cobalt 仍为企业 demo 通道；JS MCP / API Trial 加购项未见扩容或调价。H10 中文渠道折扣价（铂金折后 `$445/年、钻石 `$1291/年，07-29 日期快照）属常规 affiliate 促销、非官方调价；英文官网（helium10.com/pricing）确认 Free / Platinum `$99 / Diamond `$279（年付价）/ Enterprise `$1499 四档不变，MCP 推广横幅仍在首页顶部高亮，Listing Review Insights 未见新增模块或调价信号。新进入者扫描：搜索未发现新 Listing 优化赛道工具面世，此前标记的 Perci.ai / L-Guard / SellerShorts / SmartScout 均无新动静；未发现独立 AI 定价套餐（AI-only plan）等新型定价模式 | 无变动 | 记录「今日无变动」；未触发微信告警 |`r`n`r`n> 自动更新于 2026-07-30 15:00 GMT+8（周四）· SellerAI 竞品情报 Agent"

$result = $content.Replace($old, $new)
if ($result -eq $content) {
    Write-Host 'ERROR: Replacement text not found!'
    exit 1
}
Set-Content $path $result -Encoding UTF8
Write-Host 'SUCCESS: File updated.'
