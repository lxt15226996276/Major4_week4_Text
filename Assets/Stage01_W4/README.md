# 阶段 01 · 第 4 周 · RPG 四阶段工程

> **周节奏**：5 天 × 1 阶段（D1～D2 合并阶段 1 登录链）  
> **目标**：U16～U20 · **登录 → 主场景 → 背包/属性 → 战斗** Play 闭环  
> 路线：[`Docs/01-成长路线/W4-RPG周-当前.md`](../../Docs/01-成长路线/W4-RPG周-当前.md)

---

## 目录约定

```
Assets/Stage01_W4/
├── README.md                 ← 本文件
├── Stage1_Login/             ← U17 登录注册 + Loading
├── Stage2_Main/              ← U18 主界面 + 人物信息
├── Stage3_Inventory/         ← U16 背包 + 属性面板
└── Stage4_Battle/            ← U19 移动 + 动画 + 战斗
```

每个 `StageX/` 下自行创建：

- `Scenes/` — 本阶段场景
- `Scripts/` — 本阶段脚本（**须自己敲**）
- `Docs/` — 阶段讲义（Step 5 起由 Coach 写）

---

## 预制体素材池（44 个 · 详表）

完整盘点：[`Docs/06-Exam工程/预制体盘点_W4.md`](../../Docs/06-Exam工程/预制体盘点_W4.md)

| 阶段 | 首选 Prefab | 路径 |
|:--:|-------------|------|
| 1 登录 | `LoginCanvas` · `LoadingCanvas` | Exam01 · **Exam06** |
| 1 选服 | `ServerCanvas` · `ServerItem` | Exam08 |
| 2 主界面 | `MainCanvas` · `HPPanel` | Exam01 · Exam10 |
| 3 背包 | `BackpackPanel`（MainCanvas 内）· `SkillItem` | Exam01 |
| 4 战斗 | `Player` · `Enemy` · `Bullet` | Exam04 · Exam03 |

**规范**：[`Assets/Exams/Docs/教学规范.md`](../Exams/Docs/教学规范.md) · **Prefab 优先 · 不代写脚本**

---

## 阶段进度

| 阶段 | 状态 | 验收 |
|:--:|:----:|------|
| 1 Login | ☐ 未开始 | 注册→登录→Loading 5s→Main · [`分步教程`](Stage1_Login/Docs/分步教程.md) |
| 2 Main | ☐ | 主界面 UI + 人物信息 |
| 3 Inventory | ☐ | 背包动态列表 + 关闭 |
| 4 Battle | ☐ | 移动动画 + 技能/怪物 |
