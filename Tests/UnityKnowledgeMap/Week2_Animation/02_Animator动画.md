# Animator 动画系统（Mecanim）详解

> **参照来源（取其精华）**
>
> **课程教材（六本 · 本专题对应章节）**
> - **杜亚南**《新印象 Unity2020游戏开发基础与实战》— Animator 组件、Apply Root Motion、动画融合与位移分工
> - **马遥**《Unity 3D完全自学教程》— Mecanim 入门、Animator 与 Animation 组件对比、Humanoid 概念
> - **宣雨松**《Unity 3D 游戏开发（第3版）》— Mecanim 四大件、Root Motion、Animation Mixing 理论主干
> - **陈俊宇**《Unity 游戏开发从入门到精通》— Animator Controller 创建、Parameters 类型、脚本 Set 参数
> - **王磊**《Unity 2022 游戏开发完全学习手册》— Humanoid Rig、Avatar Configure、Culling Mode、新版 Mecanim 工作流
> - **吴亚峰**《Unity 游戏开发实战（第2版）》— 角色动画实战、`SetFloat`/`SetTrigger` 驱动模式
>
> **动画专项权威（补充深化）**
> - **Jamie Dean**《Unity Character Animation with Mecanim》(Packt) — Mecanim 三阶段工作流、Avatar Muscle、Controller 与 AI 脚本
> - **Jason Gregory**《游戏引擎架构》（第2版）— 骨骼动画管线、Humanoid Retarget 引擎层概念
>
> **Unity 官方 Manual + Scripting API（最终标准）**：[Mecanim Overview](https://docs.unity3d.com/Manual/AnimationOverview.html) · [Mecanim Animation System](https://docs.unity3d.com/Manual/MecanimAnimationSystem.html) · [Mecanim FAQ](https://docs.unity3d.com/Manual/MecanimFAQ.html) · [Animator](https://docs.unity3d.com/Manual/class-Animator.html) · [Avatar Setup](https://docs.unity3d.com/Manual/ConfiguringtheAvatar.html) · [Animator Controllers](https://docs.unity3d.com/Manual/AnimatorControllers.html) · [Animator API](https://docs.unity3d.com/ScriptReference/Animator.html) · [AnimatorStateInfo](https://docs.unity3d.com/ScriptReference/AnimatorStateInfo.html)
>
> **已剔除的糟粕**：脚本里 if-else 直接 `Play` 绕过状态机；每帧 `anim.Play("Run")` 导致动画永远从头播；Humanoid Avatar 未 Configure 就 Retarget；Root Motion 与 CharacterController 双写位移；SetTrigger 连点不 Reset 却怪动画不响应；混淆 Animator Culling Mode 与 Camera Frustum Culling。

---

## 使用频率图例

| 标记 | 含义 | 本专题学习优先级 |
|------|------|----------------|
| ⭐⭐⭐ | 角色动画几乎每个项目必会 | 第一～二周 |
| ⭐⭐ | 按模块必学（Avatar、Root Motion） | 第二～三周 |
| ⭐ | 特定优化场景 | 遇到再学 |

---

## 思维导图总览

```
Animator 动画系统（Mecanim）
│
├── 【第一梯队】四大件 ★★★
│   ├── Animator 组件 ─────────── 运行时播放入口（Behaviour）
│   ├── Animator Controller ───── 状态机逻辑（.controller 资源）
│   ├── Animation Clip ────────── 动画数据（与 Legacy 共用 .anim）
│   └── Avatar（Humanoid）─────── 人形骨骼标准映射
│
├── 【第二梯队】核心工作流 ★★★
│   ├── 脚本 Set 参数 → Controller 评估 Transition → 播放 Clip
│   ├── Parameters：Float / Int / Bool / Trigger
│   ├── State / Transition / Condition（详见 03 文档）
│   └── Layer / AvatarMask（详见 03 文档）
│
├── 【第三梯队】脚本驱动 API ★★★
│   ├── SetFloat / SetBool / SetInteger / SetTrigger
│   ├── ResetTrigger / GetFloat / GetBool
│   ├── GetCurrentAnimatorStateInfo / normalizedTime
│   └── anim.speed（0=暂停，1=正常）
│
├── 【第四梯队】组件属性 ★★
│   ├── Apply Root Motion ─── 动画 Root 曲线驱动位移
│   ├── Culling Mode ──────── 屏幕外动画更新策略
│   └── Controller / Avatar 绑定
│
├── 【第五梯队】动画融合 ★★
│   ├── Transition 过渡混合
│   └── BlendTree 参数混合（详见 04 文档）
│
└── 【注意要点】
    ├── 逻辑只 Set 参数，State 在编辑器配
    ├── Trigger 一次性，需 Reset 或冷却
    └── 角色动画首选 Mecanim，非 Legacy
```

---

## 一、类与资源关系（官方标准 · 必背）

```
UnityEngine.Object
├── AnimationClip（.anim）
├── Avatar（Humanoid 映射资产）
└── RuntimeAnimatorController
        └── AnimatorController（.controller，编辑器资源）

Component → Behaviour
└── Animator
        ├── runtimeAnimatorController → 绑定 Controller
        ├── avatar → Humanoid 时绑定 Avatar
        └── 运行时读取 Parameters，驱动 State 切换
```

**[重难点]** 脚本**不直接选 Clip**，而是 **Set 参数** → Controller 里的 Transition 决定播什么。这是 Mecanim 与 Legacy 的根本区别。

**[易错点]** 未给 Animator 绑定 Controller → 组件存在但**无任何动画响应**。

---

## 二、Mecanim vs Legacy 对比（⭐⭐⭐）

| 对比项 | Animation（Legacy） | Animator（Mecanim） |
|--------|---------------------|---------------------|
| 组件 | `Animation` | `Animator` |
| 控制 | `Play("ClipName")` | `SetFloat/SetTrigger` → 状态机 |
| 状态机 | 无 | Animator Controller |
| 混合 | CrossFade 有限 | Transition + BlendTree + Layer |
| 人形 Retarget | 不支持 | Avatar + Humanoid |
| 适用 | 门、镜头、简单 Prop | 角色、NPC、多行为 |
| 详见 | [01_Animation动画深入.md](01_Animation动画深入.md) | 本文 |

---

## 三、Animator 组件（⭐⭐⭐）

### 3.1 基本属性

| 项目 | 内容 |
|------|------|
| **是什么** | Mecanim 运行时播放组件，挂载在需要播放动画的 GameObject 上 |
| **官方** | [Manual: Animator](https://docs.unity3d.com/Manual/class-Animator.html) · [API: Animator](https://docs.unity3d.com/ScriptReference/Animator.html) |
| **必绑** | Controller（`.controller`）；Humanoid 时还需 Avatar |

### 3.2 Apply Root Motion（⭐⭐）

| 设置 | 说明 | 频率 |
|------|------|------|
| **开启** | 动画 Root 曲线驱动 Transform 位移/旋转 | ⭐⭐ |
| **关闭** | 位移由 CharacterController / Rigidbody / 脚本控制（**主流**） | ⭐⭐⭐ |
| **无 Root 曲线** | Clip 不含 Root 运动时，开启也不产生位移 | ⭐⭐ |

**[重难点]**
```
Root Motion 开 + 脚本 transform.Translate 同时写 → 滑步、漂移、双倍速度
```

**[教材精华·宣雨松/杜亚南]** 第三人称/过场可开 Root Motion；FPS/TPS 主流 **脚本/CC 移动 + Root Motion 关**。

### 3.3 Culling Mode（⭐）

| 模式 | 说明 | 频率 |
|------|------|------|
| **Always Animate** | 屏幕外也完整更新（默认） | ⭐⭐ |
| **Cull Update Transform** | 不采样动画，Transform 保持最后姿态 | ⭐ |
| **Cull Completely** | 完全不算动画（远处 NPC 优化） | ⭐ |

**[易错点]** Culling Mode 是 **Animator 更新策略**，与 Camera Frustum Culling（渲染剔除）不是同一概念。

---

## 四、Avatar 与 Humanoid（⭐⭐）

| 项目 | 说明 |
|------|------|
| **是什么** | 将模型骨骼映射到 Unity 标准 Humanoid 结构的接口 |
| **官方** | [Manual: Avatar](https://docs.unity3d.com/Manual/class-Avatar.html) · [Humanoid Avatars](https://docs.unity3d.com/Manual/ConfiguringtheAvatar.html) |
| **必需骨骼** | 至少 15 个 Humanoid 必需骨 |
| **作用** | 不同人形模型间**共享、重定向**同一套动画 |

### 配置流程

| 步骤 | 操作 | 频率 |
|:---:|------|------|
| 1 | FBX → Rig → Animation Type: **Humanoid** | ⭐⭐⭐ |
| 2 | **Configure** → 骨骼映射全绿 | ⭐⭐⭐ |
| 3 | **Apply** | ⭐⭐⭐ |
| 4 | Animator 绑定 Avatar + Controller | ⭐⭐⭐ |

**[易错点]** Configure 报红 → Retarget 失败，动画扭曲或 T-Pose。

**[教材精华·王磊/马遥/Dean]** 一套 Walk/Run Clip 多角色共用 → Humanoid + Configure 全绿 + 各自 Avatar。

---

## 五、Animator Controller（⭐⭐⭐）

| 术语 | 说明 | 频率 |
|------|------|------|
| **State** | 状态，对应一个 Motion（Clip 或 BlendTree） | ⭐⭐⭐ |
| **Transition** | 状态间切换路径 + Conditions | ⭐⭐⭐ |
| **Parameters** | Float/Int/Bool/Trigger，脚本与动画的接口 | ⭐⭐⭐ |
| **Layer** | 多层并行（上下半身分离等） | ⭐⭐ |
| **Blend Tree** | 单 State 内多 Clip 混合 | ⭐⭐ |

### 创建步骤

| 步骤 | 操作 |
|:---:|------|
| 1 | Project → Create → **Animator Controller** |
| 2 | Animator 窗口 → Create State → 分配 Clip |
| 3 | Make Transition → Add Condition |
| 4 | Parameters 面板 → 添加 Speed、Jump 等 |
| 5 | 拖到 Animator 组件 **Controller** 栏 |

详见 [03_动画状态机一.md](03_动画状态机一.md)。

---

## 六、脚本驱动 API（⭐⭐⭐）

### 6.1 写参数

| API | 说明 | 频率 |
|-----|------|------|
| `SetFloat("Speed", v)` | 浮点参数，驱动 BlendTree / 条件 | ⭐⭐⭐ |
| `SetBool("IsGrounded", b)` | 布尔参数 | ⭐⭐⭐ |
| `SetInteger("WeaponType", i)` | 整型参数 | ⭐⭐ |
| `SetTrigger("Attack")` | 一次性触发（Jump、Attack） | ⭐⭐⭐ |
| `ResetTrigger("Attack")` | 重置 Trigger | ⭐⭐ |

### 6.2 读状态

| API | 说明 | 频率 |
|-----|------|------|
| `GetCurrentAnimatorStateInfo(layer)` | 当前层状态信息 | ⭐⭐⭐ |
| `info.IsName("Run")` | 是否处于某 State | ⭐⭐⭐ |
| `info.normalizedTime` | 播放进度 0~1 | ⭐⭐⭐ |
| `anim.speed` | 全局速度（0=暂停） | ⭐⭐ |
| `GetFloat("Speed")` | 读参数当前值 | ⭐ |

```csharp
public class PlayerAnim : MonoBehaviour
{
    Animator anim;

    void Awake()
    {
        anim = GetComponent<Animator>();  // ⭐⭐⭐ 缓存
    }

    void Update()
    {
        float speed = /* 从输入或 CharacterController 读取 */;
        anim.SetFloat("Speed", speed);
        anim.SetBool("IsGrounded", CheckGrounded());

        if (Input.GetKeyDown(KeyCode.Space))
            anim.SetTrigger("Jump");
    }

    bool CheckGrounded()
    {
        // 射线或 CharacterController.isGrounded
        return true;
    }
}
```

### 6.3 Parameters 类型与用途（⭐⭐⭐）

| 类型 | 用途 | 典型 | 频率 |
|------|------|------|------|
| **Float** | 连续值 | Speed、MoveX | ⭐⭐⭐ |
| **Bool** | 开关 | IsGrounded、IsAiming | ⭐⭐⭐ |
| **Int** | 离散枚举 | WeaponType、ComboIndex | ⭐⭐ |
| **Trigger** | 一次性脉冲 | Jump、Attack、Reload | ⭐⭐⭐ |

**[教材精华·陈俊宇/吴亚峰]** 脚本只 **Set 参数**；State/Transition 在 Controller 编辑器配置 — 逻辑与表现分离。

**[重难点] Trigger 机制**

| 特点 | 说明 |
|------|------|
| 触发一次 | Transition 消耗后自动 Reset |
| 连点无效 | 第二次 SetTrigger 可能不触发，需等过渡完成或手动 ResetTrigger |
| 用途 | Jump、Attack、Reload 等**一次性**动作 |

**[易错点]**
- 参数名与 Controller 拼写不一致 → **静默失效**
- 每帧 `anim.Play("Run")` → 动画永远从第 0 帧开始，应改 SetFloat
- Update 里 GetComponent\<Animator\> → Awake 缓存

---

## 七、动画融合 Animation Mixing（⭐⭐）

| 概念 | 说明 |
|------|------|
| **Transition 混合** | 状态 A → B 时在 Duration 内混合两个 Motion |
| **BlendTree 混合** | 单 State 内按参数权重混合多个 Clip |
| **表现** | 走→跑、待机→攻击切换更自然 |

Transition 详见 03；BlendTree 详见 04。

---

## 八、注意要点与最佳实践

### 常见陷阱

| 易错点 | 说明 |
|--------|------|
| 未绑 Controller | Animator 无反应 |
| 参数名拼写不一致 | 静默失效 |
| SetTrigger 连点 | 第二次不触发 |
| 每帧 Play 同一 State | 动画永远从头播 |
| Avatar 未 Configure | 动画扭曲 |
| Root Motion + 脚本双写 | 滑步漂移 |

### 最佳实践

- **脚本 Set 参数，编辑器配 State/Transition** — 职责分离
- Float 驱动连续值（Speed）；Trigger 驱动一次性（Jump、Attack）
- `GetCurrentAnimatorStateInfo` 判断攻击是否播完再允许输入
- Humanoid 角色先 Configure Avatar 再绑动画
- 远处 NPC 用 Cull Completely 优化

**[糟粕剔除]** 脚本里大量 if-else 直接 `anim.Play("xxx")` 绕过状态机 → 违背 Mecanim 设计，难维护；应改 Parameters + Transition。

---

## 九、典型应用场景

| 场景 | 用法 | 频率 |
|------|------|------|
| 第三人称角色 | SetFloat Speed + SetTrigger Jump | ⭐⭐⭐ |
| 人形 NPC 共用动画 | 同一 Controller + 不同 Avatar | ⭐⭐ |
| 过场位移 | Root Motion 开 + 特定 Clip | ⭐⭐ |
| 远处 crowd | Cull Completely | ⭐ |
| 简单门动画 | **不用 Animator** → Legacy | — |

---

## 十、与动画专题其他文档的对应

| 本篇章节 | 详细文档 |
|----------|----------|
| Legacy 基础 | [01_Animation动画深入.md](01_Animation动画深入.md) |
| Animator 基础（本文） | 02_Animator动画.md |
| State / Transition / Layer | [03_动画状态机一.md](03_动画状态机一.md) |
| BlendTree / IK / MatchTarget | [04_动画状态机二.md](04_动画状态机二.md) |
| 射击/RPG/2D 实战 | [05_常见游戏动画设置.md](05_常见游戏动画设置.md) |

---

## 十一、课程六教材 · 本专题贡献对照

| 教材 | 本专题精读要点 | 优先级 |
|------|---------------|--------|
| 杜亚南 | Root Motion 开关、动画融合与位移 | ⭐⭐⭐ |
| 马遥 | Mecanim 入门、Humanoid 概念 | ⭐⭐ |
| 宣雨松 | 四大件、Root Motion、Mixing 理论 | ⭐⭐⭐ |
| 陈俊宇 | Controller、Parameters、Set 参数 | ⭐⭐⭐ |
| 王磊 | Avatar Configure、Culling Mode | ⭐⭐⭐ |
| 吴亚峰 | SetFloat/SetTrigger 角色实战 | ⭐⭐⭐ |
| Dean | Mecanim 工作流、Retarget 实战 | ⭐⭐ |
| Gregory | 引擎层骨骼动画管线 | ⭐⭐ |
| **Unity 官方** | **Animator/Avatar/FAQ 最终语义** | ⭐⭐⭐ |

---

## 十二、教材 vs 官方 · 对照速查

| 知识点 | 教材常见写法 | 官方/工程推荐 |
|--------|--------------|---------------|
| 控制动画 | 脚本 `anim.Play("Clip")` | **Set 参数** → Controller 切 State |
| 跳跃/攻击 | SetBool 长按 | **SetTrigger** 一次性 + Reset |
| 位移来源 | Root Motion 与脚本同时写 | 二选一：主流 **脚本/CC 移动 + Root Motion 关** |
| Avatar 报错 | 强行播放看效果 | **Configure 全绿** 再绑动画 |
| 参数失效 | 怀疑引擎 Bug | 先查 **拼写、类型、Controller 是否绑定** |
| 暂停动画 | Destroy 组件 | `anim.speed = 0` |

---

## 十三、自测清单

- [ ] 说清 Animator 四大件及各自作用
- [ ] 说清「Set 参数 → Transition → 播 Clip」流程
- [ ] 会用 SetFloat / SetBool / SetTrigger / ResetTrigger
- [ ] 会用 GetCurrentAnimatorStateInfo 与 normalizedTime
- [ ] 说清 Root Motion 开/关的适用场景
- [ ] 会配置 Humanoid Avatar（Configure 全绿）
- [ ] 说清 Trigger 连点为何不响应

---

## 十四、官方参考

- [Manual: Mecanim Animation System](https://docs.unity3d.com/Manual/AnimationSection.html)
- [Manual: Animator Component](https://docs.unity3d.com/Manual/class-Animator.html)
- [Manual: Animator Controller](https://docs.unity3d.com/Manual/AnimatorControllers.html)
- [Manual: Avatar Setup](https://docs.unity3d.com/Manual/ConfiguringtheAvatar.html)
- [API: Animator](https://docs.unity3d.com/ScriptReference/Animator.html)
- [API: AnimatorStateInfo](https://docs.unity3d.com/ScriptReference/AnimatorStateInfo.html)
