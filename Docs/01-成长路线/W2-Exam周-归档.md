# 主程成长路线 · 阶段 01 · 第 2 周

> **所属阶段**：01 · [`主程成长路线_阶段01_本月配置.md`](主程成长路线_阶段01_本月配置.md)  
> **教学规范 v7.14**：[`Assets/Exams/Docs/教学规范.md`](../../Assets/Exams/Docs/教学规范.md) · **§11.7 开套即归档**  
> **学员档案**：[`学员能力档案_lixiaotong.md`](学员能力档案_lixiaotong.md) · **P-Score 83 · K 58**

---

## 一、本周配置

| 字段 | 值 |
|------|-----|
| **本阶段第几周** | 第 2 周 / 共 4 周 |
| 本周考纲单元 | U06～U10 + U17 |
| 练习目录 | `Assets/Exams/Exam01~Exam10/` |
| 姓名全拼 | **lixiaotong** |
| **当前进度** | **Exam01/02/03/06/07 ✅ · Exam04 开套 · Exam05 逻辑链 · P-L1 5/6** |
| **日常入口** | [`lixiaotong_唯一执行入口.md`](lixiaotong_唯一执行入口.md) |
| **本周排课** | [`一周五日十套题_排课模板.md`](一周五日十套题_排课模板.md) |
| 讲解深度 | **UI：§11.27 开讲前审计 + U1～U6 矩阵**（禁止 P2 被动补丁） |

---

## 一-B、W2 实进度（2026-06-24）

| 天 | 套题 | 状态 | P-L1 |
|:--:|------|------|:----:|
| D1 | Exam01 / Exam02 | ✅ 交付 | ✅✅ |
| D2 | Exam05 / Exam06 | 05 逻辑链 · **06 ✅ 归档** | 05 进行中 · **06 ✅** |
| D3 | **Exam07** / **Exam08** | **07 ✅ · 08 开套** | 07 ✅ |
| D4～D5 | 09～04 | 未开始 | — |

详表：[`一周五日十套题_排课模板.md`](一周五日十套题_排课模板.md) **§八**

---

## 二、P-Score 追踪（本周）

| 时间点 | P-Score | S 轨 | 触发 |
|--------|:-------:|------|------|
| W2 开周 | 74 | S1+ | 基线 |
| Exam02 交付 | **80** | **S2-** | 9 大步 L1+P-L1 |
| Exam05 读码 | **82*** | S2- 过渡 | Min 双轨 |
| **Exam06 归档（v7.14）** | **83** | **S2- 过渡** | 开 Exam07 自动录入 · **P-L1 3/6** |
| W2 周末目标 | **83+** | S2- 稳固 | 余套交付 |

| 指标 | 当前 | 说明 |
|------|:----:|------|
| **K-Coverage** | **58** | U06～U10 仍 **W3 Lab** |

### 六维快照（Exam06 归档后 · P 维）

| D1 | D2 | D3 | D4 | D5 | D6 |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 8.5 | **7.5** | 8.5 | **9.0** | 7.5 | 7.5 |

---

## 三、AI 教练规则（v7.14）

| 指令 | AI 行为 |
|------|---------|
| **开下一套 / ExamYY 第 1 步** | **自动 §11.7 归档上一套** + 开新套 |
| **ExamXX 交付完成** | 同上 · 录入 ExamXX |
| 进行下一步 | **一大步** · §11.14 · §11.9 |
| 检查一下 | L1 + P-L1 双档 |

---

## 四、Exam 进度与档案记录

| Exam | 试卷 L1 | P-L1 | P+1 | 步后 P | 档案 §六 |
|------|:-------:|:----:|:---:|:------:|:--------:|
| Exam01 | ✅ | ✅ | 6/8 | 78 | ✅ |
| Exam02 | ✅ | ✅ | 2/5 | 80 | ✅ |
| **Exam06** | ✅ | ✅ | **4/6** | **83** | ✅ **v7.14 自动** |
| **Exam05** | 进行中 | 逻辑链✅ Battle⚠️ | 3/6 | 82* | 进行中 |
| **Exam07** | ✅ | ✅ | **3/6** | **84** | ✅ **v7.14 开08归档** |
| **Exam08** | 开套 | — | — | — | — |
| **Exam03** | ✅ | ✅ | **2/6** | **84** | ✅ **v7.14 开04归档** |
| **Exam04** | 开套 | — | — | — | — |
| Exam09～10 | 🔒 | | | | |

---

## 五、Exam06 存档摘要（2026-06-24 · 开 Exam07 自动归档）

| 大步 | 内容 | 状态 |
|:----:|------|:----:|
| 1～2 | 导图规划 · Loading UI | ✅ |
| 3 | LoadingController 6s · Min · Start · 静音 | ✅ P-L1 |
| 4 | Game UI · HLG+CSF · 三钮 | ✅ |
| 5 | BattleController · 命名解绑 · Clamp · §11.19 | ✅ **范本级** |
| 6 | 交付 | P+1 部分（Build/导图 ☐） |

**亮点**

- **BattleController** 一次做对 Exam05 教训（无 lambda · RemoveListener · 三钮 50）  
- **Layout Group + CSF** · 踩坑 U1/U2  
- 小灶 **Loading 商业分层** · **血量四层**

**P+1 待补（4/6）**

- ☐ Build **Exam06 置顶 0→1**  
- ☐ `Exam06_思维导图.png`  
- ☐ LoadingController 删 `VisualScripting`/`System` using · 类顶 §11.19 补全

**脚本**：`LoadingController` · `BattleController`

---

## 五、Exam03 存档摘要（2026-07-03 · 开 Exam04 自动归档）

| 大步 | 内容 | 状态 |
|:----:|------|:----:|
| 1～2 | 双场景 + Login 6666 | ✅ |
| 3 | 3D + GameSceneUI 改造 | ✅ |
| 4 | 刷怪/开火/加血/相机/坦克移动 | ✅ P-L1 |
| 5 | 断网 Build | P+1 待补 |

**亮点**

- **`CameraFollow`** InverseTransformPoint · LateUpdate · Lerp/Slerp · **IC L2 范本**
- **`TrankController`** `Space.Self` · **`PlayerHealth.AddHealth` public**
- **`FireController`** OnDestroy 解绑

**P+1 待补（2/6）**

- ☐ 第 5 步 Build **仅 Exam03** Login=0 Game=1 · 断网自证
- ☐ `EnemyController` 取消注释 `Destroy(gameObject)` · 改注入 `PlayerHealth`
- ☐ `FireController` 补 §11.19 方法思路注释

**脚本**：`LoginController` · `GameController` · `FireController` · `PlayerHealth` · `EnemyController` · `TrankController` · `CameraFollow`

---

## 六、Exam02 存档摘要

见上一版 §六 · 2026-06-24 交付 · P **80**

---

## 七、本周结束校验

- [x] Exam01/02 **P-L1**  
- [x] Exam06 **P-L1**（v7.14 归档）  
- [ ] **6/10 套 P-L1**（当前 **5/6**）  
- [ ] W2 末 P **≥83**

---

## 八、S 轨与本周关系

| S 目标 | 本周动作 | 完成度 |
|--------|----------|:------:|
| **S2- 稳固** | **6 套** Exam P-L1 交付 | **5/6** |
| W3 前 | K 大涨靠 Lab | K **58** |

---
