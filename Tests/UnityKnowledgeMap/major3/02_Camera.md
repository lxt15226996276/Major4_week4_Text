# Unity 相机 Camera 详解

> 参照：[Unity 官方 Scripting API - Camera](https://docs.unity3d.com/ScriptReference/Camera.html) · [Introduction to cameras](https://docs.unity3d.com/Manual/CamerasOverview.html)  
> 关联文档：[03_Raycast.md](./03_Raycast.md)（Physics.Raycast、RaycastHit、LayerMask 射线检测详解）  
> 学习路径：**零基础 → 入门 → 进阶**，每阶段采用 **总—分—总** 结构。  
> 讲解维度：**定义 → 本质 → 特点 → 适用场景 → 原理 → API → 步骤 → 案例 → 避坑**（进阶含多相机 / Cinemachine）。  
> 案例讲解：遵循 **案例代码讲解模板**（功能 → 代码 → 语法拆解 → 逐行详解 → 操作提示）。  
> API 讲解：入门/进阶 API 章节均采用 **逐词读懂** 格式（与 [01_PlayerPrefs.md](./01_PlayerPrefs.md) 一致：类型 → 参数 → 整行人话）。

---

## 【全文总述】

**Camera（相机）** 是 Unity 中玩家「看世界的窗口」：把 3D 场景拍成 2D 画面显示到屏幕上。  
本文从概念到脚本控制，再到多相机与进阶方案（Cinemachine）逐层展开。

### 思维导图总览

```
Unity 相机 Camera
│
├── Camera 组件（UnityEngine — 挂载在 GameObject 上的组件）
│   │
│   ├── 【知识维度】（讲师框架 — 完整版）
│   │   │
│   │   ├── 定义：Unity 中用于呈现游戏世界的相机组件
│   │   │   └── 官方描述：A Camera is a device through which the player views the world
│   │   │       通过 GameObject 添加 Camera 组件创建；场景至少有一个相机
│   │   │
│   │   ├── 本质：3D 世界 → 视锥体裁剪 → 渲染 → 2D 屏幕画面
│   │   │   ├── 组件模型：挂在 GameObject 上，与 Transform 位置旋转绑定
│   │   │   ├── 获取方式：GetComponent<Camera>() / Camera.main / 拖拽引用
│   │   │   └── 渲染链路：剔除(Cull) → 渲染(Render) → 输出到屏幕或 RenderTexture
│   │   │
│   │   ├── 官方定位：场景观察与画面输出的核心组件
│   │   │   ├── 设计用途：展示游戏世界、UI 相机、小地图、过场动画
│   │   │   └── 可无限数量：按 depth 排序，可只渲染部分 Layer
│   │   │
│   │   ├── 特点
│   │   │   ├── 优势：Inspector 可视化调参、坐标转换 API 丰富、可多相机叠加
│   │   │   └── 局限：多相机增加 Draw Call；Camera.main 有查找开销；投影模式选错影响观感
│   │   │
│   │   ├── 适用场景
│   │   │   ├── ✅ 适用：第三人称/第一人称、2D 正交、UI 相机、小地图、分屏
│   │   │   └── ❌ 不适用：用普通 Transform 代替相机「看」世界（无法输出画面）
│   │   │
│   │   ├── 核心原理：投影模式 + 视锥体 + 渲染顺序
│   │   │   ├── Perspective（透视）：近大远小，3D 游戏常用
│   │   │   ├── Orthographic（正交）：无透视，2D / 等距视角常用
│   │   │   ├── 近远裁剪面：nearClipPlane ~ farClipPlane 之间才可见
│   │   │   └── depth 越大越后渲染（显示在上层）
│   │   │
│   │   ├── 核心属性及参数（常用）
│   │   │   ├── fieldOfView：垂直视野角度（透视模式）
│   │   │   ├── orthographic / orthographicSize：正交开关与半高
│   │   │   ├── nearClipPlane / farClipPlane：近/远裁剪距离
│   │   │   ├── clearFlags / backgroundColor：清屏方式与背景色
│   │   │   ├── cullingMask：渲染哪些 Layer
│   │   │   ├── depth：多相机渲染顺序
│   │   │   └── targetTexture：渲染到 RenderTexture 而非屏幕
│   │   │
│   │   ├── 核心方法（常用）
│   │   │   ├── ScreenPointToRay：屏幕坐标 → 射线（点击检测）
│   │   │   ├── WorldToScreenPoint / ScreenToWorldPoint：坐标转换
│   │   │   ├── ViewportPointToRay：视口坐标 → 射线
│   │   │   └── Camera.main：获取 Tag 为 MainCamera 的主相机
│   │   │
│   │   ├── 三种坐标空间（官方）
│   │   │   ├── Screen Space：像素坐标，左下(0,0)，右上(pixelWidth, pixelHeight)
│   │   │   ├── Viewport Space：归一化 0~1，左下(0,0)，右上(1,1)
│   │   │   └── World Space：世界全局坐标 Transform.position
│   │   │
│   │   ├── 标准使用步骤
│   │   │   ├── 步骤1 场景放置 Camera（或 Main Camera）
│   │   │   ├── 步骤2 设置投影模式、FOV/Size、裁剪面、Clear Flags
│   │   │   ├── 步骤3 脚本获取 Camera 引用
│   │   │   └── 步骤4 在 Update/LateUpdate 中控制 Transform 或使用跟随脚本
│   │   │
│   │   ├── 生命周期与调用时机
│   │   │   ├── Update：玩家输入驱动的相机逻辑
│   │   │   ├── LateUpdate：跟随目标（目标 Update 完成后再移动相机）
│   │   │   ├── OnPreRender / OnPostRender：渲染前后回调（高级）
│   │   │   └── FixedUpdate：与物理同步的相机（较少用）
│   │   │
│   │   ├── 渲染相关
│   │   │   ├── Render Path：Forward / Deferred（项目与相机设置）
│   │   │   ├── URP：Base / Overlay 相机堆叠
│   │   │   └── Built-in：depth 控制绘制顺序
│   │   │
│   │   ├── 性能 / 调试
│   │   │   ├── 性能：减少多余相机；缓存 Camera.main；合理 cullingMask
│   │   │   └── 调试：Scene 视图 Gizmo 查看视锥体；Game 视图切换相机
│   │   │
│   │   └── 选型、封装、避坑
│   │       ├── 选型：简单跟随→自写脚本；复杂镜头→Cinemachine
│   │       ├── 封装：CameraController 统一管理引用与跟随
│   │       └── 避坑：MainCamera Tag、LateUpdate 跟随、UI 相机单独 Layer
│   │
│   ├── 第一阶段：零基础（建立认知 + 读懂代码）
│   │   ├── 理解定义、本质、透视 vs 正交
│   │   ├── 逐词读懂：Camera.main、GetComponent<Camera>()
│   │   └── 认识 Inspector 核心参数
│   │
│   ├── 第二阶段：入门（属性 + 方法 + 案例）
│   │   ├── 常用属性及参数详解
│   │   ├── 坐标转换与 ScreenPointToRay
│   │   └── 实战案例：跟随相机 / 点击射线 / 2D 正交相机
│   │
│   └── 第三阶段：进阶（多相机 + 封装 + Cinemachine）
│       ├── 多相机 depth / cullingMask 分工
│       ├── URP 相机堆叠简介
│       ├── CameraController 封装
│       └── Cinemachine 进阶方案（见下方分支）
│
└── Cinemachine（进阶相机系统 — 可选插件/包）
    │
    ├── 定义：Unity 官方相机控制包，用 Virtual Camera 驱动真实 Camera
    ├── 本质：算法模块（Follow/LookAt/Noise）替代手写 LateUpdate 跟随
    ├── 适用：第三人称、过场、镜头切换、抖动、轨道相机
    ├── 核心概念：CinemachineBrain + Virtual Camera + Follow/LookAt 目标
    └── 与手写 Camera 脚本：简单项目手写；复杂镜头优先 Cinemachine
```

| 学习阶段 | 学习目标 |
|----------|----------|
| **零基础** | 说清 Camera 是什么、透视/正交区别；读懂 `Camera.main` |
| **入门** | 掌握常用属性、坐标转换、ScreenPointToRay；完成 3 个案例 |
| **进阶** | 会多相机分工、封装、选型；了解 Cinemachine 与 URP 堆叠 |

### 讲师知识框架速览（全文脉络）

| 维度 | 零基础讲 | 入门讲 | 进阶讲 |
|------|----------|--------|--------|
| 定义 | ✅ | 回顾 | 回顾 |
| 本质 | ✅ | — | — |
| 特点 | ✅ | — | 性能补充 |
| 适用场景 | ✅ | — | 选型（Cinemachine） |
| 核心原理 | 透视/正交 | ✅ 视锥体/坐标空间 | 多相机渲染 |
| 核心 API | 读懂获取相机 | ✅ 属性+方法 | 封装 |
| 使用步骤 | Inspector | ✅ 脚本控制 | CameraController |
| 调用时机 | — | ✅ LateUpdate | — |
| 避坑 | — | 初步 | ✅ |

---

# 第一阶段：零基础篇

## 【阶段总述】

零基础阶段建立**正确认知**：Camera 是什么、怎么创建、透视和正交有何区别。  
同时学会**读懂** `Camera.main` 和 `GetComponent<Camera>()`，并认识 Inspector 核心参数。

---

## 一、定义 — Camera 是什么？

| 项目 | 说明 |
|------|------|
| **类型** | `UnityEngine` 命名空间下的 **组件（Component）** |
| **挂载** | 添加在 GameObject 上（默认 Main Camera 已带 Camera 组件） |
| **官方定义** | A Camera is a device through which the player views the world |
| **一句话** | 把 3D 场景「拍」成 2D 画面显示到屏幕的「眼睛」 |

```csharp
// 获取相机的常见写法
Camera cam = Camera.main;                    // 主相机（Tag = MainCamera）
Camera cam = GetComponent<Camera>();         // 本物体上的 Camera 组件
```

---

## 二、本质 — 相机如何「看」世界？

```
3D 场景中的物体
       │
       ▼
  视锥体裁剪（近裁剪面 ~ 远裁剪面之间）
       │
       ▼
  渲染管线（Forward / Deferred / URP）
       │
       ▼
  屏幕 或 RenderTexture（2D 画面）
```

| 概念 | 说明 |
|------|------|
| **Transform** | 相机位置/旋转决定「从哪看、朝哪看」 |
| **投影** | Perspective 透视 / Orthographic 正交 |
| **裁剪面** | 太近或太远的不渲染 |

---

## 三、透视 vs 正交

| 对比 | Perspective（透视） | Orthographic（正交） |
|------|---------------------|----------------------|
| **视觉效果** | 近大远小，有空间感 | 物体大小不随距离变化 |
| **Inspector** | `Projection: Perspective` + FOV | `Projection: Orthographic` + Size |
| **适用** | 3D 动作、FPS、第三人称 | 2D 游戏、UI 地图、等距视角 |
| **属性** | `fieldOfView`（垂直视野角度） | `orthographicSize`（半高） |

---

## 四、Inspector 核心参数（零基础必认）

| 参数 | 含义 |
|------|------|
| **Clear Flags** | 每帧渲染前如何清屏（Skybox / Solid Color / Depth Only 等） |
| **Background** | Solid Color 时的背景色 |
| **Projection** | Perspective 或 Orthographic |
| **Field of View** | 透视模式垂直视野（常用 60°） |
| **Size** | 正交模式半高度 |
| **Clipping Planes Near/Far** | 近/远裁剪距离（Near 通常 0.3，Far 根据场景） |
| **Viewport Rect** | 相机画面占屏幕的比例（分屏用） |
| **Depth** | 渲染顺序，数值大的后画（在上层） |
| **Culling Mask** | 只渲染勾选到的 Layer |

---

## 五、核心一课：如何读懂获取相机

```csharp
Camera cam = Camera.main;
```

| 部分 | 含义 |
|------|------|
| `Camera` | 类名，相机组件类型 |
| `.main` | 静态属性：场景中 **Tag 为 MainCamera** 的第一个启用相机 |
| `cam` | 变量，用来存引用，后续写 `cam.fieldOfView = 60f` 等 |

**说明**：没有 MainCamera 时 `Camera.main` 为 `null`；频繁调用有开销，建议缓存。

```csharp
Camera cam = GetComponent<Camera>();
```

| 部分 | 含义 |
|------|------|
| `GetComponent<Camera>()` | 获取**当前 GameObject** 上挂载的 Camera 组件 |
| `<Camera>` | 泛型：指定要获取的组件类型 |

---

## 【零基础阶段小结】

| 维度 | 要点 |
|------|------|
| **定义** | 看世界的组件，挂在 GameObject 上 |
| **本质** | 3D → 视锥体 → 渲染 → 2D 屏幕 |
| **投影** | 透视=3D；正交=2D/等距 |
| **获取** | `Camera.main` / `GetComponent<Camera>()` |

**阶段检验**：能区分透视与正交；能说出 `Camera.main` 的前提（MainCamera Tag）。

---

# 第二阶段：入门篇

## 【阶段总述】

入门阶段掌握 **常用属性、坐标转换、ScreenPointToRay**，并完成 3 个实战案例。  
重点：**LateUpdate 做跟随**；**ScreenPointToRay 做点击检测**。

---

## 一、核心属性及参数详解

> 以下采用与 [01_PlayerPrefs.md](./01_PlayerPrefs.md) 相同的 **逐词读懂** 格式。

### API 全景（Camera 组件常用）

```
Camera（UnityEngine 组件 — 挂在 GameObject 上）
├── 投影：fieldOfView / orthographic / orthographicSize
├── 裁剪：nearClipPlane / farClipPlane
├── 背景：clearFlags / backgroundColor
├── 多相机：depth / cullingMask
└── 静态：Camera.main
```

---

### 1.1 投影与视野 — 逐词读懂

#### `camera.fieldOfView = 60f;` 是什么？

```csharp
camera.fieldOfView = 60f;
```

| 部分 | 含义 |
|------|------|
| `camera` | **变量名**：Camera 组件引用 |
| `.fieldOfView` | **属性名**：透视模式下**垂直视野角度**（单位：度） |
| `60f` | 赋值：60° 是常用默认值；越大看得越广（鱼眼感） |

**整行人话**：只在 **Perspective（透视）** 模式下有效，控制 3D「看多宽」。

**说明**：正交模式用 `orthographicSize`，不用 fieldOfView。

---

#### `camera.orthographic = true;` 是什么？

```csharp
camera.orthographic = true;
```

| 部分 | 含义 |
|------|------|
| `orthographic` | **属性名**：bool，投影模式开关 |
| `true` | 正交投影：无近大远小，2D/等距常用 |
| `false` | 透视投影：近大远小，3D 常用 |

**整行人话**：一键切换 2D 正交 / 3D 透视。

---

#### `camera.orthographicSize = 5f;` 是什么？

```csharp
camera.orthographicSize = 5f;
```

| 部分 | 含义 |
|------|------|
| `orthographicSize` | **属性名**：正交时相机可见区域**半高**（世界单位） |
| `5f` | 半高 5 → 屏幕垂直方向总共约 10 单位可见 |

**整行人话**：只在 **orthographic = true** 时有效；数值越大，画面里看到的范围越大。

| 属性 | 类型 | 作用 |
|------|------|------|
| `fieldOfView` | float | 透视垂直 FOV（度） |
| `orthographic` | bool | true=正交，false=透视 |
| `orthographicSize` | float | 正交半高 |

---

### 1.2 裁剪与背景 — 逐词读懂

#### `camera.nearClipPlane` / `farClipPlane` 是什么？

```csharp
camera.nearClipPlane = 0.3f;
camera.farClipPlane = 1000f;
```

| 部分 | 含义 |
|------|------|
| `nearClipPlane` | **近裁剪面**：比此距离**更近**的物体不渲染 |
| `farClipPlane` | **远裁剪面**：比此距离**更远**的物体不渲染 |
| 单位 | 世界单位，相对相机位置 |

**整行人话**：只渲染「离相机 near ~ far 之间」的物体；太近穿模、太远消失都由这两个控制。

---

#### `camera.clearFlags` / `backgroundColor` 是什么？

```csharp
camera.clearFlags = CameraClearFlags.SolidColor;
camera.backgroundColor = Color.black;
```

| 部分 | 含义 |
|------|------|
| `clearFlags` | 每帧渲染前**如何清屏** |
| `CameraClearFlags.SolidColor` | 枚举值：用纯色填满背景 |
| `backgroundColor` | Solid Color 模式下的**背景颜色** |

**Clear Flags 常用值**：

| 枚举值 | 用途 |
|--------|------|
| `Skybox` | 3D 场景默认，显示天空盒 |
| `SolidColor` | 纯色背景，2D 常用 |
| `DepthOnly` | 多相机叠加时只清深度 |
| `Nothing` | 不清除（UI 叠加相机） |

**整行人话**：决定每帧开始画之前，屏幕底色是天空盒还是纯色。

---

### 1.3 多相机与 Layer — 逐词读懂

#### `camera.depth = 1;` 是什么？

```csharp
camera.depth = 1;
```

| 部分 | 含义 |
|------|------|
| `depth` | **属性名**：渲染**顺序**优先级 |
| 数值越大 | 越**后**渲染，画面叠在上层 |

**整行人话**：多相机时，depth 大的盖住 depth 小的（如 UI 相机 depth=1 叠在场景相机上）。

---

#### `camera.cullingMask = layerMask;` 是什么？

```csharp
camera.cullingMask = layerMask;
```

| 部分 | 含义 |
|------|------|
| `cullingMask` | **属性名**：该相机**只渲染**哪些 Layer |
| `layerMask` | LayerMask 类型，Inspector 里勾选 Layer |

**整行人话**：这个相机「能看哪些层」；UI 相机常只勾 UI Layer。

---

### 1.4 静态属性 `Camera.main` — 逐词读懂

```csharp
Camera mainCam = Camera.main;
```

| 部分 | 含义 |
|------|------|
| `Camera` | 类名，相机组件类型 |
| `.main` | **静态属性**：场景中 Tag 为 **MainCamera** 的第一个**启用**相机 |
| `mainCam` | 变量名，缓存引用 |

**整行人话**：快速拿「主相机」；没有 MainCamera 时返回 `null`；**宜 Awake 缓存**，不要每帧调用。

| 对比 | `Camera.main` | `GetComponent<Camera>()` |
|------|---------------|---------------------------|
| 查找范围 | 整个场景 | 当前 GameObject |
| 条件 | Tag 必须是 MainCamera | 物体上必须有 Camera |
| 性能 | 有查找开销，宜缓存 | 一次获取后可缓存 |

---

## 二、坐标空间与转换方法

### 2.1 三种坐标（官方）

| 空间 | 范围 | 用途 |
|------|------|------|
| **Screen** | 像素 (0,0) 左下 ~ (width, height) 右上 | 鼠标 `Input.mousePosition` |
| **Viewport** | 归一化 0~1 | 相对屏幕比例 |
| **World** | 场景全局坐标 | 物体 `Transform.position` |

---

### 2.2 常用转换 API — 逐词读懂

#### `cam.WorldToScreenPoint(worldPos)` 是什么？

```csharp
Vector3 screenPos = cam.WorldToScreenPoint(worldPos);
```

| 部分 | 含义 |
|------|------|
| `WorldToScreenPoint` | **方法名**：世界坐标 → 屏幕像素坐标 |
| `worldPos` | **参数**：Vector3，场景中的世界坐标 |
| **返回值** | Vector3，x/y 为屏幕像素；z 为到相机距离 |

**整行人话**：问「这个 3D 物体在屏幕的哪个像素位置」，做血条、名字牌常用。

---

#### `cam.ScreenToWorldPoint(screenPos)` 是什么？

```csharp
Vector3 worldPos = cam.ScreenToWorldPoint(new Vector3(mouseX, mouseY, depth));
```

| 部分 | 含义 |
|------|------|
| `ScreenToWorldPoint` | **方法名**：屏幕坐标 → 世界坐标 |
| `mouseX, mouseY` | 屏幕像素 x、y |
| `depth` | **关键参数**：该屏幕点对应的世界深度（到相机距离） |

**整行人话**：鼠标点 + 指定深度 → 世界坐标；**必须给 z/depth**，否则深度不对。

---

#### `cam.ScreenPointToRay(screenPos)` 是什么？

```csharp
Ray ray = cam.ScreenPointToRay(Input.mousePosition);
```

| 部分 | 含义 |
|------|------|
| `ScreenPointToRay` | **方法名**：屏幕点 → **Ray 射线**（不是单个世界点） |
| `Input.mousePosition` | **参数**：屏幕像素坐标 Vector3 |
| **返回值** | `Ray`：origin（相机侧）+ direction（指向 3D 世界） |

**整行人话**：从相机穿过鼠标点画一条线到 3D 场景，配合 `Physics.Raycast` 做点击检测（详见 [03_Raycast.md](./03_Raycast.md)）。

---

#### `cam.ViewportPointToRay(viewportPos)` 是什么？

```csharp
Ray ray = cam.ViewportPointToRay(new Vector3(0.5f, 0.5f, 0f));
```

| 部分 | 含义 |
|------|------|
| `ViewportPointToRay` | 视口坐标（0~1）→ Ray |
| `(0.5, 0.5)` | 屏幕正中心 |

**整行人话**：与 ScreenPointToRay 类似，但参数是 0~1 归一化坐标，与分辨率无关。

| 方法 | 参数 | 返回值 |
|------|------|--------|
| `WorldToScreenPoint` | 世界坐标 | 屏幕像素 |
| `ScreenToWorldPoint` | 屏幕坐标（含 z 深度） | 世界坐标 |
| `ScreenPointToRay` | 屏幕坐标 | Ray |
| `ViewportPointToRay` | 视口 0~1 | Ray |

---

## 三、标准使用步骤

```
步骤1  场景中有 Camera（Main Camera）
步骤2  Inspector 设置 Projection / FOV / Clipping / Clear Flags
步骤3  脚本获取引用（Awake 缓存 Camera.main 或 SerializeField）
步骤4  Update/LateUpdate 控制位置旋转，或 ScreenPointToRay 交互
```

| 回调 | 相机用途 |
|------|----------|
| `Update` | 鼠标旋转、输入控制 |
| `LateUpdate` | **跟随目标**（目标先动，相机后动，避免抖动） |
| `Awake/Start` | 缓存 `Camera.main` |

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

**语法拆解的标准格式**（遇到 `[SerializeField]`、`out`、`Vector3.Lerp` 等不熟悉的写法时使用）：

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

### 案例 1：第三人称跟随相机

**功能**：相机平滑跟随玩家，始终在玩家后方上方。

```csharp
using UnityEngine;                                      // 引入 Unity 核心库（Transform、MonoBehaviour 等）

public class CameraFollow : MonoBehaviour               // 脚本类，继承 MonoBehaviour 才能挂到 GameObject
{
    [SerializeField] private Transform target;          // 跟随目标：玩家 Transform（Inspector 可拖拽赋值）
    [SerializeField] private Vector3 offset = new Vector3(0f, 5f, -10f);  // 相机相对玩家的偏移：上 5、后 10
    [SerializeField] private float smoothSpeed = 5f;  // 平滑跟随速度，越大跟得越紧

    void LateUpdate()                                   // LateUpdate：所有 Update 执行完后再调用（跟随相机标配）
    {
        if (target == null) return;                     // 没指定目标则直接返回，避免空引用报错

        Vector3 desiredPos = target.position + offset;  // 期望位置 = 玩家世界坐标 + 偏移量
        transform.position = Vector3.Lerp(              // 当前位置向期望位置平滑插值（非瞬移）
            transform.position, desiredPos, smoothSpeed * Time.deltaTime);
        transform.LookAt(target);                       // 相机始终朝向玩家
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
| `void` | 无返回值 |
| `LateUpdate` | Unity 生命周期函数，在**本帧所有 Update** 执行完后调用 |
| 相机跟随用途 | 玩家先在 Update 里移动，相机再在 LateUpdate 跟随，避免一帧延迟抖动 |

**整行人话**：等目标动完再移动相机，跟随更稳定。

---

##### `[SerializeField] private Transform target` 是什么？

```csharp
[SerializeField] private Transform target;
```

| 部分 | 含义 |
|------|------|
| `[SerializeField]` | 特性：让 private 字段也在 Inspector 显示，可拖拽赋值 |
| `private` | 仅本脚本内部访问 |
| `Transform` | 位置/旋转/缩放组件类型 |
| `target` | 变量名：要跟随的目标 |

**整行人话**：在 Inspector 里拖玩家进来，脚本才能知道跟谁。

---

##### `Vector3.Lerp(...)` 是什么？

```csharp
transform.position = Vector3.Lerp(transform.position, desiredPos, smoothSpeed * Time.deltaTime);
```

| 部分 | 含义 |
|------|------|
| `Vector3.Lerp(a, b, t)` | 在 a 与 b 之间按 t（0~1）插值 |
| `smoothSpeed * Time.deltaTime` | 每帧推进比例，与帧率无关 |
| 效果 | 相机逐渐靠近目标，而非瞬间跳过去 |

**整行人话**：用插值做平滑跟随，避免相机硬切。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 3 | `public class CameraFollow : MonoBehaviour` | 可挂载的脚本类 |
| 5 | `[SerializeField] private Transform target` | 见上方语法拆解 |
| 6 | `offset = new Vector3(0f, 5f, -10f)` | 默认在玩家上方 5、后方 10 的位置 |
| 7 | `smoothSpeed = 5f` | 跟随平滑系数，可在 Inspector 调整 |
| 9 | `void LateUpdate()` | 见上方语法拆解 |
| 11 | `if (target == null) return` | 未拖入目标时不执行跟随逻辑 |
| 13 | `desiredPos = target.position + offset` | 计算相机本帧应到达的位置 |
| 14~15 | `Vector3.Lerp(...)` | 见上方语法拆解 |
| 16 | `transform.LookAt(target)` | 让相机朝向玩家中心 |

#### 操作提示

脚本挂到 **Main Camera**；Inspector 将 Player 拖到 **Target**；若相机抖动，确认玩家移动写在 **Update** 而非 FixedUpdate。

---

### 案例 2：鼠标点击发射射线

**功能**：点击屏幕，从相机发出射线检测碰到的 3D 物体。

```csharp
using UnityEngine;                                      // 引入 Unity 核心库

public class CameraClickRay : MonoBehaviour             // 点击射线检测脚本
{
    Camera cam;                                         // 缓存主相机引用，避免每帧查找

    void Awake()                                        // Awake：物体初始化时执行（早于 Start）
    {
        cam = Camera.main;                              // 获取 Tag=MainCamera 的主相机
    }

    void Update()                                       // Update：每帧执行，处理输入
    {
        if (Input.GetMouseButtonDown(0))                // 鼠标左键在本帧被按下（仅触发一次）
        {
            Ray ray = cam.ScreenPointToRay(Input.mousePosition);  // 屏幕像素坐标 → 世界空间射线
            if (Physics.Raycast(ray, out RaycastHit hit))         // 射线检测，命中则 hit 含详情
            {
                Debug.Log("点到：" + hit.collider.name);          // Console 输出被点 Collider 的名字
            }
        }
    }
}
```

#### 语法拆解

##### `cam.ScreenPointToRay(Input.mousePosition)` 是什么？

```csharp
Ray ray = cam.ScreenPointToRay(Input.mousePosition);
```

| 部分 | 含义 |
|------|------|
| `ScreenPointToRay` | Camera 方法：从相机位置穿过屏幕点画一条射线到 3D 世界 |
| `Input.mousePosition` | 鼠标屏幕像素坐标（左下角为原点） |
| 返回值 `Ray` | 射线结构体：origin（起点）+ direction（方向） |

**整行人话**：把鼠标点击的 2D 点，变成 3D 世界里的一条「激光」做碰撞检测。

---

##### `Physics.Raycast(ray, out RaycastHit hit)` 是什么？

```csharp
if (Physics.Raycast(ray, out RaycastHit hit))
```

| 部分 | 含义 |
|------|------|
| `Physics.Raycast` | 3D 物理静态方法：射线与 Collider 求交 |
| `out RaycastHit hit` | 输出参数：命中时写入交点、法线、collider 等 |
| 返回值 `bool` | true = 碰到 Collider；false = 未碰到 |

**整行人话**：射线打中物体返回 true，`hit.collider` 就是被点的碰撞体。

---

##### `Input.GetMouseButtonDown(0)` 是什么？

```csharp
if (Input.GetMouseButtonDown(0))
```

| 部分 | 含义 |
|------|------|
| `Input` | Unity 输入类 |
| `GetMouseButtonDown` | 鼠标按键**本帧刚按下**时返回 true（不是长按） |
| `0` | 0=左键，1=右键，2=中键 |

**整行人话**：只在「点下去那一瞬间」发一次射线，不会每帧连发。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 3 | `public class CameraClickRay : MonoBehaviour` | 可挂载的脚本类 |
| 5 | `Camera cam;` | 声明相机变量，用于缓存引用 |
| 7 | `void Awake()` | 初始化阶段执行一次 |
| 9 | `cam = Camera.main;` | 缓存主相机（场景需有 MainCamera Tag） |
| 11 | `void Update()` | 每帧检测输入 |
| 13 | `GetMouseButtonDown(0)` | 见上方语法拆解 |
| 15 | `ScreenPointToRay(...)` | 见上方语法拆解 |
| 16 | `Physics.Raycast(...)` | 见上方语法拆解 |
| 18 | `Debug.Log(...)` | 在 Console 打印命中物体名 |

#### 操作提示

被点击物体需有 **Collider**；场景需有 Physics 模块；主相机 Tag 为 **MainCamera**。  
射线检测的完整 API、LayerMask、RaycastAll、2D 与避坑见 **[03_Raycast.md](./03_Raycast.md)**。

---

### 案例 3：2D 正交相机设置

**功能**：脚本初始化 2D 游戏常用正交相机参数。

```csharp
using UnityEngine;                                      // 引入 Unity 核心库

public class Camera2DSetup : MonoBehaviour              // 2D 相机初始化脚本，挂到 Main Camera 上
{
    void Start()                                        // Start：第一帧 Update 前执行一次
    {
        Camera cam = GetComponent<Camera>();            // 获取本物体上的 Camera 组件（相机与脚本同物体）
        cam.orthographic = true;                        // 切换为正交投影（2D 无近大远小）
        cam.orthographicSize = 5f;                      // 正交半高：可见区域垂直方向一半为 5 单位
        cam.clearFlags = CameraClearFlags.SolidColor;   // 每帧用纯色清屏（不用天空盒）
        cam.backgroundColor = new Color(0.1f, 0.1f, 0.15f);  // 深蓝灰背景色（RGBA 0~1）
        cam.transform.position = new Vector3(0f, 0f, -10f);  // 2D 常用：相机在 Z=-10 看向 XY 平面
    }
}
```

#### 语法拆解

##### `GetComponent<Camera>()` 是什么？

```csharp
Camera cam = GetComponent<Camera>();
```

| 部分 | 含义 |
|------|------|
| `GetComponent<T>()` | 获取**当前 GameObject** 上类型为 T 的组件 |
| `<Camera>` | 泛型参数：指定要获取 Camera 组件 |
| 与 `Camera.main` 区别 | 只查本物体，不依赖 MainCamera Tag |

**整行人话**：从挂脚本的同一个物体上拿 Camera 组件。

---

##### `cam.orthographic = true` 是什么？

```csharp
cam.orthographic = true;
```

| 部分 | 含义 |
|------|------|
| `orthographic` | Camera 投影模式开关 |
| `true` | 正交：平行投影，2D 常用 |
| `false` | 透视：近大远小，3D 常用 |

**整行人话**：把相机切成 2D 正交模式。

---

##### `CameraClearFlags.SolidColor` 是什么？

```csharp
cam.clearFlags = CameraClearFlags.SolidColor;
```

| 部分 | 含义 |
|------|------|
| `clearFlags` | 每帧渲染前如何清除颜色/深度缓冲 |
| `SolidColor` | 用 `backgroundColor` 填充满屏 |
| 对比 `Skybox` | 3D 场景常用天空盒；2D 常用纯色 |

**整行人话**：不用天空盒，整屏刷成设定的背景色。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 3 | `public class Camera2DSetup : MonoBehaviour` | 可挂载的脚本类 |
| 5 | `void Start()` | 游戏开始时执行一次 |
| 7 | `GetComponent<Camera>()` | 见上方语法拆解 |
| 8 | `orthographic = true` | 见上方语法拆解 |
| 9 | `orthographicSize = 5f` | 视野半高 5，越大看得越远 |
| 10 | `clearFlags = SolidColor` | 见上方语法拆解 |
| 11 | `backgroundColor = new Color(...)` | 设置清屏背景色 |
| 12 | `position = (0,0,-10)` | 相机退到 Z 轴负方向观察 2D 平面 |

#### 操作提示

脚本挂到 **Main Camera**；2D 精灵放在 Z=0 附近；若画面全黑，检查 **Culling Mask** 是否包含精灵 Layer。

---

## 【入门阶段小结】

| 维度 | 要点 |
|------|------|
| **属性** | FOV / orthographicSize / clipping / clearFlags / depth |
| **方法** | ScreenPointToRay、WorldToScreenPoint |
| **时机** | 跟随用 LateUpdate |
| **案例** | 跟随、点击射线、2D 正交 |

---

# 第三阶段：进阶篇

## 【阶段总述】

进阶阶段：**多相机分工、Layer 与 depth、封装、Cinemachine 选型、URP 堆叠简介、避坑**。

---

## 一、多相机架构

```
主相机（depth=0）  → 渲染 3D 场景 Layer：Default
UI 相机（depth=1） → 只渲染 Layer：UI，Clear Flags = Depth Only
小地图（depth=2）  → 渲染到 RenderTexture 或 Viewport Rect
```

| 参数 | 分工 |
|------|------|
| `depth` | 谁后渲染（叠在上层） |
| `cullingMask` | 各相机看哪些 Layer |
| `clearFlags` | 叠加相机常用 Depth Only 或 Nothing |
| `targetTexture` | 渲染到纹理（小地图、监控画面） |

---

## 二、工程化封装

```csharp
public class CameraController : MonoBehaviour
{
    public static CameraController Instance { get; private set; }
    public Camera MainCam { get; private set; }

    void Awake()
    {
        Instance = this;
        MainCam = Camera.main;
    }

    public Ray ScreenRay(Vector3 screenPos) => MainCam.ScreenPointToRay(screenPos);
}
```

---

## 三、Cinemachine 进阶方案（选型）

| 对比 | 手写 CameraFollow | Cinemachine |
|------|-------------------|-------------|
| 适用 | 简单跟随、学习原理 | 复杂镜头、切换、抖动、轨道 |
| 核心 | LateUpdate + Lerp | Virtual Camera + Follow/LookAt |
| 安装 | 无需 | Package Manager 安装 Cinemachine |

**结论**：入门用手写理解原理；项目镜头需求多时用 Cinemachine。

---

## 四、URP 相机堆叠（简述）

| 类型 | 作用 |
|------|------|
| **Base Camera** | 渲染场景主体 |
| **Overlay Camera** | 叠加 UI、特效等 |

Built-in 管线用 `depth` 实现类似效果；URP 用 Camera Stack 配置。

---

## 五、常见误区与最佳实践

| 误区 | 正确做法 |
|------|----------|
| 跟随写在 Update | 改 LateUpdate |
| 每帧 `Camera.main` | Awake 缓存 |
| 多个 MainCamera Tag | 场景只保留一个 MainCamera |
| UI 和 3D 同一 Layer | UI 单独 Layer + UI 相机 |
| Near 裁剪面过大 | 3D 常用 0.1~0.3，避免近处裁剪 |

---

## 【进阶阶段小结】

| 维度 | 要点 |
|------|------|
| 多相机 | depth + cullingMask 分工 |
| 封装 | 单例 + 缓存 MainCam |
| 选型 | 简单手写 / 复杂 Cinemachine |
| 避坑 | LateUpdate、缓存 main、Layer 分离 |

---

# 【全文总结】

## 最重要的一行代码

```csharp
Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
```

| 部分 | 含义 |
|------|------|
| `Camera.main` | 主相机 |
| `ScreenPointToRay` | 屏幕点 → 3D 射线 |
| `Input.mousePosition` | 鼠标位置 |

后续 `Physics.Raycast(ray, out hit)` 及 LayerMask 等详见 **[03_Raycast.md](./03_Raycast.md)**。

## 三阶段对照

| 阶段 | 代表案例 |
|------|----------|
| 零基础 | 认识透视/正交、Inspector 参数 |
| 入门 | 跟随、点击射线、2D 正交 |
| 进阶 | 多相机、Cinemachine 选型 |

## API 速查

| 代码 | 作用 |
|------|------|
| `Camera.main` | 获取主相机 |
| `fieldOfView` | 透视视野 |
| `orthographicSize` | 正交半高 |
| `ScreenPointToRay` | 屏幕 → 射线 |
| `WorldToScreenPoint` | 世界 → 屏幕 |
| `depth` | 渲染顺序 |
| `cullingMask` | 渲染 Layer |

## 学习自检

- [ ] 透视与正交区别？
- [ ] `Camera.main` 条件？
- [ ] 为什么跟随用 LateUpdate？
- [ ] ScreenPointToRay 做什么？
- [ ] 多相机如何分工？

---

## 参考资料

| 类型 | 链接 |
|------|------|
| Camera 官方 API | https://docs.unity3d.com/ScriptReference/Camera.html |
| 相机概述 Manual | https://docs.unity3d.com/Manual/CamerasOverview.html |
| Camera.main | https://docs.unity3d.com/ScriptReference/Camera-main.html |
| Cinemachine | https://docs.unity3d.com/Packages/com.unity.cinemachine@latest |
