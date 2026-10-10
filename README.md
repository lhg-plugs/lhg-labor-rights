<!-- About 简介（推送后填写到仓库 About 栏）：
劳动维权助手：纠纷场景→仲裁流程指引→文书模板→证据清单 ｜ 一键安装：/plugin marketplace add lhg-plugs/lhg-labor-rights
-->
<!-- topics（推送后打）：claude-code, claude-plugin, agent-skills, labor-rights, legal-aid, arbitration -->

# lhg-labor-rights：劳动维权助手，仲裁维权一条龙

> ⚠️ **声明（首屏置顶）**：本插件是**劳动维权助手**（非"专家"，弱化执业暗示），**非律师意见、仅供参考**；**涉及时效与管辖等关键问题请咨询执业律师**。
>
> **一句话介绍**：给 AI 编程助手装上"劳动维权助手"——纠纷场景判定 → 仲裁/诉讼流程指引 → 仲裁申请书与证据清单模板 → 证据三要素体检；**胜诉承诺写入即拦截，5 条确定性规则兜底**。
>
> **一键安装**：在 Claude Code 里运行
> ```
> /plugin marketplace add lhg-plugs/lhg-labor-rights
> /plugin install lhg-labor-rights@lhg-plugs
> ```

## 它是什么

`lhg-labor-rights` 是一个 Claude Code 插件（plugin 为主、skill 为辅）：

- **4 个命令**（小白入口）：`labor-rights` 维权一条龙，`labor-docs` 文书起草，`labor-evidence` 证据整理，`labor-audit` 文书体检
- **4 个平台中立 skill**（方法论，可移植到豆包/Workbuddy 等 agent 平台）：纠纷场景判定（八类场景）、仲裁/诉讼流程指引、文书模板（申请书六部分+金额公式）、证据清单（三要素）
- **2 个助手 agent**：维权流程助手、文书审计员
- **1 个执业硬门 hook**：写入文件命中执业暗示/胜诉承诺关键词（保证胜诉/包赢/百分百胜诉/律师意见等）直接拦截，"非律师意见"声明不被误拦，可一键关闭
- **5 条确定性审计规则**：纯 Python 标准库、零第三方依赖，含文书必填字段、1 年时效提醒、证据三要素、管辖表述、非律师意见声明检查

## 合规设计：三层防护

1. **声明置顶**：README 首屏、每个 SKILL.md 开头、每条命令输出末尾，都有显著的"非律师意见"声明。
2. **写入硬门**：hook 在文件写入前扫描执业暗示/胜诉承诺关键词，命中即拦截（exit 2）；`LHG_LABORRIGHTS_ADVICE_OFF=1` 可关闭。
3. **审计兜底**：`rights_audit.py` 的 5 条规则（4 blocker + 1 warning），`labor-audit` 命令逐条清零。

## 4 个命令用法

| 命令 | 作用 | 示例 |
|---|---|---|
| `/lhg-labor-rights:labor-rights` | 场景→流程→文书→证据一条龙 | `/lhg-labor-rights:labor-rights "公司欠我三个月工资"` |
| `/lhg-labor-rights:labor-docs` | 起草仲裁申请书（六部分模板） | `/lhg-labor-rights:labor-docs "违法解除" "2022年3月入职"` |
| `/lhg-labor-rights:labor-evidence` | 整理证据清单（三要素） | `/lhg-labor-rights:labor-evidence ./我的材料` |
| `/lhg-labor-rights:labor-audit` | 体检：字段/时效/证据/管辖/声明 | `/lhg-labor-rights:labor-audit ./维权材料` |

## 目录结构

```
lhg-labor-rights/
├── .claude-plugin/          # plugin.json（插件清单）+ marketplace.json（本仓即市场）
├── commands/                # 4 个命令：labor-rights / labor-docs / labor-evidence / labor-audit
├── skills/                  # 4 个平台中立 skill（场景/流程/文书/证据，声明置顶）
├── agents/                  # 2 个助手 agent（advisor / doc-checker）
├── hooks/                   # 执业暗示/胜诉承诺拦截 hook（fail-open，可一键关闭）
├── scripts/audit/           # 确定性审计：rights_audit.py（零第三方依赖）
├── fixtures/                # 好/坏对照用例
├── smoke_test.py            # 冒烟测试
├── ATTRIBUTION.md           # 灵感来源声明
└── LICENSE                  # MIT
```

## 什么时候用 / 什么时候不用（FAQ）

**什么时候用**
- 被欠薪/违法解除/没签合同，不知道能主张什么 → `labor-rights` 一条龙
- 决定仲裁了，不会写申请书 → `labor-docs` 按模板起草
- 材料一堆，不知道哪些有用 → `labor-evidence` 整理成三要素清单
- 文书写完了，不确定全不全 → `labor-audit` 体检

**什么时候不用**
- 想要"这个官司能不能赢"的结论 → 本插件**不给**，请咨询执业律师
- 想要律师代理出庭 → 本插件是助手不是律所，请找执业律师
- 工伤/社保等需要行政程序前置的复杂案件 → 本插件只给框架，个案请咨询律师
- 想伪造证据"让案子更稳" → **直接拒绝**，这是违法的

## 自检与反馈

本插件自带质检：每次使用后可跑 `python3 smoke_test.py` 一键验证（JSON 合法、skill/command/agent 完整性、5 条规则、fixtures 命中、hooks 行为）。

发现 bug 或有改进建议，以 `[QC] <一句话问题>` 为标题提交到 https://github.com/lhg-plugs/lhg-labor-rights/issues，正文写清"复现步骤 → 实际表现 → 期望表现"。

| 插件 | 一句话 | 安装 |
|---|---|---|
| [lhg-fullstack](https://github.com/lhg-plugs/lhg-fullstack) | 小白一句话 → 高质量全栈应用 | `/plugin install lhg-fullstack@lhg-plugs` |
| *（后续插件在此追加，保持表格格式一致）* | | |

## 出品：刘洪光

本插件由真人出镜 IP「刘洪光」（安徽合肥）出品，归属 [lhg-skills](https://github.com/lhg-skills)。

- GitHub 主页：https://github.com/lhg-skills —— 全部 skill 开源在此，欢迎 star
- 视频号：搜「刘洪光实名上网」
- 微信：lhgsmsw
