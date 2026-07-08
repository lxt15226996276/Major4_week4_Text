# lixiaotong · Unity 主程成长 · 唯一执行入口

> **总文档地图**：[`Docs/README.md`](../README.md)  
> **你以后只打开这 3 个文件**：  
> ① **本文件**（今天干什么） ② [`../02-学员档案/学员能力档案_lixiaotong.md`](../02-学员档案/学员能力档案_lixiaotong.md) ③ [`../01-成长路线/W4-RPG周-当前.md`](../01-成长路线/W4-RPG周-当前.md)  
> **教练/AI 必读**：本文件 + 档案 + [`../04-教练参考/外部路线吸收库.md`](../04-教练参考/外部路线吸收库.md) **§六** + [`../02-学员档案/踩坑记忆库_lixiaotong.md`](../02-学员档案/踩坑记忆库_lixiaotong.md) · **每次输出前 §11.28 双遍 Doc**
**档案维护（v7.14）**：**开下一套题** 或 **「ExamXX 交付完成」** → AI **同一轮 §11.7 录入**四文件（**不须**学员再催）

---

## 零、你的真实处境（2026-07-08 · W4 起 · AI 维护）

| 项 | 值 |
|----|-----|
| Unity | 2022.3 LTS · 项目 **`Major4_week4-Text`** |
| 学院 | 元宇宙 · 专业四《Unity开发实战》· **月考纲 U01～U20** |
| SiKi | Unity A计划 · 有效至 **2027-04-15** |
| **现在** | **W4 RPG 阶段 1 · 工程骨架已建** · [`W4-RPG周-当前`](../01-成长路线/W4-RPG周-当前.md) |
| P / K / S | **84* / 58 / S2-（过渡）** → 本周目标 **P≥82 K≥75** |
| **IC 职级** | **L2 · 合格初级** · 详 [`职级全景_L0-F1`](../01-成长路线/职级全景_L0-F1_Unity客户端_lixiaotong.md) |
| **本周硬交付** | **RPG 四阶段 Play 闭环** · `Assets/Stage01_W4/` |
| **工程状态** | Exam01～10 **已重置**（仅 Prefab 素材池） · W3 Lab 归档保留 |

**三条轨（已合并，勿再拆出去问 AI）：**

| 轨 | 是什么 | 本周占比 |
|----|--------|:--------:|
| **K+P** | 学院考纲 + Exam/Lab/RPG + P-L1 | **85%** |
| **M** | SiKi 视频查缺 | **≤5h/周** |
| **I** | 面试 2 题/套 | **15min/天** |

**教练输出（v7.16.4 · §11.28 Doc 双遍 · §11.29 同类题递进 · §11.25 矩阵 · §11.27 主动审计 · **K1/R1 门禁**）**

**Doc 双遍对照（R1 · 每次输出前）**：① 总 `Docs/` + `Assets/Exams/Docs/` 规范与模板 → ② 本套 `ExamXX/Docs/` **当前大步** → ③ **9 项对照全 ✅** 才发 Chat · 讲义/档案脱节 → **先更 Doc 再输出**

**Chat 改库（K1）**：「进行下一步」= **模板 B/C · 不改仓库** · 「帮改 UI」≠ 授权 · 改 Prefab/场景/脚本须 **「帮我改/检查并修复」+ 模板 D 确认**

**UI 搭建**：三列表 · Prefab 优先（O1d）· **增删控件查矩阵 U1～U7**（Button→HLG · Input→**VLG 七步** · **Image→ARF** · Text→CSF）· **Reset 子 Anchor · Sibling 顺序** · **开讲前审计 · 禁止等学员测出才改（P2）** · [`UI布局举一反三矩阵.md`](../../Assets/Exams/Docs/UI布局举一反三矩阵.md)

| 开套 | `分步教程.md` 写全 |
| 大步 | L1=试卷 · B=FICM |
| **每模块完成** | **大厂商业对比 + 问开不开小灶**（§11.24）→ 登记 [`小灶登记`](../04-教练参考/小灶课堂/_模块商业对比登记_lixiaotong.md) |
| **小灶** | 回复 **`小灶：XXX`** → **下一条 Chat 独占** · **`跳过小灶`** → 继续 |
| 自写脚本 | 说 **「这是我自己写的脚本」** → AI **§11.16 读码校准** P-L1（略高于现状） |
| **规范迭代** | 说 **「同意迭代 v7.x」** / **「记住踩过的坑」** / **「注释规范又忘了」** → AI **§11.18 / §11.19** + **踩坑记忆库** |

**UI 布局踩坑（Exam06 · U1/U2）**：钮行 **HLG + CSF + Pivot 0.5** · Spacing **24** · Force Expand **关** · 见 [`教学规范 §11.25`](../../Assets/Exams/Docs/教学规范.md) v7.13.2

**UI 素材踩坑（Exam05 已踩）**：[`踩坑记忆库`](../02-学员档案/踩坑记忆库_lixiaotong.md) §一 **B1～B4** · §二-C **H1～H3 血条 Fill@0**

**已废止**：v7.2 小分段独立 Chat · v7.3 六维 · v7.4 双轨多表

---

## 零-B、S 轨 + IC 职级一页纸（lixiaotong · 2026-07-03）

| 项 | Coach S | **IC 行业** |
|----|:-------:|:-----------:|
| **当前** | **S2-（过渡）** | **L2 · 合格初级** |
| **相机** | P-L1 范本 | **L2** · `CameraFollow` 读码 |
| **下一档** | S2- 稳固 ← **P-L1 6/6 套** | **L3** ← Cinemachine + Exam03 闭环 |
| **阶段 01 末** | **S2 入门** · K≥75 | **M1 入口** |
| **F1** | 不追 | **2030+ 荣誉轨可选** |

详表：[`学员能力档案 §1.4～§1.5`](../02-学员档案/学员能力档案_lixiaotong.md) · [`职级全景_L0-F1`](../01-成长路线/职级全景_L0-F1_Unity客户端_lixiaotong.md)

---

## 一、今天只做这些（滚动更新）

### 2026-07-08 · **W4 RPG · Stage1_Login · 第 1 步待开讲** ← 当前

| 任务 | 说明 |
|------|------|
| 核心 | 三场景+Build+SceneNames（考点 7、8） |
| 讲义 | [`分步教程.md`](../../Assets/Stage01_W4/Stage1_Login/Docs/分步教程.md) **第 1 步** |
| 教程 | [`教程.md`](../../Assets/Stage01_W4/Stage1_Login/Docs/教程.md) |
| 工作目录 | `Assets/Stage01_W4/Stage1_Login/` |
| 可复用 Prefab | `Exam01/LoginCanvas` · `Exam06/LoadingCanvas` |
| L1 验收 | 三场景 · Build 0→1→2 · SceneNames 编译通过 |
| ⚠️ **K1** | 「进行下一步」= **只教 · 不改仓库 · 脚本须自己敲** |

### 2026-07-04 · **Exam08 · 第 4 步 选服**（并行/周末补）

| 任务 | 说明 |
|------|------|
| 核心 | ServerUI Prefab · **ServerController** · 3 服不同名 · **经 Loading 进 Main** |
| 讲义 | [`Exam08/Docs/分步教程.md`](../../Assets/Exams/Exam08/Docs/分步教程.md) **§11.29 v3** |
| 进度 | 第 1～3 步 **✅ 读码** · 第 4 步 **← 当前** |
| **递进** | vs Exam07 登录 · Exam01 选服 · Exam06 Loading **Min 双轨** |
| **读码待补** | `SelectedServer` 未赋值 · Build **0→1→2→3** 顺序 · 删 useless using |
| ⚠️ **K1** | 「进行下一步」= **只教 · 不改仓库** |

### 2026-07-04 · **Exam09 · 开套**（§11.29 递进校准）

| 任务 | 说明 |
|------|------|
| 核心 | 创建工程 · 三场景链 · 登录→Loading→Main · 减血系统 · 胜利判定 |
| 讲义 | [`Exam09/Docs/分步教程.md`](../../Assets/Exams/Exam09/Docs/分步教程.md) **§11.29 v3** · 7 步写全 |
| 进度 | 第 1 步 **← 当前** |
| **递进** | vs Exam02/06/07/08 · VLG+CSF · Min 双轨 · Fill@0 · §11.9 注释梯度 |
| **P-L1 新增** | `TryLogin(out msg)` · Clamp · OnDestroy 解绑 · Button.interactable 禁用 |
| ⚠️ **K1** | 「进行下一步」= **只教 · 不改仓库** |

### 2026-07-04 · Exam04 归档（开 Exam08 · 第 1 步未完成）

| 任务 | 说明 |
|------|------|
| 核心 | 仅完成讲义 v3 · **三场景未交付** |
| 状态 | **开套中断** · 可随时续做 |
| 讲义 | [`Exam04/Docs/分步教程.md`](../../Assets/Exams/Exam04/Docs/分步教程.md) |

### 2026-07-03 · **Exam04 开套 · 第 1 步**（已归档 ↑）

| 任务 | 说明 |
|------|------|
| 核心 | 读题 + 三场景 + Build 0→1→2 · **§11.29 递进导图** |
| 讲义 | [`Exam04/Docs/分步教程.md`](../../Assets/Exams/Exam04/Docs/分步教程.md) **v3 重生成** |
| 进度 | 第 1 步 **🔒 中断** |

### 2026-07-03 · Exam03 归档（✅ · 开 Exam04 自动录入）

| 任务 | 说明 |
|------|------|
| 核心 | 登录+射击+加血+相机+坦克移动 · L1+P-L1 ✅ |
| P+1 待补 | Build 仅 Exam03 · 敌人 Destroy · FireController 注释 |
| 亮点 | `CameraFollow` **IC L2** · `TrankController` Space.Self |

### 2026-07-02 · W2 遗留 · Exam03 **第 3～4 步**（已归档 ↑）

| 任务 | 说明 |
|------|------|
| 核心 | 3D + GameSceneUI 改造 · 刷怪/开火/加血脚本 · **须学员本人做** |
| 讲义 | [`Exam03/Docs/分步教程.md`](../../Assets/Exams/Exam03/Docs/分步教程.md) |
| 进度 | 第 1～4 步 ✅ · 第 5 步 Build **P+1 待补** |

### 2026-06-25 · W2 遗留 · Exam03 **第 3 步**（已合并上栏 · 归档说明）

| 任务 | 说明 |
|------|------|
| 核心 | 3D Plane+Tank 可见 · GameSceneUI 改造 · **Backgrouond Image 关** · BtnFire · 敌人总血 Text |
| 讲义 | [`Exam03/Docs/分步教程.md` 第 3 步](../../Assets/Exams/Exam03/Docs/分步教程.md) |
| 进度 | Prefab **须学员按讲义自改**（AI 擅自改动无效计入 P-L1） |

### 2026-06-25 · Exam03 第 2 步（✅ 归档）

| 任务 | 说明 |
|------|------|
| 核心 | LoginPanel 开 · **6666** · LoginController |
| 讲义 | [`Exam03/Docs/教程.md`](../../Assets/Exams/Exam03/Docs/教程.md) |

### 2026-06-24 · Exam08（⚠️ **L1 可交卷** · 第 6 步 Build/断网待补）

| 项 | 状态 |
|----|------|
| 场景链 Login→Loading→Server→Loading→Main | ✅ Loading 已修 · Server 经 Loading |
| MainController · 减血/关闭/胜利 | ✅ 四引用已拖 |
| SelectedServer · Login 注释 · Build 0→3 顺序 | ⚠️ 小项 |
| P-L1 整包 | ☐ 断网 + 导图 |

### 2026-06-24 · Exam08 **第 4 步 · ServerScene 动态 3 服** ← 归档

| 任务 | 说明 |
|------|------|
| 核心 | Instantiate 3 服钮 · 不同名 · 点服 → Loading → Main |
| 讲义 | [`Exam08/Docs/分步教程.md` 第 4 步](../../Assets/Exams/Exam08/Docs/分步教程.md) |
| Prefab | `Exam01/ServerItem.prefab` 改 → `Exam08/Prefabs/ServerItemButton` |

### 2026-06-24 · Exam08 **第 3 步 · LoginController + Loading**（✅ L1 · P-L1 注释小项）

| 项 | 状态 |
|----|------|
| GameSession · Trim 三字段 · NextScene | ✅ |
| LoginManager 五引用已拖 · OnDestroy 解绑 | ✅ |
| LoadingManager · Slider + Tip · Async Min 进度 | ✅ |
| LoginController 类顶 `///` · OnLoginBtnClick 思路注释 | ⚠️ 待补 |

### 2026-06-24 · Exam08 **第 2 步 · Login UI**（✅ L1 · P-L1 ✅）

| 项 | 状态 |
|----|------|
| VLG + CSF · Account→Password→Name→Btn · Spacing 24 | ✅ |
| LoginFormColumn · LoginCanvas · NameInput LE 900×80 | ✅ |

### 2026-06-24 · Exam08 **第 1 步 · 开套**（✅）

| 任务 | 说明 |
|------|------|
| 核心 | 思维导图 · **四场景** · Build 0→3 |
| 讲义 | [`Exam08/Docs/分步教程.md` 第 1 步](../../Assets/Exams/Exam08/Docs/分步教程.md) |
| 对比 | Exam02 场景链 · 多 **姓名框** · **动态 3 服** |

---

### 2026-06-24 · Exam07（✅ **§11.7 归档** · 开 Exam08 触发）

| 项 | 状态 |
|----|------|
| L1 / P-L1 | ✅ 注册·登录·锁3s·Game BGM·Cube·WS名字 |
| P+1 | **3/6**（Build·导图·LateUpdate 待补） |
| P-Score | **84** |
| 方案 | World Space 子 Canvas 跟随（无 FollowNameUI） |

---

### 2026-06-24 · Exam07 **第 4～5 步** ← 归档

### 2026-06-24 · Exam07 **第 2 步 · Login UI**（✅ L1 · P-L1 小项待补）

| 项 | 状态 |
|----|------|
| InitialPanel + 三屏 Active | ✅ |
| BtnToLogin / BtnToRegister | ✅ |
| Scaler 1920 | ✅ |
| TipText / 语义 Input 名 / LoginCanvas 改名 | ⚠️ 第 3 步前补 TipText |

---

### 2026-06-24 · Exam07 **第 1 步 · 开套**（✅）

| 项 | 状态 |
|----|------|
| 两场景 | `Exam07_Login` · `Exam07_Game` ✅ |
| 讲义 | 6 步写全 |

---

### 2026-06-24 · Exam06（✅ **§11.7 自动归档** · 开 Exam07 触发）

| 项 | 状态 |
|----|------|
| L1 / P-L1 | ✅ 逻辑链全通 · Battle 范本级 |
| P+1 | **4/6**（Clamp·6s·Min·解绑 ✅ · Build置顶·导图 ☐） |
| P-Score | **83** · 硬指标 **3/6 套** |
| 小灶 | 小灶02 Loading ✅ · 小灶01 血量 ✅ |
| 待补（不挡下一套） | Build 0→1 · `Exam06_思维导图.png` · Loading 删无用 using |

---

### 2026-06-24 · Exam06 **第 6 步 · 交付** ← 归档

### 2026-06-24 · Exam06 **第 5 步 · BattleController**（✅ 读码 P-L1）

| 项 | 状态 |
|----|------|
| 脚本 | 命名解绑 · Clamp · §11.19 · 三钮 50 ✅ |
| 小灶 | **小灶：血量** ✅ · 自检见 §11-A |
| 待你 | Inspector 拖引用 · Play 验收 |

---

### 2026-06-24 · Exam06 **第 5 步 · BattleController** ← 归档

### 2026-06-24 · Exam06 **第 4 步 · Game UI**（✅ 进入第 5 步）

| 项 | 状态 |
|----|------|
| Layout | HLG + CSF + Pivot · U2 已教 |
| 小灶 | 未开 → 默认 **跳过小灶：UI分层** |

---

### 2026-06-24 · Exam06 **第 4 步 · Game UI（Layout Group）** ← 归档

| 任务 | 说明 |
|------|------|
| 核心 | **BattlePanel 底边 Stretch** · Row 加 **CSF** · **Pivot 0.5** · Spacing **24** · 删 Btn40 |
| 禁止 | **U2**：Spacing250 · Force Expand 开 · 中间层 `ButnAttack` 100×100 |
| 规范 | [`教学规范.md §11.25`](../../Assets/Exams/Docs/教学规范.md) |
| 讲义 | [`分步教程.md` 第 4 步](../../Assets/Exams/Exam06/Docs/分步教程.md) |

---

### 2026-06-24 · Exam06 **第 3 步 + 小灶02**（✅）

| 项 | 状态 |
|----|------|
| LoadingController | L1 ✅ · Min+Start · 小灶 **自检 3/3** |
| 讲义 | [`小灶02 §11-A`](小灶课堂/小灶02_Exam06Loading商业分层.md) |

---

### 2026-06-24 · Exam06 **第 1～2 步**（✅ 归档）

### 2026-06-24 · Exam05（归档 · 逻辑链已通 · 交付可周末补）

| 项 | 状态 |
|----|------|
| Loading / Game UI / Battle | L1 ✅ · Battle P-L1 ⚠️（lambda/注释 · 06 范本一次做对） |
| 第 6 步交付 | 导图 · Build 置顶 · 断网 · 可 **与 06 并行或周末** |
| 小灶 | 已 **`跳过小灶`**（血量） |

---

### 2026-06-24 · Exam05 **第 4 步**（✅ 归档）

| 项 | 结果 |
|----|------|
| LoadingController | P-L1 ✅ · **Min 双轨** · 双 Text · 静音反馈 |

### 2026-06-24 · Exam05 **第 1～2 步**（✅ 归档）

| 分段 | 任务 | 完成 |
|:----:|------|:----:|
| 1.2 | 两场景 + Build | ✅ |
| 2.x | Loading UI Prefab 体检 | ✅ |

---

### 2026-06-24 · Exam02 **✅ 已交付**（归档）

| 项 | 结果 |
|----|------|
| 试卷 L1 | ✅ 9 大步全流程 |
| P-L1 | ✅ OnDestroy · 协程 Async 三区 · 三 Game 分脚本 |
| P+1 | **2/5**（sceneNames[] · OnDestroy） |
| 步后 P-Score | **80** · K **58** |
| 档案 | [`学员能力档案_lixiaotong.md`](学员能力档案_lixiaotong.md) §六 · §八 已更新 |

**可选复盘（不挡下一套）**

- [ ] Build 仅 Exam02 五场景  
- [ ] Game1/2/3 类顶 `///` · 删无用 using  
- [ ] `initalPanel` → `initialPanel`

---

### 下一套 · **Exam06**（W2 D2 套2 · **当前**）

| 动作 | 说明 |
|------|------|
| 开套 | ✅ 2026-06-24 · `分步教程.md` 6 步写全 |
| 第 1 步 | 导图 + `Exam06_*` 两场景 + Build |

### 本周剩余 Exam 排期

| 天 | 套 1 | 套 2 |
|:--:|------|------|
| D1 | Exam01 复盘 P+1 | **Exam02 ✅** |
| D2 | **Exam05** ← 下一套 | Exam06 |
| D3 | Exam07 | Exam08 |
| D4 | Exam09 | Exam10 |
| D5 | Exam03 | Exam04 |

---

## 二、SiKi 本周「M 轨」—— AI 已替你选好，不用翻目录

> 详表 [`SiKi_A计划路线映射_lixiaotong.md`](SiKi_A计划路线映射_lixiaotong.md) · 吸收来源 [`外部路线吸收库.md`](外部路线吸收库.md)

| 何时 | 只看这些（SiKi 内） | 禁止 |
|------|---------------------|------|
| **Panel 卡住时** | 「案例驱动 UGUI」→ **Canvas/事件 1 节** | 塔防/FPS/PVZ 整案例 |
| **Auth 第 3 步前** | 「常用 API」→ **Dictionary/事件 查表** | C# S1 从头刷 |
| **学前必读碎片** | 剩余 **8 课** · 每天 **≤20min** 直到 20/20 | 长案例 |

**SiKi 官方公开页**：https://www.sikiedu.com/page/unitypath（四阶段：零基础→入门→进阶→高级）

---

## 三、阶段 01 剩余四周（一张表看完）

| 周 | K 轨交付 | P 目标 | M 轨（SiKi） | 宏观档 |
|:--:|----------|:------:|--------------|:------:|
| **W2** | Exam01～10 | P≥78 | UGUI/API 查缺 | C- |
| **W3** | Lab×5 | P≥80 | Animator 核心篇 | C |
| **W4** | RPG 四阶段 | **P≥82 K≥75 S2** | 持久化 1 节 | C+ |
| 阶段02 | 框架+配表 | B- 入门 | C# S4 · 设计模式选修 | — |

---

## 四、2027 前主程终点栈（已搜过 · 现在**不练**）

> 行业 2025～2026 主程常见组合 · 见吸收库 §二

| 技术 | 你何时碰 | 现在 |
|------|----------|:----:|
| UGUI + ShowPanel/AccountData | **现在 Exam** | ✅ |
| Animator/Lab | W3 | 🔜 |
| Editor/Lab | W3 | 🔜 |
| Luban/Excel 配表 | W4 RPG | 🔜 |
| UI 框架 Mono 分离 | 阶段 02 | 🔒 |
| HybridCLR + YooAsset 热更 | 阶段 03 | 🔒 |
| MOBA/帧同步/ARPG | 2027 · SiKi 阶段四 | 🔒 |

**你不需要现在去搜 HybridCLR 教程**——W4 末 RPG 能 Play 闭环后再开。

---

## 五、你还用问外部 AI 吗？

| 问题类型 | 问谁 |
|----------|------|
| 今天练哪一步、代码怎么写、验收 | **本仓库 Chat**（@本文件 + 档案 + Exam 教程） |
| 学院试卷原题、Build 断网 | **本仓库 Exam** |
| SiKi 看哪一节 | **本文件 §二** + M 轨表 |
| 主程热更/框架/网络 | **阶段到了再搜** · 已写入吸收库 |
| 豆包/Kimi 大路线 | **不必** · 已合并进 [`主程成长路线_宏观五阶段.md`](主程成长路线_宏观五阶段.md) |

---

## 六、文件地图（其余文档当参考，不日常打开）

| 日常 | 文件 |
|:----:|------|
| ⭐ | **本文件** |
| ⭐ | `学员能力档案_lixiaotong.md` |
| ⭐ | `主程成长路线_阶段01_第2周.md` |
| 开套 | `Assets/Exams/ExamXX/Docs/教程.md` + **`分步教程.md`（§11.15 写全）** |
| 教练宪法 | `Assets/Exams/Docs/教学规范.md` **v7.10** |
| 吸收库（AI 维护） | `外部路线吸收库.md` |
| 归档 | 宏观五阶段 · SiKi映射 · 下阶段说明 |

---

## 变更日志（AI 自动改）

| 日期 | 变更 |
|------|------|
| 2026-06-24 | 初版：合并 SiKi/豆包/学院为唯一入口；今日任务 Exam02 第2步 |
| 2026-06-24 | **v7.3**：深度 A · 检索 Unity/MS · 六维+API · 考纲仅参考 |
| 2026-06-24 | **v7.4**：A 考试+工业双轨 · 三层 · 代码复盘 · 演进 why · 短表 |
| 2026-06-24 | **回退 v7.2**：A=是什么/卷面为何/再挖一层 + B 对照代码 |
| 2026-06-24 | **Exam02 交付完成** · P 80 K 58 · 下一套 Exam05 |
| 2026-06-24 | **v7.9** · §11.15 开套写全分步 · Exam05 讲义 6 步补全 |
| 2026-06-24 | **v7.10** · §11.16 自写脚本校准 · Exam05 LoadingController · 过程 P **81** |
| 2026-06-24 | **v7.16.1** | **§11.27 主动审计** · **U7 VLG 七步** · **P2** · [`UI布局举一反三矩阵.md`](../../Assets/Exams/Docs/UI布局举一反三矩阵.md) |
| 2026-06-24 | **v7.15.1** | **§11.13 O1d** · UI 步 Prefab 优先 · Exam08 踩坑固化 |
| 2026-06-24 | **Exam07 归档 + Exam08 开套** · P **84** · P-L1 **4/6** |
| 2026-06-24 | **v7.13.0** | **Exam06 开套** · 6 步分步写全 · D2 套2 |
| 2026-07-03 | **Exam03 归档 + Exam04 开套** · P **84** · P-L1 **5/6** · 讲义 [`Exam04/分步教程`](../../Assets/Exams/Exam04/Docs/分步教程.md) 写全 |
| 2026-07-03 | **§11.29 同类题递进** v7.16.4 · Exam04 P-L1 v2 · 学员反馈固化 |
| 2026-07-04 | **Exam04 开套中断归档 + Exam08 §11.29 v3 续做** · 当前 **第 4 步** |
| 2026-07-04 | **Exam09 开套** · §11.29 递进校准 · P-L1 v3 · 分步教程 7 步写全 · 当前 **第 1 步** |
