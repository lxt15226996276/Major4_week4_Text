# 综合案例项目实例RPG世界（一）——项目初始化与玩家基础

> 参照：[Unity 官方 Manual - Scene Management](https://docs.unity3d.com/Manual/SceneManagement.html) · [CharacterController](https://docs.unity3d.com/ScriptReference/CharacterController.html) · [Animator](https://docs.unity3d.com/ScriptReference/Animator.html) · [Camera](https://docs.unity3d.com/ScriptReference/Camera.html)  
> 关联文档：[02_RPG世界（二）.md](./02_RPG世界（二）战斗系统与交互.md) · [03_RPG世界（三）.md](./03_RPG世界（三）任务与存档.md) · [04_RPG世界（四）.md](./04_RPG世界（四）AI与优化.md) · [05_综合复习.md](./05_综合复习.md)  
> 学习路径：**零基础 → 入门 → 进阶**，每阶段采用 **总—分—总** 结构。  
> 讲解维度：**定义 → 本质 → 特点 → 适用场景 → 原理 → API → 步骤 → 案例 → 避坑**（进阶含项目架构 / 模块化 / 性能优化）。  
> 案例讲解：遵循 **案例代码讲解模板**（功能 → 代码 → 语法拆解 → 逐行详解 → 操作提示）。  
> API 讲解：入门/进阶 API 章节均采用 **逐词读懂** 格式（与 [01_PlayerPrefs.md](../major3/01_PlayerPrefs.md) 一致：类型 → 参数 → 整行人话）。

---

## 【全文总述】

**RPG（角色扮演游戏）世界综合案例** 是将前几章所学知识整合实践的完整项目。本章作为系列第一章，重点讲解 **项目初始化、场景搭建、玩家角色创建、基础移动、动画系统、摄像机跟随** 六大核心模块。

学习本案例，你将掌握：
- 如何从零开始搭建一个 RPG 游戏项目
- 如何创建可控制的玩家角色
- 如何实现走、跑、跳等基础移动
- 如何让动画与移动同步
- 如何让摄像机平滑跟随玩家

### 思维导图总览

```
RPG 世界综合案例（一）——项目初始化与玩家基础
│
├── 项目初始化（工程搭建 — RPG 游戏的地基）
│   │
│   ├── 定义：Unity 项目创建、文件夹结构规划、Package 配置
│   │   └── 官方：Project is a container for all your Unity assets
│   │
│   ├── 本质：游戏资源与代码的组织体系，为后续开发打下基础
│   │   ├── 文件夹结构：Scenes、Scripts、Prefabs、Resources、Materials 等
│   │   ├── Package 管理：导入必要插件（DOTween、TextMeshPro 等）
│   │   └── 项目设置：Player Settings、Quality Settings、Input Settings
│   │
│   ├── 特点
│   │   ├── 优势：结构化管理便于协作、资源分类清晰、可扩展性强
│   │   └── 局限：初期规划不当会导致后期重构成本高
│   │
│   └── 标准步骤
│       ├── 步骤1 创建 Unity 项目（3D Template）
│       ├── 步骤2 规划并创建文件夹结构
│       ├── 步骤3 配置 Package Manager
│       └── 步骤4 设置项目基础参数
│
├── 场景搭建（世界框架 — 玩家活动的舞台）
│   │
│   ├── 定义：Unity Scene 文件，包含地形、环境、灯光、玩家等
│   │   └── 官方：A Scene contains the environments and menus of your game
│   │
│   ├── 本质：游戏世界的空间容器，定义玩家可见的一切
│   │   ├── 地形系统：Terrain 组件绘制地表
│   │   ├── 光照系统：Directional Light、Ambient Light、Light Probes
│   │   └── 环境物体：树木、岩石、建筑等场景装饰
│   │
│   └── 实战：创建 RPG 游戏场景
│       ├── 创建 Terrain 地形
│       ├── 添加光照与天空盒
│       └── 放置基础环境物体
│
├── 玩家角色系统（核心实体 — 玩家控制的化身）
│   │
│   ├── 定义：玩家在游戏世界中的虚拟形象，承载移动、动画、属性等逻辑
│   │
│   ├── 本质：GameObject + 多个组件的组合体（Transform、CharacterController、Animator、脚本）
│   │   ├── Transform：位置、旋转、缩放
│   │   ├── CharacterController：移动与碰撞（替代 Rigidbody 做角色控制）
│   │   ├── Animator：播放角色动画
│   │   ├── CapsuleCollider：碰撞体积
│   │   └── PlayerController 脚本：玩家输入与逻辑
│   │
│   ├── 核心原理：输入 → 移动计算 → CharacterController.Move → 动画参数更新
│   │
│   ├── 核心 API 及参数
│   │   ├── CharacterController.Move(Vector3)：移动角色并检测碰撞
│   │   ├── CharacterController.SimpleMove(Vector3)：简化版移动（自动应用重力）
│   │   ├── CharacterController.isGrounded：是否着地
│   │   └── Animator.SetFloat("Speed", value)：设置动画速度参数
│   │
│   └── 标准使用步骤
│       ├── 步骤1 创建空 GameObject 命名 Player
│       ├── 步骤2 添加 CharacterController 组件
│       ├── 步骤3 添加 Animator 组件并指定 Controller
│       └── 步骤4 编写 PlayerController 脚本
│
├── 玩家基础移动（交互核心 — 玩家如何行动）
│   │
│   ├── 定义：通过键盘/手柄输入控制玩家位置与朝向
│   │
│   ├── 本质：Input.GetAxis → 向量计算 → CharacterController.Move → Transform 更新
│   │   ├── 输入获取：Horizontal / Vertical 轴
│   │   ├── 移动向量：Vector3(input.x, 0, input.y)
│   │   ├── 速度控制：moveSpeed * Time.deltaTime
│   │   └── 重力应用：y 轴负值累计
│   │
│   └── 实战：实现走、跑、跳
│       ├── 基础移动（WASD 控制）
│       ├── 跑步加速（Shift 键）
│       └── 跳跃（Space 键 + isGrounded 判断）
│
├── 玩家动画系统（生动表现 — 角色活起来）
│   │
│   ├── 定义：通过 Animator Controller 驱动角色骨骼动画
│   │
│   ├── 本质：脚本参数 → Animator Controller → Animation Clip → 骨骼变换
│   │   ├── Animator Controller：状态机（Idle、Walk、Run、Jump）
│   │   ├── Parameters：Speed（Float）、IsGrounded（Bool）、Jump（Trigger）
│   │   └── Transition：条件判断驱动状态切换
│   │
│   └── 实战：走跑跳动画
│       ├── 导入角色模型（FBX）
│       ├── 配置 Rig 与提取 Clip
│       ├── 创建 Animator Controller
│       └── 脚本驱动动画参数
│
├── 摄像机跟随系统（视角控制 — 玩家看世界的眼睛）
│   │
│   ├── 定义：摄像机跟随玩家移动，提供第三人称或第一人称视角
│   │
│   ├── 本质：LateUpdate 中计算相机期望位置 → Vector3.Lerp 平滑插值 → transform 更新
│   │   ├── 偏移量：相机相对玩家的位置（上、后）
│   │   ├── 平滑跟随：Vector3.Lerp 避免抖动
│   │   └── LookAt：相机始终朝向玩家
│   │
│   └── 实战：第三人称跟随相机
│       ├── 设置相机位置与偏移
│       ├── 编写 CameraFollow 脚本
│       └── LateUpdate 实现平滑跟随
│
├── 第一阶段：零基础（项目初始化 + 场景搭建）
│   ├── 理解项目结构与场景的关系
│   ├── 逐词读懂：CharacterController.Move(moveDirection)
│   └── 完成项目初始化与基础场景搭建
│
├── 第二阶段：入门（玩家移动 + 动画 + 相机）
│   ├── PlayerController 核心代码详解
│   ├── Animator Controller 制作流程
│   ├── CameraFollow 实现
│   └── 实战案例：完整玩家控制体验
│
└── 第三阶段：进阶（架构设计 + 模块化 + 优化）
    ├── 项目架构设计：分层与模块化
    ├── 玩家系统模块化封装
    ├── 性能优化：对象池、批处理、LOD
    └── 常见误区与最佳实践
```

| 学习阶段 | 学习目标 |
|----------|----------|
| **零基础** | 完成项目初始化与场景搭建；读懂 PlayerController 核心代码 |
| **入门** | 实现完整玩家控制（走跑跳）、动画系统、摄像机跟随；完成 3 个案例 |
| **进阶** | 理解项目架构设计；会模块化封装；掌握性能优化技巧 |

### 讲师知识框架速览（全文脉络）

| 维度 | 零基础讲 | 入门讲 | 进阶讲 |
|------|----------|--------|--------|
| 定义 | ✅ | 回顾 | 回顾 |
| 本质 | ✅ | — | — |
| 特点 | ✅ | — | 架构特点 |
| 适用场景 | ✅ | — | 项目选型 |
| 核心原理 | 项目结构 | ✅ 移动+动画链路 | 模块化设计 |
| 核心 API | 读懂 Move | ✅ CharacterController + Animator | 封装与优化 |
| 使用步骤 | 初始化步骤 | ✅ 玩家创建步骤 | 架构搭建 |
| 调用时机 | — | ✅ Update/LateUpdate | 生命周期管理 |
| 避坑 | — | 初步 | ✅ |

---

# 第一阶段：零基础篇

## 【阶段总述】

零基础阶段建立**正确认知**：RPG 项目从哪里开始、场景是什么、玩家角色由哪些部分组成。  
同时学会**读懂** `characterController.Move(moveDirection)` 每个部分的含义，并完成项目初始化与基础场景搭建。

---

## 一、定义 — RPG 项目是什么？

| 项目 | 说明 |
|------|------|
| **Unity Project** | Unity 工程文件，包含所有游戏资源和代码 |
| **Scene** | 场景文件，包含地形、环境、玩家、灯光等游戏世界内容 |
| **Player** | 玩家角色，由 GameObject + 多个组件组成 |
| **CharacterController** | Unity 角色控制组件，用于移动和碰撞检测 |
| **一句话** | RPG 项目 = 场景（世界）+ 玩家（角色）+ 系统（战斗/任务/存档） |

```
RPG 项目结构示例
Project/
├── Assets/
│   ├── Scenes/           # 场景文件
│   ├── Scripts/          # C# 脚本
│   │   ├── Player/       # 玩家相关脚本
│   │   ├── UI/           # UI 相关脚本
│   │   └── System/       # 系统脚本（任务、存档等）
│   ├── Prefabs/          # 预制体（玩家、怪物、道具）
│   ├── Resources/        # 动态加载资源
│   ├── Materials/        # 材质
│   ├── Models/           # 3D 模型（FBX）
│   ├── Animations/       # 动画资产
│   └── Textures/         # 纹理贴图
└── ProjectSettings/      # 项目设置
```

---

## 二、本质 — 项目如何组织？

### 2.1 文件夹结构本质

| 文件夹 | 作用 | 本质理解 |
|--------|------|----------|
| **Scenes** | 存放场景文件 | 游戏世界的空间容器 |
| **Scripts** | 存放 C# 脚本 | 游戏逻辑的实现 |
| **Prefabs** | 存放预制体 | 可复用的游戏对象模板 |
| **Models** | 存放 3D 模型 | 角色、怪物、道具的视觉外观 |
| **Animations** | 存放动画资产 | 角色动作的数据 |
| **Resources** | 存放动态加载资源 | 运行时按需加载的内容 |

### 2.2 玩家角色本质

```
Player GameObject
    ├── Transform（位置/旋转/缩放）
    ├── CharacterController（移动 + 碰撞）
    ├── CapsuleCollider（碰撞体积）
    ├── Animator（动画播放）
    ├── SkinnedMeshRenderer（网格渲染）
    └── PlayerController.cs（输入与逻辑）
```

**本质理解**：玩家是一个「组件组合体」，每个组件负责一项功能，脚本负责协调它们。

---

## 三、特点与适用场景

### 3.1 项目结构特点

| 特点 | 说明 |
|------|------|
| **结构化** | 资源分类清晰，便于管理和查找 |
| **可扩展** | 新增功能只需在对应文件夹添加资源 |
| **可协作** | 多人开发时不会互相覆盖文件 |
| **可维护** | 逻辑分离，修改一处不影响其他部分 |

### 3.2 RPG 游戏适用场景

| 场景 | 是否适用 | 原因 |
|------|----------|------|
| 开放世界探索 | ✅ | 地形系统支持大地图 |
| 角色成长系统 | ✅ | 组件化设计便于扩展属性 |
| 战斗系统 | ✅ | 状态机模式适合战斗逻辑 |
| 任务系统 | ✅ | 数据驱动便于策划配置 |

---

## 四、核心一课：如何读懂角色移动

```csharp
characterController.Move(moveDirection);
```

| 部分 | 含义 |
|------|------|
| `characterController` | CharacterController 组件引用 |
| `.Move` | 方法名：移动角色并检测碰撞 |
| `moveDirection` | 参数：Vector3 移动方向（含速度） |

**整行人话**：让角色按照 moveDirection 的方向和速度移动，同时处理碰撞检测。

```csharp
// 完整的移动代码片段
Vector3 move = new Vector3(h, 0, v).normalized;
move *= moveSpeed * Time.deltaTime;
characterController.Move(move);
```

| 行 | 含义 |
|----|------|
| `new Vector3(h, 0, v)` | 由水平/垂直输入合成移动向量 |
| `.normalized` | 归一化：对角线移动速度不超过单轴 |
| `* moveSpeed * Time.deltaTime` | 乘以速度和时间，得到帧位移 |
| `characterController.Move(move)` | 执行移动 |

---

## 五、零基础实战：项目初始化

### 5.1 步骤一：创建项目

1. 打开 Unity Hub，点击 **New Project**
2. 选择 **3D** Template
3. 输入项目名 **RPGWorld**，选择保存路径
4. 点击 **Create**

### 5.2 步骤二：创建文件夹结构

在 Project 窗口右键 → **Create Folder**，创建以下文件夹：

```
Assets/
├── Scenes/
├── Scripts/
│   ├── Player/
│   ├── UI/
│   └── System/
├── Prefabs/
├── Resources/
├── Materials/
├── Models/
├── Animations/
└── Textures/
```

### 5.3 步骤三：配置 Package Manager

1. 菜单 **Window → Package Manager**
2. 确保以下 Package 已安装：
   - **TextMeshPro**（UI 文字）
   - **DOTween**（补间动画，需从 Asset Store 导入）

### 5.4 步骤四：创建基础场景

1. 菜单 **File → New Scene**，保存到 `Scenes/MainScene.unity`
2. 删除默认的 SampleScene
3. 添加 Directional Light（调整角度为从右上方照射）
4. 添加 Terrain（菜单 **GameObject → 3D Object → Terrain**）

---

## 【零基础阶段小结】

| 维度 | 要点 |
|------|------|
| **定义** | Project = 工程；Scene = 世界；Player = 组件组合体 |
| **本质** | 资源结构化管理；玩家由多个组件协作 |
| **步骤** | 创建项目 → 建文件夹 → 配 Package → 建场景 |
| **读懂** | `characterController.Move(moveDirection)` |

**阶段检验**：能说出项目文件夹结构；能画出玩家组件关系图；能读懂基本移动代码。

---

# 第二阶段：入门篇

## 【阶段总述】

入门阶段掌握 **玩家移动、动画系统、摄像机跟随** 三大核心模块，并完成 3 个实战案例。  
重点：**Update 处理输入**；**LateUpdate 做相机跟随**；**Animator 参数驱动动画**。

---

## 一、PlayerController 核心代码详解

### 1.1 CharacterController API — 逐词读懂

#### `characterController.Move(moveDirection)` 是什么？

```csharp
characterController.Move(moveDirection);
```

| 部分 | 含义 |
|------|------|
| `characterController` | CharacterController 组件引用 |
| `.Move` | **方法名**：移动角色，参数为每帧位移向量 |
| `moveDirection` | **参数**：Vector3，**含速度和方向**（单位：世界单位/帧） |
| **作用** | 移动角色并与 Collider 碰撞，不会穿墙 |

**整行人话**：让角色按指定方向和距离移动一帧，并处理碰撞。

#### `characterController.SimpleMove(speed)` 是什么？

```csharp
characterController.SimpleMove(speed);
```

| 部分 | 含义 |
|------|------|
| `SimpleMove` | **方法名**：简化版移动，自动应用重力 |
| `speed` | **参数**：Vector3，**速度向量**（单位：世界单位/秒） |
| **区别** | Move 需要自己算重力；SimpleMove 自带重力 |

**整行人话**：自动处理重力的简单移动，适合不需要复杂跳跃的场景。

#### `characterController.isGrounded` 是什么？

```csharp
if (characterController.isGrounded)
{
    // 可以跳跃
}
```

| 部分 | 含义 |
|------|------|
| `isGrounded` | **属性**：bool，角色是否站在地面上 |
| **用途** | 判断能否跳跃、是否应用重力 |

**整行人话**：查角色脚底下有没有地。

---

### 1.2 PlayerController 完整代码

```csharp
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    CharacterController controller;
    Animator animator;

    public float walkSpeed = 5f;
    public float runSpeed = 8f;
    public float jumpHeight = 2f;
    public float gravity = 9.8f;

    float currentSpeed;
    Vector3 velocity;
    bool isRunning;

    void Awake()
    {
        controller = GetComponent<CharacterController>();
        animator = GetComponent<Animator>();
    }

    void Update()
    {
        float h = Input.GetAxisRaw("Horizontal");
        float v = Input.GetAxisRaw("Vertical");
        Vector3 move = new Vector3(h, 0, v).normalized;

        isRunning = Input.GetKey(KeyCode.LeftShift);
        currentSpeed = isRunning ? runSpeed : walkSpeed;

        if (move.magnitude >= 0.1f)
        {
            transform.rotation = Quaternion.LookRotation(move);
            controller.Move(move * currentSpeed * Time.deltaTime);
        }

        if (controller.isGrounded && velocity.y < 0)
        {
            velocity.y = -2f;
        }

        if (Input.GetKeyDown(KeyCode.Space) && controller.isGrounded)
        {
            velocity.y = Mathf.Sqrt(jumpHeight * 2f * gravity);
        }

        velocity.y -= gravity * Time.deltaTime;
        controller.Move(velocity * Time.deltaTime);

        animator.SetFloat("Speed", currentSpeed * move.magnitude);
        animator.SetBool("IsRunning", isRunning);
        animator.SetBool("IsGrounded", controller.isGrounded);
    }
}
```

#### 语法拆解

##### `Quaternion.LookRotation(move)` 是什么？

```csharp
transform.rotation = Quaternion.LookRotation(move);
```

| 部分 | 含义 |
|------|------|
| `Quaternion` | 四元数类型，用于表示旋转 |
| `LookRotation` | 静态方法，创建看向指定方向的旋转 |
| `move` | 方向向量，角色将面向此方向 |

**整行人话**：让角色朝向移动方向。

##### `Mathf.Sqrt(jumpHeight * 2f * gravity)` 是什么？

```csharp
velocity.y = Mathf.Sqrt(jumpHeight * 2f * gravity);
```

| 部分 | 含义 |
|------|------|
| `Mathf.Sqrt` | 平方根函数 |
| `jumpHeight * 2f * gravity` | 物理公式：v² = 2gh，求初速度 |

**整行人话**：计算能跳到指定高度所需的初始向上速度。

---

## 二、Animator Controller 制作流程

### 2.1 导入角色模型

1. 将 FBX 角色模型拖入 `Models/` 文件夹
2. 在 Inspector 中设置 **Rig** 选项卡：
   - Animation Type：Humanoid（人形角色）
   - 点击 **Configure** 检查骨骼映射
   - 点击 **Apply**
3. 在 **Animation** 选项卡勾选需要的 Clip（Idle、Walk、Run、Jump）

### 2.2 创建 Animator Controller

1. Project 窗口右键 → **Create → Animator Controller**
2. 保存到 `Animations/PlayerController.controller`
3. 双击打开 Animator 窗口

### 2.3 设置 Parameters

在 Animator 窗口点击 **Parameters → +**：

| 参数名 | 类型 | 用途 |
|--------|------|------|
| Speed | Float | 控制 Idle/Walk/Run 过渡 |
| IsRunning | Bool | 跑步状态 |
| IsGrounded | Bool | 是否着地 |
| Jump | Trigger | 触发跳跃 |

### 2.4 创建 State 与 Transition

| State | Clip | Transition 条件 |
|-------|------|-----------------|
| Idle | Idle.clip | Speed < 0.1 |
| Walk | Walk.clip | Speed >= 0.1 且 IsRunning = false |
| Run | Run.clip | IsRunning = true |
| Jump | Jump.clip | Jump Trigger |

---

## 三、CameraFollow 实现

### 3.1 CameraFollow 完整代码

```csharp
using UnityEngine;

public class CameraFollow : MonoBehaviour
{
    public Transform target;
    public Vector3 offset = new Vector3(0f, 5f, -10f);
    public float smoothSpeed = 5f;

    void LateUpdate()
    {
        if (target == null) return;

        Vector3 desiredPos = target.position + offset;
        transform.position = Vector3.Lerp(
            transform.position, desiredPos, smoothSpeed * Time.deltaTime);
        transform.LookAt(target);
    }
}
```

#### 语法拆解

##### `void LateUpdate()` 是什么？

```csharp
void LateUpdate()
```

| 部分 | 含义 |
|------|------|
| `LateUpdate` | Unity 生命周期函数，在**所有 Update 执行完后**调用 |
| **用途** | 相机跟随：目标先在 Update 移动，相机再在 LateUpdate 跟随 |

**整行人话**：等玩家动完，相机再跟上去，避免抖动。

##### `Vector3.Lerp(a, b, t)` 是什么？

```csharp
transform.position = Vector3.Lerp(transform.position, desiredPos, smoothSpeed * Time.deltaTime);
```

| 部分 | 含义 |
|------|------|
| `Vector3.Lerp` | 在 a 和 b 之间按 t（0~1）线性插值 |
| `smoothSpeed * Time.deltaTime` | 每帧推进的比例 |

**整行人话**：相机平滑地靠近目标位置，不是瞬间跳过去。

---

## 四、入门三个案例

### 案例代码讲解模板

每个案例统一按以下结构组织：

| 顺序 | 板块 | 内容 |
|:----:|------|------|
| 1 | **功能** | 案例实现什么业务 |
| 2 | **完整代码** | 带行内注释的完整脚本 |
| 3 | **语法拆解** | 对案例中较生僻的语法，逐个说明 |
| 4 | **逐行详解** | 表格：每行代码的含义 |
| 5 | **操作提示** | Unity 绑定、调用方式等 |

---

### 案例 1：玩家基础移动

**功能**：WASD 控制玩家移动，Shift 加速跑，Space 跳跃。

```csharp
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    CharacterController controller;

    public float walkSpeed = 5f;
    public float runSpeed = 8f;
    public float jumpHeight = 2f;
    public float gravity = 9.8f;

    Vector3 velocity;

    void Awake()
    {
        controller = GetComponent<CharacterController>();
    }

    void Update()
    {
        float h = Input.GetAxisRaw("Horizontal");
        float v = Input.GetAxisRaw("Vertical");
        Vector3 move = new Vector3(h, 0, v).normalized;

        if (move.magnitude > 0)
        {
            transform.rotation = Quaternion.LookRotation(move);
            float speed = Input.GetKey(KeyCode.LeftShift) ? runSpeed : walkSpeed;
            controller.Move(move * speed * Time.deltaTime);
        }

        if (controller.isGrounded && velocity.y < 0)
        {
            velocity.y = -2f;
        }

        if (Input.GetKeyDown(KeyCode.Space) && controller.isGrounded)
        {
            velocity.y = Mathf.Sqrt(jumpHeight * 2f * gravity);
        }

        velocity.y -= gravity * Time.deltaTime;
        controller.Move(velocity * Time.deltaTime);
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
| `Input` | Unity 输入类 |
| `GetAxisRaw` | 获取原始轴值（-1、0、1），无平滑 |
| `"Horizontal"` | 水平轴（A/D、左右箭头） |

**整行人话**：读键盘水平方向输入。

##### `move.normalized` 是什么？

```csharp
Vector3 move = new Vector3(h, 0, v).normalized;
```

| 部分 | 含义 |
|------|------|
| `normalized` | 向量归一化，长度变为 1 |
| **用途** | 对角线移动时速度不超过单轴 |

**整行人话**：确保前后左右移动速度一致。

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 5 | `CharacterController controller` | 声明控制器变量 |
| 7~10 | 速度/跳跃/重力参数 | Inspector 可调 |
| 12 | `Vector3 velocity` | 垂直方向速度（重力+跳跃） |
| 14 | `void Awake()` | 初始化 |
| 16 | `GetComponent<CharacterController>()` | 获取控制器组件 |
| 18 | `void Update()` | 每帧执行 |
| 20~21 | 读水平/垂直输入 | 见上方语法拆解 |
| 22 | `move.normalized` | 见上方语法拆解 |
| 24 | `move.magnitude > 0` | 有输入才移动 |
| 26 | `LookRotation(move)` | 面向移动方向 |
| 27 | 三目运算符选速度 | Shift 跑，否则走 |
| 28 | `controller.Move(...)` | 执行移动 |
| 30~32 | 着地重置垂直速度 | 防止无限下落 |
| 34~36 | 跳跃判断 | Space + 着地 |
| 38 | 重力累加 | 每帧加向下的力 |
| 39 | 应用垂直移动 | 执行重力/跳跃 |

#### 操作提示

脚本挂到 Player；Player 需有 **CharacterController** 组件；调整参数直到手感满意。

---

### 案例 2：玩家动画系统

**功能**：根据移动速度驱动 Idle/Walk/Run 动画切换。

```csharp
using UnityEngine;

public class PlayerAnimation : MonoBehaviour
{
    CharacterController controller;
    Animator animator;

    public float walkSpeed = 5f;
    public float runSpeed = 8f;

    void Awake()
    {
        controller = GetComponent<CharacterController>();
        animator = GetComponent<Animator>();
    }

    void Update()
    {
        float h = Input.GetAxisRaw("Horizontal");
        float v = Input.GetAxisRaw("Vertical");
        Vector3 move = new Vector3(h, 0, v).normalized;

        bool isRunning = Input.GetKey(KeyCode.LeftShift);
        float currentSpeed = isRunning ? runSpeed : walkSpeed;

        animator.SetFloat("Speed", currentSpeed * move.magnitude);
        animator.SetBool("IsRunning", isRunning);
        animator.SetBool("IsGrounded", controller.isGrounded);

        if (Input.GetKeyDown(KeyCode.Space) && controller.isGrounded)
        {
            animator.SetTrigger("Jump");
        }
    }
}
```

#### 语法拆解

##### `animator.SetFloat("Speed", value)` 是什么？

```csharp
animator.SetFloat("Speed", currentSpeed * move.magnitude);
```

| 部分 | 含义 |
|------|------|
| `SetFloat` | 设置 Animator 中 Float 类型参数 |
| `"Speed"` | 参数名，须与 Controller Parameters 一致 |
| `currentSpeed * move.magnitude` | 实际速度值 |

**整行人话**：告诉状态机当前速度，驱动 Idle/Walk/Run 切换。

##### `animator.SetTrigger("Jump")` 是什么？

```csharp
animator.SetTrigger("Jump");
```

| 部分 | 含义 |
|------|------|
| `SetTrigger` | 设置 Trigger 类型参数（一次性脉冲） |
| `"Jump"` | 参数名 |

**整行人话**：触发跳跃动画一次。

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 5~6 | 控制器和动画器引用 | 缓存组件 |
| 8~9 | 速度参数 | 与移动脚本一致 |
| 11~14 | 初始化 | 获取组件 |
| 16 | `void Update()` | 每帧更新动画参数 |
| 18~20 | 读输入 | 同上 |
| 22 | 判断跑步 | Shift 键 |
| 23 | 当前速度 | 跑或走 |
| 25~27 | 设置动画参数 | 速度、跑步、着地 |
| 29~31 | 跳跃触发 | Space + 着地 |

#### 操作提示

Animator Controller 中需定义 **Speed（Float）**、**IsRunning（Bool）**、**IsGrounded（Bool）**、**Jump（Trigger）**；Transition 条件与参数对应。

---

### 案例 3：第三人称跟随相机

**功能**：相机在玩家后方上方平滑跟随，始终看向玩家。

```csharp
using UnityEngine;

public class ThirdPersonCamera : MonoBehaviour
{
    public Transform target;
    public Vector3 offset = new Vector3(0f, 5f, -10f);
    public float smoothSpeed = 5f;
    public float rotationSpeed = 3f;

    float currentRotation = 0f;

    void LateUpdate()
    {
        if (target == null) return;

        currentRotation += Input.GetAxis("Mouse X") * rotationSpeed;
        Quaternion rotation = Quaternion.Euler(0f, currentRotation, 0f);

        Vector3 desiredPos = target.position + rotation * offset;
        transform.position = Vector3.Lerp(
            transform.position, desiredPos, smoothSpeed * Time.deltaTime);
        transform.LookAt(target);
    }
}
```

#### 语法拆解

##### `Quaternion.Euler(0f, currentRotation, 0f)` 是什么？

```csharp
Quaternion rotation = Quaternion.Euler(0f, currentRotation, 0f);
```

| 部分 | 含义 |
|------|------|
| `Quaternion.Euler` | 用欧拉角创建四元数旋转 |
| `currentRotation` | Y 轴旋转角度（鼠标控制） |

**整行人话**：根据鼠标输入创建绕 Y 轴的旋转。

##### `rotation * offset` 是什么？

```csharp
Vector3 desiredPos = target.position + rotation * offset;
```

| 部分 | 含义 |
|------|------|
| `rotation * offset` | 将偏移向量旋转后加到目标位置 |
| **效果** | 相机围绕玩家旋转，保持相对位置 |

**整行人话**：相机跟随玩家旋转，始终在玩家后方。

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 5 | `Transform target` | 跟随目标（玩家） |
| 6 | `offset` | 相机相对玩家的偏移 |
| 7 | `smoothSpeed` | 跟随平滑度 |
| 8 | `rotationSpeed` | 鼠标旋转灵敏度 |
| 10 | `currentRotation` | 当前旋转角度 |
| 12 | `void LateUpdate()` | 见上方语法拆解 |
| 14 | 空引用判断 | 安全检查 |
| 16 | 鼠标旋转累加 | 读 Mouse X 轴 |
| 17 | 创建旋转 | 见上方语法拆解 |
| 19 | 计算期望位置 | 目标位置 + 旋转后的偏移 |
| 20~22 | 平滑插值 | Lerp 避免抖动 |
| 23 | `LookAt(target)` | 相机看向玩家 |

#### 操作提示

脚本挂到 Main Camera；Inspector 将 Player 拖到 **Target**；调整 offset 和 smoothSpeed 直到视角舒适。

---

## 【入门阶段小结】

| 维度 | 要点 |
|------|------|
| **移动** | CharacterController.Move、重力、跳跃公式 |
| **动画** | Animator.SetFloat / SetBool / SetTrigger |
| **相机** | LateUpdate + Lerp + LookAt |
| **案例** | 基础移动、动画系统、第三人称相机 |

---

# 第三阶段：进阶篇

## 【阶段总述】

进阶阶段：**项目架构设计**、**玩家系统模块化封装**、**性能优化**、**常见误区与最佳实践**。

---

## 一、项目架构设计

### 1.1 分层架构

```
RPG 项目架构
├── Presentation 层（表现层）
│   ├── UI 系统（Canvas、面板、按钮）
│   ├── 动画系统（Animator、DOTween）
│   └── 音效系统（AudioSource、AudioClip）
│
├── Gameplay 层（游戏逻辑层）
│   ├── 玩家系统（移动、动画、属性）
│   ├── 战斗系统（攻击、受伤、死亡）
│   ├── AI 系统（怪物行为）
│   └── 交互系统（对话、拾取）
│
├── Data 层（数据层）
│   ├── 配置数据（JSON、ScriptableObject）
│   ├── 存档系统（PlayerPrefs、JsonUtility）
│   └── 任务数据（任务列表、进度）
│
└── Infrastructure 层（基础设施层）
    ├── 事件系统（EventManager）
    ├── 资源管理（ResourceManager）
    ├── 工具类（Singleton、Extensions）
    └── 对象池（ObjectPool）
```

### 1.2 模块化设计原则

| 原则 | 说明 |
|------|------|
| **单一职责** | 每个脚本只做一件事 |
| **依赖注入** | 通过引用传递依赖，不硬编码 |
| **事件驱动** | 通过事件解耦模块 |
| **接口抽象** | 用接口定义行为，便于扩展 |

---

## 二、玩家系统模块化封装

### 2.1 PlayerSystem 封装

```csharp
using UnityEngine;

public class PlayerSystem : MonoBehaviour
{
    public static PlayerSystem Instance { get; private set; }

    public PlayerMovement Movement { get; private set; }
    public PlayerAnimation Animation { get; private set; }
    public PlayerStats Stats { get; private set; }

    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }

        Movement = GetComponent<PlayerMovement>();
        Animation = GetComponent<PlayerAnimation>();
        Stats = GetComponent<PlayerStats>();
    }
}
```

### 2.2 PlayerStats 属性系统

```csharp
using UnityEngine;

public class PlayerStats : MonoBehaviour
{
    public int maxHealth = 100;
    public int currentHealth;
    public int attack = 10;
    public int defense = 5;

    void Awake()
    {
        currentHealth = maxHealth;
    }

    public void TakeDamage(int damage)
    {
        currentHealth = Mathf.Max(0, currentHealth - damage);
        if (currentHealth <= 0)
        {
            Die();
        }
    }

    void Die()
    {
        Debug.Log("玩家死亡");
    }
}
```

---

## 三、性能优化

### 3.1 对象池

```csharp
using UnityEngine;
using System.Collections.Generic;

public class ObjectPool : MonoBehaviour
{
    public static ObjectPool Instance;

    public GameObject prefab;
    public int poolSize = 10;

    Queue<GameObject> pool;

    void Awake()
    {
        Instance = this;
        pool = new Queue<GameObject>();

        for (int i = 0; i < poolSize; i++)
        {
            GameObject obj = Instantiate(prefab);
            obj.SetActive(false);
            pool.Enqueue(obj);
        }
    }

    public GameObject Get()
    {
        if (pool.Count > 0)
        {
            GameObject obj = pool.Dequeue();
            obj.SetActive(true);
            return obj;
        }
        else
        {
            GameObject obj = Instantiate(prefab);
            return obj;
        }
    }

    public void Return(GameObject obj)
    {
        obj.SetActive(false);
        pool.Enqueue(obj);
    }
}
```

### 3.2 批处理与 LOD

| 优化手段 | 说明 |
|----------|------|
| **GPU Instancing** | 相同材质的物体批量渲染 |
| **LOD Group** | 远距离物体显示低精度模型 |
| **Occlusion Culling** | 遮挡剔除，不渲染被挡住的物体 |
| **Static Batching** | 静态物体合并批次 |

---

## 四、常见误区与最佳实践

| 误区 | 正确做法 |
|------|----------|
| 用 Rigidbody 做角色移动 | 用 CharacterController，更适合 RPG |
| Update 做相机跟随 | 改 LateUpdate |
| 每帧调用 Camera.main | Awake 缓存 |
| 动画不播 | 检查 Animator 是否指定 Controller |
| 跳跃无限跳 | 用 isGrounded 判断 |
| 脚本耦合严重 | 用事件系统解耦 |
| 频繁 Instantiate/Destroy | 用对象池 |

---

## 【进阶阶段小结】

| 维度 | 要点 |
|------|------|
| 架构 | 分层设计、模块化、单一职责 |
| 封装 | PlayerSystem 单例、PlayerStats 属性 |
| 优化 | 对象池、LOD、批处理 |
| 避坑 | CharacterController、LateUpdate、解耦 |

---

# 【全文总结】

## 最重要的一行代码

```csharp
characterController.Move(move * speed * Time.deltaTime);
```

| 部分 | 含义 |
|------|------|
| `characterController` | 角色控制器 |
| `Move` | 移动方法 |
| `move * speed * Time.deltaTime` | 方向 × 速度 × 时间 = 帧位移 |

## 三阶段对照

| 阶段 | 代表案例 |
|------|----------|
| 零基础 | 项目初始化、场景搭建 |
| 入门 | 玩家移动、动画系统、第三人称相机 |
| 进阶 | 架构设计、模块化封装、性能优化 |

## API 速查

| 代码 | 作用 |
|------|------|
| `CharacterController.Move()` | 移动角色 |
| `CharacterController.isGrounded` | 是否着地 |
| `Animator.SetFloat()` | 设置动画参数 |
| `Vector3.Lerp()` | 平滑插值 |
| `Quaternion.LookRotation()` | 面向指定方向 |

## 学习自检

- [ ] 能独立创建 RPG 项目并搭建场景
- [ ] 能实现玩家走跑跳移动
- [ ] 能制作 Animator Controller 并驱动动画
- [ ] 能实现第三人称跟随相机
- [ ] 理解项目架构分层设计

---

## 参考资料

| 类型 | 链接 |
|------|------|
| CharacterController | https://docs.unity3d.com/ScriptReference/CharacterController.html |
| Animator | https://docs.unity3d.com/ScriptReference/Animator.html |
| Camera | https://docs.unity3d.com/ScriptReference/Camera.html |
| Scene Management | https://docs.unity3d.com/Manual/SceneManagement.html |

---

*文档版本：与 major3 系列、Week2_Xmind、Week3_Xmind 同系列模板。*