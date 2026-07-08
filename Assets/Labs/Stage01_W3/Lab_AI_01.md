# Lab_AI_01 · 单怪巡逻 / 追击 / 攻击 / 脱战

> **关联考纲**：U14（AI 行为）  
> **预估**：4h · **W3 第 5 天**  
> **前置**：Lab_Gameplay_01 移动 · 基础距离判断

---

## 学习目标

| 层级 | 你要做到 |
|------|----------|
| **L1** | 说清 **巡逻 / 追击 / 攻击 / 脱战** 四段触发条件 |
| **P-L1** | **1 个敌人**，四状态用 **枚举或 switch** 实现（不必 Behavior Tree） |
| **P+1** | 脱战后回巡逻点；或攻击冷却 `attackCooldown` |

---

## 场景准备

- `Lab_AI_01` 场景
- 玩家（可沿用 Gameplay Lab）
- 敌人 Cube + 巡逻点空物体 **A、B**（或两点坐标）
- 可选：简单血条 UI（不强制）

---

## 状态定义（建议）

| 状态 | 进入条件 | 行为 |
|------|----------|------|
| **Patrol** | 默认；脱战完成 | A↔B 移动或 `MoveTowards` |
| **Chase** | 与玩家距离 < `chaseRange` | 朝玩家移动 |
| **Attack** | 距离 < `attackRange` | 停移 + 播攻击/扣血（`Debug.Log` 即可） |
| **Return**（P+1） | 玩家距离 > `loseRange` | 回最近巡逻点再 Patrol |

**数值示例**：chase 8m · attack 2m · lose 12m

---

## 第 1 步：感知

- 每帧或每 0.2s：`Vector3.Distance` 或 `sqrMagnitude`（P+1 口述为何 sqr 更快）
- 不要 `Find("Player")` 每帧；Awake 缓存 `Transform player`

---

## 第 2 步：状态机主循环

```text
Patrol → (进 chaseRange) → Chase → (进 attackRange) → Attack
Chase → (超 loseRange) → Return/Patrol
Attack → (冷却结束且仍在 attackRange) → 再 Attack
```

**P-L1**：`switch (state)` + `Update` 或 `FixedUpdate` 移动在 FixedUpdate（口述选一）

---

## 第 3 步：与 Exam04 敌人对比

- Exam04：简单追击或巡逻 **一档**
- 本 Lab：**完整四段** → 档案 U14 从 0 拉到 2

---

## 面试 2 题

1. 追击用每帧 SetDestination（NavMesh）和本 Lab 直移，各什么优缺点？
2. 脱战距离为什么要大于追击距离？

---

## 完成打勾

- [ ] 四状态肉眼可演示
- [ ] 玩家可跑脱战
- [ ] 档案 U14：**2**
- [ ] 周末：复习测 2（U05～U08）
