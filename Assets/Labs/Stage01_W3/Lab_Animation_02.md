# Lab_Animation_02 · BlendTree 与 IK（二选一主做）

> **关联考纲**：U09（BlendTree）· U10（IK / 射击姿态）  
> **预估**：4h · **W3 第 2 天**  
> **前置**：完成 Lab_Animation_01 或等价 Animator 基础

---

## 学习目标

| 层级 | 你要做到 |
|------|----------|
| **L1** | 说清 BlendTree 1D/2D 用途；或说清 IK 解决什么问题 |
| **P-L1** | **主做一条**：1D BlendTree 速度混合 **或** 上半身 Aim IK |
| **P+1** | 另一条用 **口述 + 示意图** 答辩（不强制实现） |

---

## 路线 A：1D BlendTree（推荐先做）

### 场景

沿用 Lab_Animation_01 角色，或新建 `Lab_Animation_02_Blend`

### 步骤

1. Controller 里建 **Blend Tree** 状态 `Locomotion`
2. 三 Clip：Idle / Walk / Run，用 **Float 参数** `speed`（0 / 0.5 / 1）
3. 脚本根据输入 magnitude 写 `animator.SetFloat("speed", …)`，可 `Mathf.Lerp` 平滑

**检查**：慢走、快跑过渡连续，无瞬切硬跳

---

## 路线 B：IK 瞄准（与 Exam03 射击相关）

### 场景

角色 + 空物体 `AimTarget`（鼠标或另一 Cube 跟随）

### 步骤

1. Animator 开 **IK Pass**（Layer 或脚本 `OnAnimatorIK`）
2. `OnAnimatorIK` 里 `SetIKPositionWeight` / `SetIKPosition` 让双手或上身朝向目标
3. 简单 `Raycast` 或 `LookAt` 移动 AimTarget

**P-L1**：至少 **Position IK** 一项权重 > 0 且肉眼可见

---

## 与 Exam 映射

| Exam | 考点 | 本 Lab |
|------|------|--------|
| Exam03 | 射击动画、上半身 | 路线 B 直接相关 |
| Exam04 | 敌人移动混合 | 路线 A 直接相关 |

---

## 面试 2 题

1. BlendTree 和多个 Transition 相比，优点是什么？
2. IK 和直接旋转 Spine 骨骼，各有什么问题？

---

## 完成打勾

- [ ] 主路线 A 或 B 可 Play 演示
- [ ] 副路线口述 1 分钟
- [ ] 档案：U09 或 U10 → **2**（主做的那条）
