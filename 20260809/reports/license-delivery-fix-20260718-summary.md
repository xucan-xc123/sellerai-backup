# License 交付修复 - 子任务产物（摘要）

**状态：✅ 已修复并部署验证通过**

根因：`users` 表试用阶段 `email=NULL`，webhook 的 `UPDATE ... WHERE email=?` 对异邮箱买家永远不命中 → 该 visitor 永远 free → 402。

修复：新增「按购买邮箱激活」链路（`activateLicenseByEmail` + `claim-license?activate=1` + 前端 Purchase Email Tab），把购买邮箱对应的 license 绑到当前设备 visitor_id 并解锁配额。免费 402 逻辑不变。

验证（异邮箱真实签名 webhook）：
- webhook 200 + D1 license active ✅
- claim-license activate 200 → status active, remaining 999 ✅
- 同 visitor generate-listing → 200（不再 402）✅
- 站点 HTTP 200 ✅

部署版本：b46099b7-8153-4790-a76e-d11df7b0d268

详情见 `sellerai-reports/license-delivery-fix-20260718.md`。
