# Animation 动画系统（Legacy）详解

> **参照来源（取其精华）**
>
> **课程教材（六本 · 本专题对应章节）**
> - **杜亚南**《新印象 Unity2020游戏开发基础与实战》— Animation 窗口（Ctrl+6）、Record 录制、Add Property、关键帧入门
> - **马遥**《Unity 3D完全自学教程》— 外部动画/FBX 导入、Animation 组件挂载、Inspector 预览 Clip
> - **宣雨松**《Unity 3D 游戏开发（第3版）》— 动画曲线与运动节奏、Legacy 与 Mecanim 选型边界
> - **陈俊宇**《Unity 游戏开发从入门到精通》— AnimationClip 作为 Project 资源、Animation Event 帧回调
> - **王磊**《Unity 2022 游戏开发完全学习手册》— 新版 Animation 窗口、Curves 曲线编辑器、切线操作
> - **吴亚峰**《Unity 游戏开发实战（第2版）》— `Play`/`CrossFade` 代码控制、镜头漫游、Instantiate 批量播同一 Clip
>
> **动画专项权威（补充深化）**
> - **Rick Parent**《Computer Animation: Algorithms and Techniques》（第3版）— 关键帧插值、样条曲线、ease-in/ease-out（Curves 窗口数学本质）
> - **Jason Gregory**《游戏引擎架构》（第2版）— Clip 采样播放、资源与组件分离的引擎层模型
> - **Joe Hocking**《Unity in Action》（第3版）— Legacy `Animation` 组件 API 与 CrossFade 代码示例
>
> **Unity 官方 Manual + Scripting API（最终标准）**：[Animation Window](https://docs.unity3d.com/Manual/AnimationWindowGuide.html) · [Legacy Animation](https://docs.unity3d.com/Manual/Animations.html) · [Animation Scripting (Legacy)](https://docs.unity3d.com/Manual/AnimationScripting.html) · [Animation Clips](https://docs.unity3d.com/Manual/AnimationClips.html) · [Mecanim FAQ](https://docs.unity3d.com/Manual/MecanimFAQ.html) · [Animation](https://docs.unity3d.com/ScriptReference/Animation.html) · [AnimationClip](https://docs.unity3d.com/ScriptReference/AnimationClip.html) · [AnimationState](https://docs.unity3d.com/ScriptReference/AnimationState.html)
>
> **已剔除的糟粕**：用 Legacy 做角色走跑跳攻击全套状态（应换 Animator）；每帧 `Play` 同一 Clip 导致动画永远从头播；CrossFade 时间为 0 当淡入淡出用；Animation Event 绑 private 方法；在 Generic 角色上硬套 Humanoid 流程；混淆 `Animation` 组件与 `Animator` 组件。

---

## 使用频率图例

| 标记 | 含义 | 本专题学习优先级 |
|------|------|----------------|
| ⭐⭐⭐ | 做 Legacy 动画必会 | 第一～二周 |
| ⭐⭐ | 项目常见，按模块必学 | 第二～三周 |
| ⭐ | 特定场景才用 | 遇到再学 |

---

## 思维导图总览

```
Animation 动画系统（Legacy）
│
├── 【第一梯队】核心概念 ★★★
│   ├── Animation Clip（.anim）── 动画数据资源，存关键帧与曲线
│   ├── Animation 组件 ────────── Legacy 播放入口（Behaviour）
│   ├── AnimationState ────────── 运行时某一 Clip 的播放状态
│   └── 关键帧 Keyframe + 曲线 ── Clip 的时间-属性映射
│
├── 【第二梯队】编辑器工作流 ★★★
│   ├── Animation 窗口（Ctrl+6）
│   │   ├── Create New Clip
│   │   ├── Add Property（Transform / Material / Light…）
│   │   ├── Record 录制模式
│   │   └── Curves 曲线视图与切线编辑
│   ├── 外部 FBX 动画导入
│   └── 镜头 / Prop / UI 属性 K 帧
│
├── 【第三梯队】代码控制 API ★★★
│   ├── Play / Stop / CrossFade
│   ├── AnimationState：speed / time / normalizedTime / length
│   ├── isPlaying / wrapMode
│   └── 多实例共用同一 Clip 资源
│
├── 【第四梯队】Animation Event ★★
│   ├── Clip 时间轴上挂 Event
│   ├── 调用同物体 public 方法
│   └── 脚步声 / 伤害帧 / 开门逻辑同步
│
├── 【第五梯队】Legacy vs Animator 选型 ★★
│   ├── Legacy：门、旗帜、镜头、简单 Prop
│   └── Mecanim：角色多状态 → 见 02_Animator动画.md
│
└── 【注意要点】
    ├── Clip 名大小写与 Play 一致
    ├── CrossFade 优于硬 Play 切换
    └── 角色复杂行为勿用 Legacy
```

---

## 一、类与资源关系（官方标准 · 必背）

```
UnityEngine.Object
└── AnimationClip（.anim 资源）
        └── 属性曲线 + 关键帧 + Animation Event

Component → Behaviour
└── Animation（Legacy 播放组件）
        ├── 引用一个或多个 AnimationClip
        └── 运行时产生 AnimationState（按 Clip 名索引）

（对比）Animator + AnimatorController → Mecanim 状态机，见 02 文档
```

**[重难点]** `AnimationClip` 是**资源**（Project 里 `.anim`）；`Animation` 是**组件**（挂 GameObject 上播放）；`AnimationState` 是**运行时状态**（通过 `anim["ClipName"]` 访问）。

**[易错点]** 角色走跑跳攻击若全用 Legacy 手写 if-else 切 Clip，维护成本爆炸 → 应换 **Animator**。

---

## 二、AnimationClip 与关键帧（⭐⭐⭐）

### 2.1 AnimationClip

| 项目 | 内容 |
|------|------|
| **是什么** | 存储动画数据的 Unity 资源，扩展名 `.anim` |
| **官方** | [Manual: Animation Clip](https://docs.unity3d.com/Manual/AnimationClips.html) · [API: AnimationClip](https://docs.unity3d.com/ScriptReference/AnimationClip.html) |
| **命名空间** | `UnityEngine` |
| **可动画属性** | Transform、Material 颜色、Light 强度、Camera FOV、RectTransform 等 |

### 2.2 关键帧与插值

```
时间轴：  0s ────●────────●──────── 2s
              Key1      Key2
              中间由曲线插值自动补全
```

| 概念 | 说明 | 频率 |
|------|------|------|
| **Keyframe** | 某一时刻「定死」的属性值 | ⭐⭐⭐ |
| **插值** | 关键帧之间引擎按曲线计算中间值 | ⭐⭐⭐ |
| **K 帧** | Animation 窗口打 Key 的操作 | ⭐⭐⭐ |
| **切线 Tangent** | 控制关键帧两侧过渡形态（线性/缓入/缓出） | ⭐⭐ |

**[教材精华·Parent]** 只 K **变化点**，不要每一帧都打 Key → Clip 臃肿；中间帧由插值/曲线补全。

**[教材精华·杜亚南/王磊]** Animation 窗口 **Record** 适合快速试错；**Curves** 视图精调切线，同样位移不同曲线 = 不同手感。

**[易错点]** 同样位移，曲线不同 → 运动节奏完全不同；Linear 搭骨架后再统一 polish 曲线。

---

## 三、Animation 窗口编辑器工作流（⭐⭐⭐）

### 3.1 创建 Clip 基本流程

| 步骤 | 操作 | 频率 |
|:---:|------|------|
| 1 | `Window → Animation → Animation`（**Ctrl+6**） | ⭐⭐⭐ |
| 2 | Hierarchy 选中目标 GameObject | ⭐⭐⭐ |
| 3 | `Create New Clip` → 命名保存到 Project | ⭐⭐⭐ |
| 4 | 移动时间轴 → 改 Inspector 属性 → 自动/手动打 Key | ⭐⭐⭐ |
| 5 | 预览播放，Curves 视图调曲线 | ⭐⭐ |

### 3.2 Add Property 与 Record 模式

| 功能 | 说明 | 频率 |
|------|------|------|
| **Add Property** | 选择要驱动的组件属性（Transform Position 等） | ⭐⭐⭐ |
| **Record** | 开启后改 Inspector = 自动写 Key，适合快速试错 | ⭐⭐ |
| **Curves** | 切换曲线视图，精细编辑切线与手柄 | ⭐⭐ |

**[易错点]** 未选中正确 GameObject 就 Create Clip → Clip 绑错对象，播放无效果。

### 3.3 外部动画导入（⭐⭐）

| 步骤 | 操作 | 来源 |
|:---:|------|------|
| 1 | 将 `.fbx` 拖入 Project | 马遥/杜亚南 |
| 2 | Inspector → **Rig** → Animation Type：**Legacy**（本专题）或 Generic | 官方 Legacy 手册 |
| 3 | **Animation** 页签 → 勾选 Import Animation → 检查 Clip 列表 | 王磊 |
| 4 | 设置 Loop Time / Loop Pose（循环类 Clip） | 陈俊宇 |

**[教材精华·马遥/杜亚南]** 导入后若自动加了 Animation 组件，可在 Rig 里改 Animation Type；Legacy 项目需在 Import Settings 明确 Legacy。

### 3.4 Wrap Mode 循环模式（⭐⭐）

| WrapMode | 行为 | 典型 |
|----------|------|------|
| **Once** | 播完停止 | 开门、受击一次 |
| **Loop** | 播完从头循环 | 旗帜、待机循环 |
| **PingPong** | 来回播 | 往复摆动 |
| **ClampForever** | 停在最后一帧 | 需精确采样末帧时 |

```csharp
anim["Rotate"].wrapMode = WrapMode.Loop;
anim.Play("Rotate");
```

---

## 四、Animation 组件与代码 API（⭐⭐⭐）

### 4.1 Animation 组件

| 项目 | 内容 |
|------|------|
| **是什么** | Legacy 动画播放组件，直接按 Clip 名播放 |
| **官方** | [API: Animation](https://docs.unity3d.com/ScriptReference/Animation.html) |
| **挂载** | 与 AnimationClip 同挂或引用 Project 中的 Clip |

### 4.2 核心播放 API

| API | 说明 | 频率 |
|-----|------|------|
| `Play("ClipName")` | 立即播放指定 Clip | ⭐⭐⭐ |
| `Stop()` | 停止当前播放 | ⭐⭐⭐ |
| `CrossFade("ClipName", fadeLength)` | 淡入淡出切换（**推荐**） | ⭐⭐⭐ |
| `isPlaying` | 是否在播放 | ⭐⭐ |
| `PlayAutomatically` | 启用时自动播默认 Clip | ⭐⭐ |

### 4.3 AnimationState 属性

| 属性 | 说明 | 频率 |
|------|------|------|
| `anim["ClipName"].speed` | 播放速度（1=正常，0=暂停） | ⭐⭐⭐ |
| `anim["ClipName"].normalizedTime` | 进度 0~1 | ⭐⭐ |
| `anim["ClipName"].time` | 当前时间（秒） | ⭐⭐ |
| `anim["ClipName"].length` | Clip 总时长 | ⭐⭐ |
| `anim["ClipName"].wrapMode` | 循环模式（Loop/Once/PingPong） | ⭐⭐ |

```csharp
public class DoorAnim : MonoBehaviour
{
    Animation anim;

    void Awake()
    {
        anim = GetComponent<Animation>();  // ⭐⭐⭐ Awake 缓存
    }

    public void OpenDoor()
    {
        anim.CrossFade("Open", 0.2f);
    }

    public void CloseDoor()
    {
        anim.CrossFade("Close", 0.2f);
    }
}
```

**[重难点] CrossFade vs Play**

| 方法 | 行为 | 适用 |
|------|------|------|
| `Play` | 硬切，立即切换 | 首次播放、无过渡需求 |
| `CrossFade` | 在 fadeLength 内混合过渡 | 开门/关门、状态平滑切换 |

**[易错点]**
- Clip 名与 `Play("名")` **大小写敏感**，不一致 → 静默不播
- `CrossFade(..., 0f)` 等于硬切
- 每帧 `Play("Idle")` → 动画永远从第 0 帧开始

---

## 五、Clip 复用与多实例（⭐⭐）

```csharp
// 一个 Clip 资源，多个 Animation 组件实例共用
void Start()
{
    for (int x = 0; x < 10; x++)
    for (int z = 0; z < 10; z++)
    {
        var go = Instantiate(cubePrefab, new Vector3(x, 0, z), Quaternion.identity);
        go.GetComponent<Animation>().Play("Rotate");
    }
}
```

**[教材精华·Gregory]** 动画资源（Clip）与播放实例（Animation 组件）分离，是引擎动画系统的基本资源模型。

**[教材精华·吴亚峰/陈俊宇]** 一个 Clip + 多个 `Instantiate` 实例 `Play` — 预制体与动画资源复用的典型练手模式。

---

## 六、Animation Event（⭐⭐）

| 项目 | 说明 |
|------|------|
| **作用** | Clip 某一帧调用同 GameObject 上脚本的 `public` 方法 |
| **配置** | Animation 窗口 → 时间轴 → Add Event → 选 Function |
| **参数** | 可选 Float / Int / String / Object Reference |

```csharp
public class FootstepAudio : MonoBehaviour
{
    public AudioSource audioSource;
    public AudioClip footstepClip;

    // Animation Event 回调 — 必须 public，且脚本在同一物体
    public void OnFootstep()
    {
        audioSource.PlayOneShot(footstepClip);
    }
}
```

**[易错点]**
- 方法非 `public` → 不触发
- 脚本不在同一 GameObject → 不触发
- 函数名拼写与 Event 配置不一致 → 静默失败

**[糟粕剔除]** 用 Animation Event 做复杂游戏逻辑分支 → 应放脚本 Update/状态机，Event 只做**帧同步**（脚步、伤害、音效）。

---

## 七、镜头漫游与 Prop 动画（⭐⭐）

| 场景 | 做法 | 频率 |
|------|------|------|
| **镜头过场** | 选中 Camera → Create Clip → 对 Transform K 帧 | ⭐⭐ |
| **门/机关** | Open/Close 两 Clip + CrossFade + Event | ⭐⭐⭐ |
| **旗帜循环** | Loop Clip + Play Automatically | ⭐⭐ |
| **UI 微动效** | RectTransform Scale/Alpha K 帧 | ⭐⭐ |

**[教材精华·Parent/吴亚峰]** 镜头漫游：先 Linear 搭关键路径，再 Curves 调缓入缓出，避免机械匀速。

**[教材精华·宣雨松]** Legacy 适合门、镜头、Prop；角色多状态应换 Mecanim（与官方 Mecanim FAQ 一致）。

---

## 八、Legacy vs Animator 选型（⭐⭐⭐）

| 对比项 | Animation（Legacy） | Animator（Mecanim） |
|--------|---------------------|---------------------|
| 组件 | `Animation` | `Animator` |
| 控制 | `Play("Clip")` / CrossFade | `SetFloat/SetTrigger` → 状态机 |
| 状态机 | 无 | 有（Controller） |
| 混合 | CrossFade 有限 | BlendTree / Layer 丰富 |
| 适用 | 门、旗帜、镜头、简单 Prop | 角色、NPC、多行为 |
| 详见 | 本文 | [02_Animator动画.md](02_Animator动画.md) |

**[重难点]** 二者**共用 AnimationClip 资源**；Legacy 直接播 Clip；Mecanim 通过 Controller 管理何时播哪个 Clip。

---

## 九、注意要点与最佳实践

### 常见陷阱

| 易错点 | 说明 |
|--------|------|
| Clip 名拼写错误 | Play/CrossFade 静默失败 |
| 绑错对象做动画 | 先选中 GameObject 再 Create Clip |
| 角色复杂状态用 Legacy | 换 Animator + 状态机 |
| CrossFade 时间为 0 | 等于硬切，无过渡 |
| Event 方法非 public | 事件不触发 |
| Update 里 GetComponent\<Animation\> | 应 Awake 缓存 |

### 最佳实践

- 简单物体 / 环境 / 镜头 → Legacy；角色 → Animator
- 切换优先 `CrossFade`，少用硬 `Play`
- 逻辑与动画帧同步用 Animation Event，复杂逻辑放脚本
- Awake 缓存 `Animation` 引用
- 先 Linear 搭骨架，再统一调曲线 polish

---

## 十、典型应用场景

| 场景 | 用法 | 频率 |
|------|------|------|
| 开门/关门 | Open/Close Clip + CrossFade + Event | ⭐⭐⭐ |
| 镜头漫游 | Camera Transform K 帧 + 曲线缓动 | ⭐⭐ |
| 批量 Prop 旋转 | 一 Clip 多实例 Instantiate + Play | ⭐⭐ |
| UI 弹出 | RectTransform 动画 | ⭐⭐ |
| 角色走跑跳 | **不用 Legacy** → Animator | — |

---

## 十一、与动画专题其他文档的对应

| 本篇章节 | 详细文档 |
|----------|----------|
| Legacy 基础（本文） | 01_Animation动画深入.md |
| Animator / Mecanim | [02_Animator动画.md](02_Animator动画.md) |
| 状态机 / Layer | [03_动画状态机一.md](03_动画状态机一.md) |
| BlendTree / IK | [04_动画状态机二.md](04_动画状态机二.md) |
| 游戏实战 | [05_常见游戏动画设置.md](05_常见游戏动画设置.md) |

---

## 十二、课程六教材 · 本专题贡献对照

| 教材 | 本专题精读要点 | 优先级 |
|------|---------------|--------|
| 杜亚南 | Ctrl+6、Record、Add Property、K 帧流程 | ⭐⭐⭐ |
| 马遥 | FBX 导入、Animation 组件、Inspector 预览 | ⭐⭐⭐ |
| 宣雨松 | 曲线手感、Legacy vs Animator 边界 | ⭐⭐ |
| 陈俊宇 | Clip 资源化、Animation Event、预制体复用 | ⭐⭐ |
| 王磊 | 2022 Animation 窗口、Curves 编辑器 | ⭐⭐⭐ |
| 吴亚峰 | CrossFade 代码、镜头动画、批量 Play 实战 | ⭐⭐⭐ |
| Parent | 关键帧插值/ease 理论（Curves 底层） | ⭐⭐ |
| Gregory | Clip 与组件/engine 采样模型 | ⭐⭐ |
| Hocking | Legacy API 代码范式 | ⭐⭐ |
| **Unity 官方** | **Play/CrossFade/Event 最终语义** | ⭐⭐⭐ |

---

## 十三、教材 vs 官方 · 对照速查

| 知识点 | 教材常见写法 | 官方/工程推荐 |
|--------|--------------|---------------|
| 角色多状态动画 | 全用 Animation + 多个 Clip 硬切 | 换 **Animator** + 状态机 |
| 切换动画 | `Play("Run")` 硬切 | **`CrossFade`** 或 Mecanim Transition |
| 曲线编辑 | 每帧打 Key | 只 K **变化点**，Curves 调切线 |
| Event 回调 | 任意方法名 | 必须 **public**，同 GameObject |
| 组件获取 | Update 里 GetComponent | **Awake 缓存** Animation 引用 |
| 镜头动画 | 匀速 Linear 关键帧 | 缓入缓出曲线 polish |

---

## 十四、自测清单（掌握 Legacy 动画的最低标准）

- [ ] 说清 AnimationClip、Animation 组件、AnimationState 三者关系
- [ ] 会用 Ctrl+6 创建 Clip 并对 Transform K 帧
- [ ] 会用 `Play` / `CrossFade` / `Stop`，说清 CrossFade 优势
- [ ] 会读写 `anim["ClipName"].speed` 与 `normalizedTime`
- [ ] 会配置 Animation Event 并在 public 方法中响应
- [ ] 说清 Legacy 与 Animator 的适用场景差异
- [ ] 知道 Clip 名大小写敏感、Awake 缓存组件引用

---

## 十五、官方参考

- [Manual: Animation Section](https://docs.unity3d.com/Manual/AnimationSection.html)
- [Manual: Legacy Animation System](https://docs.unity3d.com/Manual/Animations.html)
- [Manual: Animation Window](https://docs.unity3d.com/Manual/AnimationWindowGuide.html)
- [API: Animation](https://docs.unity3d.com/ScriptReference/Animation.html)
- [API: AnimationClip](https://docs.unity3d.com/ScriptReference/AnimationClip.html)
- [API: AnimationState](https://docs.unity3d.com/ScriptReference/AnimationState.html)
