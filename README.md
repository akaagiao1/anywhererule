# Anywhere Rule Builder

这个仓库用于把多个规则源转换为 Anywhere 可用规则

## 输出

rule/
- apple.txt
- ai.txt
- cn.txt
- proxy.txt
- reject.txt
- all.txt
- index.json

## links.txt 格式

支持：

apple,https://example.com/apple.list
apple|https://example.com/apple.list
apple = https://example.com/apple.list
https://example.com/apple.list

## Anywhere 规则类型

0 = IPv4 CIDR  
1 = IPv6 CIDR  
2 = 域名后缀  
3 = 域名关键字  

## 建议分流

apple -> DIRECT  
cn -> DIRECT  
ai -> PROXY  
proxy -> PROXY  
reject -> REJECT  
