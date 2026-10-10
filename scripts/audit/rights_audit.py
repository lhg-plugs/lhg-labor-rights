#!/usr/bin/env python3
"""lhg-labor-rights 确定性审计：劳动维权文书体检。

扫描目标目录下的 *.md（仲裁申请书等文书）与 evidence.json（证据清单），
按规则注册表逐项检查。零第三方依赖。

规则（rule_id / 级别 / 含义）：
  DOC-FIELD-001  blocker  仲裁申请书必填字段缺失（申请人/被申请人/仲裁请求/
                          事实与理由/证据清单/签名落款）
  LIMIT-001      blocker  仲裁时效提醒缺失（须写明 1 年/一年时效）
  EVID-001       blocker  证据链三要素缺失（每条证据须含 时间/主体/金额）
  JURIS-001      warning  管辖表述缺失（用人单位注册地/劳动合同履行地）
  NON-LAWYER-001 blocker  “非律师意见”声明缺失

用法：
  python3 rights_audit.py --target <目录> [--format json|text]
退出码：0=无问题，1=有 blocker，2=只有 warning。
"""

import argparse
import json
import os
import re
import sys

# ---------------------------------------------------------------- 规则注册表
# 仲裁申请书必填字段：关键词 -> 说明
DOC_REQUIRED_FIELDS = [
    ("申请人", "申请人信息（姓名/身份证/联系方式）"),
    ("被申请人", "被申请人信息（单位名称/地址/法定代表人）"),
    ("仲裁请求", "仲裁请求（具体事项+金额）"),
    ("事实与理由", "事实与理由"),
    ("证据清单", "证据清单"),
    ("签名", "落款签名（申请人签名+日期）"),
]
EVIDENCE_FIELDS = ["时间", "主体", "金额"]


class Finding:
    def __init__(self, rule_id, level, message, location=""):
        self.rule_id = rule_id
        self.level = level
        self.message = message
        self.location = location

    def to_dict(self):
        return {"rule_id": self.rule_id, "level": self.level,
                "message": self.message, "location": self.location}


# ---------------------------------------------------------------- 检查逻辑
def check_doc_md(path, findings):
    with open(path, encoding="utf-8") as f:
        text = f.read()

    missing = [label for kw, label in DOC_REQUIRED_FIELDS if kw not in text]
    if missing:
        findings.append(Finding(
            "DOC-FIELD-001", "blocker",
            "仲裁申请书必填字段缺失：%s" % "、".join(missing), path))

    if not re.search(r"1\s*年|一年", text):
        findings.append(Finding(
            "LIMIT-001", "blocker",
            "文书缺仲裁时效提醒：须写明“劳动争议申请仲裁的时效为 1 年”", path))

    if "注册地" not in text and "履行地" not in text:
        findings.append(Finding(
            "JURIS-001", "warning",
            "文书缺管辖表述：建议写明“向用人单位注册地或劳动合同履行地的劳动仲裁委申请”",
            path))

    if "非律师意见" not in text:
        findings.append(Finding(
            "NON-LAWYER-001", "blocker",
            "文书缺声明：须写明“本插件非律师意见、仅供参考”", path))


def check_evidence_json(path, findings):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        findings.append(Finding("EVID-001", "blocker",
                                "目标目录缺少 evidence.json（证据清单）", path))
        return
    except json.JSONDecodeError as e:
        findings.append(Finding("EVID-001", "blocker",
                                "evidence.json 不是合法 JSON：%s" % e, path))
        return

    items = data if isinstance(data, list) else data.get("evidences", [])
    if not items:
        findings.append(Finding("EVID-001", "blocker",
                                "证据清单为空：至少列出 1 条证据", path))
        return
    for i, ev in enumerate(items, 1):
        name = ev.get("名称", "第%d条" % i)
        missing = [k for k in EVIDENCE_FIELDS if k not in ev]
        if missing:
            findings.append(Finding(
                "EVID-001", "blocker",
                "证据“%s”缺三要素：%s（每条证据须含 时间/主体/金额）"
                % (name, "、".join(missing)), path))


def audit(target):
    findings = []
    for name in sorted(os.listdir(target)):
        if name.endswith(".md"):
            check_doc_md(os.path.join(target, name), findings)
    check_evidence_json(os.path.join(target, "evidence.json"), findings)
    return findings


# ---------------------------------------------------------------- 输出
def main():
    ap = argparse.ArgumentParser(description="lhg-labor-rights 劳动维权文书审计")
    ap.add_argument("--target", required=True, help="待审计目录（含文书 .md 与 evidence.json）")
    ap.add_argument("--format", choices=["json", "text"], default="text")
    args = ap.parse_args()

    if not os.path.isdir(args.target):
        print("目标目录不存在：%s" % args.target, file=sys.stderr)
        return 1

    findings = audit(args.target)
    blockers = sum(1 for f in findings if f.level == "blocker")
    warnings = sum(1 for f in findings if f.level == "warning")
    summary = {"blocker": blockers, "warning": warnings,
               "total": len(findings)}

    if args.format == "json":
        print(json.dumps({"summary": summary,
                          "findings": [f.to_dict() for f in findings]},
                         ensure_ascii=False, indent=2))
    else:
        print("维权文书审计：blocker=%d warning=%d" % (blockers, warnings))
        for f in findings:
            loc = " [%s]" % f.location if f.location else ""
            print("[%s] %s%s: %s" % (f.level.upper(), f.rule_id, loc, f.message))
        if not findings:
            print("全部通过。")

    if blockers:
        return 1
    if warnings:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
