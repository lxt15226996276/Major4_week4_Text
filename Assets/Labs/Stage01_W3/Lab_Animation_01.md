# Lab_Animation_01 · Animator 基础与状态机

> **关联考纲**：U06（Animator 基础）· U07（状态机）· U08（动画事件）  
> **预估**：3.5h · **W3 第 1 天**  
> **前置**：W2 已读 U06～U08 考纲摘要（📌A 即可，不必做过 Exam04）

---

## 学习目标

| 层级 | 你要做到 |
|------|----------|
| **L1 卷面** | 能口述 Animator / Controller / Clip 关系；能建 2 状态切换 |
| **P-L1** | 自己写 `Animator.SetBool` 或 `Play` 切换；**不用** AI 整段贴 |
| **P+1** | 加 **1 个 Animation Event** 在帧上打日志或播特效占位 |

---

## 场景准备（第 0 步）

1. 新建场景 `Lab_Animation_01`（或放在 `Assets/Labs/Stage01_W3/Lab_Animation_01/`）
2. 地面 Plane + 角色（可用 Capsule + 简单 Humanoid 或自带模型）
3. 给角色挂 **Animator**，**不要**挂 Animation 旧组件

**检查点**：Hierarchy 里 Animator 的 Controller 槽为空 → 下一步建 Controller

---

## 分步任务

### 第 1 步：Animation Clip + Animator Controller

1. 做 **Idle**、**Run** 两个 Animation Clip（可用录制或简单位移/旋转关键帧）
2. 建 `PlayerAnimator.controller`，拖入 Animator
3. 两状态 **Idle ↔ Run**，用 **Bool 参数** `isRunning` 驱动 Transition

**口述验收**：Transition 的 **Has Exit Time** 开/关各试一次，说清区别（1 句话）

### 第 2 步：脚本驱动

新建 `PlayerAnimController.cs`（名字自定）：

- 读输入（键盘 WASD 或固定按钮）→ 改 `isRunning`
- 用 `animator.SetBool("isRunning", …)` **或** 你习惯的写法

**P-L1 硬指标**：

- [ ] 字段 `Animator` 在 Awake/GetComponent 缓存
- [ ] 参数名与 Controller 一致（区分大小写）
- [ ] 无每帧 `new`、无 `Find` 在 Update

### 第 3 步：Animation Event（U08）

1. 在 **Run** Clip 某一帧加 Event，调 `OnFootstep()`（或同名 public 方法）
2. 脚本里 `Debug.Log` 或触发占位粒子

**断网自检**：断网 Play → 跑起来有日志/特效 → ✅

---

## 与 Exam 的关系

| Exam | 本 Lab 补什么 |
|------|----------------|
| Exam04 | 敌人移动动画可复用本 Lab Controller 思路 |
| Exam03 | 射击动画可后接 Lab_Animation_02 |

---

## 面试 2 题（做完口述）

1. Animator Controller 里 **Layer** 是干什么的？
2. `SetBool` 和 `Play("StateName")` 各适合什么场景？

---

## 完成打勾

- [ ] L1：2 状态切换肉眼可见
- [ ] P-L1：脚本自己写 + 断网自检
- [ ] P+1：至少 1 个 Animation Event
- [ ] 档案 K 表：U06 U07 U08 → 目标 **2**
