# WorkBuddy 7 天训练营 · 打卡仓库

**规则只有一条：每天一个 commit。断一天，绿点就断了。**

- 起止：2026-11-01 → 2026-11-07
- 每天 60–90 分钟，到点就停
- **不产出文件 = 当天没完成**

## 教材

- 主线（带练习材料，每章有结果对照）：https://github.com/KimYx0207/AI-Coding-Guide-Zh → `docs/workbuddy/` 下 WB-00 ~ WB-10，练习素材在 `examples/`
- 副线（真实案例）：https://github.com/AlephAITech/WorkBuddyGuide ，在线读 https://workbuddy.homes/

## 打卡表

| Day | 主题 | 硬交付 | 完成 |
|---|---|---|---|
| 1 | 安装 + 第一份周报 | 用 5 条真实工作记录生成周报，存 Word | [x] |
| 2 | 表格与数据清洗 | 7 行订单：定口径 → 清洗 → 汇总 → 出图，改条件再跑一遍 | [ ] |
| 3 | 技能与连接器 | 装 1 个技能跑通 + 接 1 个连接器完成真实读写 | [ ] |
| 4 | 资料库与会议纪要 | 三份新旧资料练引用判断；纪要提取行动项+负责人+时间+原文依据 | [ ] |
| 5 | 定时任务与远程执行 | 先手动跑通，再设一个定时任务，写清触发/范围/失败处理 | [ ] |
| 6 | 编程模式与批处理 | 批量整理文件夹（**先副本试运行**）+ 跑一个小脚本 | [ ] |
| 7 | 沉淀成自己的系统 | 把最有用的 1 个流程写成 Skill/提示词模板 + 验收标准 + 失败回退 | [ ] |

## 每日复盘（每天 commit 时更新）

### Day 1（2026-11-01）
- 跑通了什么：5 条真实工作记录 → 周报（保留未完成项）→ Word。产出 `day1-weekly-report/` 下「工作记录-5条.md + 周报-2026-11-01.md + .docx」。
- 卡在哪：本机 HTTPS 连 github.com 被代理拦截（超时 21s 后失败），已确认必须走 SSH；环境里没有 python-docx，改用标准库手写 OOXML 生成 docx（`scripts/md2docx.py`）。
- 沉淀了什么：`prompts/周报生成.md`（四段结构 + 事实核查，禁止把未完成写成已完成）、`scripts/md2docx.py`（零依赖 md→docx）。
- 欠账：WB-00 / WB-01 / WB-02 与蓝皮书第 1–2 章未读，顺延补齐。
- **21:00 补记（第二次打卡自动化触发）**：
  - 教材已用 SSH 稀疏克隆到本地 `/tmp/aiguide`（`git clone --depth 1 --filter=blob:none --sparse` + `sparse-checkout set docs/workbuddy examples`），HTTPS 在本机确实不通，SSH 通。
  - 三章要点已读并写入 `day1-weekly-report/验收-WB-01-官方样例回归.md`（同时生成 .docx）。最重要的三条：① 5.5.4 起「自动化」改名「**定时任务**」；② WB-01 的真验收是**改一处事实重跑**，一增一减同时成立才算过；③ WB-02 §6 安全自检，首次别接敏感账号。
  - **官方样例回归**：拿教材 `examples/office-lab/work-notes.md` 的 N1–N5 套 `prompts/周报生成.md` 跑一遍，按 WB-01 §1.4 四条验收点打分 → **4/4 通过**（未把联调写成已完成 / 演示日期用 9-16 / 负责人写"待确认"未编造 / 5 条反馈未泛化）。
  - `scripts/md2docx.py` 复跑通过，零依赖 md→docx 链路仍可用。
  - **仍未完成（需本人在 App 内做，自动化代替不了）**：WB-01 §1.2 召唤专家跑周报、§1.4 变化题；WB-02 §4.2 最小任务与安全自检；蓝皮书第 1–2 章。
  - 注意：本仓库曾于 20:47 被移入 `_trash/已清除-7天训练营-2026-11-01/`，本次已按原样恢复（含 .git 与 Day 1 产物），远端仓库未受影响。

### Day 2
- 跑通了什么：
- 卡在哪：
- 沉淀了什么：

### Day 3
- 跑通了什么：
- 卡在哪：
- 沉淀了什么：

### Day 4
- 跑通了什么：
- 卡在哪：
- 沉淀了什么：

### Day 5
- 跑通了什么：
- 卡在哪：
- 沉淀了什么：

### Day 6
- 跑通了什么：
- 卡在哪：
- 沉淀了什么：

### Day 7
- 跑通了什么：
- 卡在哪：
- 沉淀了什么：

## 目录

```
day1-weekly-report/   周报与工作记录 + WB-00/01/02 章节验收与官方样例回归
day2-orders/          订单清洗与图表
day3-skills/          技能与连接器
day4-knowledge/       资料库问答与会议纪要
day5-automation/      定时任务配置
day6-coding/          批处理脚本与试运行记录
day7-system/          沉淀的 Skill 与验收标准
prompts/              可复用提示词
scripts/              自建小工具（md2docx.py：零依赖 md→Word）
```

## 环境备注（本机）

- GitHub 一律走 SSH：`git@github.com:Sherry-lin-ng/workbuddy-7day-bootcamp.git`。HTTPS 会被代理拦截报 502/超时。
- 涉及批量改文件、远程执行、自动化：**先在副本上试运行**，写清权限边界再上真数据。
- 取主线教材：HTTPS 连 github.com 被代理拦截，用 SSH 稀疏克隆即可（`--depth 1 --filter=blob:none --sparse` 只拉 `docs/workbuddy` 和 `examples`，几秒完成）。
