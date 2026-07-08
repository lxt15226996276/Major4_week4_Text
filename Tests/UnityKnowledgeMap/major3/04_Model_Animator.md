# Unity 模型与 Animator 动画详解

> 参照：[Importing a model](https://docs.unity3d.com/Manual/ImportingModelFiles.html) · [Introduction to Mecanim](https://docs.unity3d.com/Manual/AnimationOverview.html) · [Animator API](https://docs.unity3d.com/ScriptReference/Animator.html) · [Animator.SetFloat](https://docs.unity3d.com/ScriptReference/Animator.SetFloat.html) · [Animator.SetTrigger](https://docs.unity3d.com/ScriptReference/Animator.SetTrigger.html)  
> 学习路径：**零基础 → 入门 → 进阶**，每阶段采用 **总—分—总** 结构。  
> 讲解维度：**定义 → 本质 → 特点 → 适用场景 → 原理 → API → 步骤 → 案例 → 避坑**（进阶含 Humanoid / Root Motion / Blend Tree）。  
> 案例讲解：遵循 **案例代码讲解模板**（功能 → 代码 → 语法拆解 → 逐行详解 → 操作提示）。  
> API 讲解：入门/进阶 API 章节均采用 **逐词读懂** 格式（与 [01_PlayerPrefs.md](./01_PlayerPrefs.md) 一致：类型 → 参数 → 整行人话）。

---

## 【全文总述】

**3D 模型**是角色、道具在场景中的网格与骨骼载体；**Animator** 是 Unity **Mecanim** 动画系统的核心组件，负责按 **Animator Controller** 状态机播放 **Animation Clip**，并通过 **参数（Float / Bool / Int / Trigger）** 驱动状态切换。  
典型链路：**FBX 导入 → Rig 配置 → 提取 Animation Clip → 制作 Animator Controller → 挂 Animator 组件 → 脚本 SetFloat / SetTrigger**。  
本文从模型导入到脚本控制动画，逐层展开。

### 思维导图总览

```
Unity 模型与 Animator 动画
│
├── 3D 模型导入（FBX / 网格 / 骨骼 — 动画的数据来源）
│   │
│   ├── 定义：包含 Mesh、骨骼 Rig、Animation Clip、材质贴图的三维资源
│   │   └── 官方：Model files can contain meshes, animation rigs and clips, materials, textures
│   │       Unity 主要支持 FBX 格式导入
│   │
│   ├── 本质：外部 DCC（Maya/Blender/3ds Max）制作 → 导出 FBX → Unity 解析为内部资产
│   │   ├── Model 选项卡：网格、法线、Blend Shape、缩放
│   │   ├── Rig 选项卡：None / Legacy / Humanoid / Generic
│   │   └── Animation 选项卡：提取 Clip、循环、压缩、Root Transform
│   │
│   ├── 组件关系
│   │   ├── MeshRenderer + MeshFilter：静态网格（无骨骼）
│   │   ├── SkinnedMeshRenderer：带骨骼变形的网格（角色常用）
│   │   └── Animator：驱动骨骼播放动画（挂在与模型同一层级）
│   │
│   └── Rig 类型选型
│       ├── Humanoid：人形 biped，可 Retarget 复用动画，需 Avatar 映射
│       ├── Generic：任意骨骼结构，动画与模型绑定，不可跨模型复用
│       └── Legacy：旧 Animation 组件体系，新项目不推荐
│
├── Mecanim 动画系统（Animation Clip + Animator Controller + Animator）
│   │
│   ├── 【知识维度】（讲师框架 — 完整版）
│   │   │
│   │   ├── 定义：Unity 基于状态机的现代动画系统（Mecanim）
│   │   │   ├── Animation Clip：一段动画录制（位置/旋转/属性随时间变化）
│   │   │   ├── Animator Controller：状态机资产，管理状态与过渡
│   │   │   └── Animator 组件：运行时执行 Controller，挂到 GameObject 上
│   │   │
│   │   ├── 本质：Clip 数据 + 状态机逻辑 + 组件每帧求值 → 写入 Transform/属性
│   │   │   ├── Controller 像「交通指挥」：当前在哪个 State、何时 Transition
│   │   │   ├── Parameters 是脚本与状态机的「接口」
│   │   │   └── Avatar（Humanoid）：骨骼映射到 Unity 统一人形格式
│   │   │
│   │   ├── 官方定位：Gameplay 角色动画的标准方案
│   │   │   ├── 设计用途：待机/走/跑/跳、攻击、Blend Tree 混合、Layer 叠加
│   │   │   └── 与旧 Animation 组件：Mecanim 可状态机+混合；Animation 适合简单单次
│   │   │
│   │   ├── 特点
│   │   │   ├── 优势：可视化状态机、参数驱动、Humanoid 复用动画、Blend Tree 平滑混合
│   │   │   └── 局限：Idle 状态机也耗 CPU；Rebind 开销大；Humanoid 有 15~20% CPU 额外成本
│   │   │
│   │   ├── 适用场景
│   │   │   ├── ✅ 适用：人形/Generic 角色 locomotion、战斗连招、过场、门开关
│   │   │   └── ❌ 不适用：极少播放的单次动画（可用 Animation 或 Playables）；UI RectTransform 动画
│   │   │
│   │   ├── 核心原理：Mecanim 工作流（官方四步）
│   │   │   ├── 步骤1 导入 Animation Clip（FBX 或 Unity 内创建）
│   │   │   ├── 步骤2 在 Animator Controller 中编排 State 与 Transition
│   │   │   ├── 步骤3 人形模型配置 Avatar（Generic 可跳过）
│   │   │   └── 步骤4 GameObject 挂 Animator，指定 Controller（+ Avatar）
│   │   │
│   │   ├── 核心 API 及参数（Animator 脚本控制）
│   │   │   ├── 参数写入：SetFloat / SetBool / SetInteger / SetTrigger
│   │   │   ├── 参数读取：GetFloat / GetBool / GetInteger
│   │   │   ├── Trigger 复位：ResetTrigger（避免连续触发失效）
│   │   │   ├── 状态查询：GetCurrentAnimatorStateInfo(layerIndex)
│   │   │   ├── 直接播放：Play(stateName) / CrossFade（少用，优先参数驱动）
│   │   │   ├── 性能：Animator.StringToHash("Speed") 代替字符串
│   │   │   └── 属性：speed（播放倍速）、applyRootMotion（根运动位移）
│   │   │
│   │   ├── Animator Controller 核心概念
│   │   │   ├── State：绑定一个或多个 Animation Clip
│   │   │   ├── Transition：条件满足时切换 State（Has Exit Time、Conditions）
│   │   │   ├── Parameters：Float / Bool / Int / Trigger
│   │   │   ├── Blend Tree：按参数混合多段 Clip（如 Speed 混合走/跑）
│   │   │   └── Layer：上半身/全身分层，Avatar Mask 控制骨骼
│   │   │
│   │   ├── 标准使用步骤（六步）
│   │   │   ├── 步骤1 导入 FBX，Rig 选 Humanoid 或 Generic，Apply
│   │   │   ├── 步骤2 Animation 选项卡勾选需要的 Clip，Apply
│   │   │   ├── 步骤3 创建 Animator Controller，拖入 Clip 做 State
│   │   │   ├── 步骤4 添加 Parameters，设置 Transition 条件
│   │   │   ├── 步骤5 模型 Prefab 挂 Animator，指定 Controller
│   │   │   └── 步骤6 脚本 GetComponent<Animator>()，Update 里 SetFloat/SetTrigger
│   │   │
│   │   ├── 生命周期与调用时机
│   │   │   ├── Awake/Start：GetComponent<Animator>()，缓存 StringToHash
│   │   │   ├── Update：根据 Input / 角色逻辑 Set 参数
│   │   │   ├── OnAnimatorMove：自定义 Root Motion 处理（applyRootMotion 时）
│   │   │   └── FixedUpdate + animatePhysics：动画驱动 Kinematic 刚体
│   │   │
│   │   ├── Root Motion
│   │   │   ├── applyRootMotion = true：动画自带位移写入 Transform
│   │   │   ├── 适用：走/跑由动画师 K 好位移；不适用：纯代码 CharacterController 移动
│   │   │   └── deltaPosition / deltaRotation：脚本可读每帧根运动增量
│   │   │
│   │   └── 选型、封装、避坑
│   │       ├── 选型：Humanoid 复用动画库；Generic 固定骨骼；Blend Tree 做 locomotion
│   │       ├── 封装：AnimParams 常量 + CharacterAnim 组件
│   │       └── 避坑：参数名拼写、Trigger 需 Reset、缺 Controller、Rig 类型错、T-Pose 未 Apply
│   │
│   ├── 第一阶段：零基础（建立认知 + 读懂代码）
│   │   ├── 理解 Model / Clip / Controller / Animator 四者关系
│   │   ├── 逐词读懂：animator.SetFloat("Speed", 1f)
│   │   └── 认识 SkinnedMeshRenderer 与 Rig 类型
│   │
│   ├── 第二阶段：入门（导入 + Controller + API + 案例）
│   │   ├── FBX 导入与 Rig/Animation 选项卡
│   │   ├── Parameters 与 Transition 条件
│   │   └── 实战案例：Speed 走跑 / Trigger 跳跃 / 判断动画播完
│   │
│   └── 第三阶段：进阶（Blend Tree + Humanoid + Root Motion + 封装）
│       ├── Blend Tree 1D 混合 locomotion
│       ├── Humanoid Retarget 与 Avatar
│       ├── Root Motion 与 CharacterController 取舍
│       └── CharacterAnim 封装 + 性能与 Rebind 避坑
│
└── 旧 Animation 组件（Legacy — 了解即可）
    │
    ├── 定义：Legacy Rig 模型上的 Animation 组件，直接 Play 单个 Clip
    ├── 与 Animator：无状态机，适合极简单物体（旋转道具、门）
    └── 新项目优先 Mecanim Animator
```

| 学习阶段 | 学习目标 |
|----------|----------|
| **零基础** | 说清 Model、Clip、Controller、Animator 关系；读懂 SetFloat |
| **入门** | 会导入 FBX、做 Controller、Set 参数；完成 3 个案例 |
| **进阶** | 会 Blend Tree、Humanoid、Root Motion 选型；封装与避坑 |

### 讲师知识框架速览（全文脉络）

| 维度 | 零基础讲 | 入门讲 | 进阶讲 |
|------|----------|--------|--------|
| 定义 | ✅ | 回顾 | 回顾 |
| 本质 | ✅ | Mecanim 四步 | Humanoid / Root Motion |
| 特点 | ✅ | — | 性能 / Rebind |
| 适用场景 | ✅ | — | Animator vs Animation |
| 核心原理 | 模型+骨骼 | ✅ 状态机+参数 | Blend Tree |
| 核心 API | 读懂 SetFloat | ✅ 四类参数 | StringToHash |
| 使用步骤 | Inspector 导入 | ✅ 六步流程 | 封装 |
| 调用时机 | — | ✅ Update | OnAnimatorMove |
| 避坑 | — | 初步 | ✅ |

---

# 第一阶段：零基础篇

## 【阶段总述】

零基础阶段建立**正确认知**：3D 模型是什么、动画由哪些资产组成、Animator 在链路中的位置。  
同时学会**读懂** `animator.SetFloat("Speed", speed)` 每个部分的含义。

---

## 一、定义 — 模型与 Animator 是什么？

| 概念 | 说明 |
|------|------|
| **3D Model（模型）** | FBX 等文件，含网格（Mesh）、骨骼（Rig）、可选动画片段 |
| **Animation Clip** | 一段动画数据：记录骨骼/属性随时间如何变化 |
| **Animator Controller** | 状态机资产（`.controller`），编排 State、Transition、Parameters |
| **Animator** | 挂在 GameObject 上的**组件**，运行时执行 Controller |
| **官方（Mecanim）** | Animation clips → Animator Controller → Animator Component 串联播放 |

```
FBX 模型文件
    ├── Mesh（网格形状）
    ├── Rig / Bones（骨骼层级）
    └── Animation Clips（走路、跳跃…）
            │
            ▼
    Animator Controller（状态机资产）
            │
            ▼
    GameObject + Animator 组件（运行时播放）
```

---

## 二、本质 — 模型如何「动起来」？

| 层级 | 作用 |
|------|------|
| **SkinnedMeshRenderer** | 网格绑在骨骼上，骨骼动 → 表面变形 |
| **Animation Clip** | 关键帧曲线，驱动骨骼 Transform 或属性 |
| **Animator Controller** | 决定「现在播哪段 Clip、何时切换」 |
| **Animator 组件** | 每帧求值 Clip，写入骨骼 Transform |
| **脚本 SetFloat 等** | 改 Parameters → 满足 Transition 条件 → 换 State |

**一句话**：Clip 是「录像带」，Controller 是「播放列表+切换规则」，Animator 是「播放器」，脚本是「遥控器」。

---

## 三、模型导入 — Inspector 三个关键选项卡

| 选项卡 | 作用 |
|--------|------|
| **Model** | 网格缩放、法线、Blend Shape、Read/Write |
| **Rig** | 骨骼类型：None / Legacy / **Humanoid** / **Generic** |
| **Animation** | 从 FBX 提取 Clip、循环 Loop Time、Root 位移烘焙 |

### Rig 类型对比

| 类型 | 说明 | 典型用途 |
|------|------|----------|
| **Humanoid** | Unity 人形 Avatar 映射，可 Retarget | 人形角色，复用动画库 |
| **Generic** | 保留原骨骼结构 | 怪物、机械、非人形 |
| **Legacy** | 旧系统 | 老项目，新项目不用 |
| **None** | 无骨骼 | 静态道具 |

Humanoid 配置后需 **Configure…** 检查骨骼映射 → **Apply**。

---

## 四、Mecanim 核心四件套关系（官方流程）

| 步骤 | 操作 |
|------|------|
| 1 | 导入 FBX，得到 Animation Clips |
| 2 | 创建 Animator Controller，State 绑定 Clip，连 Transition |
| 3 | Humanoid 模型生成 **Avatar** 资产（Generic 不需要） |
| 4 | 模型挂 **Animator**，指定 Controller（+ Avatar） |

---

## 五、核心一课：如何读懂 SetFloat

```csharp
animator.SetFloat("Speed", 1.5f);
```

| 部分 | 含义 |
|------|------|
| `animator` | Animator 组件引用 |
| `.SetFloat` | 设置名为 Float 类型的参数值 |
| `"Speed"` | Controller 里 Parameters 窗口中定义的名字，**必须完全一致** |
| `1.5f` | 浮点值，常用于混合树或 Transition 条件（如 Speed > 0.1） |

**整行人话**：告诉状态机「当前速度参数是 1.5」，Controller 里设好的规则会自动切换走/跑等状态。

```csharp
animator.SetTrigger("Jump");
```

| 部分 | 含义 |
|------|------|
| `SetTrigger` | 触发一次型参数，自动从 true 弹回 false |
| `"Jump"` | 参数名，Transition 条件常用 `Jump`（Trigger 类型） |

**整行人话**：按一下「跳跃键」，状态机收到脉冲信号，播 Jump 动画，播完通常回到 Idle/Run。

---

## 【零基础阶段小结】

| 维度 | 要点 |
|------|------|
| **定义** | Model=资产；Clip=动画段；Controller=状态机；Animator=组件 |
| **本质** | 骨骼变形 + 状态机驱动 Clip |
| **Rig** | Humanoid 人形 / Generic 通用 |
| **读懂** | SetFloat / SetTrigger 与 Parameters 名字对应 |

**阶段检验**：能画出 FBX → Controller → Animator 链路；能说出 Parameters 是脚本与状态机的桥梁。

---

# 第二阶段：入门篇

## 【阶段总述】

入门阶段掌握 **FBX 导入设置**、**Animator Controller 制作**、**四类 Parameters API**，并完成 3 个实战案例。  
重点：**Update 里 Set 参数**；**Transition 条件与参数名一致**。

---

## 一、Animator Parameters 四类详解

> 以下采用与 [01_PlayerPrefs.md](./01_PlayerPrefs.md) 相同的 **逐词读懂** 格式。

### API 全景（脚本控制 Animator）

```
Animator（UnityEngine 组件 — 挂角色上，执行 Controller）
├── 写参数：SetFloat / SetBool / SetInteger / SetTrigger / ResetTrigger
├── 读参数：GetFloat / GetBool / GetInteger
├── 查状态：GetCurrentAnimatorStateInfo / IsInTransition
└── 属性：speed / applyRootMotion
```

---

### 1.1 `animator.SetFloat` — 逐词读懂

```csharp
animator.SetFloat("Speed", speed);
```

| 部分 | 含义 |
|------|------|
| `animator` | **变量名**：Animator 组件引用 |
| `.SetFloat` | **方法名**：设置 Controller 里 **Float 类型** Parameters |
| `"Speed"` | **参数1 name**：字符串，须与 Animator Controller **Parameters 窗口名字完全一致** |
| `speed` | **参数2 value**：float，要写入的值（如 0=停，1=全速） |

**整行人话**：告诉状态机「当前 Speed 是多少」，Transition 条件（如 Speed>0.1）据此切换 Idle/Walk/Run。

---

### 1.2 `animator.SetBool` — 逐词读懂

```csharp
animator.SetBool("IsGrounded", true);
```

| 部分 | 含义 |
|------|------|
| `.SetBool` | 设置 **Bool 类型** 参数 |
| `"IsGrounded"` | 参数名 |
| `true` / `false` | 持续状态，不像 Trigger 只脉冲一次 |

**整行人话**：告诉动画机「是否着地」等开关状态。

---

### 1.3 `animator.SetInteger` — 逐词读懂

```csharp
animator.SetInteger("AttackIndex", 2);
```

| 部分 | 含义 |
|------|------|
| `.SetInteger` | 设置 **Int 类型** 参数 |
| `2` | 整数值，用于攻击第 2 段、武器类型等离散状态 |

**整行人话**：用整数区分多种动画分支（Combo 1/2/3）。

---

### 1.4 `animator.SetTrigger` / `ResetTrigger` — 逐词读懂

```csharp
animator.SetTrigger("Jump");
animator.ResetTrigger("Jump");
```

| 部分 | 含义 |
|------|------|
| `.SetTrigger` | 设置 **Trigger 类型** 参数：发一次**脉冲** |
| 官方行为 | 自动 true 后弹回 false；Transition 消费一次 |
| `.ResetTrigger` | 手动清除 Trigger，防止连续触发失效 |

**整行人话**：Jump/Attack 等「按一下动一次」用 Trigger，不是长按一直跳。

---

### 四类 Parameters 对照

| 类型 | 脚本 API | 用途 |
|------|----------|------|
| **Float** | SetFloat / GetFloat | 速度、Blend Tree 混合 |
| **Bool** | SetBool / GetBool | 是否蹲下、是否着地 |
| **Int** | SetInteger / GetInteger | 攻击段 1/2/3 |
| **Trigger** | SetTrigger / ResetTrigger | 跳、攻击、开门（一次性） |

### Transition 条件（Animator 窗口）

| 设置 | 含义 |
|------|------|
| **Has Exit Time** | 勾选：等当前动画播到一定进度才过渡 |
| **Conditions** | 如 `Speed > 0.1`、`Jump`（Trigger）、`IsGrounded == true` |
| **Transition Duration** | 混合过渡时间，越大越平滑 |

---

## 二、Animator 常用 API — 逐词读懂

### 2.1 参数写入示例（整段）

```csharp
void Update()
{
    float h = Input.GetAxis("Horizontal");
    float v = Input.GetAxis("Vertical");
    float speed = new Vector2(h, v).magnitude;
    animator.SetFloat("Speed", speed);
}
```

| 行 | 整行人话 |
|----|----------|
| `GetAxis("Horizontal")` | 读平滑后的水平轴 -1~1 |
| `new Vector2(h, v)` | 合成 2D 输入向量 |
| `.magnitude` | 向量长度作 Speed |
| `SetFloat("Speed", speed)` | 见 1.1 |

---

### 2.2 `GetCurrentAnimatorStateInfo` — 逐词读懂

```csharp
AnimatorStateInfo state = animator.GetCurrentAnimatorStateInfo(0);
if (state.IsName("Jump"))
{
    // 当前在 Jump 状态
}
```

| 部分 | 含义 |
|------|------|
| `GetCurrentAnimatorStateInfo` | **方法名**：获取指定**层**当前状态信息 |
| `0` | **参数 layerIndex**：第 0 层（Base Layer）；多层动画时 1、2… |
| **返回值** | `AnimatorStateInfo` 结构体 |
| `state.IsName("Jump")` | 当前状态名是否为 Jump |
| `state.normalizedTime` | 动画进度 0~1（1=播完一圈） |
| `animator.IsInTransition(0)` | 第 0 层是否在**过渡混合**中 |

**整行人话**：查「现在在播哪个 State、播到哪了」，用于攻击冷却、播完再允许下一次操作。

---

### 2.3 其他常用属性 — 逐词读懂

```csharp
animator.speed = 1f;
animator.applyRootMotion = false;
```

| 部分 | 含义 |
|------|------|
| `speed` | 全局播放倍速：1=正常，2=两倍速，0=暂停 |
| `applyRootMotion` | true=动画自带位移写入 Transform；false=位移由代码控制 |

**整行人话**：一般第三人称用代码移动时设 `applyRootMotion = false`，避免和 CharacterController 抢位置。

---

## 三、标准六步流程

```
步骤1  导入 FBX → Rig（Humanoid/Generic）→ Apply
步骤2  Animation 选项卡 → 勾选 Clip → Loop Time（如需循环）→ Apply
步骤3  Project 右键 Create → Animator Controller
步骤4  双击 Controller：拖 Clip 建 State，Add Parameters，连 Transition + Conditions
步骤5  角色 Prefab：Add Component → Animator，拖入 Controller
步骤6  脚本 Awake 取 Animator，Update 里 SetFloat / SetTrigger
```

---

## 四、入门三个案例

### 案例代码讲解模板

每个案例统一按以下结构组织（下文所有案例均遵循此模板）：

| 顺序 | 板块 | 内容 |
|:----:|------|------|
| 1 | **功能** | 案例实现什么业务 |
| 2 | **完整代码** | 带行内注释的完整脚本 |
| 3 | **语法拆解** | 对案例中较生僻的语法，逐个说明（格式见下） |
| 4 | **逐行详解** | 表格：每行代码的含义 |
| 5 | **操作提示** | Unity 绑定、调用方式等（如有） |

**语法拆解的标准格式**（遇到 `GetAxisRaw`、`SetTrigger`、`StringToHash` 等不熟悉的写法时使用）：

```
#### `代码片段` 是什么？

（单独贴出该代码行）

| 部分 | 含义 |
|------|------|
| ...  | 逐部分拆解 |

**整行人话**：（一句话总结这行在干什么）

**说明**：（可选，补充注意事项）
```

---

### 案例 1：Speed 驱动 Idle / Walk / Run

**功能**：根据输入轴大小设置 Speed 参数，状态机切换待机、走、跑。

**Animator Controller 预设**（需事先做好）：

| State | 说明 |
|-------|------|
| Idle | Speed == 0 |
| Walk | Speed > 0.1 且 Speed < 0.5 |
| Run | Speed >= 0.5 |

```csharp
using UnityEngine;                                      // 引入 Unity 核心库

public class PlayerLocomotion : MonoBehaviour           // 角色移动动画驱动脚本
{
    Animator animator;                                  // 缓存 Animator 组件引用

    void Awake()                                        // Awake：初始化时获取组件
    {
        animator = GetComponent<Animator>();          // 从本物体获取 Animator（须已挂 Controller）
    }

    void Update()                                       // Update：每帧读输入并写 Animator 参数
    {
        float h = Input.GetAxisRaw("Horizontal");     // 水平输入：A/D 或摇杆 X，原始值 -1/0/1
        float v = Input.GetAxisRaw("Vertical");       // 垂直输入：W/S 或摇杆 Y
        Vector2 input = new Vector2(h, v);            // 合成二维移动向量

        float speed = input.magnitude;                // 向量长度 0~1，无输入为 0，对角线约为 1
        animator.SetFloat("Speed", speed);            // 写 Float 参数，驱动 Controller 过渡条件

        // 可选：代码控制朝向（与 Root Motion 方案二选一，勿同时抢 Transform）
        if (input.sqrMagnitude > 0.01f)               // 有有效输入时才转向（sqrMagnitude 避免开方）
        {
            transform.rotation = Quaternion.LookRotation(  // 让角色面向移动方向（Y 轴朝上）
                new Vector3(input.x, 0f, input.y));
        }
    }
}
```

#### 语法拆解

##### `Input.GetAxisRaw("Horizontal")` 是什么？

```csharp
float h = Input.GetAxisRaw("Horizontal");
```

| 部分 | 含义 |
|------|------|
| `Input` | Unity 输入静态类 |
| `GetAxisRaw` | 原始轴值，无平滑，通常为 -1 / 0 / 1 |
| `"Horizontal"` | Input Manager 里定义的轴名（A/D、左右键） |

**整行人话**：读键盘或手柄水平方向，得到 -1（左）到 1（右）。

---

##### `input.magnitude` 是什么？

```csharp
float speed = input.magnitude;
```

| 部分 | 含义 |
|------|------|
| `Vector2 input` | 二维向量 (x, y) |
| `.magnitude` | 向量长度 √((x²+y²)) |
| 取值范围 | 无输入 0；单轴满速 1；对角线约 1.414（可再 Normalize） |

**整行人话**：把 WASD 合成一个「移动强度」交给 Animator 的 Speed 参数。

---

##### `animator.SetFloat("Speed", speed)` 是什么？

```csharp
animator.SetFloat("Speed", speed);
```

| 部分 | 含义 |
|------|------|
| `SetFloat` | 设置 Animator Controller 中 Float 类型参数 |
| `"Speed"` | 参数名，须与 Controller Parameters 窗口**完全一致** |
| `speed` | 要写入的浮点值 |

**整行人话**：告诉状态机当前速度，由 Transition 条件决定播 Idle/Walk/Run。

---

##### `input.sqrMagnitude > 0.01f` 是什么？

```csharp
if (input.sqrMagnitude > 0.01f)
```

| 部分 | 含义 |
|------|------|
| `sqrMagnitude` | 向量长度的平方，比 magnitude 省一次开方 |
| `0.01f` | 阈值，过滤极小抖动输入 |
| 用途 | 只有真正在移动时才旋转朝向 |

**整行人话**：没按方向键时不乱转角色。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 3 | `public class PlayerLocomotion : MonoBehaviour` | 可挂载的脚本类 |
| 5 | `Animator animator;` | 声明 Animator 缓存 |
| 7 | `void Awake()` | 初始化阶段 |
| 9 | `GetComponent<Animator>()` | 获取同物体 Animator |
| 11 | `void Update()` | 每帧读输入 |
| 13 | `GetAxisRaw("Horizontal")` | 见上方语法拆解 |
| 14 | `GetAxisRaw("Vertical")` | 读垂直输入 |
| 15 | `new Vector2(h, v)` | 合成移动向量 |
| 17 | `input.magnitude` | 见上方语法拆解 |
| 18 | `SetFloat("Speed", speed)` | 见上方语法拆解 |
| 21 | `sqrMagnitude > 0.01f` | 见上方语法拆解 |
| 23~24 | `LookRotation(...)` | 面向移动方向 |

#### 操作提示

Controller 里 Parameters 添加 **Speed（Float）**；Transition 条件与上表一致；Clip 需从 FBX Animation 选项卡提取。

---

### 案例 2：Trigger 跳跃

**功能**：空格触发 Jump，落地后回到 locomotion。

**Controller 预设**：Any State → Jump（Condition: Jump Trigger）；Jump → Idle/Run（Exit Time 或 IsGrounded）。

```csharp
using UnityEngine;                                      // 引入 Unity 核心库

public class PlayerJump : MonoBehaviour                   // 跳跃动画驱动脚本
{
    Animator animator;                                  // Animator 组件引用
    bool isGrounded = true;                             // 是否着地（业务逻辑，防空中二段跳）

    void Awake()                                        // 初始化
    {
        animator = GetComponent<Animator>();          // 获取 Animator
    }

    void Update()                                       // 每帧同步参数与检测跳跃输入
    {
        animator.SetBool("IsGrounded", isGrounded);    // 每帧把落地状态写给 Animator（Bool 参数）

        if (Input.GetKeyDown(KeyCode.Space) && isGrounded)  // 空格按下 且 在地面 才允许跳
        {
            animator.SetTrigger("Jump");                // 触发 Jump Trigger，状态机切到 Jump 状态
            isGrounded = false;                         // 起跳后标记为空中，直到再次落地
        }
    }

    // 简化示例：落地由物理碰撞检测（正式项目可用 Raycast 脚着地更准）
    void OnCollisionEnter(Collision collision)          // 发生碰撞时 Unity 自动调用
    {
        if (collision.gameObject.CompareTag("Ground"))  // 碰到 Tag 为 Ground 的物体
            isGrounded = true;                          // 恢复着地状态
    }
}
```

#### 语法拆解

##### `animator.SetTrigger("Jump")` 是什么？

```csharp
animator.SetTrigger("Jump");
```

| 部分 | 含义 |
|------|------|
| `SetTrigger` | 设置 Trigger 类型参数（一次性脉冲） |
| `"Jump"` | 参数名，Controller 里须定义为 Trigger |
| 官方行为 | 自动 true 后弹回 false，Transition 消费一次 |

**整行人话**：按一下「跳跃键」，状态机收到脉冲，播 Jump 动画。

---

##### `animator.SetBool("IsGrounded", isGrounded)` 是什么？

```csharp
animator.SetBool("IsGrounded", isGrounded);
```

| 部分 | 含义 |
|------|------|
| `SetBool` | 设置 Bool 类型参数（持续 true/false） |
| `"IsGrounded"` | 参数名 |
| 用途 | Jump → Run 过渡条件：`IsGrounded == true` |

**整行人话**：告诉动画机脚是否着地，落地后才能切回跑步。

---

##### `CompareTag("Ground")` 是什么？

```csharp
if (collision.gameObject.CompareTag("Ground"))
```

| 部分 | 含义 |
|------|------|
| `OnCollisionEnter` | 3D 碰撞开始回调 |
| `CompareTag` | 比较物体 Tag，比 `tag == "Ground"` 更高效安全 |
| `"Ground"` | 地面物体在 Inspector 设置的 Tag |

**整行人话**：只有踩到标了 Ground 的东西才算落地。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 3 | `public class PlayerJump : MonoBehaviour` | 可挂载的脚本类 |
| 5 | `Animator animator;` | Animator 缓存 |
| 6 | `bool isGrounded = true;` | 默认着地，游戏开始可站立 |
| 8 | `void Awake()` | 初始化 |
| 10 | `GetComponent<Animator>()` | 获取 Animator |
| 12 | `void Update()` | 每帧逻辑 |
| 14 | `SetBool("IsGrounded", ...)` | 见上方语法拆解 |
| 16 | `GetKeyDown(Space) && isGrounded` | 空格且着地才跳 |
| 18 | `SetTrigger("Jump")` | 见上方语法拆解 |
| 19 | `isGrounded = false` | 起跳后标记空中 |
| 23 | `OnCollisionEnter` | 碰撞回调 |
| 25 | `CompareTag("Ground")` | 见上方语法拆解 |
| 26 | `isGrounded = true` | 恢复着地 |

#### 操作提示

Parameters：**Jump（Trigger）**、**IsGrounded（Bool）**；地面 Collider Tag 设为 **Ground**；Jump 状态 Clip 勿勾选 Loop Time。

---

### 案例 3：判断攻击动画播完

**功能**：按 J 攻击，等 Attack 状态 normalizedTime 播完再允许下一次攻击。

```csharp
using UnityEngine;                                      // 引入 Unity 核心库

public class PlayerAttack : MonoBehaviour                 // 攻击动画与冷却控制脚本
{
    Animator animator;                                  // Animator 引用
    bool canAttack = true;                              // 是否允许发起下一次攻击
    static readonly int AttackHash = Animator.StringToHash("Attack");  // 预计算状态名哈希，省 GC

    void Awake()                                        // 初始化
    {
        animator = GetComponent<Animator>();          // 获取 Animator
    }

    void Update()                                       // 每帧检测输入与动画进度
    {
        if (Input.GetKeyDown(KeyCode.J) && canAttack) // J 键且不在攻击冷却中
        {
            animator.SetTrigger(AttackHash);            // 用 int 哈希触发 Attack（Trigger 参数）
            canAttack = false;                        // 锁定，直到本段攻击播完
        }

        if (!canAttack)                               // 正在攻击中时检查是否播完
        {
            AnimatorStateInfo info = animator.GetCurrentAnimatorStateInfo(0);  // 第 0 层当前状态信息
            if (info.shortNameHash == AttackHash      // 当前状态是 Attack
                && info.normalizedTime >= 0.95f       // 动画进度 ≥95%（留余量防浮点误差）
                && !animator.IsInTransition(0))      // 且不在过渡混合中
            {
                canAttack = true;                     // 解锁，可再次攻击
            }
        }
    }
}
```

#### 语法拆解

##### `Animator.StringToHash("Attack")` 是什么？

```csharp
static readonly int AttackHash = Animator.StringToHash("Attack");
```

| 部分 | 含义 |
|------|------|
| `StringToHash` | 把状态/参数名字符串转为 int 哈希 |
| `static readonly` | 类级别只算一次，全实例共享 |
| 用途 | `SetTrigger(int)`、`shortNameHash` 比较，减少字符串 GC |

**整行人话**：用数字代替字符串跟 Animator 打交道，更省性能。

---

##### `normalizedTime >= 0.95f` 是什么？

```csharp
info.normalizedTime >= 0.95f
```

| 部分 | 含义 |
|------|------|
| `AnimatorStateInfo` | 当前层状态信息（进度、是否循环等） |
| `normalizedTime` | 归一化进度：0=开始，1=播完一圈 |
| `0.95f` | 留 5% 余量，避免浮点误差导致判不到结束 |

**整行人话**：攻击动画快结束时解锁下一次攻击。

---

##### `!animator.IsInTransition(0)` 是什么？

```csharp
!animator.IsInTransition(0)
```

| 部分 | 含义 |
|------|------|
| `IsInTransition(0)` | 第 0 层是否正在状态过渡混合 |
| `!` | 取反：必须**不在**过渡中才算播完 |
| 原因 | 过渡中 normalizedTime 可能不准确 |

**整行人话**：等过渡结束、真正站在 Attack 状态末尾再解锁。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 3 | `public class PlayerAttack : MonoBehaviour` | 可挂载的脚本类 |
| 5 | `Animator animator;` | Animator 缓存 |
| 6 | `bool canAttack = true;` | 攻击冷却锁 |
| 7 | `AttackHash = StringToHash(...)` | 见上方语法拆解 |
| 9 | `void Awake()` | 初始化 |
| 11 | `GetComponent<Animator>()` | 获取 Animator |
| 13 | `void Update()` | 每帧逻辑 |
| 15 | `GetKeyDown(J) && canAttack` | 按键且可攻击 |
| 17 | `SetTrigger(AttackHash)` | 触发攻击 |
| 18 | `canAttack = false` | 上锁 |
| 21 | `if (!canAttack)` | 攻击进行中 |
| 23 | `GetCurrentAnimatorStateInfo(0)` | 读第 0 层状态 |
| 24~26 | 三个条件判断 | 见上方语法拆解 |
| 28 | `canAttack = true` | 解锁 |

#### 操作提示

State 名 **Attack** 与哈希一致；Any State → Attack 用 Trigger；Attack → Idle 可用 Exit Time；Controller 参数 Attack 也建议用同名 Trigger。

---

## 【入门阶段小结】

| 维度 | 要点 |
|------|------|
| **Parameters** | Float / Bool / Int / Trigger |
| **API** | SetFloat、SetTrigger、GetCurrentAnimatorStateInfo |
| **流程** | 导入 → Controller → 挂 Animator → 脚本 Set |
| **案例** | Speed 走跑、Trigger 跳、播完检测 |

---

# 第三阶段：进阶篇

## 【阶段总述】

进阶阶段：**Blend Tree 混合移动**、**Humanoid Retarget**、**Root Motion 取舍**、**CharacterAnim 封装**、**性能与 Rebind 避坑**。

---

## 一、Blend Tree（1D 混合树）

| 概念 | 说明 |
|------|------|
| **作用** | 一个 State 内按 Float 参数混合多段 Clip（Idle↔Walk↔Run） |
| **创建** | Controller 右键 Create State → From New Blend Tree → 双击进入 |
| **Blend Parameter** | 如 Speed：0=Idle，0.5=Walk，1=Run |
| **优势** | 比多个 State + Transition 更平滑，locomotion 标配 |

```
Blend Tree "Locomotion"
├── Speed = 0   → Idle.clip
├── Speed = 0.5 → Walk.clip
└── Speed = 1   → Run.clip
```

脚本仍只需 `SetFloat("Speed", value)`，混合在 Controller 内完成。

---

## 二、Humanoid 与 Avatar Retarget

| 概念 | 说明 |
|------|------|
| **Avatar** | Humanoid Rig Apply 后生成，存骨骼映射 |
| **Retarget** | 同 Humanoid 动画 Clip 可套到不同人形模型 |
| **代价** | CPU 比 Generic 高约 15~20%（官方建议自行实测） |
| **建议** | 项目内统一 Humanoid **或** Generic，避免混用 |

配置路径：FBX → Rig → Animation Type **Humanoid** → Configure → Apply。

---

## 三、Root Motion 取舍

| 模式 | applyRootMotion | 移动来源 |
|------|-----------------|----------|
| **代码移动** | false | Transform / CharacterController / Rigidbody |
| **动画位移** | true | Clip 根骨骼位移写入 Transform |
| **混合** | true + OnAnimatorMove | 读 deltaPosition 自行施加 |

```csharp
void OnAnimatorMove()
{
    if (!applyRootMotion) return;
    Vector3 delta = animator.deltaPosition;
    characterController.Move(delta);
}
```

| 选型 | 建议 |
|------|------|
| 第三人称走跑 | 常关闭 Root Motion，用代码移动 + 只播上半身 |
| 动作游戏精确步伐 | 可开启 Root Motion |
| 与 NavMeshAgent | 一般关闭，由 Agent 驱动位置 |

---

## 四、Layer 与 Avatar Mask（简述）

| 概念 | 说明 |
|------|------|
| **Layer** | 多层状态机叠加，如 Base Layer 全身 + Upper Body 瞄准 |
| **Avatar Mask** | 指定哪些骨骼受该 Layer 影响 |
| **SetLayerWeight** | 动态调整层权重 0~1 |

```csharp
animator.SetLayerWeight(1, 1f);  // 启用第 1 层（如射击上半身）
```

---

## 五、工程化封装 CharacterAnim

```csharp
using UnityEngine;

public class CharacterAnim : MonoBehaviour
{
    public static class Params
    {
        public static readonly int Speed = Animator.StringToHash("Speed");
        public static readonly int Jump = Animator.StringToHash("Jump");
        public static readonly int IsGrounded = Animator.StringToHash("IsGrounded");
    }

    Animator _anim;

    void Awake()
    {
        _anim = GetComponent<Animator>();
    }

    public void SetSpeed(float speed) => _anim.SetFloat(Params.Speed, speed);

    public void Jump()
    {
        _anim.ResetTrigger(Params.Jump);
        _anim.SetTrigger(Params.Jump);
    }

    public void SetGrounded(bool grounded) => _anim.SetBool(Params.IsGrounded, grounded);

    public bool IsStateFinished(int stateHash, int layer = 0, float threshold = 0.95f)
    {
        var info = _anim.GetCurrentAnimatorStateInfo(layer);
        return info.shortNameHash == stateHash
            && info.normalizedTime >= threshold
            && !_anim.IsInTransition(layer);
    }
}
```

---

## 六、Animation Event（脚本回调）

在 Animation 窗口或 Clip 上添加 **Animation Event**，指定帧调用脚本方法：

```csharp
public void OnFootstep()
{
    // 脚落地时播脚步声
}

public void OnAttackHit()
{
    // 攻击判定帧造成伤害
}
```

| 注意 | 说明 |
|------|------|
| 方法须 `public` | 且可在带 Animator 的对象上找到 |
| 参数类型 | 支持 float / int / string / Object reference |

---

## 七、常见误区与最佳实践

| 误区 | 正确做法 |
|------|----------|
| 动画不播 | 检查 Animator 是否指定 Controller；Clip 是否提取 |
| SetFloat 无效 | Parameters **名字大小写**必须与 Controller 完全一致 |
| Trigger 跳不出来 | 条件是否满足；是否需 ResetTrigger；Has Exit Time 是否挡住 |
| T-Pose 不变形 | Rig 未 Apply；Avatar 未配置；缺 SkinnedMeshRenderer |
| Humanoid 乱扭 | Configure Avatar 骨骼映射错误 |
| 滑步 | 动画速度与代码移动速度不匹配；用 Blend Tree 或调 Clip 速度 |
| 性能差 | 减少无用 Layer；用 StringToHash；避免频繁换 Controller 触发 Rebind |
| 对象池复用 | 禁用 GameObject 会 Rebind；官方建议池化时 **Disable Animator 组件** 而非整个 GO |
| UI 动画卡顿 | RectTransform 用 Animation 组件而非 Animator（官方建议） |

---

## 【进阶阶段小结】

| 维度 | 要点 |
|------|------|
| Blend Tree | 1D Speed 混合 Idle/Walk/Run |
| Humanoid | Avatar + Retarget，注意 CPU |
| Root Motion | applyRootMotion 与代码移动二选一或 OnAnimatorMove |
| 封装 | Params 哈希 + CharacterAnim |
| 避坑 | 参数名、Trigger、Rebind、Rig Apply |

---

# 【全文总结】

## 最重要的一行代码

```csharp
animator.SetFloat("Speed", Input.GetAxisRaw("Horizontal"));
```

| 部分 | 含义 |
|------|------|
| `animator` | Animator 组件 |
| `SetFloat` | 写 Float 参数 |
| `"Speed"` | Controller 里定义的参数名 |

## 三阶段对照

| 阶段 | 代表案例 |
|------|----------|
| 零基础 | 读懂 Model / Clip / Controller / Animator |
| 入门 | Speed 走跑、Trigger 跳、攻击播完检测 |
| 进阶 | Blend Tree、Humanoid、Root Motion、CharacterAnim |

## Mecanim 资产关系图

```
FBX ──→ Animation Clips
              │
              ▼
       Animator Controller（Parameters + States + Transitions）
              │
              ▼
    GameObject + Animator + SkinnedMeshRenderer
              │
              ▼
         脚本 SetFloat / SetTrigger
```

## 官方文档索引

| 主题 | 链接 |
|------|------|
| 导入模型 | https://docs.unity3d.com/Manual/ImportingModelFiles.html |
| Mecanim 概述 | https://docs.unity3d.com/Manual/AnimationOverview.html |
| Animator | https://docs.unity3d.com/ScriptReference/Animator.html |
| SetFloat | https://docs.unity3d.com/ScriptReference/Animator.SetFloat.html |
| SetTrigger | https://docs.unity3d.com/ScriptReference/Animator.SetTrigger.html |

---

*文档版本：与 01_PlayerPrefs.md、02_Camera.md、03_Raycast.md 同系列模板。*
