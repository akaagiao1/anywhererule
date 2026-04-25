# Anywhere Rule Builder

自动将公开规则源转换为 [Anywhere](https://github.com/NodePassProject/Anywhere) 可导入的自定义规则格式。

本项目通过 GitHub Actions 定时拉取规则源，自动转换、分类、去重，并输出到 `rule/` 目录，方便在 Anywhere 中通过远程规则使用。

---

## Features

- 自动读取 `links.txt` 中的规则源
- 支持 Surge / Clash 常见规则格式
- 自动转换为 Anywhere 规则格式
- 自动分类输出：
  - Apple
  - AI
  - CN
  - Proxy
  - Reject
  - All
- 自动去重
- GitHub Actions 每日自动更新
- 可配合 GitHub Pages 作为远程规则地址使用

---

## Anywhere Rule Format

Anywhere 自定义规则使用数字类型：

| 类型 | 含义 |
|---|---|
| `0` | IPv4 CIDR |
| `1` | IPv6 CIDR |
| `2` | Domain Suffix |
| `3` | Domain Keyword |

示例：

```txt
2, google.com
2, openai.com
3, telegram
0, 1.1.1.0/24
1, 2606:4700::/32
```
## 📝 links.txt

在仓库根目录创建并编辑 `links.txt`，每行定义一个规则源。

### 推荐格式

```txt
apple,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Apple/Apple_All_No_Resolve.list
icloud,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/iCloud/iCloud_No_Resolve.list
google,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Google/Google.list
ai,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/OpenAI/OpenAI.list
ads,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Advertising/Advertising.list
