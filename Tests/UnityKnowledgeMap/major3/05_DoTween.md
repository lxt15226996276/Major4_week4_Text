# Unity 插件 DOTween 详解

> 参照：[DOTween 官方文档](http://dotween.demigiant.com/documentation.php) · [DOTween API](https://dotween.demigiant.com/api/class_d_g_1_1_tweening_1_1_d_o_tween.html) · [ShortcutExtensions](https://dotween.demigiant.com/api/class_d_g_1_1_tweening_1_1_shortcut_extensions.html)  
> 作者：Demigiant（Daniele Giardini）— **第三方插件**，非 Unity 内置。  
> 学习路径：**零基础 → 入门 → 进阶**，每阶段采用 **总—分—总** 结构。  
> 讲解维度：**定义 → 本质 → 特点 → 适用场景 → 原理 → API → 步骤 → 案例 → 避坑**（进阶含 Sequence / UI / 生命周期）。  
> 案例讲解：遵循 **案例代码讲解模板**（功能 → 代码 → 语法拆解 → 逐行详解 → 操作提示）。  
> API 讲解：入门/进阶 API 章节均采用 **逐词读懂** 格式（与 [01_PlayerPrefs.md](./01_PlayerPrefs.md) 一致：类型 → 参数 → 整行人话）。

---

## 【全文总述】

**DOTween**（常写作 DoTween）是 Unity 最流行的**补间动画（Tween）**插件：用一行代码让位置、缩放、透明度等在指定时间内平滑变化，无需手写插值、无需 Animator Controller。  
核心概念：**Tweener**（单属性动画）与 **Sequence**（多段串联）；常用链式写法：`transform.DOMove(...).SetEase(...).OnComplete(...)`。  
典型用途：UI 弹窗、按钮反馈、物体移动、淡入淡出、过场衔接——**短平快的程序化动画**首选。

### 思维导图总览

```
Unity 插件 DOTween（Demigiant — 第三方 Tween 补间引擎）
│
├── 安装与初始化
│   │
│   ├── 定义：对属性/字段做「从当前值 → 目标值」时间插值的动画库
│   │   └── 官方：Tweener takes a property/field and animates it towards a given value
│   │
│   ├── 获取方式
│   │   ├── Unity Asset Store 搜索 DOTween（免费版）
│   │   ├── 或 demigiant.com 下载导入
│   │   └── 导入后首次 Setup：Tools → Demigiant → DOTween Utility Panel → Setup DOTween
│   │
│   ├── Setup 必做
│   │   ├── 勾选需要的 Modules：UI / TextMeshPro / 2D / Audio 等
│   │   ├── 生成 DOTween 设置与程序集引用
│   │   └── 未 Setup 时 DOFade(DOAnchorPos) 等 UI 扩展不可用
│   │
│   └── 初始化 DOTween.Init（推荐手动，在首次创建 Tween 之前）
│       ├── DOTween.Init() — 使用 Utility Panel 中的偏好设置
│       ├── useSafeMode：目标被 Destroy 时自动安全处理
│       └── SetCapacity：预分配 Tweener/Sequence 容量，减少运行时扩容卡顿
│
├── 核心概念（官方 Nomenclature）
│   │
│   ├── 【知识维度】（讲师框架 — 完整版）
│   │   │
│   │   ├── 定义：补间动画引擎，程序化驱动数值/Transform/UI 属性变化
│   │   │   ├── Tweener：控制单个属性，如 position、alpha、scale
│   │   │   ├── Sequence：控制多个 Tweener/Interval/Callback 的时间线
│   │   │   └── Tween：Tweener 与 Sequence 的统称
│   │   │
│   │   ├── 本质：每帧按 Ease 曲线插值 → 写入 getter/setter 或 Unity 组件属性
│   │   │   ├── 非 Animator：不依赖 Animation Clip 与 Controller
│   │   │   ├── 非 Coroutine 手写 Lerp：内置缓动、链式 API、Kill/Complete
│   │   │   └── Shortcut（DO 前缀）：transform.DOMove 自动绑定 target
│   │   │
│   │   ├── 官方定位：代码驱动的轻量动画，与 Mecanim 互补
│   │   │   ├── DOTween 适合：UI、反馈、过渡、简单位移/缩放/淡入淡出
│   │   │   └── Animator 适合：角色 locomotion、复杂骨骼、Blend Tree
│   │   │
│   │   ├── 特点
│   │   │   ├── 优势：API 简洁、链式 Set/On、Sequence 编排、UI 模块丰富、性能好
│   │   │   └── 局限：第三方依赖；复杂角色动画不如 Mecanim；需 Kill 防泄漏
│   │   │
│   │   ├── 适用场景
│   │   │   ├── ✅ 适用：UI 面板、血条、飘字、按钮缩放、相机 FOV、材质 Fade
│   │   │   └── ❌ 不适用：多骨骼连招、Root Motion 角色跑跳（用 Animator）
│   │   │
│   │   ├── 命名前缀（官方）
│   │   │   ├── DO：快捷方法 DOMove / DOFade / DOTween.Sequence()
│   │   │   ├── Set：链式设置 SetEase / SetLoops / SetDelay / SetUpdate
│   │   │   └── On：回调 OnComplete / OnKill / OnUpdate
│   │   │
│   │   ├── 核心 API 及参数
│   │   │   ├── Transform：DOMove / DOLocalMove / DOScale / DORotate / DOJump
│   │   │   ├── UI：CanvasGroup.DOFade / RectTransform.DOAnchorPos / Image.DOFillAmount
│   │   │   ├── 通用：DOTween.To(getter, setter, endValue, duration)
│   │   │   ├── Sequence：Append / Join / AppendInterval / AppendCallback
│   │   │   ├── 设置：SetEase / SetLoops / SetDelay / SetUpdate / SetLink
│   │   │   └── 控制：Kill / Complete / Pause / Play / DORestart（target 快捷）
│   │   │
│   │   ├── 标准使用步骤（五步）
│   │   │   ├── 步骤1 导入 DOTween 并 Setup（勾选 UI Module）
│   │   │   ├── 步骤2 脚本 using DG.Tweening;
│   │   │   ├── 步骤3 可选 Awake 中 DOTween.Init()
│   │   │   ├── 步骤4 创建 Tweener 或 Sequence，链式 SetEase / OnComplete
│   │   │   └── 步骤5 物体销毁前 transform.DOKill() 或 SetLink(gameObject)
│   │   │
│   │   ├── 生命周期与调用时机
│   │   │   ├── 触发时创建：按钮点击、面板打开、关卡开始
│   │   │   ├── OnDestroy / OnDisable：DOKill() 停止并释放
│   │   │   ├── SetUpdate(true)：timeScale=0 时 UI 仍可播（暂停菜单）
│   │   │   └── SetLink(go)：物体 Destroy 时自动 Kill
│   │   │
│   │   ├── Ease 缓动
│   │   │   ├── OutQuad / InOutCubic / OutBack / OutElastic 等
│   │   │   ├── 默认：Ease.OutQuad（可在 Utility Panel 改）
│   │   │   └── 参考：easings.net 曲线预览
│   │   │
│   │   └── 选型、封装、避坑
│   │       ├── 选型：单属性 → Tweener；多步编排 → Sequence
│   │       ├── 封装：TweenUI.ShowPanel / TweenUI.HidePanel
│   │       └── 避坑：未 Setup、重复 Tween 冲突、未 Kill、From 瞬间跳变、与 Animator 抢 Transform
│   │
│   ├── 第一阶段：零基础（建立认知 + 读懂代码）
│   │   ├── 理解 Tweener / Sequence / Tween
│   │   ├── 逐词读懂：transform.DOMove(pos, 1f).SetEase(Ease.OutQuad)
│   │   └── 区分 DOTween 与 Unity Animator
│   │
│   ├── 第二阶段：入门（Shortcut + Set + 案例）
│   │   ├── DOMove / DOScale / DOFade 与链式 API
│   │   ├── Sequence：Append / Join / AppendInterval
│   │   └── 实战案例：物体移动 / UI 淡入淡出 / 面板弹出 Sequence
│   │
│   └── 第三阶段：进阶（DOTween.To + 控制 + 封装 + 性能）
│       ├── DOTween.To 泛型补间任意字段
│       ├── Kill / Complete / SetLink / SetUpdate
│       ├── From 反向补间、SetLoops、DOVirtual
│       └── TweenHelper 封装 + 与 Animator 协作避坑
│
└── DOTween Pro（付费扩展 — 了解即可）
    │
    ├── 可视化 DOTween Animation 组件、Path 路径编辑
    ├── 本教程以免费版 API 为主，Pro 为可选增强
    └── 官网：http://dotween.demigiant.com
```

| 学习阶段 | 学习目标 |
|----------|----------|
| **零基础** | 说清 Tweener/Sequence；读懂 DOMove + SetEase；会 Setup |
| **入门** | 掌握 DO 快捷方法、链式 Set/On、Sequence；完成 3 案例 |
| **进阶** | 会 DOTween.To、Kill/SetLink、timeScale UI；封装与避坑 |

### 讲师知识框架速览（全文脉络）

| 维度 | 零基础讲 | 入门讲 | 进阶讲 |
|------|----------|--------|--------|
| 定义 | ✅ | 回顾 | 回顾 |
| 本质 | ✅ | — | — |
| 特点 | ✅ | — | DOTween vs Animator |
| 适用场景 | ✅ | — | 选型 |
| 核心原理 | 插值+Ease | ✅ Shortcut | DOTween.To |
| 核心 API | 读懂 DOMove | ✅ DOFade/Sequence | Kill/SetLink |
| 使用步骤 | Setup | ✅ 五步 | 封装 |
| 调用时机 | — | ✅ 点击触发 | OnDestroy Kill |
| 避坑 | — | 初步 | ✅ |

---

# 第一阶段：零基础篇

## 【阶段总述】

零基础阶段建立**正确认知**：DOTween 是什么、与 Animator 有何不同、安装后为何要 Setup。  
同时学会**读懂** `transform.DOMove(target, 1f).SetEase(Ease.OutQuad)`。

---

## 一、定义 — DOTween 是什么？

| 项目 | 说明 |
|------|------|
| **类型** | 第三方插件，命名空间 `DG.Tweening` |
| **作者** | Demigiant（Daniele Giardini） |
| **官方定义** | Animation engine for Unity — tweening library |
| **一句话** | 用代码让数值/Transform/UI 属性在指定时间内平滑变化 |

| 术语 | 说明 |
|------|------|
| **Tweener** | 控制**一个**属性从 A 到 B 的补间 |
| **Sequence** | 把多个 Tweener、等待、回调按时间线编排 |
| **Tween** | Tweener + Sequence 的统称 |

```csharp
using DG.Tweening;

// Tweener：移动 1 秒
transform.DOMove(new Vector3(0, 2, 0), 1f);

// Sequence：先移后缩
Sequence seq = DOTween.Sequence();
seq.Append(transform.DOMove(Vector3.zero, 0.5f));
seq.Append(transform.DOScale(1.2f, 0.3f));
```

---

## 二、本质 — DOTween 如何工作？

```
创建 Tween（指定 endValue + duration）
       │
       ▼
每帧按 Ease 曲线计算插值（0→1）
       │
       ▼
写入目标属性（Transform.position / CanvasGroup.alpha …）
       │
       ▼
完成 → OnComplete；或 Kill 提前终止
```

| 对比 | DOTween | Unity Animator |
|------|---------|----------------|
| 数据来源 | 代码指定目标值 | Animation Clip 关键帧 |
| 状态机 | Sequence 简单编排 | Animator Controller |
| 典型用途 | UI、反馈、短动画 | 角色骨骼、跑跳攻击 |
| 依赖 | 需导入插件 | Unity 内置 |

---

## 三、安装与 Setup（必做）

| 步骤 | 操作 |
|------|------|
| 1 | Asset Store 或官网下载 **DOTween**，导入 Unity 工程 |
| 2 | 菜单 **Tools → Demigiant → DOTween Utility Panel** |
| 3 | 点击 **Setup DOTween…**，勾选需要的 **Modules**（至少勾 **UI** 若做界面） |
| 4 | 点击 Apply，等待编译完成 |
| 5 | 脚本顶部 `using DG.Tweening;` |

| Module | 作用 |
|--------|------|
| **UI** | CanvasGroup / RectTransform / Image 的 DOFade、DOAnchorPos |
| **TextMeshPro** | TMP 文字 DOFade、DOCounter |
| **2D** | SpriteRenderer DOFade、DOColor |
| **Physics** | Rigidbody DOMove（与 Transform 版二选一） |

未 Setup 时调用 `canvasGroup.DOFade` 会报错或找不到扩展方法。

---

## 四、初始化 DOTween.Init（推荐）

官方：第一次创建 Tween 时会**自动 Init**；建议在**任何 Tween 之前**手动调用一次。

```csharp
void Awake()
{
    DOTween.Init();  // 使用 Utility Panel 中的默认设置
}
```

| 参数 | 含义 |
|------|------|
| `recycleAllByDefault` | true：Kill 后回收到池，少 GC，需注意引用 |
| `useSafeMode` | true：目标 Destroy 时 tween 安全停止（推荐 true） |
| `logBehaviour` | 日志级别：ErrorsOnly / Warnings / Verbose |

```csharp
// 预分配容量，减少运行时扩容（官方 SetCapacity）
DOTween.Init(false, true, LogBehaviour.ErrorsOnly).SetCapacity(200, 50);
```

---

## 五、核心一课：如何读懂 DOMove

```csharp
transform.DOMove(new Vector3(0, 5, 0), 1f).SetEase(Ease.OutQuad);
```

| 部分 | 含义 |
|------|------|
| `transform` | Transform 引用，DOTween 扩展方法的目标 |
| `.DOMove` | **DO 前缀**快捷方法：补间**世界坐标** position |
| `new Vector3(0, 5, 0)` | 目标位置 endValue |
| `1f` | 持续时间 duration（秒） |
| `.SetEase(Ease.OutQuad)` | **Set 前缀**：缓动曲线，先快后慢 |

**整行人话**：1 秒内平滑移到 (0,5,0)，结尾减速。

```csharp
canvasGroup.DOFade(0f, 0.5f).OnComplete(() => gameObject.SetActive(false));
```

| 部分 | 含义 |
|------|------|
| `DOFade` | 补间 CanvasGroup.alpha 到 0（全透明） |
| `OnComplete` | **On 前缀**：播完时执行的回调 |

---

## 【零基础阶段小结】

| 维度 | 要点 |
|------|------|
| **定义** | Tweener=单属性；Sequence=时间线 |
| **Setup** | Utility Panel 勾 Module |
| **前缀** | DO 创建 / Set 配置 / On 回调 |
| **读懂** | DOMove(end, duration).SetEase(...) |

**阶段检验**：能区分 DOTween 与 Animator；能说出 Setup 的作用。

---

# 第二阶段：入门篇

## 【阶段总述】

入门阶段掌握 **常用 DO 快捷方法**、**链式 Set/On**、**Sequence 编排**，并完成 3 个实战案例。

---

## 一、常用 Shortcut 详解 — 逐词读懂

> 以下采用与 [01_PlayerPrefs.md](./01_PlayerPrefs.md) 相同的 **逐词读懂** 格式。  
> DOTween 扩展方法均以 **DO** 为前缀，挂在 Transform / CanvasGroup 等对象上调用。

### API 全景

```
Shortcut（DO 前缀 — 从对象直接创建 Tweener）
├── Transform：DOMove / DOLocalMove / DOScale / DORotate / DOJump
├── UI：DOFade / DOAnchorPos / DOFillAmount
└── 其他：Camera.DOFieldOfView / Material.DOFade
```

---

### 1.1 `transform.DOMove` — 核心 API 逐词读懂

```csharp
transform.DOMove(endPos, 1f);
```

| 部分 | 含义 |
|------|------|
| `transform` | **调用对象**：Transform 组件（谁在动） |
| `.DOMove` | **扩展方法名**：补间 **世界坐标** position |
| `endPos` | **参数1 endValue**：Vector3，目标世界坐标 |
| `1f` | **参数2 duration**：float，动画持续时间（**秒**，不是速度） |
| **返回值** | `Tweener`，可继续 `.SetEase()` / `.OnComplete()` |

**整行人话**：1 秒内把物体从**当前位置**平滑移到 `endPos`。

---

### 1.2 Transform 其它 Shortcut

#### `DOLocalMove(localPos, duration)`

| 部分 | 含义 |
|------|------|
| `DOLocalMove` | 补间 **本地坐标**（相对父物体） |
| 对比 DOMove | DOMove=世界坐标；DOLocalMove=本地坐标 |

#### `DOScale(endScale, duration)`

```csharp
transform.DOScale(1.5f, 0.3f);
transform.DOScale(new Vector3(1, 2, 1), 0.3f);
```

| 部分 | 含义 |
|------|------|
| `1.5f` | 均匀缩放至 1.5 倍 |
| `Vector3(1,2,1)` | X/Z 1 倍、Y 2 倍（非均匀） |

#### `DORotate` / `DOLocalRotate`

| 方法 | 含义 |
|------|------|
| `DORotate` | 补间**世界**旋转（欧拉角 Vector3） |
| `DOLocalRotate` | 补间**本地**旋转 |

#### `DOJump(endValue, jumpPower, numJumps, duration)`

| 参数 | 含义 |
|------|------|
| `endValue` | 落点世界坐标 |
| `jumpPower` | 跳跃高度力度 |
| `numJumps` | 跳跃次数 |
| `duration` | 总时长 |

**整行人话**：带抛物线弧度的移动（返回 Sequence，不是普通 Tweener）。

---

### 1.3 UI Shortcut — 逐词读懂（需 Setup UI Module）

#### `canvasGroup.DOFade(endAlpha, duration)`

```csharp
canvasGroup.DOFade(1f, 0.3f);
```

| 部分 | 含义 |
|------|------|
| `CanvasGroup` | UI 成组组件，统一控制子 UI 透明度 |
| `DOFade` | 补间 **alpha**：0=全透明，1=不透明 |
| `1f` | 目标 alpha |
| `0.3f` | 0.3 秒完成 |

**整行人话**：整块 UI 淡入/淡出。

---

#### `rectTransform.DOAnchorPos(endPos, duration)`

```csharp
rectTransform.DOAnchorPos(new Vector2(0, 0), 0.5f);
```

| 部分 | 含义 |
|------|------|
| `RectTransform` | UI 矩形变换 |
| `DOAnchorPos` | 补间 **anchoredPosition**（相对锚点的 UI 坐标） |
| 对比 DOMove | UI 用 DOAnchorPos；3D 用 DOMove |

---

#### `image.DOFillAmount(endValue, duration)`

| 部分 | 含义 |
|------|------|
| `DOFillAmount` | 补间 Image **fillAmount**（0~1），进度条常用 |

---

### 1.4 其他常用

```csharp
camera.DOFieldOfView(60f, 1f);   // 补间相机 FOV
material.DOFade(0f, 1f);        // 材质 alpha（须支持透明）
audioSource.DOFade(0f, 1f);     // 补间 AudioSource.volume
```

---

## 二、链式 Set 与 On — 逐词读懂

> **Set** 前缀 = 配置 Tweener；**On** 前缀 = 回调。链式写在创建 Tweener **之后**。

### 2.1 `SetEase` — 缓动曲线

```csharp
.SetEase(Ease.OutBack)
```

| 部分 | 含义 |
|------|------|
| `SetEase` | 设置插值曲线 |
| `Ease.OutBack` | 枚举：结束时有轻微 overshoot 回弹 |
| 参考 | easings.net 预览曲线 |

**整行人话**：决定「怎么动过去」——匀速、先快后慢、弹性等。

---

### 2.2 `SetDelay` / `SetLoops` / `SetUpdate` / `SetLink`

| 方法 | 逐词读懂 |
|------|----------|
| `SetDelay(0.2f)` | 延迟 0.2 **秒**后再开始播 |
| `SetLoops(2, LoopType.Yoyo)` | 循环 2 次；Yoyo=来回往返 |
| `SetUpdate(true)` | **忽略** `Time.timeScale`，暂停游戏时 UI 仍能动 |
| `SetLink(gameObject)` | 绑定生命周期；物体 Destroy 时**自动 Kill** 此 Tween |

---

### 2.3 `OnComplete` / `OnKill` — 回调

```csharp
.OnComplete(() => Debug.Log("完成"))
.OnKill(() => myRef = null)
```

| 方法 | 含义 |
|------|------|
| `OnComplete` | Tween **正常播完**（含所有 Loop）后执行 |
| `OnKill` | Tween 被 **Kill** 时执行，可用于清空引用 |

**整行人话**：播完做下一件事用 OnComplete；被中断时清理用 OnKill。

---

### 2.4 链式示例 — 整段读懂

```csharp
transform.DOScale(1.2f, 0.2f)
    .SetEase(Ease.OutBack)
    .SetLoops(2, LoopType.Yoyo)
    .OnComplete(() => Debug.Log("弹完"));
```

| 行 | 整行人话 |
|----|----------|
| `DOScale(1.2f, 0.2f)` | 0.2 秒缩放到 1.2 倍 |
| `SetEase(OutBack)` | 带回弹感 |
| `SetLoops(2, Yoyo)` | 来回弹 2 次 |
| `OnComplete(...)` | 全部结束后 Log |

---

## 三、Sequence 编排 — 逐词读懂

### `DOTween.Sequence()` 是什么？

```csharp
Sequence seq = DOTween.Sequence();
```

| 部分 | 含义 |
|------|------|
| `DOTween` | DOTween 静态类 |
| `.Sequence()` | **静态方法**：创建空 **Sequence**（时间线容器） |
| `Sequence` | 特殊 Tween，编排多个子动画的顺序/并行 |
| `seq` | 变量名，存这条时间线 |

**整行人话**：像剪映时间轴，把多段 DOMove、DOScale 排成一组播。

---

### Append / Join / AppendInterval — 逐词读懂

```csharp
Sequence seq = DOTween.Sequence();
seq.Append(transform.DOScale(1.2f, 0.3f));
seq.Join(transform.DORotate(new Vector3(0,180,0), 0.3f));
seq.AppendInterval(0.2f);
seq.Append(transform.DOScale(1f, 0.2f));
seq.OnComplete(() => Debug.Log("Sequence 结束"));
```

| 方法 | 整行人话 |
|------|----------|
| `Append(tween)` | **排队**：接在前一段**之后**播放 |
| `Join(tween)` | **并排**：与**上一个** Append/Join **同时**开始 |
| `AppendInterval(0.2f)` | 插入 **0.2 秒空白**等待 |
| `AppendCallback(() => {})` | 在该时间点执行回调 |
| `SetLoops(-1)` | 整个 Sequence 无限循环（-1） |

**整行人话**：Append=一个接一个；Join=与上一段一起动。

---

## 四、标准五步流程

```
步骤1  导入 DOTween → Utility Panel Setup → 勾选 UI Module
步骤2  using DG.Tweening;
步骤3  触发点创建 Tweener/Sequence（如按钮 OnClick）
步骤4  链式 SetEase / SetUpdate / OnComplete
步骤5  OnDestroy 时 target.DOKill() 或创建时 SetLink(gameObject)
```

---

## 五、入门三个案例

### 案例代码讲解模板

每个案例统一按以下结构组织（下文所有案例均遵循此模板）：

| 顺序 | 板块 | 内容 |
|:----:|------|------|
| 1 | **功能** | 案例实现什么业务 |
| 2 | **完整代码** | 带行内注释的完整脚本 |
| 3 | **语法拆解** | 对案例中较生僻的语法，逐个说明（格式见下） |
| 4 | **逐行详解** | 表格：每行代码的含义 |
| 5 | **操作提示** | Unity 绑定、调用方式等（如有） |

**语法拆解的标准格式**（遇到 `using DG.Tweening`、`SetEase`、`OnComplete`、`Append/Join` 等不熟悉的写法时使用）：

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

### 案例 1：物体移动并旋转

**功能**：启动后 1 秒移到目标点，带 OutCubic 缓动，完成后 Log。

```csharp
using UnityEngine;                                      // 引入 Unity 核心库
using DG.Tweening;                                      // 引入 DOTween 命名空间（Setup 后可用）

public class TweenMoveDemo : MonoBehaviour                // DOTween 移动演示脚本
{
    public Vector3 targetPos = new Vector3(3f, 0f, 0f); // 目标世界坐标，可在 Inspector 调整
    public float duration = 1f;                         // 补间持续时间（秒）

    void Start()                                        // Start：游戏开始时执行一次
    {
        transform.DOMove(targetPos, duration)           // 创建移动 Tweener：position → targetPos
            .SetEase(Ease.OutCubic)                    // 链式设置缓动：先快后慢（Out 缓动）
            .OnComplete(() => Debug.Log("移动完成"));   // 播完回调：Lambda 无参委托
    }

    void OnDestroy()                                    // 物体销毁时 Unity 自动调用
    {
        transform.DOKill();                             // 杀死本 Transform 上所有活跃 Tween
    }
}
```

#### 语法拆解

##### `transform.DOMove(targetPos, duration)` 是什么？

```csharp
transform.DOMove(targetPos, duration)
```

| 部分 | 含义 |
|------|------|
| `DOMove` | DOTween 扩展方法（DO 前缀），补间 Transform.position |
| `targetPos` | 终点世界坐标 endValue |
| `duration` | 持续时间（秒），不是速度 |
| 返回值 | Tweener，可继续链式 `.SetEase()` 等 |

**整行人话**：从当前位置滑到 targetPos，用时 duration 秒。

---

##### `.SetEase(Ease.OutCubic)` 是什么？

```csharp
.SetEase(Ease.OutCubic)
```

| 部分 | 含义 |
|------|------|
| `Set` 前缀 | DOTween 链式配置方法 |
| `Ease.OutCubic` | 缓动枚举：结束阶段减速 |
| 参考 | easings.net 可预览曲线 |

**整行人话**：移动结尾自然减速，不是匀速硬停。

---

##### `.OnComplete(() => Debug.Log(...))` 是什么？

```csharp
.OnComplete(() => Debug.Log("移动完成"))
```

| 部分 | 含义 |
|------|------|
| `On` 前缀 | DOTween 回调方法 |
| `OnComplete` | Tween 正常播完（含所有 Loop）后触发 |
| `() => ...` | Lambda 表达式：无参匿名函数 |

**整行人话**：动画播完时在 Console 打一行日志。

---

##### `transform.DOKill()` 是什么？

```csharp
transform.DOKill();
```

| 部分 | 含义 |
|------|------|
| `DOKill` | 目标快捷方法：Kill 该 Transform 上所有 Tween |
| 调用时机 | OnDestroy，防止物体销毁后 Tween 仍改 Transform |
| 对比 `Kill()` | DOKill 按 target 过滤；myTween.Kill() 只杀单个 |

**整行人话**：物体销毁前关掉还在跑的补间，避免空引用报错。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 2 | `using DG.Tweening;` | 引用 DOTween（须先 Setup） |
| 4 | `public class TweenMoveDemo : MonoBehaviour` | 可挂载的脚本类 |
| 6 | `targetPos = new Vector3(3f, 0f, 0f)` | 默认目标点 X=3 |
| 7 | `duration = 1f` | 默认 1 秒完成 |
| 9 | `void Start()` | 开始时触发移动 |
| 11 | `DOMove(...)` | 见上方语法拆解 |
| 12 | `SetEase(OutCubic)` | 见上方语法拆解 |
| 13 | `OnComplete(...)` | 见上方语法拆解 |
| 16 | `void OnDestroy()` | 销毁生命周期 |
| 18 | `DOKill()` | 见上方语法拆解 |

#### 操作提示

挂到任意 3D 物体；Play 后观察 Scene 视图位移；可与 [03_Raycast.md](./03_Raycast.md) 点击移动对比（Raycast 定目标，DOTween 负责平滑过去）。

---

### 案例 2：UI 面板淡入淡出

**功能**：显示时 alpha 0→1；关闭时 1→0 后 SetActive(false)。

```csharp
using UnityEngine;                                      // 引入 Unity 核心库
using DG.Tweening;                                      // 引入 DOTween

public class TweenPanelFade : MonoBehaviour               // UI 面板淡入淡出脚本，挂 Panel 根节点
{
    CanvasGroup canvasGroup;                            // 控制整组 UI 透明度与射线阻挡
    public float fadeDuration = 0.35f;                  // 淡入/淡出时长（秒）

    void Awake()                                        // 初始化 CanvasGroup
    {
        canvasGroup = GetComponent<CanvasGroup>();     // 尝试获取已有组件
        if (canvasGroup == null)                        // 若没有则自动添加
            canvasGroup = gameObject.AddComponent<CanvasGroup>();
    }

    public void Show()                                  // 公开方法：绑到「打开面板」按钮 OnClick
    {
        gameObject.SetActive(true);                     // 先激活物体（否则 Tween 不更新）
        canvasGroup.alpha = 0f;                         // 初始全透明
        canvasGroup.DOFade(1f, fadeDuration)            // alpha 0 → 1 淡入
            .SetUpdate(true)                            // 忽略 timeScale（暂停时 UI 仍能动）
            .SetLink(gameObject);                       // 物体 Destroy 时自动 Kill 此 Tween
    }

    public void Hide()                                  // 公开方法：绑到「关闭」按钮 OnClick
    {
        canvasGroup.DOFade(0f, fadeDuration)            // alpha 1 → 0 淡出
            .SetUpdate(true)                            // 同上，暂停菜单友好
            .SetLink(gameObject)                        // Destroy 自动清理
            .OnComplete(() => gameObject.SetActive(false));  // 淡出完再隐藏，避免闪断
    }
}
```

#### 语法拆解

##### `CanvasGroup.DOFade(1f, fadeDuration)` 是什么？

```csharp
canvasGroup.DOFade(1f, fadeDuration)
```

| 部分 | 含义 |
|------|------|
| `CanvasGroup` | UI 成组组件：统一 alpha、blocksRaycasts、interactable |
| `DOFade` | 补间 alpha：0 全透明，1 不透明 |
| 前提 | DOTween Setup 时勾选 **UI Module** |

**整行人话**：整块 UI 一起淡入，不用逐个 Image 调 alpha。

---

##### `.SetUpdate(true)` 是什么？

```csharp
.SetUpdate(true)
```

| 部分 | 含义 |
|------|------|
| 官方参数 | `SetUpdate(UpdateType.Normal, isIndependentUpdate: true)` |
| 效果 | Tween **忽略** `Time.timeScale` |
| 用途 | 游戏暂停（timeScale=0）时菜单动画照常播 |

**整行人话**：暂停了游戏，UI 动画照样走。

---

##### `.SetLink(gameObject)` 是什么？

```csharp
.SetLink(gameObject)
```

| 部分 | 含义 |
|------|------|
| `SetLink` | 将 Tween 生命周期绑定到 GameObject |
| 默认行为 | 物体 Destroy 时自动 Kill 该 Tween |
| 用途 | 不必手写 OnDestroy DOKill（仍建议复杂场景双保险） |

**整行人话**：面板被销毁时，上面的淡入淡出会自动停，不会报错。

---

##### `.OnComplete(() => SetActive(false))` 是什么？

```csharp
.OnComplete(() => gameObject.SetActive(false))
```

| 部分 | 含义 |
|------|------|
| 时机 | 淡出 Tween 完全结束后 |
| `SetActive(false)` | 隐藏 GameObject，停止 Update 与渲染 |
| 顺序 | 先淡出再隐藏，避免突然消失 |

**整行人话**：等变透明了再关掉面板，体验更顺。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 2 | `using DG.Tweening;` | 引用 DOTween |
| 4 | `public class TweenPanelFade : MonoBehaviour` | 可挂载的脚本类 |
| 6 | `CanvasGroup canvasGroup;` | 成组透明度控制 |
| 7 | `fadeDuration = 0.35f` | 淡入淡出时长 |
| 9 | `void Awake()` | 初始化组件 |
| 11 | `GetComponent<CanvasGroup>()` | 获取已有 CanvasGroup |
| 12~13 | `AddComponent` | 没有则自动加 |
| 16 | `public void Show()` | 供 UI 按钮调用 |
| 18 | `SetActive(true)` | 显示根物体 |
| 19 | `alpha = 0f` | 从透明开始 |
| 20~22 | `DOFade + SetUpdate + SetLink` | 见上方语法拆解 |
| 25 | `public void Hide()` | 关闭面板入口 |
| 27~30 | 淡出链式调用 | 见上方语法拆解 |

#### 操作提示

Panel 根节点挂脚本；Show/Hide 绑到按钮 **OnClick**；alpha=0 时若需穿透点击，设 `canvasGroup.blocksRaycasts = false`。

---

### 案例 3：Sequence 弹窗动画

**功能**：面板从下方弹入：先移入 + 放大，再微缩回正常尺寸。

```csharp
using UnityEngine;                                      // 引入 Unity 核心库
using DG.Tweening;                                      // 引入 DOTween

public class TweenPanelPopup : MonoBehaviour              // UI 弹窗 Sequence 编排脚本
{
    RectTransform rect;                                 // UI 矩形变换组件
    public Vector2 hiddenPos = new Vector2(0f, -800f);  // 屏幕外起始 anchoredPosition
    public Vector2 shownPos = Vector2.zero;             // 最终显示位置（通常为 0,0）
    public float moveDuration = 0.4f;                  // 第一段移入+放大时长

    void Awake()                                        // 缓存 RectTransform
    {
        rect = GetComponent<RectTransform>();         // UI 元素必有 RectTransform
    }

    public void PlayPopup()                             // 播放弹窗动画（绑按钮或打开面板时调用）
    {
        rect.anchoredPosition = hiddenPos;              // 瞬间放到屏幕外起点
        rect.localScale = Vector3.one * 0.8f;           // 初始略小，配合放大动画

        Sequence seq = DOTween.Sequence();              // 创建空 Sequence（时间线容器）
        seq.Append(rect.DOAnchorPos(shownPos, moveDuration).SetEase(Ease.OutCubic));  // 顺序：移入
        seq.Join(rect.DOScale(1.1f, moveDuration).SetEase(Ease.OutBack));  // 并行：与移入同时放大
        seq.Append(rect.DOScale(1f, 0.15f).SetEase(Ease.InOutQuad));     // 顺序：微缩回 1
        seq.SetUpdate(true);                            // 忽略 timeScale
        seq.SetLink(gameObject);                        // Destroy 自动 Kill
    }

    void OnDestroy()                                    // 销毁时清理
    {
        rect.DOKill();                                  // 杀死 rect 上所有 Tween（含 Sequence 内嵌）
    }
}
```

#### 语法拆解

##### `Append` 与 `Join` 区别？

```csharp
seq.Append(...);
seq.Join(...);
```

| 方法 | 时间关系 |
|------|----------|
| `Append(tween)` | 接在前一段**之后**顺序播放 |
| `Join(tween)` | 与**上一个 Append/Join** 同时开始 |
| `AppendInterval(0.5f)` | 插入纯等待 0.5 秒 |

**整行人话**：Append 排队，Join 并排。

---

##### `DOAnchorPos` 是什么？

```csharp
rect.DOAnchorPos(shownPos, moveDuration)
```

| 部分 | 含义 |
|------|------|
| 目标属性 | RectTransform.anchoredPosition |
| 坐标系 | 相对锚点的 UI 坐标，非世界坐标 |
| 对比 DOMove | 3D 物体用 DOMove；UI 用 DOAnchorPos |

**整行人话**：UI 在父 Rect 里滑到指定锚点位置。

---

##### `DOTween.Sequence()` 是什么？

```csharp
Sequence seq = DOTween.Sequence();
```

| 部分 | 含义 |
|------|------|
| `Sequence` | 特殊 Tween，编排多个子 Tweener/Interval/Callback |
| 与 Tweener 区别 | Tweener 控一个值；Sequence 控时间线 |
| 返回值 | 可 Append/Join，也可 SetEase/OnComplete |

**整行人话**：像剪映时间轴一样，把多段动画排在一起播。

---

##### `Ease.OutBack` 是什么？

```csharp
.SetEase(Ease.OutBack)
```

| 部分 | 含义 |
|------|------|
| `OutBack` | 结束时会略「冲过头」再回弹 |
| 本案例 | 放大到 1.1 时有轻微 overshoot，弹窗更有弹性 |
| 注意 | Back/Elastic 类缓动不适用于 Path  tween |

**整行人话**：缩放结尾带一点 Q 弹 overshoot。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 2 | `using DG.Tweening;` | 引用 DOTween |
| 4 | `public class TweenPanelPopup : MonoBehaviour` | 可挂载的脚本类 |
| 6 | `RectTransform rect;` | UI 变换引用 |
| 7 | `hiddenPos = (0, -800)` | 屏幕下方外 |
| 8 | `shownPos = zero` | 目标居中 |
| 9 | `moveDuration = 0.4f` | 第一段时长 |
| 11 | `void Awake()` | 缓存组件 |
| 13 | `GetComponent<RectTransform>()` | 获取 UI Transform |
| 16 | `public void PlayPopup()` | 播放入口 |
| 18 | `anchoredPosition = hiddenPos` | 重置到屏外 |
| 19 | `localScale = 0.8` | 初始缩小 |
| 21 | `DOTween.Sequence()` | 见上方语法拆解 |
| 22 | `Append(DOAnchorPos...)` | 见上方语法拆解 |
| 23 | `Join(DOScale 1.1...)` | 见上方语法拆解 |
| 24 | `Append(DOScale 1...)` | 缩回正常 |
| 25~26 | SetUpdate + SetLink | 暂停友好 + 自动清理 |
| 29 | `void OnDestroy()` | 销毁回调 |
| 31 | `rect.DOKill()` | 清理 Tween |

#### 操作提示

Panel 为 UI RectTransform；`hiddenPos` 按 Canvas 分辨率调整；与案例 2 可组合（先 Popup 再 Fade）。

---

## 【入门阶段小结】

| 维度 | 要点 |
|------|------|
| **Shortcut** | DOMove / DOScale / DOFade / DOAnchorPos |
| **链式** | SetEase / SetDelay / SetUpdate / OnComplete |
| **Sequence** | Append 顺序 / Join 并行 |
| **清理** | DOKill / SetLink |
| **案例** | 移动、UI 淡入淡出、弹窗 Sequence |

---

# 第三阶段：进阶篇

## 【阶段总述】

进阶阶段：**DOTween.To 泛型补间**、**From 反向**、**Kill/Complete 控制**、**TweenHelper 封装**、**与 Animator 协作**、**性能避坑**。

---

## 一、DOTween.To — 补间任意值（逐词读懂）

当没有 DOMove/DOFade 等 Shortcut 时，用 **泛型** 方式 tween 任意字段：

```csharp
DOTween.To(() => hp, x => hp = x, 0f, 1f)
```

| 部分 | 含义 |
|------|------|
| `DOTween` | DOTween 静态类 |
| `.To` | **泛型方法**：自定义 getter/setter 补间 |
| `() => hp` | **参数1 getter**：Lambda，**读**当前值 |
| `x => hp = x` | **参数2 setter**：Lambda，**写**回新值 |
| `0f` | **参数3 to**：目标 endValue |
| `1f` | **参数4 duration**：秒数 |

**整行人话**：1 秒内把 `hp` 从当前值变到 0，每帧自动调用 setter。

```csharp
float hp = 100f;
DOTween.To(() => hp, x => hp = x, 0f, 1f)
    .OnUpdate(() => hpBar.fillAmount = hp / 100f);
```

| 行 | 整行人话 |
|----|----------|
| `OnUpdate(...)` | 每帧 Tween 更新时刷新血条 fillAmount |

---

#### `DOVirtual.Float` — 简化 float 补间

```csharp
DOVirtual.Float(100f, 0f, 1f, value => {
    hpText.text = Mathf.CeilToInt(value).ToString();
});
```

| 参数 | 含义 |
|------|------|
| `100f` | 起始值 startValue |
| `0f` | 结束值 endValue |
| `1f` | duration |
| `value => ...` | 每帧把当前插值 float 传给你的回调 |

**整行人话**：不用自己写 getter/setter，适合纯显示用的数字滚动。

---

## 二、From 反向补间 — 逐词读懂

```csharp
transform.DOMove(targetPos, 1f).From();
```

| 部分 | 含义 |
|------|------|
| `.From()` | 把 Tweener 变成 **FROM** 模式 |
| 行为 | 物体**立刻跳到** endValue（targetPos），再 Tween **回到** 调用前的原位置 |
| `.From(true)` | 相对 From：endValue 相对当前位置的偏移 |

**整行人话**：写 `.From()` 的瞬间会跳变；适合「从屏幕外飞入到原位」。

| 注意 | 说明 |
|------|------|
| 顺序 | `From` 须在其它 `Set` 之前链（官方要求） |

---

## 三、Tween 控制 API — 逐词读懂

#### `transform.DOKill()` 是什么？

```csharp
transform.DOKill();
transform.DOMove(newPos, 0.5f);
```

| 部分 | 含义 |
|------|------|
| `DOKill` | 目标快捷：Kill **该 Transform 上所有** Tween |
| 用途 | 新动画前清掉旧的，避免叠加冲突 |

---

#### `myTween.Kill()` / `Complete()` / `DOTween.IsTweening`

| API | 整行人话 |
|-----|----------|
| `myTween.Kill()` | 杀死**这一条** Tween |
| `myTween.Complete()` | 瞬间跳到终点再 Kill |
| `myTween.Pause()` / `Play()` | 暂停 / 继续 |
| `DOTween.IsTweening(transform)` | 该 target 上是否还有活跃 Tween |

**autoKill**：默认播完自动 Kill；若要播完后 `Restart()`，需 `SetAutoKill(false)`。

---

## 四、SetLoops 与 LoopType

```csharp
transform.DORotate(new Vector3(0, 360, 0), 2f, RotateMode.FastBeyond360)
    .SetLoops(-1, LoopType.Restart);  // 无限循环旋转
```

| LoopType | 行为 |
|----------|------|
| `Restart` | 每圈从头播 |
| `Yoyo` | 来回往返 |
| `Incremental` | 每圈累加 endValue（仅 Tweener） |

---

## 五、工程化封装 TweenUI

```csharp
using UnityEngine;
using DG.Tweening;

public static class TweenUI
{
    public static Tween FadeIn(CanvasGroup group, float duration = 0.3f)
    {
        group.alpha = 0f;
        return group.DOFade(1f, duration).SetUpdate(true).SetLink(group.gameObject);
    }

    public static Tween FadeOut(CanvasGroup group, float duration = 0.3f, bool deactivate = true)
    {
        return group.DOFade(0f, duration)
            .SetUpdate(true)
            .SetLink(group.gameObject)
            .OnComplete(() => {
                if (deactivate) group.gameObject.SetActive(false);
            });
    }

    public static Sequence Popup(RectTransform rect, Vector2 from, Vector2 to, float duration = 0.4f)
    {
        rect.anchoredPosition = from;
        rect.localScale = Vector3.one * 0.85f;
        var seq = DOTween.Sequence();
        seq.Append(rect.DOAnchorPos(to, duration).SetEase(Ease.OutCubic));
        seq.Join(rect.DOScale(1f, duration).SetEase(Ease.OutBack));
        seq.SetUpdate(true);
        seq.SetLink(rect.gameObject);
        return seq;
    }
}
```

---

## 六、DOTween 与 Animator 协作

| 场景 | 建议 |
|------|------|
| 角色跑跳 | **Animator** 播 Clip，DOTween 不抢骨骼 Transform |
| 角色位移（代码控制） | Transform 用代码/DOTween；Animator `applyRootMotion = false` |
| 受击闪红 | Material DOColor / DOFade 短 Tweener |
| 开门 | 简单门：Transform DORotate；复杂：Animator State |

同一 Transform 上**避免**同时 DOMove 与 Root Motion 动画抢位置。

---

## 七、常见误区与最佳实践

| 误区 | 正确做法 |
|------|----------|
| UI 扩展方法找不到 | 先 **Setup DOTween** 并勾 UI Module |
| 重复点击动画叠加 | 新 Tween 前 `target.DOKill()` |
| 物体销毁报 MissingReference | `SetLink(go)` 或 OnDestroy `DOKill()` |
| 暂停时 UI 不动 | `SetUpdate(true)` |
| From 物体突然跳一下 | 正常现象；或用 DOAnchorPos 从屏幕外起始 |
| 与 Animator 滑步/拉扯 | 分工：骨骼 Animator，位移代码或 Root Motion 二选一 |
| 大量 Tween 卡顿 | Init 时 `SetCapacity`；避免频繁 `DOTween.KillAll()` |
| useSafeMode 关闭 | 保持 true，目标 Destroy 时更安全 |
| Sequence 里 SetLoops(-1) | 无限循环对嵌套 Sequence 有限制，查官方说明 |
| 每帧 DOTween.To | 避免；Tween 创建一次，用 OnUpdate 读值 |

---

## 【进阶阶段小结】

| 维度 | 要点 |
|------|------|
| 泛型 | DOTween.To / DOVirtual.Float |
| From | 飞入效果，注意瞬间跳变 |
| 控制 | Kill / Complete / IsTweening |
| 封装 | TweenUI 静态方法 |
| 协作 | UI/反馈用 DOTween；角色用 Animator |
| 避坑 | Setup、DOKill、SetLink、SetUpdate |

---

# 【全文总结】

## 最重要的一行代码

```csharp
transform.DOMove(targetPos, 1f).SetEase(Ease.OutQuad).OnComplete(() => Debug.Log("完成"));
```

| 部分 | 含义 |
|------|------|
| `DOMove` | 创建移动 Tweener |
| `SetEase` | 缓动曲线 |
| `OnComplete` | 结束回调 |

## 三阶段对照

| 阶段 | 代表案例 |
|------|----------|
| 零基础 | Tweener/Sequence、Setup、读懂 DOMove |
| 入门 | 移动、UI Fade、Popup Sequence |
| 进阶 | DOTween.To、Kill/SetLink、TweenUI 封装 |

## DOTween 与系列文档关系

| 主题 | 文档 |
|------|------|
| UI RectTransform 坐标 | 本文 DOAnchorPos |
| 3D Transform 移动 | 本文 DOMove；点击移动见 [03_Raycast.md](./03_Raycast.md) |
| 角色骨骼动画 | [04_Model_Animator.md](./04_Model_Animator.md)（Animator，非 DOTween） |

## 官方文档索引

| 主题 | 链接 |
|------|------|
| 完整文档 | http://dotween.demigiant.com/documentation.php |
| DOTween 类 | https://dotween.demigiant.com/api/class_d_g_1_1_tweening_1_1_d_o_tween.html |
| Shortcut 扩展 | https://dotween.demigiant.com/api/class_d_g_1_1_tweening_1_1_shortcut_extensions.html |
| 缓动曲线预览 | https://easings.net |

---

*文档版本：与 01_PlayerPrefs.md ~ 04_Model_Animator.md 同系列模板。*
