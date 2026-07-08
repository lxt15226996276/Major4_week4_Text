# Unity 射线 Raycast 详解

> 参照：[Unity Scripting API - Ray](https://docs.unity3d.com/ScriptReference/Ray.html) · [Physics.Raycast](https://docs.unity3d.com/ScriptReference/Physics.Raycast.html) · [RaycastHit](https://docs.unity3d.com/ScriptReference/RaycastHit.html) · [Physics2D.Raycast](https://docs.unity3d.com/ScriptReference/Physics2D.Raycast.html)  
> 关联文档：[02_Camera.md](./02_Camera.md)（ScreenPointToRay 与坐标空间）  
> 学习路径：**零基础 → 入门 → 进阶**，每阶段采用 **总—分—总** 结构。  
> 讲解维度：**定义 → 本质 → 特点 → 适用场景 → 原理 → API → 步骤 → 案例 → 避坑**（进阶含 LayerMask / RaycastAll / 2D）。  
> 案例讲解：遵循 **案例代码讲解模板**（功能 → 代码 → 语法拆解 → 逐行详解 → 操作提示）。  
> API 讲解：入门/进阶 API 章节均采用 **逐词读懂** 格式（与 [01_PlayerPrefs.md](./01_PlayerPrefs.md) 一致：类型 → 参数 → 整行人话）。

---

## 【全文总述】

**射线（Ray）** 是 Unity 中「从一点沿一个方向无限延伸的直线」的数学表示；**射线检测（Raycast）** 则是让这条线去「打」场景里的 **Collider**，判断碰到了什么、打在哪里。  
3D 点击选物体、地面移动、射击判定、视线检测，底层几乎都是 **Camera.ScreenPointToRay + Physics.Raycast** 或 **Physics.Raycast(origin, direction)**。  
本文从 Ray / RaycastHit 概念到 3D / 2D 实战，逐层展开。

### 思维导图总览

```
Unity 射线 Raycast
│
├── 射线体系（Ray + Physics 物理查询 — 3D 碰撞检测核心手段）
│   │
│   ├── 【知识维度】（讲师框架 — 完整版）
│   │   │
│   │   ├── 定义：从起点沿方向发射的无限直线，用于检测与 Collider 的交点
│   │   │   ├── Ray 结构体：origin（起点）+ direction（方向）
│   │   │   └── Physics.Raycast：让射线与场景中 Collider 做相交测试
│   │   │
│   │   ├── 本质：数学射线 + 物理引擎碰撞查询（非渲染、非子弹实体）
│   │   │   ├── Ray：只描述「从哪、往哪」，不自动产生碰撞
│   │   │   ├── Physics.Raycast：调用 PhysX，返回最近命中 Collider
│   │   │   └── RaycastHit：命中结果（点、法线、距离、物体引用）
│   │   │
│   │   ├── 官方定位：Gameplay 交互与物理查询的标准 API
│   │   │   ├── 设计用途：鼠标点击、射击、视线、地面检测、拖拽放置
│   │   │   └── 前提：被检测物体必须有 Collider（3D）或 Collider2D（2D）
│   │   │
│   │   ├── 特点
│   │   │   ├── 优势：精确、开销可控、与 Layer 过滤配合灵活、与相机坐标转换无缝衔接
│   │   │   └── 局限：起点在 Collider 内部时 3D 可能检测不到；需 Collider；2D/3D API 不同
│   │   │
│   │   ├── 适用场景
│   │   │   ├── ✅ 适用：点击选单位、点地移动、FPS 射击、地面检测、UI 穿透 3D 物体
│   │   │   └── ❌ 不适用：纯 2D 像素精确点选（可用 OverlapPoint）；大范围 AoE（用 OverlapSphere）
│   │   │
│   │   ├── 核心原理：起点 + 方向 + 最大距离 → 物理引擎求最近交点
│   │   │   ├── 屏幕点击链：鼠标 Screen 坐标 → Camera.ScreenPointToRay → Ray → Physics.Raycast
│   │   │   ├── 角色前方检测：transform.position + transform.forward → Physics.Raycast
│   │   │   └── 返回 bool；true 时 RaycastHit 含 point / normal / collider / distance
│   │   │
│   │   ├── 核心 API 及参数
│   │   │   ├── Ray：new Ray(origin, direction) / ray.GetPoint(distance)
│   │   │   ├── Physics.Raycast 重载：
│   │   │   │   ├── Raycast(origin, direction) → bool
│   │   │   │   ├── Raycast(origin, direction, out hit) → bool + 命中信息
│   │   │   │   ├── Raycast(origin, direction, maxDistance, layerMask) → 带距离与 Layer 过滤
│   │   │   │   └── Raycast(ray, out hit, maxDistance, layerMask) → 传入 Ray 结构体
│   │   │   ├── RaycastHit 常用：point / normal / distance / collider / transform
│   │   │   ├── Camera.ScreenPointToRay(screenPos) → 屏幕点转世界射线
│   │   │   ├── Physics.RaycastAll → 返回所有命中（非仅最近）
│   │   │   ├── Physics.SphereCast → 粗射线（带半径，适合角色体型检测）
│   │   │   └── Physics2D.Raycast → 2D 专用，返回 RaycastHit2D
│   │   │
│   │   ├── 标准使用步骤（四步 — 3D 点击为例）
│   │   │   ├── 步骤1 获取射线：Camera.main.ScreenPointToRay(Input.mousePosition)
│   │   │   ├── 步骤2 执行检测：Physics.Raycast(ray, out hit, maxDistance, layerMask)
│   │   │   ├── 步骤3 判断返回值：true 表示命中，读 hit.point / hit.collider
│   │   │   └── 步骤4 业务逻辑：移动、选中、播放特效、改材质等
│   │   │
│   │   ├── 生命周期与调用时机
│   │   │   ├── Update：鼠标点击、即时交互（官方示例亦常用）
│   │   │   ├── FixedUpdate：与刚体/物理同步的连续检测（地面、前方障碍）
│   │   │   └── 注意：物理查询在 FixedUpdate 中与刚体结果更一致
│   │   │
│   │   ├── LayerMask 与 Trigger
│   │   │   ├── layerMask：只检测指定 Layer 的 Collider
│   │   │   ├── LayerMask.GetMask("Ground", "Enemy") 构建掩码
│   │   │   ├── QueryTriggerInteraction：是否命中 Is Trigger 的 Collider
│   │   │   └── Physics.queriesHitTriggers 全局默认行为
│   │   │
│   │   ├── 调试
│   │   │   ├── Debug.DrawRay(origin, direction * length, color, duration)
│   │   │   └── Debug.DrawLine(ray.origin, hit.point) 可视化命中段
│   │   │
│   │   └── 选型、封装、避坑
│   │       ├── 选型：单点最近 → Raycast；穿透多物体 → RaycastAll；2D → Physics2D
│   │       ├── 封装：RaycastHelper.TryRaycastFromMouse(out hit)
│   │       └── 避坑：缺 Collider、Layer 不对、Trigger 被忽略、2D/3D 混用、方向未归一化
│   │
│   ├── 第一阶段：零基础（建立认知 + 读懂代码）
│   │   ├── 理解 Ray / Raycast / RaycastHit 分别是什么
│   │   ├── 逐词读懂：Physics.Raycast(ray, out RaycastHit hit)
│   │   └── 认识 Collider 是射线检测的前提
│   │
│   ├── 第二阶段：入门（API + 步骤 + 案例）
│   │   ├── Physics.Raycast 重载与 RaycastHit 属性
│   │   ├── ScreenPointToRay 与点击检测四步流程
│   │   └── 实战案例：点击选中 / 点地移动 / 2D 地面检测
│   │
│   └── 第三阶段：进阶（LayerMask + 多命中 + 封装 + 2D/3D 对比）
│       ├── LayerMask、maxDistance、QueryTriggerInteraction
│       ├── RaycastAll / SphereCast / Linecast 对比
│       ├── RaycastHelper 封装 + Debug 可视化
│       └── Physics2D 与 3D 差异、常见避坑清单
│
└── Physics2D 射线（2D 物理 — Collider2D 检测）
    │
    ├── 定义：在 XY 平面做射线检测，返回 RaycastHit2D
    ├── 本质：Physics2D.Raycast(origin, direction) 或 Camera.ScreenToWorldPoint 转世界坐标后检测
    ├── 常用：平台游戏地面检测、2D 点击（需把屏幕坐标转世界坐标）
    └── 与 3D 区别：无 ScreenPointToRay 直接 2D 版；用 Collider2D；注意 Z 轴 depth 过滤
```

| 学习阶段 | 学习目标 |
|----------|----------|
| **零基础** | 说清 Ray、Raycast、RaycastHit；读懂 `Physics.Raycast(ray, out hit)` |
| **入门** | 掌握重载参数、ScreenPointToRay 四步流程；完成 3 个案例 |
| **进阶** | 会 LayerMask / RaycastAll；封装 Helper；区分 2D 与 3D |

### 讲师知识框架速览（全文脉络）

| 维度 | 零基础讲 | 入门讲 | 进阶讲 |
|------|----------|--------|--------|
| 定义 | ✅ | 回顾 | 回顾 |
| 本质 | ✅ | — | — |
| 特点 | ✅ | — | — |
| 适用场景 | ✅ | — | 选型（Raycast vs Overlap） |
| 核心原理 | 射线 + 碰撞 | ✅ ScreenPointToRay 链路 | Layer / Trigger |
| 核心 API | 读懂 Raycast | ✅ 重载 + RaycastHit | RaycastAll / SphereCast |
| 使用步骤 | Collider 前提 | ✅ 四步流程 | 封装 |
| 调用时机 | — | ✅ Update 点击 | FixedUpdate 物理 |
| 避坑 | — | 初步 | ✅ |

---

# 第一阶段：零基础篇

## 【阶段总述】

零基础阶段建立**正确认知**：Ray 是什么、Raycast 做什么、为什么场景里要有 Collider。  
同时学会**读懂** `Physics.Raycast(ray, out RaycastHit hit)` 每个部分的含义。

---

## 一、定义 — 射线与射线检测是什么？

| 项目 | 说明 |
|------|------|
| **Ray** | `UnityEngine` 结构体，表示一条射线：`origin`（起点）+ `direction`（方向） |
| **Physics.Raycast** | 静态方法，让射线与场景中 **3D Collider** 求交，返回是否命中 |
| **RaycastHit** | 结构体，存储命中信息：交点、法线、距离、碰到的 Collider |
| **官方描述（Ray）** | A ray is an infinite line starting at origin and going in some direction |
| **一句话** | 从 A 点沿某方向「打一条激光」，看第一个打中谁 |

```csharp
// 手动构造一条射线：从 (0,10,0) 向下打
Ray ray = new Ray(new Vector3(0f, 10f, 0f), Vector3.down);

// 检测是否碰到 Collider
if (Physics.Raycast(ray, out RaycastHit hit))
{
    Debug.Log("打中了：" + hit.collider.name);
}
```

---

## 二、本质 — 射线检测如何工作？

```
输入：起点 origin + 方向 direction（+ 可选 maxDistance、layerMask）
       │
       ▼
  PhysX 物理引擎在场景中遍历 Collider
       │
       ▼
  找到沿射线方向、距离最近的交点
       │
       ▼
  输出：bool（是否命中）+ RaycastHit（point, normal, distance, collider…）
```

| 概念 | 说明 |
|------|------|
| **Ray 本身** | 只是数学描述，**不会**自动产生物理碰撞或伤害 |
| **Raycast** | 一次性**查询**，类似「问物理引擎：这条线上有什么？」 |
| **Collider** | 被检测物体**必须**有 Collider（Box/Mesh/Sphere/Capsule 等） |
| **与子弹区别** | 子弹常用 Rigidbody 实体；Raycast 是即时查询，无飞行时间 |

---

## 三、特点与适用场景

| 特点 | 说明 |
|------|------|
| **精确** | 返回世界坐标交点 `hit.point`、表面法线 `hit.normal` |
| **高效** | 单条 Raycast 开销小，适合每帧或点击时调用 |
| **可过滤** | `layerMask` 只检测指定 Layer；`maxDistance` 限制射程 |
| **局限** | 3D 下射线**起点在 Collider 内部**时可能检测不到该 Collider |

| 场景 | 是否适用 |
|------|----------|
| 鼠标点击 3D 物体 | ✅ ScreenPointToRay + Raycast |
| RTS 点地移动 | ✅ 射线打 Ground Layer |
| FPS 射击命中 | ✅ 从相机或枪口 origin 沿 forward |
| 角色是否着地 | ✅ 脚下短射线 `Raycast(pos, Vector3.down, 0.1f)` |
| 检测周围所有敌人 | ❌ 更适合 `OverlapSphere` |

---

## 四、Ray 与 RaycastHit 核心成员

### 4.1 Ray — 逐词读懂

#### `Ray ray = new Ray(origin, direction);` 是什么？

```csharp
Ray ray = new Ray(transform.position, transform.forward);
```

| 部分 | 含义 |
|------|------|
| `Ray` | **类型名**：射线结构体，表示「从一点沿一个方向延伸的直线」 |
| `ray` | **变量名**：存一条射线的实例 |
| `new Ray(...)` | 构造函数：用起点 + 方向创建射线 |
| `origin`（参数1） | `Vector3`，射线**起点**世界坐标 |
| `direction`（参数2） | `Vector3`，射线**方向**（长度建议为 1，即归一化） |

**整行人话**：在 `transform.position` 朝 `transform.forward` 造一条射线，供后续 Raycast 使用。

| 成员 | 含义 |
|------|------|
| `ray.origin` | 读起点 |
| `ray.direction` | 读方向 |
| `ray.GetPoint(10f)` | 沿方向走 10 单位处的点 |

---

### 4.2 RaycastHit — 逐词读懂

#### `RaycastHit hit;` 是什么？

```csharp
RaycastHit hit;
```

| 部分 | 含义 |
|------|------|
| `RaycastHit` | **类型名**：Unity **结构体**，存放射线**命中结果**（打在哪、打到谁） |
| `hit` | **变量名**：习惯命名，可改为 `hitInfo` 等 |

**整行人话**：声明一个「命中信息盒子」，Raycast 成功时 Unity 会把交点、法线、Collider 等写进去。

**说明**：`RaycastHit` 是 struct；配合 `out` 传给 `Physics.Raycast` 时，方法内部填充，调用方直接读 `hit.point` 等。

#### RaycastHit 常用属性

| 属性 | 含义 |
|------|------|
| `hit.point` | 命中点**世界坐标**（Vector3） |
| `hit.normal` | 命中表面**法线**，朝外（Vector3） |
| `hit.distance` | 从射线起点到命中点的**距离**（float） |
| `hit.collider` | 命中的 **Collider 组件** |
| `hit.transform` | 命中物体的 **Transform** |
| `hit.rigidbody` | 若 Collider 挂在 Rigidbody 上则返回，否则 null |

```csharp
// 示例：命中后读取
Debug.Log(hit.point);           // 打在哪
Debug.Log(hit.collider.name);  // 打到谁
```

---

## 五、核心一课：如何读懂 Raycast

```csharp
Physics.Raycast(ray, out RaycastHit hit)
```

| 部分 | 含义 |
|------|------|
| `Physics` | 物理静态类，3D 射线检测入口 |
| `.Raycast` | 射线投射方法 |
| `ray` | 传入的 Ray（起点 + 方向） |
| `out RaycastHit hit` | **输出参数**：命中时填充 hit，调用方直接读 hit.point 等 |
| 返回值 `bool` | `true` = 碰到 Collider；`false` = 什么都没碰到 |

**整行人话**：拿 `ray` 这条线去扫场景，打中了就把详情塞进 `hit`，并返回 true。

```csharp
Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
```

| 部分 | 含义 |
|------|------|
| `Camera.main` | 主相机（详见 [02_Camera.md](./02_Camera.md)） |
| `ScreenPointToRay` | 从相机位置，穿过屏幕像素点，生成指向 3D 世界的 Ray |
| `Input.mousePosition` | 鼠标屏幕坐标（左下角为原点） |

**整行人话**：鼠标点在屏幕哪，就从相机「看」向 3D 场景的对应方向。

---

## 【零基础阶段小结】

| 维度 | 要点 |
|------|------|
| **定义** | Ray = 起点 + 方向；Raycast = 物理查询 |
| **本质** | 数学射线 + PhysX，不是实体子弹 |
| **前提** | 被检测物体要有 Collider |
| **读懂** | `Physics.Raycast(ray, out hit)` 与 `ScreenPointToRay` |

**阶段检验**：能说出 Ray 两个字段；能解释为什么没 Collider 就点不中。

---

# 第二阶段：入门篇

## 【阶段总述】

入门阶段掌握 **Physics.Raycast 重载**、**RaycastHit 常用属性**、**ScreenPointToRay 四步流程**，并完成 3 个实战案例。  
重点：**Update 处理点击**；**hit.point 用于移动/放置**。

---

## 一、Physics.Raycast 重载详解

> 以下采用与 [01_PlayerPrefs.md](./01_PlayerPrefs.md) 相同的 **逐词读懂** 格式：先讲类型/方法/参数，再讲整行人话。

### API 全景

```
Physics（UnityEngine 静态类 — 3D 物理查询入口）
└── Raycast（静态方法 — 射线与 Collider 求交）
    ├── Raycast(origin, direction)                                    → bool
    ├── Raycast(origin, direction, out hit)                         → bool + 填充 hit
    ├── Raycast(origin, direction, out hit, maxDistance)            → 限射程
    ├── Raycast(origin, direction, out hit, maxDistance, layerMask) → 限 Layer
    └── Raycast(ray, out hit, maxDistance, layerMask)               → 传入 Ray 对象
```

---

### 先搞懂：`Physics`、`Raycast`、`origin`、`direction`、`out hit`

#### `Physics` 是什么？

| 项目 | 说明 |
|------|------|
| **类型** | `UnityEngine` 命名空间下的**静态类** |
| **作用** | 3D 物理入口：重力、射线、Overlap、Rigidbody 同步等 |
| **调用方式** | 不能 `new`，直接 `Physics.Raycast(...)` |

---

#### `Physics.Raycast` 是什么？

| 项目 | 说明 |
|------|------|
| **方法名** | Raycast = Ray（射线）+ cast（投射） |
| **做什么** | 从起点沿方向发射一条线，与场景中 **Collider** 求交 |
| **返回什么** | `bool`：true=碰到至少一个 Collider；false=没碰到 |
| **前提** | 被检测物体必须有 **Collider**（Mesh/Box/Sphere 等） |

---

#### 参数 `origin` 是什么？

```csharp
Vector3 origin = transform.position;
```

| 部分 | 含义 |
|------|------|
| `origin` | **参数名**，类型 `Vector3` |
| **含义** | 射线**发射起点**的世界坐标 |
| **常见取值** | 相机位置、角色脚下、枪口 `transform.position` |

**整行人话**：射线从场景的哪个点开始射出去。

---

#### 参数 `direction` 是什么？

```csharp
Vector3 direction = transform.forward;
```

| 部分 | 含义 |
|------|------|
| `direction` | **参数名**，类型 `Vector3` |
| **含义** | 射线**方向**（不是终点！） |
| **注意** | 应为**单位向量**（长度 1）；距离由 `maxDistance` 控制，不要靠 direction 长度 |

**整行人话**：射线往哪个方向延伸（例如 `Vector3.down` 向下、`transform.forward` 向前）。

---

#### 参数 `out RaycastHit hit` 是什么？

```csharp
Physics.Raycast(origin, direction, out RaycastHit hit)
//                              ↑关键字  ↑类型      ↑变量名
```

| 部分 | 含义 |
|------|------|
| `out` | C# 关键字：**输出参数**，方法内赋值，调用方直接读 |
| `RaycastHit` | 命中信息结构体类型 |
| `hit` | 你起的变量名，存命中结果 |

**整行人话**：如果打中了，Unity 把交点、法线、碰到的 Collider 写进 `hit`；没打中则不应依赖 hit 内容。

---

#### 整行示例：`if (Physics.Raycast(origin, direction, out hit))`

```csharp
RaycastHit hit;
if (Physics.Raycast(origin, direction, out hit))
{
    Debug.Log(hit.point);
}
```

| 行 | 整行人话 |
|----|----------|
| `RaycastHit hit;` | 准备一个空盒子接命中信息 |
| `Physics.Raycast(...)` | 从 origin 沿 direction 射线检测 |
| `if (...)` | 打中了才进大括号 |
| `hit.point` | 读命中点世界坐标 |

---

### 1.1 最简形式 — 只关心有没有碰到

```csharp
bool isHit = Physics.Raycast(origin, direction);
//           ↑类      ↑方法    ↑起点    ↑方向
```

| 参数 | 类型 | 含义 |
|------|------|------|
| `origin` | Vector3 | 射线起点 |
| `direction` | Vector3 | 射线方向 |
| **返回值** | bool | true=碰到；false=未碰到 |

**缺什么**：没有 `hit`，不知道打在哪、打到谁；距离无限远；检测所有 Layer。

**整行人话**：只问「前面有没有 Collider」，不要命中详情时用。

---

### 1.2 带命中信息（最常用）

```csharp
RaycastHit hit;
if (Physics.Raycast(origin, direction, out hit))
{
    Debug.Log(hit.point);
}
```

| 参数 | 类型 | 含义 |
|------|------|------|
| `origin` | Vector3 | 射线起点 |
| `direction` | Vector3 | 射线方向 |
| `out hit` | RaycastHit | 输出：最近命中的详情 |
| **返回值** | bool | 同 1.1 |

**整行人话**：打中了返回 true，同时 `hit.point` / `hit.collider` 可用；这是**入门最常用**重载。

---

### 1.3 带最大距离 `maxDistance`

```csharp
if (Physics.Raycast(origin, direction, out hit, 100f))
{
    // 只检测 100 单位以内
}
```

| 参数 | 类型 | 含义 |
|------|------|------|
| 前 3 个 | 同上 | origin、direction、out hit |
| `maxDistance` | float | 射线**最远**检测距离（如 `100f`）；默认无限可用 `Mathf.Infinity` |

**整行人话**：超过 100 单位的 Collider 不会被检测到；适合射击射程、脚下短距着地检测。

---

### 1.4 带 LayerMask `layerMask`

```csharp
int groundMask = LayerMask.GetMask("Ground");
if (Physics.Raycast(origin, direction, out hit, Mathf.Infinity, groundMask))
{
    // 只打 Ground 层
}
```

| 参数 | 类型 | 含义 |
|------|------|------|
| `maxDistance` | float | 此处 `Mathf.Infinity` = 不限距离 |
| `layerMask` | int（LayerMask） | **位掩码**：只与指定 Layer 的 Collider 求交 |

**`LayerMask.GetMask("Ground")` 逐词读懂**：

| 部分 | 含义 |
|------|------|
| `LayerMask` | Layer 掩码类型 |
| `GetMask("Ground")` | 静态方法，生成只含 Ground 层的掩码 |

**整行人话**：射线只认 Ground 层物体，点地移动、只点地面时常用。

---

### 1.5 传入 Ray 结构体（配合 ScreenPointToRay）

```csharp
Ray ray = cam.ScreenPointToRay(Input.mousePosition);
if (Physics.Raycast(ray, out hit, 100f))
{
    Debug.Log("命中");
}
```

| 参数 | 类型 | 含义 |
|------|------|------|
| `ray` | Ray | 已含 origin + direction 的射线对象 |
| `out hit` | RaycastHit | 命中详情 |
| `maxDistance` | float | 最远 100 单位 |

**整行人话**：鼠标点击时先用相机生成 `ray`，再交给 Raycast；等价于把 `ray.origin`、`ray.direction` 拆开传入。

---

### 重载对照表

| 重载 | 参数 | 典型用途 |
|------|------|----------|
| `(origin, direction)` | 无 hit | 只关心有没有碰到 |
| `(origin, direction, out hit)` | 最近命中 | **通用首选** |
| `(origin, direction, out hit, maxDistance)` | 限射程 | 射击、短距检测 |
| `(origin, direction, out hit, maxDistance, layerMask)` | 限 Layer | 只点地面、只打敌人 |
| `(ray, out hit, maxDistance, layerMask)` | Ray 对象 | 与 ScreenPointToRay 配合 |

---

### 1.6 Physics2D.Raycast（2D 专用）— 逐词读懂

```csharp
RaycastHit2D hit = Physics2D.Raycast(origin, Vector2.down, rayLength, groundMask);
```

| 部分 | 含义 |
|------|------|
| `Physics2D` | **类名**：2D 物理静态类（不是 Physics） |
| `.Raycast` | 2D 射线检测方法 |
| `origin` | **参数1**：Vector2，射线起点（XY 平面） |
| `Vector2.down` | **参数2 direction**：方向，`(0, -1)` 向下 |
| `rayLength` | **参数3 distance**：最远检测距离 |
| `groundMask` | **参数4 layerMask**：LayerMask，过滤 Collider2D |
| **返回值** | `RaycastHit2D`（不是 bool + out） |

#### `RaycastHit2D hit` 是什么？

| 部分 | 含义 |
|------|------|
| `RaycastHit2D` | 2D 命中信息结构体 |
| `hit.collider` | 命中的 Collider2D；**未命中时为 null** |
| `hit.point` | 命中点 Vector2 |

**整行人话**：2D 平台游戏脚下着地检测用 Physics2D；**不要用 Physics.Raycast 打 Collider2D**。

| 对比 | 3D `Physics.Raycast` | 2D `Physics2D.Raycast` |
|------|----------------------|-------------------------|
| Collider | Collider | Collider2D |
| 返回值 | bool + out RaycastHit | RaycastHit2D |
| 坐标 | Vector3 | Vector2 |

---

## 二、标准四步流程（3D 鼠标点击）

```
步骤1  射线来源
       屏幕点击 → Camera.main.ScreenPointToRay(Input.mousePosition)
       角色前方 → new Ray(transform.position, transform.forward)

步骤2  执行 Raycast
       Physics.Raycast(ray, out RaycastHit hit, maxDistance, layerMask)

步骤3  判断返回值
       if (命中) 读 hit.collider / hit.point / hit.normal

步骤4  业务逻辑
       选中、移动、Instantiate 特效、SendMessage 等
```

| 回调 | 射线用途 |
|------|----------|
| `Update` + `GetMouseButtonDown` | 鼠标点击选中 |
| `FixedUpdate` | 连续地面检测、前方障碍 |
| `Awake/Start` | 缓存 Camera.main、LayerMask |

---

## 三、入门三个案例

### 案例代码讲解模板

每个案例统一按以下结构组织（下文所有案例均遵循此模板）：

| 顺序 | 板块 | 内容 |
|:----:|------|------|
| 1 | **功能** | 案例实现什么业务 |
| 2 | **完整代码** | 带行内注释的完整脚本 |
| 3 | **语法拆解** | 对案例中较生僻的语法，逐个说明（格式见下） |
| 4 | **逐行详解** | 表格：每行代码的含义 |
| 5 | **操作提示** | Unity 绑定、调用方式等（如有） |

**语法拆解的标准格式**（遇到 `out`、`LayerMask`、`MoveTowards` 等不熟悉的写法时使用）：

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

### 案例 1：鼠标点击选中 3D 物体

**功能**：左键点击，射线检测命中的物体并输出日志（选中逻辑入口）。

```csharp
using UnityEngine;                                      // 引入 Unity 核心库

public class ClickSelect : MonoBehaviour                // 3D 点击选中脚本
{
    Camera cam;                                         // 缓存主相机，避免每帧 Camera.main 查找

    void Awake()                                        // Awake：初始化阶段执行
    {
        cam = Camera.main;                              // 获取 Tag=MainCamera 的主相机
    }

    void Update()                                       // Update：每帧检测鼠标输入
    {
        if (Input.GetMouseButtonDown(0))                // 左键在本帧按下（只触发一次）
        {
            Ray ray = cam.ScreenPointToRay(Input.mousePosition);  // 屏幕坐标 → 世界射线
            if (Physics.Raycast(ray, out RaycastHit hit))         // 3D 射线检测，命中写入 hit
            {
                Debug.Log("选中：" + hit.collider.gameObject.name);  // 打印被点物体的名字
                // 可扩展：hit.collider.GetComponent<Selectable>()?.Select();
            }
        }
    }
}
```

#### 语法拆解

##### `out RaycastHit hit` 是什么？

```csharp
if (Physics.Raycast(ray, out RaycastHit hit))
```

| 部分 | 含义 |
|------|------|
| `out` | 输出参数关键字；方法内部赋值，调用方直接读取 |
| `RaycastHit` | 命中信息结构体（point、normal、collider 等） |
| `hit` | 变量名，Raycast 成功后被填充 |

**整行人话**：Raycast 打中了就把「打在哪、打到谁」写进 `hit` 给你用。

---

##### `hit.collider.gameObject` 是什么？

```csharp
hit.collider.gameObject.name
```

| 部分 | 含义 |
|------|------|
| `hit.collider` | 命中的 Collider 组件 |
| `.gameObject` | 该组件所在的 GameObject |
| `.name` | Hierarchy 中显示的对象名 |

**整行人话**：从命中信息一路拿到「被点的那个物体」的名字。

---

##### `cam.ScreenPointToRay(Input.mousePosition)` 是什么？

```csharp
Ray ray = cam.ScreenPointToRay(Input.mousePosition);
```

| 部分 | 含义 |
|------|------|
| `ScreenPointToRay` | 从相机穿过屏幕点画射线到 3D 世界 |
| `Input.mousePosition` | 鼠标屏幕像素坐标 |
| 返回值 `Ray` | 射线：origin + direction |

**整行人话**：把鼠标点变成 3D 检测用的激光。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 3 | `public class ClickSelect : MonoBehaviour` | 可挂载的脚本类 |
| 5 | `Camera cam;` | 声明相机缓存变量 |
| 7 | `void Awake()` | 初始化时执行一次 |
| 9 | `cam = Camera.main;` | 缓存主相机引用 |
| 11 | `void Update()` | 每帧检测输入 |
| 13 | `GetMouseButtonDown(0)` | 左键按下那一帧 |
| 15 | `ScreenPointToRay(...)` | 见上方语法拆解 |
| 16 | `Physics.Raycast(...)` | 见上方语法拆解 |
| 18 | `hit.collider.gameObject.name` | 见上方语法拆解 |

#### 操作提示

脚本挂到任意物体（如 GameManager）；被点物体需 **Collider**；主相机 Tag 为 **MainCamera**。  
更完整的相机坐标说明见 [02_Camera.md 案例 2](./02_Camera.md)。

---

### 案例 2：点击地面移动角色

**功能**：鼠标点击 Ground 层，角色平滑移动到 `hit.point`。

```csharp
using UnityEngine;                                      // 引入 Unity 核心库

public class ClickToMove : MonoBehaviour                // 点击地面移动脚本，挂到角色上
{
    Camera cam;                                         // 主相机引用
    LayerMask groundMask;                               // 地面 Layer 掩码，Raycast 只检测 Ground
    public float moveSpeed = 5f;                        // 移动速度（单位/秒），Inspector 可调
    Vector3 targetPos;                                  // 当前要移动到的目标世界坐标

    void Awake()                                        // 初始化
    {
        cam = Camera.main;                              // 缓存主相机
        groundMask = LayerMask.GetMask("Ground");       // 构建只含 "Ground" 层的掩码
        targetPos = transform.position;                 // 初始目标 = 当前位置（避免开局乱跑）
    }

    void Update()                                       // 每帧：检测点击 + 向目标移动
    {
        if (Input.GetMouseButtonDown(0))                // 左键点击
        {
            Ray ray = cam.ScreenPointToRay(Input.mousePosition);  // 屏幕点 → 射线
            if (Physics.Raycast(ray, out RaycastHit hit, 500f, groundMask))  // 限距 500 + 只打 Ground
            {
                targetPos = hit.point;                  // 记录地面交点为移动目标
            }
        }

        transform.position = Vector3.MoveTowards(       // 每帧向 targetPos 靠近（匀速，遇障碍不绕路）
            transform.position, targetPos, moveSpeed * Time.deltaTime);
    }
}
```

#### 语法拆解

##### `LayerMask.GetMask("Ground")` 是什么？

```csharp
groundMask = LayerMask.GetMask("Ground");
```

| 部分 | 含义 |
|------|------|
| `LayerMask` | Layer 位掩码类型，本质是 int |
| `GetMask("Ground")` | 按 Layer 名称生成掩码，只包含 Ground 层 |
| 传入 Raycast | 射线**仅**与 Ground 层 Collider 求交 |

**整行人话**：地面单独一层，射线不会误点敌人或 UI 碰撞体。

---

##### `Physics.Raycast(ray, out hit, 500f, groundMask)` 是什么？

```csharp
Physics.Raycast(ray, out RaycastHit hit, 500f, groundMask)
```

| 部分 | 含义 |
|------|------|
| `500f` | maxDistance：最远检测 500 单位 |
| `groundMask` | layerMask：只检测指定 Layer |
| `hit.point` | 命中点世界坐标，作为角色移动目标 |

**整行人话**：从鼠标方向打射线，最多 500 米，只认地面，交点就是要走的地方。

---

##### `Vector3.MoveTowards(...)` 是什么？

```csharp
transform.position = Vector3.MoveTowards(
    transform.position, targetPos, moveSpeed * Time.deltaTime);
```

| 部分 | 含义 |
|------|------|
| `MoveTowards(current, target, maxDistanceDelta)` | 从 current 向 target 移动，本帧最多移动 maxDistanceDelta |
| `moveSpeed * Time.deltaTime` | 与帧率无关的每帧位移量 |
| 对比 `Lerp` | MoveTowards 是匀速靠近；Lerp 是比例插值 |

**整行人话**：角色以固定速度朝目标点走过去。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 3 | `public class ClickToMove : MonoBehaviour` | 可挂载的脚本类 |
| 5 | `Camera cam;` | 相机缓存 |
| 6 | `LayerMask groundMask;` | 地面 Layer 掩码变量 |
| 7 | `moveSpeed = 5f` | 移动速度，可在 Inspector 调整 |
| 8 | `Vector3 targetPos;` | 移动目标点 |
| 10 | `void Awake()` | 初始化 |
| 12 | `cam = Camera.main;` | 缓存主相机 |
| 13 | `GetMask("Ground")` | 见上方语法拆解 |
| 14 | `targetPos = transform.position` | 初始不移动 |
| 16 | `void Update()` | 每帧逻辑 |
| 18 | `GetMouseButtonDown(0)` | 左键点击 |
| 20 | `ScreenPointToRay(...)` | 生成射线 |
| 21 | `Raycast(..., 500f, groundMask)` | 见上方语法拆解 |
| 23 | `targetPos = hit.point` | 更新移动目标 |
| 26~27 | `MoveTowards(...)` | 见上方语法拆解 |

#### 操作提示

地面 Plane 的 Layer 设为 **Ground**（Edit → Project Settings → Tags and Layers）；地面**必须有 Collider**；角色无需 Collider 也能用本脚本移动。

---

### 案例 3：2D 地面检测（Physics2D）

**功能**：2D 角色每帧向下射线，判断是否站在平台上。

```csharp
using UnityEngine;                                      // 引入 Unity 核心库

public class GroundCheck2D : MonoBehaviour              // 2D 着地检测，挂到玩家上
{
    public float rayLength = 0.1f;                      // 向下检测距离（略大于与地面的间隙）
    public LayerMask groundMask;                        // Inspector 勾选 Ground 层
    public bool isGrounded;                             // 是否着地，供跳跃脚本读取

    void FixedUpdate()                                  // FixedUpdate：与 2D 物理步长同步
    {
        Vector2 origin = transform.position;            // 射线起点：角色当前位置（2D 用 Vector2）
        RaycastHit2D hit = Physics2D.Raycast(         // 2D 射线检测，返回 RaycastHit2D
            origin, Vector2.down, rayLength, groundMask);
        isGrounded = hit.collider != null;              // 命中 Collider 则着地，否则空中

        Debug.DrawRay(origin, Vector2.down * rayLength, // Scene 视图画射线：绿=着地，红=空中
            isGrounded ? Color.green : Color.red);
    }
}
```

#### 语法拆解

##### `Physics2D.Raycast` 与 3D 有何不同？

```csharp
RaycastHit2D hit = Physics2D.Raycast(origin, Vector2.down, rayLength, groundMask);
```

| 对比 | Physics.Raycast（3D） | Physics2D.Raycast（2D） |
|------|----------------------|-------------------------|
| Collider | Collider | Collider2D |
| 返回值 | bool + out RaycastHit | 直接返回 RaycastHit2D |
| 坐标 | Vector3 | Vector2（XY 平面） |
| 典型场景 | 3D 点击、FPS | 平台跳跃着地检测 |

**整行人话**：2D 游戏用 Physics2D，不是 Physics。

---

##### `hit.collider != null` 是什么？

```csharp
isGrounded = hit.collider != null;
```

| 部分 | 含义 |
|------|------|
| `RaycastHit2D` | 2D 命中结构；未命中时 collider 为 null |
| `!= null` | 有 Collider 即表示射线碰到了地面 |

**整行人话**：脚下短射线碰到东西就算在地面。

---

##### `void FixedUpdate()` 是什么？

```csharp
void FixedUpdate()
```

| 部分 | 含义 |
|------|------|
| `FixedUpdate` | 固定时间步长调用，与 Physics2D 同步 |
| 与 Update 区别 | 物理检测放 FixedUpdate 结果更稳定 |
| 本案例 | 着地状态与刚体/碰撞在同一物理帧更新 |

**整行人话**：跟 2D 物理同一节奏检测脚下有没有地。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 3 | `public class GroundCheck2D : MonoBehaviour` | 可挂载的脚本类 |
| 5 | `rayLength = 0.1f` | 向下检测 0.1 单位 |
| 6 | `LayerMask groundMask` | 在 Inspector 勾选 Ground 层 |
| 7 | `bool isGrounded` | 对外公开的着地状态 |
| 9 | `void FixedUpdate()` | 见上方语法拆解 |
| 11 | `Vector2 origin = transform.position` | 从角色位置向下打射线 |
| 12~13 | `Physics2D.Raycast(...)` | 见上方语法拆解 |
| 14 | `isGrounded = hit.collider != null` | 见上方语法拆解 |
| 16~17 | `Debug.DrawRay(...)` | Scene 视图可视化调试 |

#### 操作提示

平台加 **BoxCollider2D**；Layer 设为 Ground 并在 Inspector **Ground Mask** 勾选；跳跃脚本读 `isGrounded` 再决定是否 `SetTrigger("Jump")`。

---

## 【入门阶段小结】

| 维度 | 要点 |
|------|------|
| **API** | Raycast 重载、RaycastHit、ScreenPointToRay |
| **流程** | 造射线 → Raycast → 读 hit → 业务 |
| **Layer** | GetMask 过滤地面/敌人 |
| **2D** | Physics2D.Raycast + RaycastHit2D |
| **案例** | 点击选中、点地移动、2D 着地 |

---

# 第三阶段：进阶篇

## 【阶段总述】

进阶阶段：**LayerMask 与 Trigger 控制**、**RaycastAll / SphereCast 选型**、**RaycastHelper 封装**、**Debug 可视化**、**2D/3D 避坑清单**。

---

## 一、LayerMask 与 QueryTriggerInteraction — 逐词读懂

#### `LayerMask.GetMask("Enemy")` 是什么？

```csharp
int enemyMask = LayerMask.GetMask("Enemy");
```

| 部分 | 含义 |
|------|------|
| `LayerMask` | Layer 掩码类型，本质是 int 位标记 |
| `GetMask` | 静态方法，按 **Layer 名称** 生成掩码 |
| `"Enemy"` | 只包含 Enemy 这一层 |

**整行人话**：构建「只检测 Enemy 层」的过滤器，传给 Raycast 第 5 个参数。

---

#### `QueryTriggerInteraction` 是什么？

```csharp
Physics.Raycast(ray, out hit, 100f, enemyMask, QueryTriggerInteraction.Ignore);
```

| 部分 | 含义 |
|------|------|
| 第 6 参数 | 控制是否命中 **Is Trigger = true** 的 Collider |
| `UseGlobal` | 用 Project Settings → Physics 全局默认 |
| `Ignore` | **忽略** Trigger 碰撞体 |
| `Collide` | **强制命中** Trigger（传送门、感应区常用） |

**整行人话**：Trigger 默认可能被忽略，点不中传送门时改 `Collide`。

**LayerMask 构建方式**：

```csharp
int mask = LayerMask.GetMask("Ground", "Wall");  // 多层：Ground + Wall
public LayerMask interactableMask;               // Inspector 勾选（SerializeField）
Physics.Raycast(ray, out hit, 100f, interactableMask);
```

---

## 二、Raycast 家族 API 对比

| API | 作用 | 何时用 |
|-----|------|--------|
| `Physics.Raycast` | 最近一条命中 | 点击、射击、单点检测 |
| `Physics.RaycastAll` | 所有命中（数组） | 穿透玻璃、多层 UI 后的 3D |
| `Physics.Linecast` | 两点间线段检测 | 两点是否有障碍 |
| `Physics.SphereCast` | 带半径的粗射线 | 角色体型、薄墙不易漏检 |
| `Physics2D.Raycast` | 2D 射线 | 平台游戏 |
| `Physics2D.RaycastAll` | 2D 全部命中 | 2D 穿透检测 |

```csharp
// RaycastAll 示例：获取射线上所有物体
RaycastHit[] hits = Physics.RaycastAll(ray, 100f);
foreach (RaycastHit h in hits)
{
    Debug.Log(h.collider.name);
}
```

---

## 三、工程化封装 RaycastHelper

```csharp
using UnityEngine;

public static class RaycastHelper
{
    static Camera _cam;
    static Camera Cam => _cam != null ? _cam : (_cam = Camera.main);

    /// <summary>从鼠标发射射线，返回是否命中</summary>
    public static bool TryFromMouse(out RaycastHit hit, float maxDistance = Mathf.Infinity, int layerMask = Physics.DefaultRaycastLayers)
    {
        Ray ray = Cam.ScreenPointToRay(Input.mousePosition);
        return Physics.Raycast(ray, out hit, maxDistance, layerMask);
    }

    /// <summary>从屏幕坐标发射射线</summary>
    public static bool TryFromScreen(Vector3 screenPos, out RaycastHit hit, float maxDistance = Mathf.Infinity, int layerMask = Physics.DefaultRaycastLayers)
    {
        Ray ray = Cam.ScreenPointToRay(screenPos);
        return Physics.Raycast(ray, out hit, maxDistance, layerMask);
    }
}
```

**使用**：

```csharp
if (RaycastHelper.TryFromMouse(out RaycastHit hit, 200f, groundMask))
{
    player.MoveTo(hit.point);
}
```

---

## 四、Debug 可视化

```csharp
void Update()
{
    Ray ray = cam.ScreenPointToRay(Input.mousePosition);
    if (Physics.Raycast(ray, out RaycastHit hit, 100f))
    {
        // 命中段：起点到交点
        Debug.DrawLine(ray.origin, hit.point, Color.green);
        // 未命中段：交点沿方向延伸（可选）
        Debug.DrawRay(hit.point, ray.direction * (100f - hit.distance), Color.red);
    }
    else
    {
        Debug.DrawRay(ray.origin, ray.direction * 100f, Color.yellow);
    }
}
```

| 方法 | 说明 |
|------|------|
| `Debug.DrawRay` | 从起点画方向向量（需乘长度才可见） |
| `Debug.DrawLine` | 两点连线 |
| 可见性 | 仅在 **Scene 视图** 显示；Game 视图需 Gizmos 或运行时 LineRenderer |

---

## 五、Update 与 FixedUpdate 选型

| 时机 | 适合 | 原因 |
|------|------|------|
| `Update` | 鼠标点击、UI 同步交互 | 与输入帧一致 |
| `FixedUpdate` | 着地检测、移动平台、与 Rigidbody 同步 | 与物理步长一致 |

官方文档注明：物理相关示例常用 FixedUpdate；点击检测用 Update 即可。

---

## 六、2D 点击检测补充

2D 没有 `ScreenPointToRay` 的 2D 专用版，常见做法：

```csharp
Vector3 world = cam.ScreenToWorldPoint(Input.mousePosition);
world.z = 0f;  // 2D 游戏常固定 Z
RaycastHit2D hit = Physics2D.Raycast(world, Vector2.zero, 0f, clickMask);
// 或用 OverlapPoint：Physics2D.OverlapPoint(world, clickMask)
```

| 方式 | 说明 |
|------|------|
| `Raycast(world, Vector2.zero, 0f)` | 点检测（方向为零、距离为零） |
| `OverlapPoint` | 2D 点选更直观，无需方向 |

---

## 七、常见误区与最佳实践

| 误区 | 正确做法 |
|------|----------|
| 物体点不中 | 检查是否有 **Collider**、是否被 Layer 排除 |
| 地面点不中 | 地面 Collider + Layer 与 layerMask 一致 |
| Trigger 点不中 | 设置 `QueryTriggerInteraction.Collide` 或勾选 Physics 全局 Hit Triggers |
| 2D 用了 Physics.Raycast | 2D Collider 用 **Physics2D.Raycast** |
| direction 长度很大 | 方向应 **归一化**（`direction.normalized`），距离用 maxDistance |
| 起点在 Collider 内（3D） | 把起点稍微移出 Collider，或用 RaycastAll / Overlap |
| 每帧 Camera.main | Awake 缓存 |
| 射线看不见 | 用 Debug.DrawRay，注意 direction 要乘距离 |

---

## 【进阶阶段小结】

| 维度 | 要点 |
|------|------|
| Layer | GetMask / SerializeField LayerMask |
| Trigger | QueryTriggerInteraction |
| 选型 | 单点 Raycast / 多层 RaycastAll / 2D OverlapPoint |
| 封装 | RaycastHelper.TryFromMouse |
| 避坑 | Collider、Layer、2D/3D、Trigger、方向归一化 |

---

# 【全文总结】

## 最重要的一行代码

```csharp
if (Physics.Raycast(Camera.main.ScreenPointToRay(Input.mousePosition), out RaycastHit hit))
{
    Debug.Log(hit.collider.name);
}
```

| 部分 | 含义 |
|------|------|
| `ScreenPointToRay` | 屏幕点 → 世界射线 |
| `Physics.Raycast` | 3D 物理查询 |
| `hit.collider` | 命中的 Collider |

## 三阶段对照

| 阶段 | 代表案例 |
|------|----------|
| 零基础 | 读懂 Ray / Raycast / RaycastHit |
| 入门 | 点击选中、点地移动、2D 着地 |
| 进阶 | LayerMask、RaycastAll、RaycastHelper |

## 与 Camera 文档的关系

| 主题 | 文档 |
|------|------|
| ScreenPointToRay、三种坐标空间 | [02_Camera.md](./02_Camera.md) |
| Physics.Raycast、LayerMask、2D | 本文 03_Raycast.md |

## 官方文档索引

| 主题 | 链接 |
|------|------|
| Ray | https://docs.unity3d.com/ScriptReference/Ray.html |
| Physics.Raycast | https://docs.unity3d.com/ScriptReference/Physics.Raycast.html |
| RaycastHit | https://docs.unity3d.com/ScriptReference/RaycastHit.html |
| Physics2D.Raycast | https://docs.unity3d.com/ScriptReference/Physics2D.Raycast.html |
| LayerMask | https://docs.unity3d.com/ScriptReference/LayerMask.html |

---

*文档版本：与 01_PlayerPrefs.md、02_Camera.md 同系列模板。*
