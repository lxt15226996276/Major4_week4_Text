# Lab_Gameplay_01 · 摇杆移动与简单状态机

> **关联考纲**：U11（摇杆/触摸）· U12（状态机思想）· U13（玩法循环入门）  
> **预估**：4h · **W3 第 4 天**  
> **前置**：U01 移动基础（Exam04 做过更佳）

---

## 学习目标

| 层级 | 你要做到 |
|------|----------|
| **L1** | 说清摇杆向量如何映射到 `transform` 或 `CharacterController` |
| **P-L1** | **EasyTouch 或自写 UI 摇杆** 控制移动 + **2 状态**（如 Idle / Attack） |
| **P+1** | 状态用 **枚举 + switch** 或 **简单类**，不用 5 个 bool 互斥 |

---

## 场景准备

- 场景 `Lab_Gameplay_01`
- 玩家 Capsule + `CharacterController`（或 Rigidbody 方案需口述原因）
- UI：**摇杆**（EasyTouch 预制或 Unity UI 自绘）

---

## 第 1 步：摇杆输入

1. 摇杆输出 `Vector2 direction`（归一化）
2. 映射到世界空间移动：`controller.Move(direction * speed * Time.deltaTime)`
3. 相机相对移动（可选 P+1）：用 `Camera.main.transform` 的 forward/right

**检查**：只动摇杆、键盘不碰也能走

---

## 第 2 步：玩法状态（至少 2 个）

建议枚举：

```csharp
enum PlayerState { Idle, Moving, Attacking }
```

- **Moving**：摇杆有输入
- **Attacking**：按钮触发，持续 0.5s 内不能移动（或减速）
- 用 **一个** `Update` 分支或 `switch (currentState)` 驱动

**禁止 P-L1 反面**：`isIdle` `isMoving` `isAttack` 三个 bool 同时改

---

## 第 3 步：与动画衔接（可选）

- Moving → Lab_Animation_01 的 `isRunning`
- Attack → 触发 `Play("Attack")` 或 Trigger

---

## 与 Exam 关系

| Exam | 关系 |
|------|------|
| Exam04 | 键盘移动；本 Lab 换输入源 |
| Exam07/08 | 主场景移动可复用状态机结构 |

---

## 面试 2 题

1. 摇杆 dead zone 是什么，为什么要设？
2. 玩法状态机和 Animator 状态机，能合并成一个吗？

---

## 完成打勾

- [ ] 摇杆移动 L1
- [ ] 2 状态玩法 P-L1
- [ ] 档案 U11 U12：**2**；U13：**1→2**
