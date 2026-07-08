# 小灶 02 · Loading 加载系统 · 考试版 vs 商业分层（lixiaotong · S2-）

> **触发**：**§11.24** → 你回复 **`小灶：Loading`** → **本 Chat 独占**  
> **定位**：不占大步 Chat · 架构 / 模式 / API / 面试话 / 对照你自写代码  
> **双轨**：**交卷** 仍用 `LoadingController` P-L1 · **理解/面试** 用本讲义商业分层  
> **吸收**：[`外部路线吸收库.md`](../外部路线吸收库.md) **§6.4 F05-LOAD** · Unity `AsyncOperation` · 手游 Loading 通用实践

---

## 零、你现在该学什么

| 阶段 | 位置 | 本讲义 | 不必现在做 |
|------|------|--------|------------|
| **W2 Exam06 交卷** | 第 3～6 步 | **Min 双轨 + 6s + Start 启协程** | Addressables 全套 |
| **S2- 理解力** | P 81* | **能画 Loading 四层** · 口述 fake/real | 热更新资源包 |
| **S2+ 练手** | 阶段 02 | 拆 **LoadingView** 只订阅进度事件 | 多语言 Tips 表 |
| **S3 / 讲师** | 2027+ | 分包下载 · 断点续传 · 合规隐私条 | 王者荣耀级 CDN |

---

## 一、考试版 vs 商业版 · 核心差距

| 问题 | 考试写法（能得分） | 商业上线（手游/MMO 通用） |
|------|-------------------|---------------------------|
| 结构 | 一个 `LoadingController`：协程+Slider+Text+静音+切场景 | **配置 / 编排 / 表现 / 转场 / 音频** 分层 |
| 进度 | `t/duration` 假进度 + 可选 `op.progress/0.9f` | **ProgressModel** 统一算 `DisplayProgress` · UI 只读 |
| 时长 | 写死 `6f` / `5f` | **LoadingConfig** ScriptableObject：最小时长 · 最大等待 · Tips 表 |
| 切场景 | `LoadSceneAsync` + `allowSceneActivation` | **SceneFlowService** · 场景名 const · 失败重试 · 埋点 |
| UI | 脚本里直接改 `slider.value`、Text | **LoadingView** 订阅 `OnProgressChanged` · 逻辑不知 Slider |
| 静音 | `audioSource.mute` 写在 Loading 脚本里 | **AudioSettingsService** · Loading 只发「静音切换」命令 |
| 生命周期 | 曾用 `OnEnable` 启协程（踩坑 L3） | **Start 启流程** · **OnDisable 停协程+退订** |
| 扩展 | 无 | 分包进度 · 版本号 · 用户协议 · 重试按钮 |

**阅卷**：Min 双轨 + 6s + 双 Text + 静音 = 10 分够用；**商业分层是面试与主程视野，不是 W2 硬性交付**。

---

## 二、商业四层 + 两服务（对标大厂客户端通用）

```
[ 表现层 ]  LoadingView              ← Slider / TipTop / TipBottom / 静音图标
      ↑ OnProgressChanged / OnTipChanged / OnMuteChanged
[ 编排层 ]  LoadingOrchestrator        ← 协程：Min(fake,real) · 等最小时长 · 激活场景
      ↑ 读配置 · 驱动
[ 数据层 ]  LoadingConfig (SO/struct) ← minDuration · sceneName · tipThresholds[]
      ↑
[ 转场层 ]  SceneTransitionService     ← LoadSceneAsync · allowSceneActivation · 失败回调
      ↑
[ 音频层 ]  BgmController（可选独立）   ← mute 状态 · 与 Loading 编排解耦
```

**设计模式（面试能讲）**

| 模式 | 在 Loading 里 |
|------|----------------|
| **观察者** | `OnProgressChanged(float)` · View 订阅 |
| **单一职责** | Orchestrator 不算 UI · View 不调 LoadSceneAsync |
| **数据驱动** | Tips 按进度段配表 · 策划改 SO 不改代码 |
| **门面 Facade** | `SceneTransitionService.LoadGame()` 隐藏 Async 细节 |
| **策略** | `IProgressStrategy`：纯时间 / Min 双轨 / 真实下载字节 |

---

## 三、数据层 · LoadingConfig

```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "LoadingConfig", menuName = "Exam/LoadingConfig")]
public class LoadingConfig : ScriptableObject
{
    [Header("场景")]
    public string targetSceneName = "Exam06_Game";

    [Header("时间")]
    public float minDisplaySeconds = 6f;   // 卷面：5s/6s 在此配
    public float postFullDelay = 0.3f;       // 100% 后停留再进

    [Header("Tips 分段 (0~1)")]
    public string tipBelow33 = "正在连接服务器...";
    public string tipBelow66 = "正在加载场景...";
    public string tipAbove66 = "即将进入游戏...";
}
```

**要点**：Exam05=5 · Exam06=6 **只改 SO 一处**，代码不重编译。

---

## 四、编排层 · LoadingOrchestrator（核心算法 · 你已会）

```csharp
using System;
using System.Collections;
using UnityEngine;

/// <summary>
/// 加载编排：不算 UI，只产出 progress 并驱动转场。
/// </summary>
public class LoadingOrchestrator : MonoBehaviour
{
    [SerializeField] private LoadingConfig config;

    /// <summary>UI 订阅：0~1 显示进度。</summary>
    public event Action<float> OnProgressChanged;
    public event Action<string> OnTipChanged;
    public event Action OnLoadingComplete;

    public void BeginLoad()
    {
        StartCoroutine(LoadRoutine());
    }

    private IEnumerator LoadRoutine()
    {
        var op = SceneTransitionService.LoadAsync(config.targetSceneName);
        float elapsed = 0f;

        while (elapsed < config.minDisplaySeconds)
        {
            elapsed += Time.deltaTime;
            float fake = elapsed / config.minDisplaySeconds;
            float real = op.Progress01; // 封装 op.progress/0.9f
            float display = Mathf.Clamp01(Mathf.Min(fake, real)); // 诚实瓶颈 · 禁止 Max

            OnProgressChanged?.Invoke(display);
            OnTipChanged?.Invoke(config.GetTip(display));
            yield return null;
        }

        OnProgressChanged?.Invoke(1f);
        yield return new WaitForSeconds(config.postFullDelay);
        op.AllowActivation();
        OnLoadingComplete?.Invoke();
    }
}
```

**API 必记**

| API | 含义 | 坑 |
|-----|------|-----|
| `LoadSceneAsync` | 异步加载 | 场景必须在 Build |
| `allowSceneActivation = false` | 按住不切场景 | 不设则加载到 0.9 可能自动切 |
| `op.progress` | 0~0.9 | **要 `/0.9f` 才映射 0~1** |
| `Mathf.Min(fake, real)` | 双轨 honest | **Max 会条虚高**（踩坑 L1） |
| `Time.deltaTime` | 帧间隔 | **OnEnable 首帧可能异常大**（踩坑 L3） |

---

## 五、转场层 · SceneTransitionService

```csharp
using UnityEngine.SceneManagement;

public static class SceneTransitionService
{
    public static AsyncLoadHandle LoadAsync(string sceneName)
    {
        var op = SceneManager.LoadSceneAsync(sceneName);
        op.allowSceneActivation = false;
        return new AsyncLoadHandle(op);
    }
}

public readonly struct AsyncLoadHandle
{
    private readonly AsyncOperation _op;
    public AsyncLoadHandle(AsyncOperation op) => _op = op;
    public float Progress01 => _op.progress / 0.9f;
    public void AllowActivation() => _op.allowSceneActivation = true;
}
```

**大厂为什么要包一层**：后期加 **Additive 加载 · 预加载下一场 · 失败重试 · 埋点** 只改 Service。

---

## 六、表现层 · LoadingView（只订阅 · 不 LoadScene）

```csharp
using UnityEngine;
using UnityEngine.UI;

public class LoadingView : MonoBehaviour
{
    [SerializeField] private Slider progressSlider;
    [SerializeField] private Text tipProgressText;
    [SerializeField] private Text tipBottomText;
    [SerializeField] private LoadingOrchestrator orchestrator;

    private void OnEnable()
    {
        orchestrator.OnProgressChanged += OnProgress;
        orchestrator.OnTipChanged += OnTip;
    }

    private void OnDisable()
    {
        orchestrator.OnProgressChanged -= OnProgress;
        orchestrator.OnTipChanged -= OnTip;
    }

    private void OnProgress(float p)
    {
        progressSlider.value = p;
        tipProgressText.text = $"加载中 {(int)(p * 100)}%";
    }

    private void OnTip(string tip) => tipBottomText.text = tip;
}
```

**与血量小灶对称**：HpView 听 `OnHpChanged` · LoadingView 听 `OnProgressChanged`。

---

## 七、你的 Exam06 代码 · 与四层的「最小映射」

| 商业层 | 你现在的写法 | 评价 |
|--------|--------------|------|
| **Config** | `duration=6f` · `nextSceneName` 字段 | ✅ 卷面够 · 商业→SO |
| **Orchestrator** | `LoadingScene()` 协程 · Min 双轨 | ✅ **核心算法已大厂级** |
| **Transition** | 协程内直接 `LoadSceneAsync` | ✅ W2 可 inline · 商业→Service |
| **View** | `ReFreshUI()` 改 Slider/Text | ✅ 卷面够 · 商业→拆 View+事件 |
| **Audio** | `OnMuteBtnClick` + mute | ✅ 可保留 · 商业→AudioService |
| **生命周期** | `Start` 启协程 · `OnDestroy` 解绑 | ✅ 已修 L3 · 商业补 **OnDisable** |

**你已写对（Coach 禁止范本低于此）**：Min · allowSceneActivation · 6s · 命名静音 · Start 启协程

**P-L1 仍差（与小灶无关，交卷要补）**：§11.19 五层注释 · 删 VisualScripting using · Start 同步 `isMute`

---

## 八、OnEnable vs Start · 小灶专讲（你刚踩的坑）

| | OnEnable 启加载协程 | Start 启加载协程 |
|--|---------------------|------------------|
| **调用次数** | 每次 Enable 都调 | 每次 Play 只调一次 |
| **典型风险** | 多协程并行 · 首帧 deltaTime 异常 · 与 UI 开关叠加 | 时机稳定 |
| **行业分工** | OnEnable/OnDisable **只做订阅** | **Start 启业务流程** |
| **踩坑编号** | **L3** | P-L1 v3 标准 |

**面试一句话**：「Loading 这种 **只跑一次的流程** 放 Start；OnEnable 只做 **可重复** 的监听注册，并 OnDisable 对称退订。」

---

## 九、进阶扩展（阶段 02+ · 主程视野）

| 模块 | 行业扩展 |
|------|----------|
| **Addressables** | 按 label 下载 · `DownloadDependenciesAsync` 进度当 real |
| **分包** | fake=解压进度 · real=网络字节 |
| **MoveTowards** | 条平滑逼近 target · 防 jitter |
| **超时** | real 卡住 · 弹重试 / 切 WiFi 提示 |
| **版本/热更** | Loading 显示版本号 · 强制更新门 |
| **埋点** | 加载耗时 · 流失率 · 哪段 Tip 停留久 |

---

## 十、面试 3 句话（讲师预备）

1. 「Loading 我们 **Config 配最短展示时间**，进度用 **Min(时间轴, AsyncOperation/0.9)**，避免条虚高或真实加载未完成就进游戏。」  
2. 「**allowSceneActivation=false** 按住场景，条满且满足最小时长后再激活，这是 Unity 异步加载标配。」  
3. 「UI 用 **事件订阅** 刷新 Slider，编排层不引用 Slider；**Start 启协程、OnDisable 停协程**，避免 OnEnable 重复启动。」

---

## 十一、自检题（简讲师课后）

1. 为什么 `op.progress` 要除以 **0.9f**？不设 `allowSceneActivation=false` 会怎样？  
2. **Max(fake, real)** 和 **Min(fake, real)** 哪个是「诚实瓶颈」？各适合什么产品诉求？  
3. Exam06 若只加 **一个** 商业特性且不超 P-L1，你选 **LoadingConfig SO** 还是 **抽 SceneTransitionService**？为什么？

---

## 十一-A、自检题 · 标准答案（lixiaotong · 2026-06-24 · Coach 核对）

> **用途**：你做完自检后对照；档案/踩坑库引用本段 · **禁止**比 Min 双轨更低的范本。

### 题 1 · `op.progress / 0.9f` 与 `allowSceneActivation`

**为什么要 `/0.9f`？**

| 事实 | 说明 |
|------|------|
| Unity 行为 | `LoadSceneAsync` 在 **`allowSceneActivation = false`** 时，加载在后台进行，`op.progress` **最多到约 0.9**（90%） |
| 剩余 0.1 | 只有当你设 **`allowSceneActivation = true`** 才真正激活场景，那时 progress 才到 **1.0** |
| UI 需要 0~1 | 条要显示「真实加载完成了多少」，要把 **0~0.9 映射成 0~1** → **`real = op.progress / 0.9f`** |

**不设 `allowSceneActivation = false` 会怎样？**

| 后果 | 说明 |
|------|------|
| **抢跑切场景** | 加载到约 **0.9** 时 Unity **可能自动激活** 新场景 |
| **最短展示时间失效** | 你的 **6 秒 / 5 秒** 协程还没跑完，Loading 界面就被卸掉 → 玩家感觉「没过渡就进了」 |
| **双轨失控** | 无法保证「条满 + 时间到 + 真实加载完成」三者同时满足 |

**一句话**：`/0.9f` 是为了 **UI 进度条刻度正确**；`allowSceneActivation=false` 是为了 **按住场景，把切场时机交还给你的协程**。

---

### 题 2 · Min vs Max · 谁是「诚实瓶颈」

**答案：`Min(fake, real)` 是「诚实瓶颈」（你 Exam05/06 的写法 ✅）**

| 写法 | 条显示谁 | 含义 | 适用 |
|------|----------|------|------|
| **`Min(fake, real)`** | 取 **较慢** 的那条轨 | 时间到了但真实加载慢 → 条 **不会超过真实**；真实快但时间未到 → 条 **不会超过时间轴** | **考试 · 诚实 UX · 大厂常规**（阿里/腾讯系 Loading 常见） |
| **`Max(fake, real)`** | 取 **较快** 的那条轨 | 条容易 **虚高到 100%** 而资源还没好；或 **时间没到条就满** | 仅「假快」营销 Loading · **本仓库禁止**（踩坑 **L1**） |

**产品诉求对照**

- **诚实 / 防投诉 / 防进空场景**：**Min** + `allowSceneActivation=false` + 最小时长  
- **宁可条假快、不暴露慢加载**（少数休闲广告向）：Max（**本课程不教**）

**面试句**：「我们用 **Min 双轨** 做 honest progress，避免条虚高或玩家以为加载完成其实还在 IO。」

---

### 题 3 · 只加一个商业特性：SO 还是 SceneTransitionService？

**推荐：优先 `LoadingConfig` ScriptableObject（SO）**

| 维度 | **LoadingConfig SO** | **SceneTransitionService** |
|------|----------------------|----------------------------|
| **解决 Exam05 vs Exam06** | **直接**：5s/6s · 场景名 · Tips 改 SO 即可 | 间接：仍要在某处配 duration |
| **改动量** | 小：字段搬进 SO · 逻辑几乎不动 | 中：抽 static/类 · 改调用链 |
| **W2 P-L1 风险** | **低** · 仍是一个 Mono + 协程 | 中 · 易过度抽象 |
| **商业收益** | **数据驱动** · 策划可调 · 面试能讲 SO | **架构门面** · 适合 retry/埋点/Additive |
| **阶段** | **现在（S2-）** ✅ | **阶段 02+** 更合适 |

**为什么不是先 Service？**

- 你 **Min + Async + Start** 已具备；当前痛点是 **5 秒 / 6 秒 / 场景名 / Tips 写死在代码** → **SO 更对症**  
- Service 的价值在 **失败重试、埋点、多场景编排** — Exam06 卷面 **不要求**，提前抽容易 ** over-engineer**

**若面试追问「第二个加什么」**：再加 **SceneTransitionService**（统一 `LoadAsync` + `AllowActivation` + 错误回调）。

**标准答法（30 秒）**：  
「W2 我只加一个 **LoadingConfig SO**，把最小时长、目标场景、Tips 分段配置化，Exam05/06 只换资产不换代码；**SceneTransitionService** 留到需要重试和埋点再上。」

---

## 十一-B、自检完成登记

| 字段 | 值 |
|------|-----|
| 学员 | lixiaotong |
| 小灶 | 02 Loading |
| 自检 | **3/3 已阅答案** · 2026-06-24 |
| 下一动作 | Chat **「进行下一步」** → Exam06 第 4 步 |

---

## 十二、项目经理 1 段（何时上四层）

| 阶段 | 建议 |
|------|------|
| **W2 交卷** | 单脚本 Min 双轨 ✅ 不必拆四文件 |
| **阶段 02 小项目** | 拆 View + Orchestrator · Config SO |
| **上线前** | SceneTransitionService + 超时重试 + 埋点 |
| **带 5 人以内** | 先统一 Loading 规范文档，再要求分层 |

---

**下一模块**：Exam06 第 4 步 Game UI · 或 **`小灶：血量`**（若未上）  
**回到练习**：下一条 Chat 发 **「进行下一步」** → 第 4 步三钮 UI（本 Chat 不夹带教学）
