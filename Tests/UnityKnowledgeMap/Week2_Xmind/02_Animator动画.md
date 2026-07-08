# Unity Animator 动画系统详解

> 参照：[Unity 官方 Manual - Mecanim Animation System](https://docs.unity3d.com/Manual/AnimationOverview.html) · [Animator Controller](https://docs.unity3d.com/Manual/AnimatorControllers.html) · [Animator API](https://docs.unity3d.com/ScriptReference/Animator.html) · [Blend Tree](https://docs.unity3d.com/Manual/class-BlendTree.html) · [Animation Layers](https://docs.unity3d.com/Manual/AnimationLayers.html)  
> 关联文档：[01_Animation动画深入.md](./01_Animation动画深入.md)（Animation Clip 与曲线） · [03_状态机（有限状态机）.md](./03_状态机（有限状态机）.md)（FSM 设计模式）  
> 学习路径：**零基础 → 入门 → 进阶**，每阶段采用 **总—分—总** 结构。  
> 讲解维度：**定义 → 本质 → 特点 → 适用场景 → 原理 → API → 步骤 → 案例 → 避坑**（进阶含 Blend Tree / Layer / Avatar Mask / IK）。  
> 案例讲解：遵循 **案例代码讲解模板**（功能 → 代码 → 语法拆解 → 逐行详解 → 操作提示）。  
> API 讲解：入门/进阶 API 章节均采用 **逐词读懂** 格式：类型 → 参数 → 整行人话。

---

## 【全文总述】

**Animator** 是 Unity **Mecanim** 动画系统的核心组件，负责按 **Animator Controller（状态机资产）** 中的规则播放 **Animation Clip**，并通过 **Parameters（参数）** 驱动状态切换。  
典型链路：**FBX 导入 → Rig 配置 → 提取 Animation Clip → 制作 Animator Controller → 挂 Animator 组件 → 脚本 SetFloat/SetTrigger**。  
本文从 Animator 组件、Controller 状态机、参数系统、Blend Tree、Layer、IK 到性能优化，全面深入讲解。

### 思维导图总览

```
Unity Animator 动画系统（Mecanim）
│
├── Animator 组件（UnityEngine — 挂在 GameObject 上的组件）
│   │
│   ├── 【知识维度】（讲师框架 — 完整版）
│   │   │
│   │   ├── 定义：Mecanim 动画系统的运行时组件，执行 Animator Controller 状态机
│   │   │   └── 官方描述：Interface to control the Mecanim animation system
│   │   │       挂载在 GameObject 上，指定 Controller（+ Avatar for Humanoid）
│   │   │
│   │   ├── 本质：状态机逻辑 + 动画曲线采样 + 骨骼/属性写入 的统一调度器
│   │   │   ├── 数据来源：Animator Controller 资产（States + Transitions + Parameters）
│   │   │   ├── 每帧工作：计算当前状态/混合权重 → 采样 Animation Clip 曲线 → 写入骨骼/属性
│   │   │   └── 脚本接口：通过 Parameters 间接控制，不直接切换状态（推荐做法）
│   │   │
│   │   ├── 官方定位：角色动画的标准解决方案
│   │   │   ├── 设计用途：人形/Generic 角色 locomotion、战斗连招、过场动画
│   │   │   └── 与 Legacy Animation 区别：状态机、混合、层级、Humanoid 复用
│   │   │
│   │   ├── 特点
│   │   │   ├── 优势：可视化状态机、参数驱动、Humanoid 动画复用、Blend Tree 平滑混合、Layer 分层
│   │   │   └── 局限：Animator 组件有 CPU 开销、Rebind 成本高、UI 动画不如 DOTween 轻量
│   │   │
│   │   ├── 适用场景
│   │   │   ├── ✅ 适用：人形角色动作系统、复杂连招、多动画混合、上半身/下半身分层
│   │   │   └── ❌ 不适用：简单 UI 动画（DOTween 更轻）、单个物体旋转（Legacy 足够）
│   │   │
│   │   ├── 核心原理：状态机 + 混合树 + 曲线采样
│   │   │   ├── 状态机：当前 State + Transition 条件 → 决定下一帧在哪个状态
│   │   │   ├── 混合：Blend Tree 按参数混合多段 Clip；Transition 内交叉淡入
│   │   │   ├── 采样：当前帧各 Clip 混合后的最终值 → 写入骨骼 Transform
│   │   │   └── Layer：多层状态机叠加，Avatar Mask 控制哪些骨骼参与
│   │   │
│   │   ├── 核心属性（Animator 组件）
│   │   │   ├── controller：Animator Controller 资产引用
│   │   │   ├── avatar：Humanoid 用的 Avatar（Generic 可空）
│   │   │   ├── applyRootMotion：是否应用根运动位移
│   │   │   ├── speed：全局播放倍速
│   │   │   ├── cullingMode：离屏时是否更新动画
│   │   │   └── updateMode：Normal / Animate Physics / Unscaled Time
│   │   │
│   │   ├── 核心 API（脚本控制）
│   │   │   ├── 参数写入：SetFloat / SetBool / SetInteger / SetTrigger
│   │   │   ├── 参数读取：GetFloat / GetBool / GetInteger
│   │   │   ├── Trigger 复位：ResetTrigger（防止连续触发失效）
│   │   │   ├── 状态查询：GetCurrentAnimatorStateInfo(layerIndex)
│   │   │   ├── 过渡查询：IsInTransition(layerIndex)
│   │   │   ├── 直接播放：Play(stateName) / CrossFade(stateName, fadeDuration)
│   │   │   ├── Layer 控制：SetLayerWeight(layerIndex, weight)
│   │   │   ├── 性能：Animator.StringToHash(name) 预计算哈希
│   │   │   └── 根运动：deltaPosition / deltaRotation / OnAnimatorMove
│   │   │
│   │   ├── Animator Controller 核心概念
│   │   │   ├── State：状态，绑定一个或多个 Animation Clip（或 Blend Tree）
│   │   │   ├── Transition：过渡，条件满足时从一个 State 切到另一个
│   │   │   ├── Parameters：参数，Float/Bool/Int/Trigger 四种类型
│   │   │   ├── Any State：特殊状态，表示「从任意状态」都能触发的过渡
│   │   │   ├── Entry / Exit：状态机入口/出口
│   │   │   ├── Blend Tree：混合树，一个状态内按参数混合多段 Clip
│   │   │   └── Layer：层，多层状态机叠加，每层有独立权重
│   │   │
│   │   ├── Transition 详细配置
│   │   │   ├── Has Exit Time：是否等当前动画播到一定进度才允许过渡
│   │   │   ├── Fixed Duration：过渡时间是秒数还是百分比
│   │   │   ├── Transition Duration (s)：过渡时长，越大越平滑
│   │   │   ├── Transition Offset：目标状态从多少进度开始
│   │   │   ├── Interruption Source：哪些来源可以中断当前过渡
│   │   │   └── Conditions：条件列表，全部满足才触发过渡
│   │   │
│   │   ├── 标准使用步骤（六步）
│   │   │   ├── 步骤1 导入 FBX，Rig 选 Humanoid 或 Generic，Apply
│   │   │   ├── 步骤2 Animation 选项卡勾选需要的 Clip，设置 Loop，Apply
│   │   │   ├── 步骤3 创建 Animator Controller（右键 → Create → Animator Controller）
│   │   │   ├── 步骤4 双击打开 Controller：拖 Clip 建 State，Add Parameters，连 Transition
│   │   │   ├── 步骤5 模型挂 Animator 组件，指定 Controller（Humanoid 还要 Avatar）
│   │   │   └── 步骤6 脚本 Awake 取 Animator，Update 里 SetFloat/SetTrigger
│   │   │
│   │   ├── 生命周期与调用时机
│   │   │   ├── Awake/Start：GetComponent<Animator>()，缓存 StringToHash
│   │   │   ├── Update：根据 Input/角色逻辑 Set 参数（推荐做法）
│   │   │   ├── FixedUpdate：animatePhysics 模式下与物理同步
│   │   │   ├── OnAnimatorMove：自定义 Root Motion 处理
│   │   │   ├── OnAnimatorIK：反向运动学（IK）回调
│   │   │   └── OnStateEnter/Exit/Update：State Machine Behaviour 回调
│   │   │
│   │   └── 选型、封装、避坑
│   │       ├── 选型：角色动画用 Animator；UI 用 DOTween；简单物体用 Legacy
│   │       ├── 封装：AnimParams 哈希常量 + CharacterAnim 组件
│   │       └── 避坑：参数名拼写、Trigger 不复位、Has Exit Time 坑、Rebind 开销
│   │
│   ├── 第一阶段：零基础（建立认知 + 读懂代码）
│   │   ├── 理解 Animator / Controller / State / Clip 四者关系
│   │   ├── 逐词读懂：animator.SetFloat("Speed", speed)
│   │   └── 认识 Animator 窗口：Layers / Parameters / 状态机画布
│   │
│   ├── 第二阶段：入门（Controller 制作 + API + 案例）
│   │   ├── 四类 Parameters、Transition 配置、Any State
│   │   ├── Animator 常用 API 详解
│   │   └── 实战案例：走跑切换 / 跳跃 Trigger / 攻击连招状态
│   │
│   └── 第三阶段：进阶（Blend Tree / Layer / IK / 性能）
│       ├── Blend Tree 1D/2D 混合 locomotion
│       ├── Animation Layer + Avatar Mask 分层（上半身射击）
│       ├── IK 反向运动学（OnAnimatorIK）
│       ├── State Machine Behaviour 状态行为
│       └── 性能优化：StringToHash / 精简曲线 / Culling / Rebind 避坑
│
└── Humanoid Avatar（人形映射 — Humanoid 专用）
    │
    ├── 定义：将模型骨骼映射到 Unity 标准人形骨架的资产
    ├── 作用：Retarget 动画复用（同一 Clip 可套到不同人形模型）
    ├── 配置：FBX → Rig → Humanoid → Configure → 检查绿色勾 → Apply
    └── 代价：CPU 比 Generic 高约 15~20%
```

| 学习阶段 | 学习目标 |
|----------|----------|
| **零基础** | 说清 Animator、Controller、State、Clip 关系；读懂 `SetFloat` |
| **入门** | 会做 Controller、设 Parameters、连 Transition；完成 3 个案例 |
| **进阶** | 会 Blend Tree、Layer 分层、IK；懂性能优化与封装 |

### 讲师知识框架速览（全文脉络）

| 维度 | 零基础讲 | 入门讲 | 进阶讲 |
|------|----------|--------|--------|
| 定义 | ✅ | 回顾 | 回顾 |
| 本质 | ✅ 状态机驱动 | — | Layer + IK |
| 特点 | ✅ | — | 性能/开销 |
| 适用场景 | ✅ | — | 选型（Animator vs DOTween） |
| 核心原理 | 四者关系 | ✅ Transition 工作流程 | Blend Tree / Layer 混合 |
| 核心 API | 读懂 SetFloat | ✅ 四类参数 + 状态查询 | StringToHash / Layer / IK |
| 使用步骤 | Animator 窗口 | ✅ 六步流程 | 工程化封装 |
| 调用时机 | — | ✅ Update | OnAnimatorIK / StateMachineBehaviour |
| 避坑 | — | 初步 | ✅ Rebind / Trigger / 性能 |

---

# 第一阶段：零基础篇

## 【阶段总述】

零基础阶段建立**正确认知**：Animator 是什么、Animator Controller 是什么、State 和 Clip 怎么关联。  
同时学会**读懂** `animator.SetFloat("Speed", speed)` 的含义，并认识 Animator 窗口布局。

---

## 一、定义 — Animator 是什么？

| 项目 | 说明 |
|------|------|
| **类型** | `UnityEngine.Animator`，**组件**（挂在 GameObject 上） |
| **作用** | 运行时执行 Animator Controller，驱动动画播放 |
| **官方定义** | Interface to control the Mecanim animation system |
| **一句话** | 动画播放器——按状态机规则播动画，根据参数自动切换 |

```
Animator 组件（运行时）
    ├── 引用：Animator Controller 资产（状态机逻辑）
    ├── 引用：Avatar（Humanoid 才需要）
    ├── 输入：脚本 SetFloat / SetTrigger 等参数
    └── 输出：骨骼 Transform / 属性每帧更新
```

---

## 二、四大核心概念关系

### 2.1 类比理解

| 概念 | 类比 | 说明 |
|------|------|------|
| **Animation Clip** | 录像带 | 一段具体的动作（走路、跳跃、挥拳） |
| **State（状态）** | 播放器插槽 | 一个插槽放一盘录像带（或一个混合树） |
| **Animator Controller** | 播放列表 + 切换规则 | 有哪些插槽、什么时候切到哪个插槽 |
| **Animator 组件** | 播放机器 | 真正执行播放逻辑的硬件 |

### 2.2 数据流向

```
脚本 Set 参数 → Animator Controller 判断 Transition → 切到新 State → 播放对应 Clip
                                                                         ↓
                                                               采样曲线 → 写入骨骼/属性
```

**本质理解**：脚本不直接「播哪个动画」，而是「告诉状态机当前是什么情况」（速度多少、是否着地、要不要跳），状态机自己根据规则决定播什么。  
这叫**参数驱动**——把「决定播什么」的逻辑放在 Controller 里（设计师可调），代码只管输入状态。

---

## 三、Animator 窗口三件套

打开 **Window → Animation → Animator** 看到：

| 区域 | 作用 |
|------|------|
| **左上角 Layers** | 动画层（Base Layer 是最底层，上层叠加） |
| **左上角 Parameters** | 参数列表（Float/Bool/Int/Trigger） |
| **中间大画布** | 状态机图：State 方块，Transition 箭头 |

状态机画布中：
- **Entry**：入口箭头，游戏开始时从这里进入默认状态
- **橙色方块**：当前默认状态（Default State）
- **Any State**：特殊状态，表示「任何状态」都能跳出去
- **Exit**：退出（子状态机用得多）

---

## 四、Rig 类型与 Avatar

| Rig 类型 | 是否需要 Avatar | 动画可复用 | 典型用途 |
|----------|----------------|-----------|----------|
| **Humanoid** | ✅ 需要 | ✅ 可跨模型 Retarget | 人形角色（人、类人生物） |
| **Generic** | ❌ 不需要 | ❌ 与模型绑定 | 怪物、机械、非人形 |
| **Legacy** | ❌ 不需要 | ❌ | 旧系统，新项目不用 |
| **None** | — | — | 无骨骼纯网格 |

**怎么选**：
- 两个胳膊两条腿的人形角色 → **Humanoid**（动画库可以复用，划算）
- 怪物、四足、机械 → **Generic**（结构特殊，复用不了）
- 性能极敏感的同屏大量角色 → 评估后可选 Generic（CPU 低一些）

---

## 五、核心一课：如何读懂 SetFloat

```csharp
animator.SetFloat("Speed", speed);
```

| 部分 | 含义 |
|------|------|
| `animator` | Animator 组件引用变量 |
| `.SetFloat` | 设置 Float 类型参数的方法 |
| `"Speed"` | 参数名，必须与 Controller 的 Parameters 窗口**完全一致** |
| `speed` | 要写入的浮点值 |

**整行人话**：告诉状态机「当前速度是 speed」，状态机会根据你设的规则（比如 Speed > 0.1 就从 Idle 切到 Walk）自动切换动画。

```csharp
animator.SetTrigger("Jump");
```

| 部分 | 含义 |
|------|------|
| `.SetTrigger` | 设置 Trigger 类型参数：发一个脉冲信号 |
| `"Jump"` | 参数名 |

**整行人话**：按一下「跳跃按钮」，状态机收到脉冲，播一次 Jump 动画，播完自动回来。

> **为什么不直接 Play("Jump")？**  
> 因为状态机会处理过渡、混合、打断等复杂逻辑；直接 Play 会跳过硬切，不自然。推荐用 **参数驱动**。

---

## 【零基础阶段小结】

| 维度 | 要点 |
|------|------|
| **定义** | Animator=组件；Controller=状态机资产；State=状态；Clip=动画片段 |
| **本质** | 参数驱动状态切换，状态决定播哪段 Clip |
| **Rig** | Humanoid（可复用） / Generic（不可复用） |
| **读懂** | `SetFloat("Speed", speed)` = 告诉状态机当前速度 |

**阶段检验**：能画出 Clip → State → Controller → Animator 四层关系；能解释「什么叫参数驱动」。

---

# 第二阶段：入门篇

## 【阶段总述】

入门阶段掌握 **Animator Controller 制作**、**四类 Parameters**、**Transition 配置**、**Animator 常用 API**，并完成 3 个实战案例。  
重点：**参数驱动**；**Transition 条件与 Has Exit Time**；**Trigger 脉冲机制**。

---

## 一、Parameters 四类参数详解

> 以下采用 **逐词读懂** 格式。

### API 全景

```
Animator（组件）
├── 写参数：SetFloat / SetBool / SetInteger / SetTrigger / ResetTrigger
├── 读参数：GetFloat / GetBool / GetInteger
├── 查状态：GetCurrentAnimatorStateInfo / IsInTransition
└── 层控制：SetLayerWeight
```

---

### 1.1 `animator.SetFloat` — 逐词读懂

```csharp
animator.SetFloat("Speed", speed);
```

| 部分 | 含义 |
|------|------|
| `animator` | 变量：Animator 组件引用 |
| `.SetFloat` | 方法名：设置 **Float** 类型参数 |
| `"Speed"` | 参数1 name：字符串，必须与 Parameters 窗口名字**完全一致**（大小写敏感） |
| `speed` | 参数2 value：float 值 |

**整行人话**：把 Controller 里叫 "Speed" 的那个浮点数参数改成 speed。

**典型用途**：速度、方向、Blend Tree 混合参数。

---

### 1.2 `animator.SetBool` — 逐词读懂

```csharp
animator.SetBool("IsGrounded", true);
```

| 部分 | 含义 |
|------|------|
| `.SetBool` | 设置 **Bool** 类型参数（true/false 持续状态） |
| `"IsGrounded"` | 参数名 |
| `true` | 值：着地为 true，空中为 false |

**整行人话**：告诉状态机「现在脚沾地了」或「现在在空中」。

**典型用途**：是否着地、是否蹲下、是否举盾——持续的开关状态。

---

### 1.3 `animator.SetInteger` — 逐词读懂

```csharp
animator.SetInteger("WeaponType", 2);
```

| 部分 | 含义 |
|------|------|
| `.SetInteger` | 设置 **Int** 类型参数 |
| `"WeaponType"` | 参数名 |
| `2` | 整数值：0=赤手，1=剑，2=弓 |

**整行人话**：用整数区分多种离散状态（武器类型、攻击段数）。

**典型用途**：武器切换、Combo 第几段、姿势编号。

---

### 1.4 `animator.SetTrigger` / `ResetTrigger` — 逐词读懂

```csharp
animator.SetTrigger("Jump");
animator.ResetTrigger("Jump");
```

| 部分 | 含义 |
|------|------|
| `.SetTrigger` | 设置 **Trigger** 类型参数：发一个**脉冲** |
| 官方行为 | 置为 true 后自动弹回 false；Transition 消费一次 |
| `.ResetTrigger` | 手动清除，防止「连按两次导致第二次没反应」 |

**整行人话**：按一下按钮的效果——不是一直按着，而是「哒」一声触发一次。

**典型用途**：跳跃、攻击、受击、翻滚——一次性动作。

> **Trigger 坑**：连续快速 SetTrigger，如果前一个还没被消费，第二个会覆盖。最佳实践是 SetTrigger 之前先 ResetTrigger。

---

### 四类参数对比表

| 类型 | API | 特性 | 典型场景 |
|------|-----|------|----------|
| **Float** | SetFloat / GetFloat | 连续值，可小数 | 速度、方向、Blend Tree |
| **Bool** | SetBool / GetBool | 持续 true/false | 是否着地、是否蹲下 |
| **Int** | SetInteger / GetInteger | 离散整数 | 武器类型、Combo 段数 |
| **Trigger** | SetTrigger / ResetTrigger | 脉冲，自动复位 | 跳跃、攻击、受击 |

---

## 二、Transition 过渡配置详解

### 2.1 过渡的核心设置

选中箭头（Transition）后 Inspector 里的关键项：

| 设置项 | 含义 | 默认 | 注意 |
|--------|------|------|------|
| **Has Exit Time** | 是否需要等当前动画播到 Exit Time 才能切 | 勾选 | 想立刻切（如跳跃）要**取消勾选** |
| **Exit Time** | 多少进度（0~1）后允许过渡 | 0.75 | Has Exit Time 勾选时才有效 |
| **Fixed Duration** | 过渡时长是秒数还是归一化时间 | 勾选（秒） | — |
| **Transition Duration** | 过渡时间（秒或百分比） | 0.25 | 越大越平滑，太小会硬切 |
| **Transition Offset** | 目标状态从什么进度开始（0~1） | 0 | 同步两段动画相位时用 |
| **Interruption Source** | 谁可以打断当前过渡 | None | 连招打断常用 |
| **Conditions** | 触发条件列表（全部满足才触发） | 空 | 参数变化满足条件时切 |

### 2.2 Has Exit Time 两大模式

| 模式 | Has Exit Time | 行为 | 适用 |
|------|---------------|------|------|
| **播完再切** | ✅ 勾选 | 当前动画播到 Exit Time 才开始过渡 | 攻击连招（必须挥完刀） |
| **立刻切** | ❌ 取消 | 参数一满足立刻过渡 | 跳跃、翻滚（反应要快） |

> **新手常见坑**：跳跃切不出来——忘了取消 Has Exit Time，结果一直等 Idle 播完才能跳。

### 2.3 Conditions 条件运算

多个条件之间是 **AND 关系**（全部满足才触发）：

```
条件1：Speed > 0.1
条件2：IsGrounded == true
→ 速度 > 0.1 AND 着地 才切到 Walk
```

如果要 OR（满足其中一个就行），只能多加几条 Transition 箭头。

---

## 三、Any State — 从任意状态跳转

**Any State** 是一个特殊状态，表示「从任何状态（包括它自己）都能跳转到目标状态」。

| 用法 | 示例 | 注意 |
|------|------|------|
| 全局可触发 | 受击动画（无论在走路还是跑步都能被打） | 可能打断自己，加 Can Transition To Self = false |
| 全局 Jump | 从任何着地状态都能跳 | 条件要加 IsGrounded，不然空中也能跳 |

> **Any State 坑**：如果目标状态也在 Any State 的源里，且条件一直满足，会无限循环跳转。记得在目标状态把条件设为不满足，或设置 Can Transition To Self = false。

---

## 四、标准六步流程

```
步骤1  导入 FBX → Rig 选 Humanoid/Generic → Apply
步骤2  Animation 选项卡 → 勾选需要的 Clip → 设 Loop Time → Apply
步骤3  右键 Create → Animator Controller
步骤4  双击 Controller：拖 Clip 建 State → Add Parameters → 连 Transition + Conditions
步骤5  角色挂 Animator → 指定 Controller（Humanoid 指定 Avatar）
步骤6  脚本 Awake 取 Animator，Update 里 SetFloat/SetTrigger
```

---

## 五、入门三个案例

### 案例代码讲解模板

每个案例统一按以下结构组织（下文所有案例均遵循此模板）：

| 顺序 | 板块 | 内容 |
|:----:|------|------|
| 1 | **功能** | 案例实现什么业务 |
| 2 | **完整代码** | 带行内注释的完整脚本 |
| 3 | **语法拆解** | 对案例中较生僻的语法，逐个说明 |
| 4 | **逐行详解** | 表格：每行代码的含义 |
| 5 | **操作提示** | Unity 绑定、调用方式等 |

---

### 案例 1：速度驱动 Idle / Walk / Run 切换

**功能**：WASD 输入，根据速度大小在 Idle、Walk、Run 之间切换。

**Animator Controller 预设**：

| State | 进入条件 |
|-------|----------|
| Idle（默认） | Speed < 0.1 |
| Walk | Speed >= 0.1 且 Speed < 0.6 |
| Run | Speed >= 0.6 |

```csharp
using UnityEngine;                                      // 引入 Unity 核心库

public class PlayerLocomotionAnim : MonoBehaviour        // 角色移动动画驱动
{
    Animator anim;                                      // Animator 组件缓存
    static readonly int SpeedHash = Animator.StringToHash("Speed");  // 预哈希，省性能

    void Awake()
    {
        anim = GetComponent<Animator>();               // 获取同物体上的 Animator
    }

    void Update()
    {
        float h = Input.GetAxisRaw("Horizontal");     // 水平输入 -1~1
        float v = Input.GetAxisRaw("Vertical");       // 垂直输入 -1~1
        Vector2 input = new Vector2(h, v);
        float speed = Mathf.Clamp01(input.magnitude); // 速度 0~1（Clamp01 限制不超过 1）
        anim.SetFloat(SpeedHash, speed);               // 用哈希值设置参数
    }
}
```

#### 语法拆解

##### `Animator.StringToHash("Speed")` 是什么？

```csharp
static readonly int SpeedHash = Animator.StringToHash("Speed");
```

| 部分 | 含义 |
|------|------|
| `StringToHash` | Animator 静态方法：把参数字符串转成 int 哈希值 |
| `static readonly` | 类级别只算一次，所有实例共享 |
| 为什么用哈希 | 字符串比较比 int 慢，用哈希减少 CPU 开销和 GC |

**整行人话**：用数字代替字符串跟 Animator 打交道，更快。

**说明**：最佳实践——所有参数名、状态名都预计算哈希，存在静态只读字段里。

---

##### `Mathf.Clamp01(input.magnitude)` 是什么？

```csharp
float speed = Mathf.Clamp01(input.magnitude);
```

| 部分 | 含义 |
|------|------|
| `input.magnitude` | 输入向量长度（0~约 1.414，因为斜着走 h 和 v 都是 1） |
| `Mathf.Clamp01` | 限制在 0~1 之间，超过 1 的截断成 1 |

**整行人话**：把斜着走的 1.414 压成 1，确保速度最大值统一。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 3 | `public class PlayerLocomotionAnim : MonoBehaviour` | 可挂载脚本类 |
| 5 | `Animator anim` | Animator 缓存变量 |
| 6 | `SpeedHash = StringToHash("Speed")` | 预计算参数哈希 |
| 8~11 | `Awake()` | 初始化时获取 Animator 组件 |
| 13~20 | `Update()` | 每帧读输入，算速度，设参数 |

#### 操作提示

1. 创建 Animator Controller，Parameters 加 **Speed（Float）**  
2. 拖入 Idle、Walk、Run 三个 Clip 建三个 State  
3. Idle 设为 Default（右键 → Set as Layer Default State）  
4. 连六条 Transition（Idle↔Walk、Walk↔Run、Idle↔Run），每条设对应的 Speed 条件  
5. 所有 Transition **取消 Has Exit Time**，Transition Duration 设 0.15s  
6. 脚本挂角色，角色挂 Animator 并指定 Controller → Play 测试

---

### 案例 2：Trigger 跳跃 + Bool 着地

**功能**：空格跳跃（Trigger），着地状态用 Bool 同步给 Animator。

**Controller 预设**：
- Any State → Jump（Condition: Jump Trigger，Has Exit Time = false）
- Jump → Idle（Conditions: Exit Time + IsGrounded == true）

```csharp
using UnityEngine;                                      // 引入 Unity 核心库

public class PlayerJumpAnim : MonoBehaviour
{
    Animator anim;
    static readonly int JumpHash = Animator.StringToHash("Jump");
    static readonly int IsGroundedHash = Animator.StringToHash("IsGrounded");

    bool isGrounded = true;                             // 是否着地
    public float jumpHeight = 2f;
    public float gravity = -9.81f;
    Vector3 velocity;

    void Awake()
    {
        anim = GetComponent<Animator>();
    }

    void Update()
    {
        anim.SetBool(IsGroundedHash, isGrounded);      // 每帧同步着地状态

        if (Input.GetKeyDown(KeyCode.Space) && isGrounded)
        {
            anim.ResetTrigger(JumpHash);               // 先复位，防止连续按失效
            anim.SetTrigger(JumpHash);                 // 触发跳跃
            isGrounded = false;                         // 标记空中
            velocity.y = Mathf.Sqrt(jumpHeight * -2f * gravity);  // 起跳速度公式
        }

        // 简易垂直运动
        velocity.y += gravity * Time.deltaTime;
        transform.position += velocity * Time.deltaTime;

        // 落地检测（简化版：低于 y=0 算落地）
        if (transform.position.y <= 0f)
        {
            transform.position = new Vector3(transform.position.x, 0f, transform.position.z);
            velocity.y = 0f;
            isGrounded = true;
        }
    }
}
```

#### 语法拆解

##### `anim.ResetTrigger(JumpHash)` 为什么要写？

```csharp
anim.ResetTrigger(JumpHash);
anim.SetTrigger(JumpHash);
```

| 问题 | 原因 |
|------|------|
| 快速连按跳跃没反应 | 前一个 Trigger 还没被 Transition 消费，第二个 SetTrigger 不会叠加 |
| ResetTrigger | 先清空之前可能残留的 Trigger 状态，再重新设，确保每次都生效 |

**整行人话**：先把按钮弹起来再按下去，保证每次都能触底反弹。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 5~6 | 静态哈希字段 | Jump 和 IsGrounded 参数的预哈希 |
| 8 | `isGrounded = true` | 默认着地 |
| 15~18 | `Awake` | 获取 Animator |
| 20~43 | `Update` | 每帧同步着地状态、检测跳跃、处理物理 |
| 22 | `SetBool(IsGroundedHash, isGrounded)` | 同步着地 Bool |
| 24 | `GetKeyDown(Space) && isGrounded` | 空格按下且着地才跳 |
| 26 | `ResetTrigger` | 先复位 Trigger |
| 27 | `SetTrigger` | 触发跳跃动画 |
| 31 | `Mathf.Sqrt(...)` | 由跳跃高度算初速度（物理公式） |

#### 操作提示

1. Controller 加 **Jump（Trigger）** 和 **IsGrounded（Bool）** 参数  
2. 建 Jump State，Clip 是跳跃动画（不循环）  
3. Any State → Jump：条件 Jump Trigger，Has Exit Time = false  
4. Jump → Idle：Has Exit Time 勾选，Exit Time = 0.9，加条件 IsGrounded == true  
5. 脚本挂角色测试

---

### 案例 3：攻击连招（Int 段数 + 播完判定）

**功能**：按 J 攻击，第一段播完前再按 J 接第二段，实现连招。

```csharp
using UnityEngine;                                      // 引入 Unity 核心库

public class PlayerComboAnim : MonoBehaviour
{
    Animator anim;
    static readonly int AttackHash = Animator.StringToHash("Attack");
    static readonly int ComboStepHash = Animator.StringToHash("ComboStep");
    static readonly int AttackStateHash = Animator.StringToHash("Base Layer.Attack1");

    int comboStep = 0;                                  // 当前连招段数 0=无，1=一段，2=二段
    bool canCombo = false;                              // 是否在可连招窗口

    void Awake()
    {
        anim = GetComponent<Animator>();
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.J))
        {
            if (comboStep == 0)                          // 第一次攻击
            {
                comboStep = 1;
                anim.SetInteger(ComboStepHash, comboStep);
                anim.SetTrigger(AttackHash);
            }
            else if (canCombo && comboStep < 3)         // 连招窗口内且未到上限
            {
                comboStep++;
                anim.SetInteger(ComboStepHash, comboStep);
                anim.SetTrigger(AttackHash);
            }
        }

        // 检测当前是否在攻击状态且到了可连招的进度
        AnimatorStateInfo info = anim.GetCurrentAnimatorStateInfo(0);
        if (info.shortNameHash == AttackStateHash)
        {
            // 动画播到 70%~90% 之间是连招窗口
            canCombo = info.normalizedTime % 1f >= 0.7f && info.normalizedTime % 1f <= 0.9f;
        }
        else
        {
            canCombo = false;
        }

        // 播完回到 Idle 时重置段数
        if (info.IsName("Idle") && comboStep > 0)
        {
            comboStep = 0;
            anim.SetInteger(ComboStepHash, 0);
        }
    }
}
```

#### 语法拆解

##### `anim.GetCurrentAnimatorStateInfo(0)` 是什么？

```csharp
AnimatorStateInfo info = anim.GetCurrentAnimatorStateInfo(0);
```

| 部分 | 含义 |
|------|------|
| `GetCurrentAnimatorStateInfo` | 获取指定层当前状态信息 |
| `0` | 层索引：Base Layer 是第 0 层 |
| 返回值 | `AnimatorStateInfo` 结构体 |

**常用属性**：

| 属性 | 含义 |
|------|------|
| `info.shortNameHash` | 状态名的哈希值（不含层名） |
| `info.normalizedTime` | 归一化时间：整数部分是循环次数，小数部分是进度 0~1 |
| `info.length` | 状态长度（秒） |
| `info.IsName("name")` | 当前状态名是否匹配 |

**整行人话**：查「现在在播哪个状态、播到百分之几」。

---

##### `info.normalizedTime % 1f` 是什么？

```csharp
float progress = info.normalizedTime % 1f;
```

| 部分 | 含义 |
|------|------|
| `%` | 取模（取余数） |
| `normalizedTime` | 1.3 表示播了 1 圈又 30% |
| `% 1f` | 取小数部分（0~1），即当前这一圈的进度 |

**整行人话**：不管循环了几次，只看当前这一遍播到哪了。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 5~7 | 哈希字段 | Attack、ComboStep、Attack1 状态名的预哈希 |
| 9~10 | comboStep / canCombo | 当前段数、是否在连招窗口 |
| 16~31 | 攻击输入逻辑 | 第一次起手 / 连招窗口内追加段数 |
| 34 | `GetCurrentAnimatorStateInfo(0)` | 获取第 0 层状态信息 |
| 35~41 | 连招窗口判断 | 攻击状态的 70%~90% 进度内可连 |
| 44~49 | 回到 Idle 重置 | 播完回到 Idle 时把段数清零 |

#### 操作提示

1. Controller 加 **Attack（Trigger）**、**ComboStep（Int）** 参数  
2. 建 Attack1、Attack2、Attack3 三个 State  
3. Attack1 → Attack2：条件 Attack Trigger + ComboStep == 2  
4. Attack2 → Attack3：条件 Attack Trigger + ComboStep == 3  
5. 每个攻击 → Idle：Has Exit Time 勾选  
6. 脚本挂角色测试连招手感

---

## 【入门阶段小结】

| 维度 | 要点 |
|------|------|
| **参数** | Float / Bool / Int / Trigger 四类 |
| **Transition** | Has Exit Time 两种模式、Conditions 全满足才切 |
| **API** | SetFloat / SetBool / SetTrigger / GetCurrentAnimatorStateInfo |
| **性能** | StringToHash 预计算，不用字符串 |
| **案例** | 走跑切换、跳跃 Trigger、攻击连招 |

---

# 第三阶段：进阶篇

## 【阶段总述】

进阶阶段：**Blend Tree 混合树**、**Animation Layer + Avatar Mask 分层动画**、**IK 反向运动学**、**State Machine Behaviour**、**性能优化**。

---

## 一、Blend Tree 混合树

### 1.1 什么是 Blend Tree？

**Blend Tree（混合树）** 是一种特殊的 State：不是绑定单个 Clip，而是按一个或多个参数值**混合多段 Animation Clip**，输出平滑的过渡动画。

| 对比 | 多个 State + Transition | 一个 Blend Tree |
|------|------------------------|----------------|
| 过渡 | 状态切换时有硬过渡感 | 连续平滑，无级变速 |
| 适用 | 差异大的动作（走 vs 跳） | 速度变化（Idle↔Walk↔Run） |
| 参数 | Transition 条件判断 | 连续 Float 参数直接混合 |

**一句话**：速度从 0 到 1 之间，Idle 和 Walk 和 Run 按比例混在一起，动作连续变化不突兀。

### 1.2 1D Blend Tree（最常用）

**一个参数控制，混合多段 Clip**：

```
Blend Tree 1D（Parameter: Speed）
    ├── 阈值 0.0 → Idle.anim
    ├── 阈值 0.5 → Walk.anim
    └── 阈值 1.0 → Run.anim

Speed = 0.25 → Idle 50% + Walk 50%
Speed = 0.75 → Walk 50% + Run 50%
```

**创建方式**：Controller 右键 → Create State → From New Blend Tree → 双击进入 Blend Tree 编辑器 → Add Motion Field 加 Clip → 设 Threshold。

### 1.3 2D Blend Tree（方向 + 速度）

**两个参数控制，比如 X 和 Y 方向**，适用于八方向移动。

| 类型 | 参数数 | 适用 |
|------|--------|------|
| **1D** | 1 个 Float | 速度（Idle/Walk/Run） |
| **2D Simple Directional** | 2 个 Float | 八方向移动 |
| **2D Freeform Directional** | 2 个 Float | 方向+速度，点位更自由 |
| **2D Freeform Cartesian** | 2 个 Float | 任意 X/Y 参数 |

### 1.4 为什么 Blend Tree 手感好？

- 速度慢慢增加时，动画从 Idle 渐变成 Walk，再渐变成 Run，**没有台阶感**
- Transition 是「要么 A 要么 B」，Blend Tree 是「A 和 B 按比例混合」
- locomotion（走跑跳）标配

---

## 二、Animation Layer + Avatar Mask 分层动画

### 2.1 什么是 Layer？

**Animation Layer（动画层）**：多层状态机**叠加**，每层有独立的状态机和权重。上层覆盖下层的骨骼。

典型案例：**Base Layer 全身走跑 + Upper Body Layer 上半身瞄准/射击**。

```
第 0 层 Base Layer（权重 1）：全身走路
        ↓ 叠加
第 1 层 Upper Body（权重 0~1）：上半身瞄准
        ↓ 输出
最终：下半身在走路，上半身在瞄准
```

### 2.2 Avatar Mask — 遮罩哪些骨骼

**Avatar Mask** 资产：指定「这一层只影响哪些骨骼」。  
比如 Upper Body Layer 的 Mask 只勾脊柱以上的骨骼，这样走路的腿不会被上半身层覆盖。

**创建方式**：右键 → Create → Avatar Mask →  Inspector 里点 Humanoid 人形图，红色=不参与，绿色=参与。

### 2.3 SetLayerWeight — 动态开关层

```csharp
anim.SetLayerWeight(1, 1f);  // 第 1 层权重设为 1（完全启用）
anim.SetLayerWeight(1, 0f);  // 第 1 层权重设为 0（完全关闭）
```

| 部分 | 含义 |
|------|------|
| `SetLayerWeight(layerIndex, weight)` | 设置指定层的权重 0~1 |
| 第 0 层 | Base Layer，一般权重恒为 1 |
| 第 1 层及以上 | 叠加层，权重可动态调 |

**整行人话**：举枪时把上半身层权重拉满，收枪时降到 0。

---

## 三、IK — 反向运动学

### 3.1 什么是 IK？

**IK（Inverse Kinematics，反向运动学）**：给定**末端目标位置**，自动算出中间骨骼怎么弯。  
比如「手要放到墙上这个点」，IK 自动算肩膀、手肘、手腕的角度。

| 对比 | 正向运动学（FK） | 反向运动学（IK） |
|------|-----------------|-----------------|
| 驱动方式 | 父骨骼带动子骨骼 | 末端目标反推父骨骼 |
| 典型用途 | 普通走跑跳动画 | 手抓物体、脚踩地面、瞄准 |
| 数据来源 | Animation Clip | 运行时计算 + 动画基础 |

### 3.2 OnAnimatorIK 回调

在 Animator 组件上勾选 **IK Pass**（Layer 设置里），然后写脚本实现 `OnAnimatorIK(int layerIndex)`：

```csharp
void OnAnimatorIK(int layerIndex)
{
    anim.SetIKPosition(AvatarIKGoal.LeftHand, target.position);
    anim.SetIKPositionWeight(AvatarIKGoal.LeftHand, 1f);
    anim.SetIKRotation(AvatarIKGoal.LeftHand, target.rotation);
    anim.SetIKRotationWeight(AvatarIKGoal.LeftHand, 1f);
}
```

| 方法 | 作用 |
|------|------|
| `SetIKPosition(goal, position)` | 设置 IK 目标位置 |
| `SetIKPositionWeight(goal, weight)` | 位置权重 0~1（0=完全用动画，1=完全用IK） |
| `SetIKRotation(goal, rotation)` | 设置 IK 目标旋转 |
| `SetIKRotationWeight(goal, weight)` | 旋转权重 |
| `AvatarIKGoal` | 枚举：LeftHand / RightHand / LeftFoot / RightFoot |

**典型用途**：
- 脚下地形不平，脚自动贴合地面（Foot IK）
- 角色右手抓枪，手始终对准枪柄
- 角色看某个物体，头和眼睛转过去（Look At IK）

---

## 四、State Machine Behaviour — 状态行为

**State Machine Behaviour**：给某个 State 挂一个脚本，在进入/退出/更新该状态时自动回调。

```csharp
public class AttackStateBehaviour : StateMachineBehaviour
{
    public override void OnStateEnter(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
    {
        // 进入攻击状态时：开启碰撞检测、播放攻击音效
    }

    public override void OnStateUpdate(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
    {
        // 状态持续中每帧
    }

    public override void OnStateExit(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
    {
        // 退出攻击状态时：关闭碰撞检测
    }
}
```

**为什么用？**  
把「某个状态该做什么」的逻辑封装在 State 上，而不是全写在 Update 里 if-else 判断当前状态。  
适合：攻击帧的伤害判定、某个状态的特效生成/销毁。

**添加方式**：选中 State → Inspector → Add Behaviour → 选自定义的 StateMachineBehaviour 脚本。

---

## 五、性能优化

| 优化项 | 做法 | 原因 |
|--------|------|------|
| **StringToHash** | 所有参数/状态名预计算哈希 | 减少字符串比较 GC |
| **Optimal 压缩** | Animation Import 设置 Compression = Optimal | 文件更小，采样更快 |
| **精简曲线** | 移除不用的属性曲线（如手指不用就不导入） | 减少每帧计算量 |
| **Culling Mode** | Animator 组件 Culling Mode = Cull Update Transforms | 离屏或被遮挡时减少更新 |
| **减少 Rebind** | 对象池复用时 Disable Animator 组件，不是 Disable GameObject | GameObject 禁用会触发 Rebind，开销大 |
| **统一 Rig 类型** | 项目全 Humanoid 或全 Generic，别混用 | 避免 Avatar 转换开销 |
| **Animator 数量** | 同屏角色数控制；远的降低质量 | 每个 Animator 都有 CPU 成本 |
| **Replace Animator** | 简单物体用 DOTween 或 Legacy Animation | UI、小道具没必要上 Animator |

> **Rebind 坑**：`gameObject.SetActive(false)` 再设回 true，Animator 会 Rebind 一次（重建内部状态），开销不小。对象池复用建议 `animator.enabled = false` 而不是整个 GO 禁用。

---

## 六、常见误区与最佳实践

| 误区 | 正确做法 |
|------|----------|
| 动画不动 | 检查 Animator 是否指定 Controller；模型 Rig 是否正确；Clip 是否提取 |
| SetFloat 无效 | 参数名**大小写**是否与 Controller 完全一致；Layer 是否对 |
| Trigger 没反应 | Has Exit Time 挡住了；或需要 ResetTrigger |
| 跳跃切不出来 | 取消 Transition 的 Has Exit Time |
| 动画一直 T-Pose | Avatar 没 Configure 好；SkinnedMeshRenderer 没挂 |
| 滑步 | 代码速度和动画速度不匹配；用 Root Motion 或调 speed |
| 连招连不上 | Transition 的 Interruption Source 设置 + 连招窗口判断 |
| 动画卡 | 太多 Animator；开 Optimal 压缩；精简骨骼曲线 |
| Trigger 偶发失效 | SetTrigger 前先 ResetTrigger |
| 频繁换 Controller 卡 | 避免运行时换 Controller；用 Layer 或 Blend Tree 替代 |

---

## 【进阶阶段小结】

| 维度 | 要点 |
|------|------|
| Blend Tree | 1D/2D，连续参数平滑混合多段 Clip |
| Layer + Avatar Mask | 多层叠加，Mask 控制骨骼范围 |
| IK | OnAnimatorIK + SetIKPosition，手/脚动态对齐目标 |
| StateMachineBehaviour | 状态 Enter/Exit/Update 回调 |
| 性能 | StringToHash、Optimal 压缩、Culling、减少 Rebind |
| 避坑 | 参数名拼写、Has Exit Time、Trigger 复位、Rebind |

---

# 【全文总结】

## 最重要的一行代码

```csharp
anim.SetFloat(SpeedHash, input.magnitude);
```

| 部分 | 含义 |
|------|------|
| `anim` | Animator 组件 |
| `SetFloat` | 设 Float 参数 |
| `SpeedHash` | 预计算的参数哈希 |
| `input.magnitude` | 速度值 |

## 三阶段对照

| 阶段 | 代表案例 |
|------|----------|
| 零基础 | 理解 Animator/Controller/State/Clip 关系 |
| 入门 | 走跑切换、跳跃 Trigger、攻击连招 |
| 进阶 | Blend Tree、Layer 分层、IK、性能优化 |

## 与系列文档关系

| 主题 | 文档 |
|------|------|
| Animation Clip 与曲线底层 | [01_Animation动画深入.md](./01_Animation动画深入.md) |
| 有限状态机设计模式 | [03_状态机（有限状态机）.md](./03_状态机（有限状态机）.md) |
| 模型导入与 Animator 基础 | 见 major3/04_Model_Animator.md |
| DOTween 补间动画 | 见 major3/05_DoTween.md |

## 官方文档索引

| 主题 | 链接 |
|------|------|
| Mecanim 概述 | https://docs.unity3d.com/Manual/AnimationOverview.html |
| Animator Controller | https://docs.unity3d.com/Manual/AnimatorControllers.html |
| Animator API | https://docs.unity3d.com/ScriptReference/Animator.html |
| Blend Tree | https://docs.unity3d.com/Manual/class-BlendTree.html |
| Animation Layers | https://docs.unity3d.com/Manual/AnimationLayers.html |
| Avatar Mask | https://docs.unity3d.com/Manual/class-AvatarMask.html |
| IK | https://docs.unity3d.com/Manual/InverseKinematics.html |

---

*文档版本：与 major3/01_PlayerPrefs.md ~ 05_DoTween.md 同系列模板。*
