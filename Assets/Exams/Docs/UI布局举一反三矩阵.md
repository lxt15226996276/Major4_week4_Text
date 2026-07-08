# UI 布局举一反三矩阵（v7.16.1 · 全 Exam 共用 · Coach 开讲前必读）

> **宪法**：[`教学规范.md`](教学规范.md) **§11.25 · §11.27**  
> **踩坑**：[`踩坑记忆库_lixiaotong.md`](../../../Tests/阶段性主程成长路线/踩坑记忆库_lixiaotong.md) **U1～U7 · P2**  
> **用途**：UI 大步 **开讲前审计** · 分步讲义 **Layout 改造列** · **禁止等学员 Play 测出才补**

---

## 核心纪律

1. **少写死坐标** — 增删控件靠 **Layout Group + Layout Element + CSF**。  
2. **Prefab 复用** — Unpack 后 **先改 Layout**，再差量改字段；**禁止** Pos Y / 手拉 Image 当方案。  
3. **举一反三** — 下表 **一行一方案**；换控件类型 **换列**，不换思想。  
4. **主动挖掘** — Coach **§11.27 六步** · 体检表必含 **Layout 改造** 列。

---

## 矩阵（禁止手调 Pos/Size 凑位）

| 你要做的事 | 控件 | 标准方案 | 踩坑 |
|------------|------|----------|:----:|
| 横排增删 **Button** | Button | **HLG + CSF + LE** · Spacing **24** · Pivot **0.5** · Force Expand **关** | U1/U2 |
| 纵排增删 **InputField** | InputField | **VLG 七步 + CSF + LE** · `LoginFormColumn` · **Reset 子 Anchor** · Sibling **Account→Password→Name→Btn** | U3/U7 |
| 钮内/Item 内 **图标** | Image | **Aspect Ratio Fitter** · Fit **In Parent** · **Preserve Aspect 开** · **LE** 64×64 等 | U4 |
| **Panel 底图** 随 Panel 拉大 | Image | Anchor **Stretch** · Image Type **Sliced (9-slice)** | U4 |
| **TipText / Label** 字数不固定 | Text | 父 **VLG/HLG** · **CSF Preferred** · Overflow **Wrap** | U5 |
| **N 个服务器 / 背包格** | Item Prefab | **Grid Layout Group** 或 **Scroll View → Content(VLG)** · Instantiate 到 Content | U6 |
| **血条 Fill** | Slider | **只改 value** · Fill Stretch · §11.20 | H1 |

---

## Prefab 体检 · Layout 改造列（示例）

| Prefab 现状 | Layout 改造 |
|-------------|-------------|
| Input `AnchoredPosition Y=120/-35` | → **LoginFormColumn VLG 七步 + LE 900×80 + Reset 子 Anchor** |
| VLG 有但 **Pos X≈450 / Top-Left Anchor** | → **U7**：CSF · **Middle Center** · 子 Anchor Reset · **禁止 100×100 列盒** |
| Hierarchy **Account→Name→Password** | → **Account→Password→Name→BtnLogin** |
| Btn 行各写 Pos X | → **AttackButtonRow + HLG + CSF** |
| Icon 无 ARF、手设 100×50 | → **LE 64×64 + ARF Fit In Parent + Preserve Aspect** |
| LoginPanel 底图固定 1300×900 | → **Anchor Stretch + Image Sliced** |
| TipText 固定 Width 200 截断 | → **CSF Vertical Preferred + 父 VLG** |
| 3 服 Btn 手摆 | → **ServerButtonRoot VLG/Grid + Instantiate** |

---

## Coach 开讲前六步（§11.27）

1. Glob `Assets/Exams/**/Prefabs`  
2. Grep 绝对坐标风险  
3. 本步矩阵 **逐行勾选**  
4. 讲义写 **Layout 改造**（非 Pos 微调）  
5. 读踩坑库 **U1～U7 · P2**  
6. 过 **§11.26 三列表 + 本节** → 不合格 **不发 Chat**

---

## 变更日志

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.1 | 2026-06-24 | **U7** VLG 半套 · Reset 子 Anchor · Sibling 顺序 · v7.16.1 |
| v1.0 | 2026-06-24 | v7.16.0 · U4 Image · U5 Text · U6 Grid · P2 主动审计 |
