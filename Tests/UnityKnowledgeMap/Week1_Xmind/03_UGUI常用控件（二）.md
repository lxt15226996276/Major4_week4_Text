# Unity UGUI 常用控件（二）详解

> 参照：[Unity 官方 Manual - Toggle](https://docs.unity3d.com/Manual/script-Toggle.html) · [Slider](https://docs.unity3d.com/Manual/script-Slider.html) · [Scrollbar](https://docs.unity3d.com/Manual/script-Scrollbar.html) · [ScrollRect](https://docs.unity3d.com/Manual/script-ScrollRect.html)  
> 关联文档：[02_UGUI常用控件（一）.md](./02_UGUI常用控件（一）.md)（Text/Image/Button）· [04_UGUI常用控件（三）.md](./04_UGUI常用控件（三）.md)（InputField/Dropdown/事件接口）· [../major3/01_PlayerPrefs.md](../major3/01_PlayerPrefs.md)（PlayerPrefs 保存设置）  
> 学习路径：**零基础 → 入门 → 进阶**，每阶段采用 **总—分—总** 结构。  
> 讲解维度：**定义 → 本质 → 特点 → 适用场景 → 原理 → API → 步骤 → 案例 → 避坑**（进阶含 ToggleGroup / ScrollRect 性能优化 / 自定义滑块）。  
> 案例讲解：遵循 **案例代码讲解模板**（功能 → 代码 → 语法拆解 → 逐行详解 → 操作提示）。  
> API 讲解：入门/进阶 API 章节均采用 **逐词读懂** 格式（与 [../major3/01_PlayerPrefs.md](../major3/01_PlayerPrefs.md) 一致：类型 → 参数 → 整行人话）。

---

## 【全文总述】

**Toggle（开关）** 是 UGUI 的「单选/复选框」：选中和未选中两种状态，支持 ToggleGroup 实现单选互斥。  
**Slider（滑块）** 是 UGUI 的「连续调节器」：拖动滑块在最小值和最大值之间连续取值，适合音量、亮度等需要精细调节的参数。  
**Scrollbar（滚动条）** 是 UGUI 的「滚动控制器」：配合 ScrollRect 使用，手动控制滚动位置，也可由内容自动驱动。  
**ScrollRect（滚动视图）** 是 UGUI 的「可滚动容器」：当内容超过可视区域时，允许用户拖动或滑动查看更多内容，是制作列表、背包、聊天记录的核心控件。  
本文从开关和滑块的基础用法，到滚动视图的实现，逐层展开。

### 思维导图总览

```
Unity UGUI 常用控件（二）
│
├── Toggle（开关控件 — 单选/复选）
│   │
│   ├── 【知识维度】（讲师框架 — 完整版）
│   │   │
│   │   ├── 定义：可切换选中/未选中状态的控件，支持单选组
│   │   │   └── 官方描述：The Toggle component is a selectable that controls a boolean state
│   │   │       创建方式：右键 UI → Toggle（含 Label 和 Checkmark）
│   │   │
│   │   ├── 本质：Selectable + bool 状态 + 选中图形切换
│   │   │   ├── 组件模型：Toggle + Text（Label）+ Image（Checkmark）
│   │   │   ├── 获取方式：GetComponent<Toggle>()
│   │   │   └── 状态链路：点击 → isOn 切换 → OnValueChanged 事件 → 图形更新
│   │   │
│   │   ├── 官方定位：二选一或多选控件
│   │   │   ├── 设计用途：选项开关、设置勾选、单选互斥组
│   │   │   └── ToggleGroup：同一组内只能选一个（互斥）
│   │   │
│   │   ├── 特点
│   │   │   ├── 优势：简单直观、支持 ToggleGroup、事件驱动、状态持久化方便
│   │   │   └── 局限：只能二选一、自定义样式复杂、ToggleGroup 需手动关联
│   │   │
│   │   ├── 适用场景
│   │   │   ├── ✅ 适用：音乐开关、音效开关、选项勾选、难度选择（单选）、设置面板
│   │   │   └── ❌ 不适用：多选项（用 Dropdown）、连续值调节（用 Slider）
│   │   │
│   │   ├── 核心属性及参数（Inspector 常用）
│   │   │   ├── Is On：当前是否选中
│   │   │   ├── Toggle Group：所属的 ToggleGroup（单选组）
│   │   │   ├── Transition：状态过渡方式
│   │   │   ├── Graphic：背景图形
│   │   │   ├── Checkmark：选中时显示的勾选图形
│   │   │   ├── Label：旁边的文字标签
│   │   │   └── On Value Changed：状态变化时的事件
│   │   │
│   │   ├── 核心 API
│   │   │   ├── isOn：获取/设置选中状态（最常用）
│   │   │   ├── group：设置所属的 ToggleGroup
│   │   │   └── onValueChanged：状态变化事件
│   │   │
│   │   └── 标准使用步骤
│   │       ├── 步骤1 创建 Toggle（右键 UI → Toggle）
│   │       ├── 步骤2 设置 Is On 默认值、Checkmark 和 Label
│   │       ├── 步骤3（可选）创建 ToggleGroup，把 Toggle 拖入 Group
│   │       ├── 步骤4 代码监听 onValueChanged 事件
│   │       └── 步骤5 运行测试选中/取消效果
│   │
│   ├── Slider（滑块控件 — 连续调节）
│   │   │
│   │   ├── 定义：在最小值和最大值之间连续取值的控件
│   │   │   ├── Min Value：最小值（默认 0）
│   │   │   ├── Max Value：最大值（默认 1）
│   │   │   ├── Value：当前值（0~1 之间）
│   │   │   └── Whole Numbers：是否只取整数
│   │   │
│   │   ├── 本质：Selectable + 拖动检测 + 值计算 + 事件触发
│   │   │
│   │   ├── 核心属性：minValue / maxValue / value / wholeNumbers
│   │   │
│   │   └── 适用：音量调节、亮度调节、灵敏度调节、进度显示
│   │
│   ├── Scrollbar（滚动条控件 — 滚动控制）
│   │   │
│   │   ├── 定义：控制 ScrollRect 滚动位置的控件
│   │   │   ├── Direction：滚动方向（LeftToRight / RightToLeft / BottomToTop / TopToBottom）
│   │   │   ├── Value：滚动位置（0~1）
│   │   │   ├── Size：滑块大小（内容占比）
│   │   │   └── Number Of Steps：步长数（0=连续）
│   │   │
│   │   ├── 本质：Selectable + 拖动 + ScrollRect 联动
│   │   │
│   │   ├── 核心属性：direction / value / size / numberOfSteps
│   │   │
│   │   └── 适用：配合 ScrollRect 使用，手动控制滚动
│   │
│   └── ScrollRect（滚动视图控件 — 可滚动容器）
│       │
│       ├── 定义：内容超过可视区域时可滚动的容器
│       │   ├── Content：要滚动的内容区域（子物体）
│       │   ├── Horizontal：是否允许水平滚动
│       │   ├── Vertical：是否允许垂直滚动
│       │   ├── Movement Type：滚动模式（Unrestricted / Elastic / Clamped）
│       │   └── Inertia：惯性滚动（松手后继续滑）
│       │
│       ├── 本质：裁剪 + 拖动检测 + 内容位置偏移
│       │
│       ├── 核心属性：content / horizontal / vertical / movementType / inertia
│       │
│       └── 适用：列表、背包、聊天记录、长文本、地图滚动
```

| 学习阶段 | 学习目标 |
|----------|----------|
| **零基础** | 说清四个控件各自是什么、区别；读懂 `toggle.isOn = true` |
| **入门** | 掌握四个控件常用属性、代码控制；完成 3 个交互案例 |
| **进阶** | 会 ToggleGroup 单选、ScrollRect 优化、自定义滚动行为 |

### 讲师知识框架速览（全文脉络）

| 维度 | 零基础讲 | 入门讲 | 进阶讲 |
|------|----------|--------|--------|
| 定义 | ✅ | 回顾 | 回顾 |
| 本质 | ✅ | — | — |
| 特点 | ✅ | — | 性能补充 |
| 适用场景 | ✅ | — | 选型（滚动方案） |
| 核心原理 | 控件用途 | ✅ 属性与 API | 滚动机制原理 |
| 核心 API | 读懂 isOn/value | ✅ 常用属性 | ScrollRect 联动 |
| 使用步骤 | Inspector 创建 | ✅ 代码控制 | 进阶案例 |
| 调用时机 | — | ✅ Start/Update | — |
| 避坑 | — | 初步 | ✅ |

---

# 第一阶段：零基础篇

## 【阶段总述】

零基础阶段建立**正确认知**：Toggle/Slider/Scrollbar/ScrollRect 各自是什么、分别用来做什么、有什么区别。  
同时学会**读懂** `toggle.isOn = true;` 和 `slider.value = 0.5f;`，并认识每个控件的 Inspector 核心参数。

---

## 一、四个控件定义对照

| 控件 | 一句话定义 | 核心作用 | 类比 |
|------|-----------|----------|------|
| **Toggle** | 开关控件，选中/未选中两种状态 | 二选一、复选、单选组 | 开关灯、选择题 |
| **Slider** | 滑块控件，连续取值 | 精细调节参数 | 音量旋钮、亮度调节 |
| **Scrollbar** | 滚动条控件，控制滚动位置 | 配合 ScrollRect 手动滚动 | 网页滚动条 |
| **ScrollRect** | 滚动视图控件，可滚动容器 | 显示超出屏幕的内容 | 手机屏幕滑动 |

---

## 二、本质 — 它们怎么工作？

```
Toggle 工作流程：
  点击 → isOn 取反 → Checkmark 显隐切换 → OnValueChanged 事件触发

Slider 工作流程：
  拖动滑块 → 计算当前值（基于位置比例）→ value 更新 → OnValueChanged 事件触发

ScrollRect 工作流程：
  拖动内容 → 检测拖动方向和距离 → Content 的 anchoredPosition 更新 → 裁剪显示可视区域
```

| 概念 | 说明 |
|------|------|
| **ToggleGroup** | 单选组，同一组内只能有一个 Toggle 被选中 |
| **ScrollRect.Content** | 要滚动的内容区域，必须是 ScrollRect 的子物体 |
| **Mask** | 配合 ScrollRect 使用，裁剪超出可视区域的内容 |

---

## 三、ScrollRect 的三种 Movement Type

| 模式 | 效果 | 适用 |
|------|------|------|
| **Unrestricted** | 可以无限滚动，内容可拖出边界 | 极少用 |
| **Elastic** | 拖出边界后回弹，有弹性效果 | 移动端滑动 |
| **Clamped** | 到边界就停，不允许拖出 | PC 端精确控制 |

---

## 四、核心一课：如何读懂一行代码

### 4.1 Toggle — 设置选中状态

```csharp
toggle.isOn = true;
```

| 部分 | 含义 |
|------|------|
| `toggle` | Toggle 组件引用（变量名） |
| `.isOn` | 属性名：是否选中（true=选中，false=未选中） |
| `true` | 赋值：设置为选中状态 |

**整行人话**：把开关设为打开状态（勾选上）。

### 4.2 Slider — 设置当前值

```csharp
slider.value = 0.75f;
```

| 部分 | 含义 |
|------|------|
| `slider` | Slider 组件引用（变量名） |
| `.value` | 属性名：当前值（范围：minValue ~ maxValue） |
| `0.75f` | 赋值：设为 75% 的位置 |

**整行人话**：把滑块拖到 75% 的位置（默认 0~1 范围）。

---

## 【零基础阶段小结】

| 维度 | 要点 |
|------|------|
| **Toggle** | 开关，用 `isOn` 控制选中状态，支持 ToggleGroup |
| **Slider** | 滑块，用 `value` 控制当前值，范围 minValue~maxValue |
| **Scrollbar** | 滚动条，用 `value` 控制滚动位置，配合 ScrollRect |
| **ScrollRect** | 滚动视图，用 `content.anchoredPosition` 控制滚动 |
| **区别** | Toggle 是二选一，Slider 是连续值，ScrollRect 是容器 |

**阶段检验**：能说出四个控件各自的用途；能解释 ScrollRect 和 Scrollbar 的关系。

---

# 第二阶段：入门篇

## 【阶段总述】

入门阶段掌握 **Toggle/Slider/Scrollbar/ScrollRect** 的常用属性和代码控制方式，学会绑定事件和实现常用交互功能。  
重点：**Toggle 的状态切换、Slider 的值变化事件、ScrollRect 的滚动内容设置**。

---

## 一、核心属性及参数详解（逐词读懂）

### 1.1 Toggle 常用属性

```csharp
Toggle toggle = GetComponent<Toggle>();
toggle.isOn = true;                                          // 是否选中
toggle.group = toggleGroup;                                  // 设置所属的 ToggleGroup
toggle.isOn = !toggle.isOn;                                  // 切换状态
toggle.onValueChanged.AddListener(OnToggleChanged);          // 状态变化事件
```

| 属性 | 类型 | 含义 |
|------|------|------|
| `isOn` | bool | 是否选中（true=选中） |
| `group` | ToggleGroup | 所属的单选组（为空则独立） |
| `onValueChanged` | UnityEvent\<bool\> | 状态变化时的事件（参数为新状态） |

### 1.2 Slider 常用属性

```csharp
Slider slider = GetComponent<Slider>();
slider.minValue = 0f;                                        // 最小值
slider.maxValue = 100f;                                      // 最大值
slider.value = 50f;                                          // 当前值
slider.wholeNumbers = true;                                  // 是否只取整数
slider.onValueChanged.AddListener(OnSliderChanged);          // 值变化事件
```

| 属性 | 类型 | 含义 |
|------|------|------|
| `minValue` | float | 最小值（默认 0） |
| `maxValue` | float | 最大值（默认 1） |
| `value` | float | 当前值（范围：minValue~maxValue） |
| `wholeNumbers` | bool | 是否只取整数（false=连续） |
| `onValueChanged` | UnityEvent\<float\> | 值变化时的事件（参数为新值） |

### 1.3 ScrollRect 常用属性

```csharp
ScrollRect scrollRect = GetComponent<ScrollRect>();
scrollRect.content = contentRectTransform;                    // 要滚动的内容
scrollRect.horizontal = false;                                // 是否允许水平滚动
scrollRect.vertical = true;                                   // 是否允许垂直滚动
scrollRect.movementType = ScrollRect.MovementType.Elastic;     // 滚动模式
scrollRect.inertia = true;                                    // 是否有惯性
scrollRect.velocity = Vector2.zero;                           // 当前滚动速度
```

| 属性 | 类型 | 含义 |
|------|------|------|
| `content` | RectTransform | 要滚动的内容区域 |
| `horizontal` | bool | 是否允许水平滚动 |
| `vertical` | bool | 是否允许垂直滚动 |
| `movementType` | ScrollRect.MovementType | 滚动模式（Unrestricted/Elastic/Clamped） |
| `inertia` | bool | 惯性滚动（松手后继续滑动） |
| `velocity` | Vector2 | 当前滚动速度（只读） |

### 1.4 Scrollbar 常用属性

```csharp
Scrollbar scrollbar = GetComponent<Scrollbar>();
scrollbar.direction = Scrollbar.Direction.BottomToTop;        // 滚动方向
scrollbar.value = 0.5f;                                      // 滚动位置（0~1）
scrollbar.size = 0.3f;                                       // 滑块大小（内容占比）
scrollbar.numberOfSteps = 0;                                  // 步长（0=连续）
```

| 属性 | 类型 | 含义 |
|------|------|------|
| `direction` | Scrollbar.Direction | 滚动方向 |
| `value` | float | 滚动位置（0~1） |
| `size` | float | 滑块大小（0~1，代表内容占可视区域的比例） |
| `numberOfSteps` | int | 步长数（0=连续，>0=按步长跳） |

---

## 二、标准使用步骤

### 2.1 Toggle 使用步骤

```
步骤1  创建 Toggle（右键 UI → Toggle）
步骤2  设置 Is On 默认值、Checkmark Sprite
步骤3 （单选组）创建 ToggleGroup，把多个 Toggle 的 Group 拖入同一个 ToggleGroup
步骤4  代码监听 onValueChanged 事件
步骤5  运行测试选中/取消效果
```

### 2.2 ScrollRect 使用步骤

```
步骤1  创建 ScrollRect（右键 UI → Scroll Rect）
步骤2  设置 Viewport（可视区域）和 Content（内容区域）
步骤3  给 Viewport 添加 Mask 组件（裁剪超出部分）
步骤4  在 Content 下添加要显示的内容
步骤5  （可选）添加 Scrollbar，绑定到 ScrollRect
步骤6  运行测试滚动效果
```

---

## 三、入门三个案例

### 案例代码讲解模板

每个案例统一按以下结构组织（下文所有案例均遵循此模板）：

| 顺序 | 板块 | 内容 |
|:----:|------|------|
| 1 | **功能** | 案例实现什么业务 |
| 2 | **完整代码** | 带行内注释的完整脚本 |
| 3 | **语法拆解** | 对案例中较生僻的语法，逐个说明 |
| 4 | **逐行详解** | 表格：每行代码的含义 |
| 5 | **操作提示** | Unity 绑定、调用方式等 |

**语法拆解的标准格式**（遇到 `ToggleGroup`、`ScrollRect`、`UnityEvent<bool>` 等不熟悉的写法时使用）：

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

### 案例 1：设置面板 — ToggleGroup 单选难度

**功能**：三个 Toggle 组成单选组，选择游戏难度（简单/普通/困难），选择后保存到 PlayerPrefs。

```csharp
using UnityEngine;
using UnityEngine.UI;

public class DifficultySettings : MonoBehaviour
{
    [SerializeField] private Toggle _easyToggle;        // 简单难度
    [SerializeField] private Toggle _normalToggle;      // 普通难度
    [SerializeField] private Toggle _hardToggle;        // 困难难度
    [SerializeField] private Text _descriptionText;     // 难度描述
    
    private const string DIFFICULTY_KEY = "GameDifficulty";

    void Start()
    {
        LoadDifficulty();
        
        _easyToggle.onValueChanged.AddListener(OnDifficultyChanged);
        _normalToggle.onValueChanged.AddListener(OnDifficultyChanged);
        _hardToggle.onValueChanged.AddListener(OnDifficultyChanged);
    }

    void LoadDifficulty()
    {
        int saved = PlayerPrefs.GetInt(DIFFICULTY_KEY, 1);
        
        switch (saved)
        {
            case 0: _easyToggle.isOn = true; break;
            case 1: _normalToggle.isOn = true; break;
            case 2: _hardToggle.isOn = true; break;
        }
        
        UpdateDescription(saved);
    }

    void OnDifficultyChanged(bool isOn)
    {
        if (!isOn) return;
        
        int difficulty = 0;
        if (_easyToggle.isOn) difficulty = 0;
        else if (_normalToggle.isOn) difficulty = 1;
        else if (_hardToggle.isOn) difficulty = 2;
        
        PlayerPrefs.SetInt(DIFFICULTY_KEY, difficulty);
        PlayerPrefs.Save();
        
        UpdateDescription(difficulty);
    }

    void UpdateDescription(int difficulty)
    {
        switch (difficulty)
        {
            case 0: _descriptionText.text = "简单：敌人伤害降低 50%，血量翻倍"; break;
            case 1: _descriptionText.text = "普通：标准难度，适合大多数玩家"; break;
            case 2: _descriptionText.text = "困难：敌人伤害翻倍，血量降低 30%"; break;
        }
    }
}
```

#### 语法拆解

##### `toggle.onValueChanged.AddListener(OnDifficultyChanged)` 是什么？

```csharp
_easyToggle.onValueChanged.AddListener(OnDifficultyChanged);
```

| 部分 | 含义 |
|------|------|
| `onValueChanged` | Toggle 状态变化事件（UnityEvent\<bool\>） |
| `AddListener` | 添加回调方法 |
| `OnDifficultyChanged` | 回调方法（参数 bool：新的 isOn 状态） |

**整行人话**：告诉 Toggle「状态变化时执行 OnDifficultyChanged 方法」。

---

##### `if (!isOn) return;` 是什么？

```csharp
void OnDifficultyChanged(bool isOn)
{
    if (!isOn) return;
    // ...
}
```

| 部分 | 含义 |
|------|------|
| `isOn` | 参数：新的选中状态 |
| `!isOn` | 逻辑非：false 的时候 |
| `return` | 直接返回，不执行后面的代码 |

**整行人话**：只有选中时才处理，取消选中时什么都不做（因为 ToggleGroup 会自动取消其他 Toggle）。

---

#### 逐行详解

| 行 | 代码 | 含义 |
|----|------|------|
| 5~8 | Toggle 和 Text 引用 | Inspector 拖入 |
| 10 | `DIFFICULTY_KEY` | PlayerPrefs 存档 Key |
| 12 | `Start()` | 初始化加载存档并绑定事件 |
| 14 | `LoadDifficulty()` | 读取上次保存的难度 |
| 16~18 | 三个 Toggle 绑定同一回调 | — |
| 21 | `LoadDifficulty()` | 根据存档设置选中状态 |
| 23~30 | switch 根据存档值设置 Toggle | — |
| 32 | `UpdateDescription()` | 更新描述文字 |
| 35 | `OnDifficultyChanged(bool isOn)` | 难度变化回调 |
| 37 | `if (!isOn) return` | 只有选中才处理 |
| 39~44 | 判断哪个 Toggle 被选中 | — |
| 46~47 | 保存到 PlayerPrefs | — |
| 49 | 更新描述 | — |
| 52 | `UpdateDescription()` | 根据难度显示描述 |

#### 操作提示

1. Canvas 下创建三个 Toggle：Easy、Normal、Hard  
2. 创建一个 ToggleGroup（右键 UI → Toggle Group）  
3. 把三个 Toggle 的 **Toggle Group** 属性都拖入同一个 ToggleGroup  
4. 创建 Text 显示描述  
5. 脚本挂到任意 GameObject，拖入引用  
6. Play 测试：选一个难度，重启后仍保持选中

---

### 案例 2：音量滑块 — Slider 实时调节音量

**功能**：Slider 控件调节背景音乐音量，实时生效，且保存到 PlayerPrefs。

```csharp
using UnityEngine;
using UnityEngine.UI;

public class VolumeSlider : MonoBehaviour
{
    [SerializeField] private Slider _volumeSlider;      // 音量滑块
    [SerializeField] private Text _volumeText;         // 音量百分比文字
    
    private const string VOLUME_KEY = "MasterVolume";
    private AudioSource _audioSource;

    void Start()
    {
        _audioSource = FindObjectOfType<AudioSource>();
        
        float savedVolume = PlayerPrefs.GetFloat(VOLUME_KEY, 1f);
        _volumeSlider.value = savedVolume;
        
        _volumeSlider.onValueChanged.AddListener(OnVolumeChanged);
        
        OnVolumeChanged(savedVolume);
    }

    void OnVolumeChanged(float volume)
    {
        if (_audioSource != null)
        {
            _audioSource.volume = volume;
        }
        
        int percent = Mathf.RoundToInt(volume * 100);
        _volumeText.text = $"{percent}%";
        
        PlayerPrefs.SetFloat(VOLUME_KEY, volume);
        PlayerPrefs.Save();
    }
}
```

#### 语法拆解

##### `slider.onValueChanged.AddListener(OnVolumeChanged)` 是什么？

```csharp
_volumeSlider.onValueChanged.AddListener(OnVolumeChanged);
```

| 部分 | 含义 |
|------|------|
| `onValueChanged` | Slider 值变化事件（UnityEvent\<float\>） |
| `AddListener` | 添加回调方法 |
| `OnVolumeChanged` | 回调方法（参数 float：新的值） |

**整行人话**：滑块拖动时，实时调用 OnVolumeChanged 方法更新音量。

---

##### `Mathf.RoundToInt(volume * 100)` 是什么？

```csharp
int percent = Mathf.RoundToInt(volume * 100);
```

| 部分 | 含义 |
|------|------|
| `Mathf.RoundToInt` | 四舍五入取整 |
| `volume * 100` | 把 0~1 的值转成 0~100 的百分比 |

**整行人话**：把音量值（0~1）转成百分比（0~100）并四舍五入。

---

#### 逐行详解

| 行 | 代码 | 含义 |
|----|------|------|
| 5~6 | Slider 和 Text 引用 | Inspector 拖入 |
| 8 | `VOLUME_KEY` | PlayerPrefs 存档 Key |
| 9 | `_audioSource` | 音频源引用 |
| 11 | `Start()` | 初始化 |
| 13 | `FindObjectOfType<AudioSource>()` | 找场景中的音频源 |
| 15~16 | 读取存档并设置滑块值 | — |
| 18 | 绑定滑块值变化事件 | — |
| 20 | 初始化时调用一次（设置初始音量） | — |
| 23 | `OnVolumeChanged(float volume)` | 音量变化回调 |
| 25~28 | 设置 AudioSource 音量 | — |
| 30 | 计算百分比 | — |
| 31 | 显示百分比文字 | — |
| 33~34 | 保存到 PlayerPrefs | — |

#### 操作提示

1. Canvas 下创建 Slider 和 Text  
2. 设置 Slider 的 minValue=0，maxValue=1  
3. 场景中添加 AudioSource 并拖入背景音乐  
4. 脚本挂到任意 GameObject，拖入引用  
5. Play 拖动滑块，音量实时变化

---

### 案例 3：滚动列表 — ScrollRect 动态生成列表项

**功能**：用代码动态生成列表项，放入 ScrollRect 中，支持垂直滚动查看。

```csharp
using UnityEngine;
using UnityEngine.UI;

public class ScrollList : MonoBehaviour
{
    [SerializeField] private ScrollRect _scrollRect;    // 滚动视图
    [SerializeField] private RectTransform _content;    // 内容区域
    [SerializeField] private Text _itemPrefab;          // 列表项预制体（Text）
    [SerializeField] private int _itemCount = 50;      // 列表项数量

    void Start()
    {
        GenerateItems();
    }

    void GenerateItems()
    {
        for (int i = 0; i < _itemCount; i++)
        {
            Text item = Instantiate(_itemPrefab, _content);
            item.text = $"列表项 {i + 1}";
            item.name = $"Item_{i + 1}";
        }
        
        LayoutRebuilder.ForceRebuildLayoutImmediate(_content);
    }

    public void ScrollToTop()
    {
        _scrollRect.verticalNormalizedPosition = 1f;
    }

    public void ScrollToBottom()
    {
        _scrollRect.verticalNormalizedPosition = 0f;
    }

    public void ScrollToItem(int index)
    {
        float normalizedPos = 1f - (float)index / (_itemCount - 1);
        _scrollRect.verticalNormalizedPosition = normalizedPos;
    }
}
```

#### 语法拆解

##### `LayoutRebuilder.ForceRebuildLayoutImmediate(content)` 是什么？

```csharp
LayoutRebuilder.ForceRebuildLayoutImmediate(_content);
```

| 部分 | 含义 |
|------|------|
| `LayoutRebuilder` | Unity UI 布局重建器 |
| `ForceRebuildLayoutImmediate` | 立即强制重建布局 |
| `_content` | 内容区域的 RectTransform |

**整行人话**：动态添加子物体后，强制重新计算布局，让 Content 高度正确。

---

##### `_scrollRect.verticalNormalizedPosition = 1f` 是什么？

```csharp
_scrollRect.verticalNormalizedPosition = 1f;
```

| 部分 | 含义 |
|------|------|
| `verticalNormalizedPosition` | 垂直滚动的归一化位置（0=底部，1=顶部） |
| `1f` | 滚动到顶部 |
| `0f` | 滚动到底部 |

**整行人话**：把滚动视图滚到最顶部（0=最底部）。

---

#### 逐行详解

| 行 | 代码 | 含义 |
|----|------|------|
| 5~8 | ScrollRect、Content、预制体引用 | Inspector 拖入 |
| 10 | `Start()` | 初始化生成列表 |
| 12 | `GenerateItems()` | 生成列表项 |
| 14 | for 循环生成 itemCount 个项 | — |
| 16 | Instantiate 创建列表项 | — |
| 17~18 | 设置文字和名字 | — |
| 21 | 强制重建布局 | — |
| 24 | `ScrollToTop()` | 滚动到顶部 |
| 26 | `verticalNormalizedPosition = 1f` | 顶部位置 |
| 29 | `ScrollToBottom()` | 滚动到底部 |
| 31 | `verticalNormalizedPosition = 0f` | 底部位置 |
| 34 | `ScrollToItem(int index)` | 滚动到指定项 |
| 36 | 计算归一化位置 | — |
| 37 | 设置滚动位置 | — |

#### 操作提示

1. Canvas 下创建 Scroll Rect（右键 UI → Scroll Rect）  
2. 创建一个 Text 预制体（Canvas → UI → Text，拖到 Project 面板）  
3. 确保 ScrollRect 的 Viewport 有 Mask 组件  
4. 把 Content 的锚点设为顶部（anchorMin=anchorMax=(0,1)）  
5. 给 Content 添加 Vertical Layout Group 和 Content Size Fitter  
6. 脚本挂到任意 GameObject，拖入引用  
7. Play 测试滚动效果

---

## 【入门阶段小结】

| 维度 | 要点 |
|------|------|
| **Toggle** | `isOn` 控制状态，`onValueChanged` 事件，ToggleGroup 单选 |
| **Slider** | `value` 控制值，`onValueChanged` 事件，minValue/maxValue 范围 |
| **ScrollRect** | `content` 设置内容，`verticalNormalizedPosition` 控制滚动位置 |
| **案例** | 设置面板单选、音量调节、动态列表 |

---

# 第三阶段：进阶篇

## 【阶段总述】

进阶阶段：**ToggleGroup 深入**、**ScrollRect 性能优化**、**自定义滚动行为**、**分页滚动**、**常见踩坑清单**。

---

## 一、ToggleGroup 深入

### 1.1 ToggleGroup 的属性

```csharp
ToggleGroup toggleGroup = GetComponent<ToggleGroup>();
toggleGroup.allowSwitchOff = true;                         // 是否允许全部取消选中
```

| 属性 | 说明 |
|------|------|
| `allowSwitchOff` | true=允许点击已选中的 Toggle 取消选中；false=至少选中一个 |

### 1.2 代码获取选中的 Toggle

```csharp
Toggle selected = toggleGroup.ActiveToggles().FirstOrDefault();
if (selected != null)
{
    Debug.Log("选中的是：" + selected.name);
}
```

---

## 二、ScrollRect 性能优化

### 2.1 对象池 — 复用列表项

```csharp
public class ListPool : MonoBehaviour
{
    public Text itemPrefab;
    private Queue<Text> _pool = new Queue<Text>();
    
    public Text GetFromPool()
    {
        if (_pool.Count > 0)
        {
            Text item = _pool.Dequeue();
            item.gameObject.SetActive(true);
            return item;
        }
        return Instantiate(itemPrefab);
    }
    
    public void ReturnToPool(Text item)
    {
        item.gameObject.SetActive(false);
        _pool.Enqueue(item);
    }
}
```

### 2.2 虚拟滚动 — 只渲染可见项

当列表项很多（几百几千个）时，不需要全部渲染，只渲染可见的几个：

| 步骤 | 说明 |
|------|------|
| 1 | 计算可见区域能容纳多少个列表项 |
| 2 | 只创建可见数量 + 2（预加载）个列表项 |
| 3 | 滚动时，把离开屏幕的列表项移到另一侧并更新内容 |
| 4 | 更新 Content 的大小让滚动条正常工作 |

---

## 三、自定义滚动行为

### 3.1 禁止惯性滚动

```csharp
scrollRect.inertia = false;
```

### 3.2 滚动到指定位置（带动画）

```csharp
using UnityEngine.UI;
using DG.Tweening;

public void ScrollToPosition(float targetPos)
{
    DOTween.To(() => scrollRect.verticalNormalizedPosition, 
               x => scrollRect.verticalNormalizedPosition = x, 
               targetPos, 0.3f);
}
```

### 3.3 监听滚动位置

```csharp
scrollRect.onValueChanged.AddListener(OnScrollChanged);

void OnScrollChanged(Vector2 pos)
{
    Debug.Log("滚动位置：" + pos);
}
```

---

## 四、常见误区与最佳实践

| 误区 | 正确做法 |
|------|----------|
| ToggleGroup 不起作用 | 确认所有 Toggle 的 Group 属性都拖入了同一个 ToggleGroup |
| ScrollRect 不能滚动 | 确认 Content 高度大于 Viewport 高度；确认 Content 是 ScrollRect 的子物体 |
| ScrollRect 没有遮罩 | 给 Viewport 添加 Mask 组件 |
| 列表项很多卡顿 | 使用对象池或虚拟滚动 |
| Slider 值范围不对 | 检查 minValue 和 maxValue 设置 |
| Toggle 点击没反应 | 检查 EventSystem、GraphicRaycaster 是否存在 |
| ScrollRect 滚动边界错误 | 检查 Content 的锚点设置；添加 ContentSizeFitter |
| 动态添加列表项后不滚动 | 添加后调用 `LayoutRebuilder.ForceRebuildLayoutImmediate` |

---

## 【进阶阶段小结】

| 维度 | 要点 |
|------|------|
| ToggleGroup | allowSwitchOff、ActiveToggles() 获取选中 |
| ScrollRect 性能 | 对象池、虚拟滚动、减少可见项 |
| 自定义行为 | 禁止惯性、动画滚动、位置监听 |
| 避坑 | ToggleGroup 关联、Content 高度、Mask 遮罩 |

---

# 【全文总结】

## 最重要的一行代码

```csharp
scrollRect.verticalNormalizedPosition = 0f;
```

| 部分 | 含义 |
|------|------|
| `scrollRect` | 滚动视图组件引用 |
| `verticalNormalizedPosition` | 垂直滚动的归一化位置 |
| `0f` | 滚动到底部（1f=顶部） |

## 三阶段对照

| 阶段 | 代表案例 |
|------|----------|
| 零基础 | 认识四个控件、读懂基本代码 |
| 入门 | 设置面板单选、音量滑块、动态列表 |
| 进阶 | ToggleGroup、ScrollRect 优化、自定义滚动 |

## API 速查

| 控件 | 常用代码 |
|------|----------|
| Toggle | `toggle.isOn = true` / `toggle.onValueChanged.AddListener` |
| Slider | `slider.value = 0.5f` / `slider.onValueChanged.AddListener` |
| ScrollRect | `scrollRect.content = rect` / `scrollRect.verticalNormalizedPosition = 1f` |
| Scrollbar | `scrollbar.value = 0.5f` / `scrollbar.size = 0.3f` |

## 学习自检

- [ ] Toggle/Slider/Scrollbar/ScrollRect 各自的用途？
- [ ] ToggleGroup 是什么？怎么实现单选？
- [ ] ScrollRect 的 Content 和 Viewport 是什么关系？
- [ ] Slider 的 onValueChanged 事件参数是什么类型？
- [ ] 为什么动态添加列表项后需要调用 LayoutRebuilder？
- [ ] 列表项很多时怎么优化性能？

---

## 参考资料

| 类型 | 链接 |
|------|------|
| Toggle 官方 Manual | https://docs.unity3d.com/Manual/script-Toggle.html |
| Slider 官方 Manual | https://docs.unity3d.com/Manual/script-Slider.html |
| Scrollbar 官方 Manual | https://docs.unity3d.com/Manual/script-Scrollbar.html |
| ScrollRect 官方 Manual | https://docs.unity3d.com/Manual/script-ScrollRect.html |
| ToggleGroup API | https://docs.unity3d.com/ScriptReference/UI.ToggleGroup.html |
| LayoutRebuilder | https://docs.unity3d.com/ScriptReference/UI.LayoutRebuilder.html |

---

*文档版本：与 major3/01_PlayerPrefs.md ~ 05_DoTween.md、Week2_Xmind、Week3_Xmind 同系列模板。*