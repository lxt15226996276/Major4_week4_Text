# 主程成长路线 · 阶段 01 · 第 4 周（RPG 四阶段 · 当前）

> **所属阶段**：[`阶段01-本月配置.md`](阶段01-本月配置.md)  
> **上一周归档**：[`W3-Lab周-归档.md`](W3-Lab周-归档.md)  
> **教学规范**：[`Assets/Exams/Docs/教学规范.md`](../../Assets/Exams/Docs/教学规范.md) v7.16  
> **日常入口**：[`../00-每日入口/lixiaotong_唯一执行入口.md`](../00-每日入口/lixiaotong_唯一执行入口.md)

---

## 一、本周配置

| 字段 | 值 |
|------|-----|
| **本阶段第几周** | 第 **4** 周 / 共 4 周 |
| 本周考纲单元 | **U16～U20**（RPG 属性 · 登录 · 主场景 · 战斗 · 综合） |
| 练习形态 | **RPG 四阶段串联项目**（Exam 作对照，不强制重做 10 套） |
| 工程目录 | `Assets/Stage01_W4/` |
| 预制体素材池 | `Assets/Exams/Exam01~10/Prefabs/`（已清空场景/脚本/Docs） |
| 试卷参照 | `Tests/考试试卷/考试试题1~10.doc` |
| 姓名全拼 | **lixiaotong** |
| Unity 项目 | `Major4_week4-Text` |

---

## 二、W3 收尾快照（进 W4 前）

| 项 | 状态 |
|----|------|
| Lab 包 | `Assets/Labs/Stage01_W3/` 归档保留 |
| Exam 工程 | Exam01～10 **已重置**（仅 Prefab + 空文件夹骨架） |
| W2 十套卷 | **学员已全部完成**（2026-07-11 确认）· 作读码参照 · 不重复排欠账 |
| W4 目标 | **登录 → 主场景 → 背包/属性 → 战斗** Play 闭环 |
| 阶段硬指标 | **P≥82 · K≥75 · S2 入门** |

---

## 二-B、W4 Exam01 踩坑索引（2026-07-11 · 已写入记忆库）

> 完整表：[`踩坑记忆库_lixiaotong.md`](../02-学员档案/踩坑记忆库_lixiaotong.md) **§二-O**

| 代号 | 症状 | 一句话解法 |
|:----:|------|------------|
| A1/A2 | AnimationEvent no receiver | `public void OnAttack()` 挂 Player |
| Cam1 | 相机挂 Player 不跟 Skill6 | `pelvis/Main_Camera` 骨 + 相机子级 |
| SK2 | SetTrigger 对不上 | 用 `animTrigger` = Skill1/2/4/6 |
| BG1 | 背包开两次变 40 个 | `_itemsCreated` 防重复 |
| SK3 | 编译风险 | 删 `UnityEditor.*` using |

---

## 三、RPG 四阶段排课

| 阶段 | 天 | 目录 | 考纲 | 卷面对照 | L1 验收 |
|:--:|:--:|------|------|----------|---------|
| **1** | D1～D2 | `Stage1_Login/` | U17 | 试题1 · 试题3 · 试题6 | 注册/登录 → Loading → 进主场景 |
| **2** | D3 | `Stage2_Main/` | U18 | 试题4 · 试题5 · 试题7 | 主界面 · 人物信息 · 商城/技能入口 |
| **3** | D4 | `Stage3_Inventory/` | U16 | 试题1 背包 · 试题3 背包 · 试题6 商城 | 动态背包 · 属性面板 · 关闭返回 |
| **4** | D5 | `Stage4_Battle/` | U19 | 试题2 · 试题3 · 试题9 · 试题10 | 移动+动画 · 技能/射击 · 怪物 AI |

**周末**：U20 综合复习测 · 档案 P/K 复测 · 断网 Play 全流程

---

## 四、预制体素材池（Glob 优先 · 禁止从零手搭）

| 阶段 | 优先 Prefab | 来源 Exam |
|------|-------------|-----------|
| 登录 | `LoginCanvas` · `LoadingCanvas` | Exam01 · Exam06 · Exam08 |
| 选服/Loading | `ServerSceneUI` · `LoadingCanvas` | Exam02 · Exam08 |
| 主界面 | `MainCanvas` · `GameCanvas` | Exam01 · Exam07 · Exam08 |
| 背包/商城 | `SkillItem` · `GameSceneUI` | Exam01 · Exam04 |
| 战斗 | `Player` · `Enemy` · `Bullet` | Exam03 · Exam04 · Exam10 |

详表：[`Docs/06-Exam工程/预制体盘点_W4.md`](../../Docs/06-Exam工程/预制体盘点_W4.md)  
**Stage1 讲义**：[`Stage1_Login/Docs/分步教程.md`](../../Assets/Stage01_W4/Stage1_Login/Docs/分步教程.md)

---

## 五、本周硬指标

| 指标 | W4 末目标 |
|------|-----------|
| RPG 四阶段 | **4/4** 可 Play |
| 持久化 | **≥1** 模块（PlayerPrefs 或 JSON 二选一） |
| K-Coverage | **58 → 75+** |
| P-Score | **≥82**（S2 入门） |
| U16～U19 | 各 **≥ 已掌握(2)** |

---

## 六、AI 教练规则（W4）

| 指令 | AI 行为 |
|------|---------|
| 进行下一步 | 按 **StageX 讲义** 一大步 · §11.14 · **不代写脚本** |
| 检查一下 | L1 + P-L1 双档 |
| 开阶段 | Read 本文件 + `Stage01_W4/README.md` · **Prefab Glob 优先（O1d）** |
| 帮改 UI | 须 **模板 D 列文件** + 学员明示授权（K1） |

---

## 七、档案更新

每阶段交付后更新 [`../02-学员档案/学员能力档案_lixiaotong.md`](../02-学员档案/学员能力档案_lixiaotong.md) §六 + U16～U20 表。
