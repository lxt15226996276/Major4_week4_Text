# Unity Animation 动画深入详解

> 参照：[Unity 官方 Manual - Animation System](https://docs.unity3d.com/Manual/AnimationSystem.html) · [Animation Clip](https://docs.unity3d.com/Manual/animeditor-AnimationClips.html) · [Animation Curves](https://docs.unity3d.com/Manual/animeditor-AnimationCurves.html) · [Animation Events](https://docs.unity3d.com/Manual/animeditor-AnimationEvents.html)  
> 关联文档：[02_Animator动画.md](./02_Animator动画.md)（Animator 组件与状态机） · [03_状态机（有限状态机）.md](./03_状态机（有限状态机）.md)（FSM 设计模式）  
> 学习路径：**零基础 → 入门 → 进阶**，每阶段采用 **总—分—总** 结构。  
> 讲解维度：**定义 → 本质 → 特点 → 适用场景 → 原理 → API → 步骤 → 案例 → 避坑**（进阶含动画曲线 / 动画事件 / 根运动 / 压缩）。  
> 案例讲解：遵循 **案例代码讲解模板**（功能 → 代码 → 语法拆解 → 逐行详解 → 操作提示）。  
> API 讲解：入门/进阶 API 章节均采用 **逐词读懂** 格式：类型 → 参数 → 整行人话。

---

## 【全文总述】

**Animation Clip（动画片段）** 是 Unity 动画系统的「原材料」：一段记录了物体属性（位置、旋转、缩放、骨骼、材质参数等）随时间变化的关键帧数据。  
**动画曲线（Animation Curve）** 是 Clip 的底层数据结构：每个属性对应一条曲线，曲线上的点叫关键帧（Keyframe），两帧之间由插值算法算出中间值。  
**Animation Event（动画事件）** 是 Clip 上的「时间触发器」：在指定帧调用脚本方法，实现「脚落地时播放脚步声」「攻击挥刀帧造成伤害」等时机精确的逻辑。  
本文从 Clip 是什么、曲线原理、关键帧编辑，到动画事件、根运动、压缩优化，逐层深入。

### 思维导图总览

```
Unity Animation 动画深入
│
├── Animation Clip（动画片段 — 动画系统的基本数据单元）
│   │
│   ├── 【知识维度】（讲师框架 — 完整版）
│   │   │
│   │   ├── 定义：记录一个或多个属性随时间变化的动画数据资产
│   │   │   └── 官方描述：Animation Clips are the smallest building blocks of animation in Unity
│   │   │       可从 FBX 导入，也可在 Unity 内 Animation 窗口录制
│   │   │
│   │   ├── 本质：时间 → 属性值 的映射集合（多条 Animation Curve 打包）
│   │   │   ├── 数据模型：每个动画属性对应一条 AnimationCurve
│   │   │   ├── 每条曲线由多个 Keyframe（时间 + 值 + 切线）组成
│   │   │   └── 播放链路：时间推进 → 曲线采样 → 写入目标属性
│   │   │
│   │   ├── 官方定位：动画系统的最小数据单元，由 Animator 或 Animation 组件播放
│   │   │   ├── 设计用途：角色动作、UI 动效、材质变化、相机抖动
│   │   │   └── 两种来源：外部导入（FBX） / 内部录制（Animation 窗口）
│   │   │
│   │   ├── 特点
│   │   │   ├── 优势：数据驱动、可预览、可混合（Blend Tree）、可事件触发
│   │   │   └── 局限：关键帧多则文件大；骨骼动画 CPU 开销；复杂逻辑需事件配合
│   │   │
│   │   ├── 适用场景
│   │   │   ├── ✅ 适用：角色走跑跳、门开关、UI 弹窗、材质颜色过渡、参数驱动动画
│   │   │   └── ❌ 不适用：纯物理模拟（Ragdoll）、完全程序化生成的运动
│   │   │
│   │   ├── 核心原理：时间采样 + 曲线插值
│   │   │   ├── 关键帧 Keyframe：time + value + inTangent + outTangent + tangentMode
│   │   │   ├── 插值模式：Clamp / Linear / Smooth / Free（自定义切线）
│   │   │   ├── 采样频率：由运行时帧率决定，曲线连续采样
│   │   │   └── Wrap Mode：Once / Loop / PingPong / ClampForever
│   │   │
│   │   ├── 核心属性（Animation Clip）
│   │   │   ├── length：动画总时长（秒，只读）
│   │   │   ├── frameRate：采样帧率（导入时设置）
│   │   │   ├── isLooping：是否循环
│   │   │   ├── wrapMode：循环模式（旧 Animation 组件用）
│   │   │   ├── localBounds：动画本地空间包围盒（优化裁剪用）
│   │   │   └── legacy：是否为 Legacy 动画（旧系统用）
│   │   │
│   │   ├── 核心 API（运行时脚本控制曲线）
│   │   │   ├── AnimationCurve.Evaluate(time) → 按时间采样曲线上的值
│   │   │   ├── AnimationCurve.keys → 关键帧数组
│   │   │   ├── Keyframe(time, value, inTangent, outTangent) → 构造关键帧
│   │   │   ├── AnimationClip.SetCurve(path, type, propertyName, curve) → 运行时绑定曲线
│   │   │   └── AnimationClip.SampleAnimation(gameObject, time) → 采样某一时刻状态
│   │   │
│   │   ├── 动画事件 Animation Event
│   │   │   ├── 定义：Clip 时间轴上的标记，到达指定时间调用目标脚本方法
│   │   │   ├── 参数：float / int / string / Object reference（四种之一）
│   │   │   ├── 查找逻辑：在Animator所在GameObject及子物体上找public方法
│   │   │   └── 典型用途：脚步声、攻击判定、特效生成、音效同步
│   │   │
│   │   ├── 根运动 Root Motion
│   │   │   ├── 定义：动画中根骨骼的位移/旋转随动画播放写入 Transform
│   │   │   ├── 开启：Animator.applyRootMotion = true
│   │   │   ├── 数据来源：Animation Clip 中 Root Transform 曲线
│   │   │   └── 脚本读取：animator.deltaPosition / deltaRotation
│   │   │
│   │   └── 性能与压缩
│   │       ├── 压缩模式：Off / Keyframe Reduction / Optimal
│   │       ├── 位置/旋转/缩放误差：误差越大文件越小
│   │       └── 优化建议：移除无用曲线、Optimal 压缩、精简关键帧
│   │
│   ├── 第一阶段：零基础（建立认知 + 读懂曲线）
│   │   ├── 理解 Clip / Curve / Keyframe 三者关系
│   │   ├── 逐词读懂：AnimationCurve.Evaluate(0.5f)
│   │   └── 认识 Animation 窗口：时间轴、关键帧、曲线视图
│   │
│   ├── 第二阶段：入门（动画事件 + 曲线编辑 + 案例）
│   │   ├── Animation Event 添加与脚本回调
│   │   ├── Animation Curve 关键帧切线与插值
│   │   └── 实战案例：脚步声事件 / 材质颜色动画 / 自定义曲线子弹飞行
│   │
│   └── 第三阶段：进阶（根运动 + 压缩 + 运行时创建 + 封装）
│       ├── Root Motion 原理与 OnAnimatorMove
│       ├── 动画压缩设置与性能优化
│       ├── 运行时用代码创建 AnimationClip
│       └── 选型：Animation Clip vs DOTween vs 程序动画
│
└── Legacy Animation 组件（旧系统 — 了解即可）
    │
    ├── 定义：挂在物体上直接 Play/Stop 单个 Clip，无状态机
    ├── 适用：极简单物体（旋转道具、门），新项目优先 Mecanim
    └── API：animation.Play("clip") / animation.CrossFade(...)
```

| 学习阶段 | 学习目标 |
|----------|----------|
| **零基础** | 说清 Clip、Curve、Keyframe 关系；读懂 `AnimationCurve.Evaluate(t)` |
| **入门** | 会添加动画事件、编辑曲线切线；完成 3 个案例 |
| **进阶** | 懂根运动原理、动画压缩、运行时创建 Clip；会选型 |

### 讲师知识框架速览（全文脉络）

| 维度 | 零基础讲 | 入门讲 | 进阶讲 |
|------|----------|--------|--------|
| 定义 | ✅ | 回顾 | 回顾 |
| 本质 | ✅ 曲线+关键帧 | — | 根运动/压缩 |
| 特点 | ✅ | — | 性能开销 |
| 适用场景 | ✅ | — | 选型（Clip vs DOTween） |
| 核心原理 | 时间采样 | ✅ 切线与插值 | 压缩算法概览 |
| 核心 API | 读懂 Evaluate | ✅ Animation Event / Keyframe | SetCurve / SampleAnimation |
| 使用步骤 | Animation 窗口 | ✅ 事件绑定 + 曲线编辑 | 运行时创建 |
| 调用时机 | — | ✅ Update / 事件回调 | OnAnimatorMove |
| 避坑 | — | 初步 | ✅ 压缩/事件查找路径 |

---

# 第一阶段：零基础篇

## 【阶段总述】

零基础阶段建立**正确认知**：Animation Clip 是什么、底层由什么组成、动画播放时数据怎么流动。  
同时学会**读懂** `curve.Evaluate(time)` 的含义，并认识 Unity Animation 窗口。

---

## 一、定义 — Animation Clip 是什么？

| 项目 | 说明 |
|------|------|
| **类型** | Unity 资产（`.anim` 文件），`UnityEngine.AnimationClip` 类 |
| **本质** | 多条**动画曲线（AnimationCurve）**的打包集合 |
| **官方定义** | Animation Clips are the smallest building blocks of animation in Unity |
| **一句话** | 一段「录制好的动作数据」，告诉 Unity「从第 0 秒到第 2 秒，物体位置从 A 变到 B」 |

```
Animation Clip（走路.anim）
    ├── 位置曲线 Position.x：  0s→0  0.5s→1  1s→2  ...
    ├── 位置曲线 Position.y：  0s→0  0.5s→0  1s→0.1  ...
    ├── 旋转曲线 Rotation.z：  0s→0  0.5s→5° 1s→0  ...
    └── ...（骨骼越多，曲线越多）
```

---

## 二、本质 — 动画怎么「动起来」？

### 2.1 三层数据结构

| 层级 | 含义 | 类比 |
|------|------|------|
| **Animation Clip** | 一段完整动画（如「走路」） | 一整首歌 |
| **Animation Curve** | 单个属性的变化（如 Position.x） | 单条音轨 |
| **Keyframe** | 曲线上的一个时间点（时间 + 值） | 音符 |

### 2.2 播放链路

```
时间 t 推进（由 Animator / 动画系统驱动）
        │
        ▼
  每条 AnimationCurve.Evaluate(t)  → 算出当前帧该属性的值
        │
        ▼
  写入目标属性（Transform.position / Material.color / ...）
        │
        ▼
  物体表现为「在动」
```

**本质理解**：动画不是「一帧帧图片」，而是**数学曲线**——给定任意时间 t，都能算出当时的属性值。所以 Unity 动画可以任意慢放、快进、倒放、混合。

---

## 三、关键帧 Keyframe 四要素

每个关键帧不只是「时间+值」，还包含**切线信息**，决定两帧之间怎么过渡：

| 字段 | 含义 |
|------|------|
| `time` | 时间点（秒） |
| `value` | 该时刻的属性值 |
| `inTangent` | 进入该点的切线斜率（左边曲线怎么弯过来） |
| `outTangent` | 离开该点的切线斜率（右边曲线怎么弯出去） |

```
value ↑
      │    ● ← Keyframe（time=1, value=3, outTangent=平缓）
      │   ╱
      │  ╱
      │ ● ← Keyframe（time=0, value=0, inTangent=陡）
      └─────────→ time
        0       1
```

切线模式决定了「动画是匀速的还是先快后慢的」——这和 DOTween 的 Ease 曲线本质相通。

---

## 四、Wrap Mode — 播完之后怎么办？

一段动画播完了（时间超过 length），后续怎么表现？

| Wrap Mode | 行为 |
|-----------|------|
| `Once` | 播完停在最后一帧 |
| `Loop` | 循环播放，从第 0 秒重新开始 |
| `PingPong` | 来回往返（正放→倒放→正放…） |
| `ClampForever` | 永远保持最后一帧的值 |

> **注意**：在 Mecanim Animator 系统中，循环由 Clip 的 **Loop Time** 勾选 + Animator Controller 状态机共同决定，不完全依赖 WrapMode。

---

## 五、核心一课：如何读懂曲线采样

```csharp
float val = curve.Evaluate(0.5f);
```

| 部分 | 含义 |
|------|------|
| `curve` | AnimationCurve 类型变量，存一条曲线 |
| `.Evaluate(...)` | 方法名：「求值 / 采样」——给定时间，返回对应的值 |
| `0.5f` | 参数 time：时间点（秒） |
| 返回值 `float` | 该时间点曲线上的值 |

**整行人话**：问这条曲线「0.5 秒的时候值是多少？」。

```csharp
// 示例：一条从 0→10 的简单曲线
AnimationCurve curve = AnimationCurve.Linear(0f, 0f, 1f, 10f);
float v = curve.Evaluate(0.3f);  // v = 3
```

---

## 【零基础阶段小结】

| 维度 | 要点 |
|------|------|
| **定义** | Clip = 一段动画；Curve = 一条属性变化；Keyframe = 一个时间点 |
| **本质** | 时间 → 曲线采样 → 写入属性 |
| **关键帧** | time + value + 切线（in/out） |
| **读懂** | `curve.Evaluate(t)` = 问 t 时刻的值是多少 |

**阶段检验**：能说出 Clip、Curve、Keyframe 三层关系；能解释「为什么动画可以慢放」。

---

# 第二阶段：入门篇

## 【阶段总述】

入门阶段掌握 **Animation Event（动画事件）**、**Animation Curve 切线编辑**、**Animation 窗口使用**，并完成 3 个实战案例。  
重点：**动画事件精确触发逻辑**；**曲线切线控制运动手感**。

---

## 一、Animation Event — 动画事件

### 1.1 定义 — 逐词读懂

动画事件就是在 Clip 时间轴上钉一个「标记」，动画播到这个时间点时，自动调用脚本上的方法。

```
时间轴：  0s ───●─── 0.5s ───●─── 1.0s
                  ↑            ↑
              OnFootstep   OnAttackHit
              （脚步声）   （攻击判定）
```

| 概念 | 说明 |
|------|------|
| **添加位置** | Animation 窗口 / FBX 导入设置的 Animation 选项卡 |
| **调用对象** | 挂 Animator 组件的 GameObject 及其子物体上的所有 MonoBehaviour |
| **方法要求** | `public` 方法，参数最多一个，且为 float/int/string/Object 之一 |

**整行人话**：动画播到哪一帧该做什么事，不用代码里数秒数，直接在动画上钉个标记。

---

### 1.2 参数类型（四种选一）

| 参数类型 | 示例方法签名 | 用途 |
|----------|-------------|------|
| 无参数 | `public void OnFootstep()` | 纯触发，不需要数据 |
| `float` | `public void OnDamage(float amount)` | 传数值（伤害量等） |
| `int` | `public void OnAttackIndex(int index)` | 传整数（第几段攻击） |
| `string` | `public void OnPlaySFX(string sfxName)` | 传字符串（音效名） |
| `Object` | `public void OnSpawnEffect(GameObject prefab)` | 传物体引用（特效 Prefab） |

---

### 1.3 查找规则（重要）

当动画事件触发时，Unity 会在 **Animator 所在的 GameObject** 上，以及它的**所有子物体**上，寻找匹配的 public 方法。

```
Player（Animator 组件在这里）
    ├── Body（SkinnedMeshRenderer）
    └── Weapon（脚本：PlayerWeapon.cs，有 OnAttackHit 方法）
```

> 动画事件会找到 Weapon 上的 `OnAttackHit`，因为 Weapon 是 Animator 所在物体的子物体。

**常见坑**：方法写在父物体上找不到？检查 Animator 挂在哪一层。**最佳实践**：把动画事件回调脚本挂在与 Animator 同一物体上或其子物体上。

---

## 二、Animation Curve 切线模式 — 控制运动手感

### 2.1 五种常用切线模式

在 Animation 窗口右键关键帧，可以设置切线：

| 模式 | 曲线形态 | 运动手感 |
|------|----------|----------|
| **Free Smooth** | 平滑 S 型 | 自然过渡，柔和 |
| **Flat** | 出入切线水平 | 两端慢，中间快 |
| **Linear** | 直线 | 匀速 |
| **Constant** | 阶梯 | 瞬间跳变（无过渡） |
| **Broken** | 左右切线独立调 | 自定义入和出 |

```
value ↑
      │    ╭─●  ← Flat（出切线水平）
      │  ╱
      │ ●← Linear（直线）
      │  ╲
      │   ╰───● ← Constant（阶跃）
      └─────────→ time
```

**举一反三**：DOTween 的 Ease 枚举（OutQuad / InCubic / Linear）本质上也是描述「时间-值」曲线的形状。原理一样，只是一个用枚举选，一个手动画。

---

### 2.2 为什么「先快后慢」手感好？

- **Linear 匀速**：机械感强，适合 UI 进度条
- **Out 型（先快后慢）**：自然减速，符合物理直觉（物体停下有惯性）
- **In 型（先慢后快）**：加速启动，适合角色起跑
- **InOut 型**：两端慢中间快，适合镜头推拉

> 这就是为什么 DOTween 默认 OutQuad 好看——和人眼的物理直觉匹配。

---

## 三、标准动画事件使用步骤

```
步骤1  在 Animation 窗口或 FBX Animation 选项卡中，定位到目标帧
步骤2  点击 Add Event（或时间轴上右键 → Add Animation Event）
步骤3  在 Inspector 中选择函数名，填参数（可选）
步骤4  在目标脚本中写对应 public 方法
步骤5  运行测试：动画播到该帧时是否触发
```

---

## 四、入门三个案例

### 案例代码讲解模板

每个案例统一按以下结构组织（下文所有案例均遵循此模板）：

| 顺序 | 板块 | 内容 |
|:----:|------|------|
| 1 | **功能** | 案例实现什么业务 |
| 2 | **完整代码** | 带行内注释的完整脚本 |
| 3 | **语法拆解** | 对案例中较生僻的语法，逐个说明 |
| 4 | **逐行详解** | 表格：每行代码的含义 |
| 5 | **操作提示** | Unity 绑定、调用方式等 |

**语法拆解的标准格式**（遇到 `AnimationCurve`、`Animation Event`、`Evaluate` 等不熟悉的写法时使用）：

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

### 案例 1：脚步声动画事件

**功能**：角色走路动画中，每只脚落地的帧添加 Animation Event，触发时播放脚步声。

```csharp
using UnityEngine;                                      // 引入 Unity 核心库

public class FootstepHandler : MonoBehaviour            // 脚步声回调脚本，挂到与 Animator 同一物体或子物体
{
    public AudioClip footstepSound;                     // 脚步声音效，Inspector 拖入
    public float volume = 0.5f;                         // 音量，可调

    public void OnFootstep()                            // 动画事件回调方法名，须与事件中函数名一致
    {
        if (footstepSound == null) return;              // 未配置音效则跳过，避免空引用
        AudioSource.PlayClipAtPoint(                    // 在角色当前位置播放一次 3D 音效
            footstepSound, transform.position, volume);
    }
}
```

#### 语法拆解

##### `public void OnFootstep()` 是什么？

```csharp
public void OnFootstep()
```

| 部分 | 含义 |
|------|------|
| `public` | 必须公开，动画事件系统才能找到 |
| `void` | 无返回值 |
| `OnFootstep` | 方法名，必须与 Animation Event 中设置的函数名**完全一致**（大小写敏感） |

**整行人话**：动画播到「脚落地」那一帧，Unity 自动调用这个方法。

**说明**：方法名写错一个字母都不会触发，也不会报错——调试时优先检查拼写。

---

##### `AudioSource.PlayClipAtPoint(...)` 是什么？

```csharp
AudioSource.PlayClipAtPoint(footstepSound, transform.position, volume);
```

| 部分 | 含义 |
|------|------|
| `PlayClipAtPoint` | AudioSource 静态方法：在世界坐标某点播放一次音效 |
| `footstepSound` | 要播放的 AudioClip |
| `transform.position` | 播放位置（角色脚下） |
| `volume` | 音量 0~1 |

**整行人话**：不用挂 AudioSource 组件，临时在角色位置响一声脚步。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 3 | `public class FootstepHandler : MonoBehaviour` | 可挂载的脚本类 |
| 5 | `AudioClip footstepSound` | 脚步声音效引用 |
| 6 | `float volume = 0.5f` | 音量默认 50% |
| 8 | `OnFootstep()` | 动画事件回调方法 |
| 10 | `if (footstepSound == null) return` | 空引用保护 |
| 11~12 | `PlayClipAtPoint(...)` | 在角色位置播放一次音效 |

#### 操作提示

1. 在 Animation 窗口打开 Walk Clip  
2. 时间轴拖到脚落地帧 → 右键 → Add Animation Event  
3. 在 Inspector Function 下拉选 `OnFootstep`  
4. 脚本挂到角色上（与 Animator 同物体或子物体）  
5. 拖入 AudioClip → Play 测试

---

### 案例 2：材质颜色动画（Animation 窗口录制）

**功能**：在 Unity 内用 Animation 窗口录制一段「材质颜色从红变蓝」的动画，挂到物体上循环播放。

> 本案例以操作步骤为主，展示 Animation 窗口的基本用法。

#### 操作步骤

1. 选中场景中的 Cube
2. 菜单 **Window → Animation → Animation** 打开动画窗口
3. 点击 **Create** → 保存为 `ColorAnim.anim`
4. 点击 **Add Property** → MeshRenderer → Material → Color
5. 时间轴拖到 0 秒 → 把颜色设为红色（记录第一个关键帧）
6. 时间轴拖到 2 秒 → 把颜色设为蓝色（自动生成第二个关键帧）
7. 点击 Play 预览：颜色从红渐变到蓝
8. 如需循环：选中 .anim 文件 → Inspector 勾选 **Loop Time** → Apply

#### 为什么不用代码写？

- 可视化调整，美术直接上手
- 可配合其他属性一起动（位置+缩放+颜色同时变）
- 不需要 DOTween 等第三方插件

> **选型对比**：简单的、设计师要调的 → 用 Animation Clip；纯代码逻辑控制的 → 用 DOTween。

---

### 案例 3：自定义曲线驱动子弹飞行

**功能**：用 `AnimationCurve` 在 Inspector 画出一条「高度-时间」曲线，代码控制子弹沿 X 轴飞行，Y 高度由曲线决定，实现抛物线或任意路径。

```csharp
using UnityEngine;                                      // 引入 Unity 核心库

public class BulletCurve : MonoBehaviour                // 子弹飞行脚本，挂到子弹 Prefab
{
    public AnimationCurve heightCurve;                  // 高度曲线：横轴=进度 0~1，纵轴=高度
    public float speed = 10f;                           // 水平飞行速度
    public float maxHeight = 3f;                        // 曲线最大高度倍率
    public float flightDistance = 20f;                  // 总飞行距离

    Vector3 startPos;                                   // 起点位置
    float progress = 0f;                                // 飞行进度 0~1

    void Start()
    {
        startPos = transform.position;                  // 记录初始位置
    }

    void Update()
    {
        progress += (speed * Time.deltaTime) / flightDistance;  // 按速度推进进度
        if (progress >= 1f) { Destroy(gameObject); return; }    // 飞完 100% 销毁

        float y = heightCurve.Evaluate(progress) * maxHeight;   // 曲线采样当前高度
        Vector3 pos = startPos + Vector3.right * progress * flightDistance;
        pos.y += y;
        transform.position = pos;
    }
}
```

#### 语法拆解

##### `public AnimationCurve heightCurve` 是什么？

```csharp
public AnimationCurve heightCurve;
```

| 部分 | 含义 |
|------|------|
| `AnimationCurve` | 类型：一条动画曲线 |
| `heightCurve` | 变量名 |
| **Inspector 效果** | 显示一条可编辑的曲线面板，点击即可添加/拖拽关键帧 |

**整行人话**：在 Inspector 里手动画一条曲线，代码每帧去曲线上取值当高度。

**说明**：这是 Unity 提供的「设计师友好」方式——非程序也能调弹道弧线。

---

##### `heightCurve.Evaluate(progress)` 是什么？

```csharp
float y = heightCurve.Evaluate(progress) * maxHeight;
```

| 部分 | 含义 |
|------|------|
| `progress` | 0~1 的飞行进度 |
| `Evaluate(progress)` | 从曲线上取进度时刻对应的高度值 |
| `* maxHeight` | 曲线的值通常 0~1，乘以实际最大高度得到世界坐标 |

**整行人话**：问曲线「飞到一半的时候应该有多高？」。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 3 | `public class BulletCurve : MonoBehaviour` | 可挂载的脚本类 |
| 5 | `AnimationCurve heightCurve` | 可在 Inspector 编辑的曲线字段 |
| 6 | `speed = 10f` | 水平速度 |
| 7 | `maxHeight = 3f` | 最大高度倍率 |
| 8 | `flightDistance = 20f` | 总飞行距离 |
| 11 | `startPos` | 起点缓存 |
| 12 | `progress = 0f` | 当前飞行进度 0~1 |
| 14~17 | `Start()` | 记录初始位置 |
| 19~27 | `Update()` | 每帧推进进度，采样曲线，更新位置 |

#### 操作提示

1. 创建子弹 Prefab，挂脚本
2. Inspector 点击 heightCurve 曲线区域，打开曲线编辑器
3. 添加 3 个关键帧：(0,0)、(0.5,1)、(1,0) → 形成抛物线
4. 设置 speed、maxHeight、flightDistance
5. 运行时 Instantiate 子弹，观察飞行轨迹

> **举一反三**：不止子弹，任何「时间驱动的单属性变化」都可以用 AnimationCurve 做——相机抖动、UI 弹性、灯光闪烁……设计师调曲线，程序员只负责采样。

---

## 【入门阶段小结】

| 维度 | 要点 |
|------|------|
| **动画事件** | Animation Event + public 方法 + 同一物体/子物体查找 |
| **曲线切线** | Free / Flat / Linear / Constant / Broken 五种模式 |
| **Animation 窗口** | 录制、编辑关键帧、添加事件 |
| **案例** | 脚步声事件、材质动画、曲线驱动子弹 |

---

# 第三阶段：进阶篇

## 【阶段总述】

进阶阶段：**根运动 Root Motion 原理**、**动画压缩与性能优化**、**运行时代码创建 AnimationClip**、**选型决策**。

---

## 一、Root Motion — 根运动详解

### 1.1 定义

**Root Motion**：动画片段中，角色**根骨骼（Root Bone）**的位移和旋转，在动画播放时被提取出来，直接应用到角色的 Transform 上。

| 模式 | applyRootMotion | 位置来源 | 适用 |
|------|-----------------|----------|------|
| 代码移动 | false | Transform.Translate / CharacterController / Rigidbody | 灵活、由逻辑控制 |
| 根运动 | true | 动画中 Root Transform 的曲线 | 动画师 K 好位移，动作自然 |
| 混合 | true + OnAnimatorMove | 读 deltaPosition 自己决定怎么用 | 最灵活 |

---

### 1.2 为什么需要根运动？

- **避免滑步**：代码移动速度如果和动画速度不匹配，角色会像在滑冰
- **动作自然**：动画师可以精确控制起步、停止、转身的细微位移
- **不同动作不同速度**：走路慢、跑步快，动画里自带，不用代码调

**根运动的数据来源**：FBX 导入后，在 Animation 选项卡中可以看到 **Root Transform Rotation**、**Root Transform Position (Y)**、**Root Transform Position (XZ)** 三条曲线是否被烘焙（Bake Into Pose）。

| 烘焙选项 | 含义 |
|----------|------|
| **不勾选 Bake** | 该轴的运动作为 Root Motion 输出，会移动 Transform |
| **勾选 Bake Into Pose** | 该轴的运动被烘焙进姿势，不影响 Transform（只在原地动） |

> 常见配置：走跑动画 **Position XZ 不 Bake**（水平位移作为 Root Motion），**Position Y 不 Bake**（上下颠簸也跟着动），旋转视需求。

---

### 1.3 OnAnimatorMove — 自定义根运动

当 `applyRootMotion = true` 时，Unity 每帧会调用 `OnAnimatorMove()`，你可以在这里读取根运动增量并自己控制：

```csharp
void OnAnimatorMove()
{
    Vector3 delta = animator.deltaPosition;      // 本帧根运动位移量
    Quaternion deltaRot = animator.deltaRotation; // 本帧根运动旋转量

    // 自定义：只应用水平位移，垂直交给重力
    characterController.Move(new Vector3(delta.x, 0f, delta.z));
    transform.rotation *= deltaRot;
}
```

| 方法 | 含义 |
|------|------|
| `animator.deltaPosition` | 本帧根运动应该移动的向量（世界坐标） |
| `animator.deltaRotation` | 本帧根运动应该旋转的量 |
| `OnAnimatorMove()` | 启用 Root Motion 时每帧调用，覆写默认行为 |

**整行人话**：动画里带的位移我不全用，我挑着用——XZ 让动画控制，Y 轴交给物理/重力。

---

## 二、动画压缩与性能优化

### 2.1 压缩模式（Animation Import Settings）

| 模式 | 说明 | 文件大小 | 质量 |
|------|------|----------|------|
| **Off** | 不压缩，保留所有关键帧 | 最大 | 最高 |
| **Keyframe Reduction** | 删除冗余关键帧（误差内合并） | 中 | 中 |
| **Optimal** | 自动选择最佳压缩方式（旋转用四元数压缩等） | 最小 | 通常足够好 |

**官方推荐**：**Optimal**，除非你发现有明显失真才调回 Keyframe Reduction。

### 2.2 误差设置

在 Animation 导入设置中，有三个误差滑块：

| 设置 | 含义 | 建议 |
|------|------|------|
| **Position Error** | 位置允许的误差（相对于模型大小百分比） | 0.5% 起步，再调 |
| **Rotation Error** | 旋转允许的误差（角度） | 0.5° 起步 |
| **Scale Error** | 缩放误差 | 通常 1% 以上 |

**原则**：在**看不出差异**的前提下，误差越大越好——文件越小、CPU 采样越快。

### 2.3 其他优化建议

| 优化项 | 做法 |
|--------|------|
| 移除无用曲线 | FBX 里可能带了大量用不到的属性曲线，用 Mask 或精简 |
| 复用 Animation Clip | 同一个动作不要多份拷贝 |
| Humanoid CPU 开销 | Humanoid 比 Generic 高约 15~20%，同项目统一类型 |
| 减少 Animator 数量 | 场景中同时播放动画的角色越多，CPU 压力越大 |
| LOD 动画 | 远的角色降低动画采样率或简化骨骼 |

---

## 三、运行时代码创建 AnimationClip

极少数场景需要用代码动态生成 Clip（比如编辑器工具、程序化动画）：

```csharp
AnimationClip clip = new AnimationClip();
clip.frameRate = 60f;

// 给 Position.x 绑一条曲线：0秒=0，1秒=5
AnimationCurve curve = AnimationCurve.EaseInOut(0f, 0f, 1f, 5f);
clip.SetCurve("", typeof(Transform), "localPosition.x", curve);

clip.wrapMode = WrapMode.Loop;
```

| API | 含义 |
|-----|------|
| `clip.SetCurve(path, type, propertyName, curve)` | 把曲线绑到指定属性 |
| `path` | 相对路径，空字符串表示当前物体 |
| `type` | 组件类型（typeof(Transform) 等） |
| `propertyName` | 属性名，如 "localPosition.x"、"m_Color.r" |

**注意**：运行时创建 Clip 有 GC 开销，正常游戏业务不要这么用——直接做好 `.anim` 文件拖进去。

---

## 四、选型决策 — 什么时候用什么？

| 方案 | 适合场景 | 不适合 |
|------|----------|--------|
| **Animation Clip + Animator** | 角色动作、复杂状态机、骨骼动画、Blend Tree 混合 | 简单的 UI 淡入淡出（太重） |
| **DOTween** | UI 动效、按钮反馈、简单位移、数值过渡 | 角色骨骼连招（太弱） |
| **AnimationCurve 字段** | 设计师调的曲线数据（弹道、弹性、相机震动曲线） | 多属性复杂动画 |
| **Legacy Animation** | 老项目维护 / 极简单物体（门、旋转道具） | 新项目（官方推荐 Mecanim） |
| **程序动画（IK / Procedural）** | 自适应地形、物理驱动、 ragdoll | 固定动作（性价比低） |

**决策口诀**：骨骼动作用 Animator，UI 反馈用 DOTween，数值曲线用 AnimationCurve。

---

## 五、常见误区与最佳实践

| 误区 | 正确做法 |
|------|----------|
| 动画事件没反应 | 检查方法名拼写、是否 public、脚本是否在 Animator 同物体/子物体 |
| 事件触发多次 | 检查是否 Loop 了循环触发；或加状态判断 |
| 关键帧很多文件大 | 开 Optimal 压缩；精简无用曲线 |
| 根运动角色乱飞 | 检查 Root Transform Position 是否误设为 Bake 了 |
| 动画不循环 | Clip 勾选 Loop Time；Animator 状态也要配合 |
| 曲线编辑卡顿 | 减少关键帧数量；复杂曲线用脚本计算 |
| 颜色动画不生效 | 确保是 Material.color 还是材质的某个 shader 属性名 |
| SetCurve 找不到属性 | 用 Debug 模式查组件内部属性名，或查官方属性名文档 |

---

## 【进阶阶段小结】

| 维度 | 要点 |
|------|------|
| 根运动 | applyRootMotion + deltaPosition + OnAnimatorMove |
| 压缩 | Optimal 优先；误差越大文件越小 |
| 运行时创建 | SetCurve（极少用） |
| 选型 | 骨骼 Animator / UI DOTween / 曲线 AnimationCurve |
| 避坑 | 事件方法名、循环触发、压缩质量 |

---

# 【全文总结】

## 最重要的一行代码

```csharp
float y = heightCurve.Evaluate(progress);
```

| 部分 | 含义 |
|------|------|
| `heightCurve` | 动画曲线（可在 Inspector 手动画） |
| `Evaluate` | 采样求值 |
| `progress` | 时间/进度参数 |

## 三阶段对照

| 阶段 | 代表案例 |
|------|----------|
| 零基础 | 理解 Clip/Curve/Keyframe 三层结构 |
| 入门 | 脚步声事件、材质动画、曲线驱动子弹 |
| 进阶 | 根运动、动画压缩、选型决策 |

## 与系列文档关系

| 主题 | 文档 |
|------|------|
| Animator 状态机播放 Clip | [02_Animator动画.md](./02_Animator动画.md) |
| 有限状态机设计模式 | [03_状态机（有限状态机）.md](./03_状态机（有限状态机）.md) |
| DOTween 补间动画 | 见 major3/05_DoTween.md |
| 模型导入与 Animator 基础 | 见 major3/04_Model_Animator.md |

## 官方文档索引

| 主题 | 链接 |
|------|------|
| Animation Clip | https://docs.unity3d.com/Manual/animeditor-AnimationClips.html |
| Animation Curves | https://docs.unity3d.com/Manual/animeditor-AnimationCurves.html |
| Animation Events | https://docs.unity3d.com/Manual/animeditor-AnimationEvents.html |
| AnimationCurve API | https://docs.unity3d.com/ScriptReference/AnimationCurve.html |
| Root Motion | https://docs.unity3d.com/Manual/RootMotion.html |

---

*文档版本：与 major3/01_PlayerPrefs.md ~ 05_DoTween.md 同系列模板。*
