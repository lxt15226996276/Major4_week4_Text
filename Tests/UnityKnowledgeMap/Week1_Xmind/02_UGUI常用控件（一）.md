# Unity UGUI 常用控件（一）详解

> 参照：[Unity 官方 Manual - UI Text](https://docs.unity3d.com/Manual/script-Text.html) · [UI Image](https://docs.unity3d.com/Manual/script-Image.html) · [UI Button](https://docs.unity3d.com/Manual/script-Button.html) · [RawImage](https://docs.unity3d.com/Manual/script-RawImage.html)  
> 关联文档：[01_画布和基础布局.md](./01_画布和基础布局.md)（Canvas、RectTransform）· [03_UGUI常用控件（二）.md](./03_UGUI常用控件（二）.md)（Toggle/Slider/ScrollRect）· [04_UGUI常用控件（三）.md](./04_UGUI常用控件（三）.md)（InputField/Dropdown/事件接口）  
> 学习路径：**零基础 → 入门 → 进阶**，每阶段采用 **总—分—总** 结构。  
> 讲解维度：**定义 → 本质 → 特点 → 适用场景 → 原理 → API → 步骤 → 案例 → 避坑**（进阶含 Button 事件系统 / 图文混排 / 性能优化）。  
> 案例讲解：遵循 **案例代码讲解模板**（功能 → 代码 → 语法拆解 → 逐行详解 → 操作提示）。  
> API 讲解：入门/进阶 API 章节均采用 **逐词读懂** 格式（与 [../major3/01_PlayerPrefs.md](../major3/01_PlayerPrefs.md) 一致：类型 → 参数 → 整行人话）。

---

## 【全文总述】

**Text（文本）** 是 UGUI 最基础的控件：显示文字、设置字体大小、颜色、对齐方式。  
**Image（图片）** 是 UGUI 的「图片框」：显示 Sprite 图片，支持颜色叠加、填充模式、九宫格拉伸。  
**RawImage（原始图片）** 是 UGUI 的「纹理框」：显示 Texture2D，不经过 Sprite 裁剪，适合动态纹理（摄像头画面、RenderTexture）。  
**Button（按钮）** 是 UGUI 的「交互入口」：点击触发事件，自带按下/悬停/禁用状态切换，是游戏中最常用的交互控件。  
本文从最基础的文字和图片显示，到按钮交互，逐层展开。

### 思维导图总览

```
Unity UGUI 常用控件（一）
│
├── Text（文本控件 — 显示文字）
│   │
│   ├── 【知识维度】（讲师框架 — 完整版）
│   │   │
│   │   ├── 定义：UGUI 文本显示控件，用于展示文字信息
│   │   │   └── 官方描述：The Text component displays a non-editable piece of text to the user
│   │   │       创建方式：右键 UI → Text
│   │   │
│   │   ├── 本质：字体渲染器 + 文本布局引擎，把文字变成可显示的网格
│   │   │   ├── 组件模型：Text 组件 + Font（字体）+ Material（材质）
│   │   │   ├── 获取方式：GetComponent<Text>()
│   │   │   └── 渲染链路：字符串 → 字符网格 → Canvas 渲染管线
│   │   │
│   │   ├── 官方定位：显示静态/动态文本信息的标准控件
│   │   │   ├── 设计用途：标题、描述、数值显示、状态提示
│   │   │   └── 支持富文本：<color>、<size>、<b>、<i> 等标签
│   │   │
│   │   ├── 特点
│   │   │   ├── 优势：支持富文本、自动换行、多种对齐方式、字体资源丰富
│   │   │   └── 局限：长文本性能差、中文需要中文字体、换行逻辑简单
│   │   │
│   │   ├── 适用场景
│   │   │   ├── ✅ 适用：游戏标题、UI 描述、数值显示、状态提示、对话文本
│   │   │   └── ❌ 不适用：大量滚动文本（用 TextMeshPro）、需要编辑的文本（用 InputField）
│   │   │
│   │   ├── 核心属性及参数（Inspector 常用）
│   │   │   ├── Text：要显示的字符串内容
│   │   │   ├── Font：字体资源（系统字体或自定义字体）
│   │   │   ├── Font Size：字体大小（像素）
│   │   │   ├── Color：文字颜色
│   │   │   ├── Alignment：对齐方式（左/中/右，上/中/下）
│   │   │   ├── Horizontal/Vertical Overflow：水平/垂直溢出处理
│   │   │   └── Rich Text：是否启用富文本标签
│   │   │
│   │   ├── 核心 API
│   │   │   ├── text：设置/获取文本内容（最常用）
│   │   │   ├── fontSize：设置字体大小
│   │   │   ├── color：设置文字颜色
│   │   │   ├── alignment：设置对齐方式
│   │   │   └── supportRichText：是否支持富文本
│   │   │
│   │   └── 标准使用步骤
│   │       ├── 步骤1 在 Canvas 下创建 Text
│   │       ├── 步骤2 Inspector 设置 Font、Font Size、Color
│   │       ├── 步骤3 设置 Alignment 和 Overflow
│   │       └── 步骤4 代码修改 text 属性更新内容
│   │
│   └── 第一阶段：零基础（认识控件 + 读懂代码）
│       ├── 理解 Text/Image/RawImage/Button 各自是什么
│       ├── 逐词读懂：text.text = "Hello";
│       └── 认识 Inspector 核心参数
│
├── Image（图片控件 — 显示 Sprite）
│   │
│   ├── 定义：显示 Sprite 类型图片的控件
│   │   ├── Sprite：2D 精灵图片（需先导入为 Sprite 类型）
│   │   ├── Color：颜色叠加（白色不影响，其他颜色会叠加）
│   │   └── Image Type：图片类型（Simple / Sliced / Tiled / Filled）
│   ├── 本质：Sprite 渲染器，把纹理贴到矩形网格上
│   ├── 核心属性：sprite / color / imageType / preserveAspect
│   └── 适用：按钮背景、图标、血条、装饰图片
│
├── RawImage（原始图片控件 — 显示 Texture）
│   │
│   ├── 定义：显示 Texture2D 类型图片的控件，不经过 Sprite 处理
│   ├── 本质：直接渲染纹理，适合动态生成的图片
│   ├── 核心属性：texture / color / uvRect
│   └── 适用：摄像头画面、RenderTexture、动态生成的纹理
│
└── Button（按钮控件 — 交互入口）
    │
    ├── 定义：可点击的交互控件，点击时触发事件
    │   ├── Interactable：是否可交互（禁用时变灰）
    │   ├── Transition：状态过渡方式（Color Tint / Sprite Swap / Animation）
    │   └── On Click：点击事件回调列表
    ├── 本质：选择器（Selectable）+ 点击检测 + 事件触发
    ├── 核心属性：interactable / transition / onClick
    └── 适用：菜单按钮、功能按钮、确认/取消按钮
```

| 学习阶段 | 学习目标 |
|----------|----------|
| **零基础** | 说清四个控件各自是什么、区别；读懂 `text.text = "内容"` |
| **入门** | 掌握四个控件常用属性、代码控制；完成 3 个交互案例 |
| **进阶** | 会按钮事件绑定、图文混排、性能优化；理解 Selectable 体系 |

### 讲师知识框架速览（全文脉络）

| 维度 | 零基础讲 | 入门讲 | 进阶讲 |
|------|----------|--------|--------|
| 定义 | ✅ | 回顾 | 回顾 |
| 本质 | ✅ | — | — |
| 特点 | ✅ | — | 性能补充 |
| 适用场景 | ✅ | — | 选型（Text vs TextMeshPro） |
| 核心原理 | 控件用途 | ✅ 属性与 API | 事件系统原理 |
| 核心 API | 读懂 text.text | ✅ 常用属性 | 事件绑定 + Selectable |
| 使用步骤 | Inspector 创建 | ✅ 代码控制 | 进阶案例 |
| 调用时机 | — | ✅ Start/Update | — |
| 避坑 | — | 初步 | ✅ |

---

# 第一阶段：零基础篇

## 【阶段总述】

零基础阶段建立**正确认知**：Text/Image/RawImage/Button 各自是什么、分别用来做什么、有什么区别。  
同时学会**读懂** `text.text = "Hello";` 和 `button.onClick.AddListener(...)`，并认识每个控件的 Inspector 核心参数。

---

## 一、四个控件定义对照

| 控件 | 一句话定义 | 核心作用 | 类比 |
|------|-----------|----------|------|
| **Text** | 显示文字的控件 | 展示文本信息 | 广告牌上的字 |
| **Image** | 显示 Sprite 的控件 | 展示图片 | 相框里的照片 |
| **RawImage** | 显示 Texture 的控件 | 展示原始纹理 | 显示器屏幕 |
| **Button** | 可点击的交互控件 | 触发事件 | 门铃按钮 |

---

## 二、本质 — 它们怎么工作？

```
Text 工作流程：
  字符串 "Hello" → Font 字体文件 → 字符网格 → Canvas 渲染 → 屏幕显示

Image 工作流程：
  Sprite 图片 → 裁剪/拉伸 → 颜色叠加 → Canvas 渲染 → 屏幕显示

Button 工作流程：
  鼠标点击 → GraphicRaycaster 检测 → Selectable 状态切换 → OnClick 事件触发 → 执行回调
```

| 概念 | 说明 |
|------|------|
| **GraphicRaycaster** | UI 射线检测组件，判断点击是否命中控件 |
| **Selectable** | Button/Toggle/Slider 等交互控件的基类，处理选中/悬停/按下状态 |
| **EventSystem** | 输入事件管理器，分发点击、拖拽、按键等事件 |

---

## 三、Image vs RawImage — 什么时候用哪个？

| 对比 | Image | RawImage |
|------|-------|----------|
| **图片类型** | Sprite（需导入设置为 Sprite） | Texture2D（直接用纹理） |
| **裁剪功能** | 支持 Sprite 裁剪（九宫格、填充） | 不裁剪，直接显示 |
| **UV 控制** | 不支持自定义 UV | 支持 uvRect 控制显示区域 |
| **性能** | Sprite 批处理优化好 | 直接渲染，无额外处理 |
| **适用** | 按钮背景、图标、UI 元素 | 摄像头画面、RenderTexture、动态纹理 |

> **小白必记**：普通 UI 图片用 **Image** + Sprite；动态生成的图片（如截图、摄像头）用 **RawImage**。

---

## 四、Button 的三种 Transition — 状态怎么变？

| Transition | 效果 | 适用 |
|------------|------|------|
| **Color Tint** | 不同状态显示不同颜色 | 简单按钮、快速原型 |
| **Sprite Swap** | 不同状态切换不同 Sprite | 需要精细状态图标的按钮 |
| **Animation** | 不同状态播放不同动画 | 复杂交互、特效按钮 |

---

## 五、核心一课：如何读懂一行代码

### 5.1 Text — 修改文字内容

```csharp
text.text = "你好，世界！";
```

| 部分 | 含义 |
|------|------|
| `text` | Text 组件引用（变量名） |
| `.text` | 属性名：要显示的字符串内容 |
| `"你好，世界！"` | 赋值：要显示的文字 |

**整行人话**：把文本控件的显示内容改成「你好，世界！」。

### 5.2 Button — 添加点击事件

```csharp
button.onClick.AddListener(OnButtonClicked);
```

| 部分 | 含义 |
|------|------|
| `button` | Button 组件引用（变量名） |
| `.onClick` | 属性名：点击事件列表 |
| `.AddListener` | 方法名：往事件列表里加一个回调方法 |
| `OnButtonClicked` | 要执行的方法名（无参数的 void 方法） |

**整行人话**：告诉按钮「点击时执行 OnButtonClicked 方法」。

---

## 【零基础阶段小结】

| 维度 | 要点 |
|------|------|
| **Text** | 显示文字，用 `text.text` 修改内容 |
| **Image** | 显示 Sprite，用 `image.sprite` 修改图片 |
| **RawImage** | 显示 Texture，用 `rawImage.texture` 修改纹理 |
| **Button** | 点击触发事件，用 `onClick.AddListener` 绑定回调 |
| **区别** | Image 用 Sprite（可裁剪），RawImage 用 Texture（不裁剪） |

**阶段检验**：能说出四个控件各自的用途；能解释 Image 和 RawImage 的区别。

---

# 第二阶段：入门篇

## 【阶段总述】

入门阶段掌握 **Text/Image/RawImage/Button** 的常用属性和代码控制方式，学会动态更新 UI 内容和绑定按钮事件。  
重点：**Text 的富文本标签、Image 的九宫格拉伸、Button 的事件绑定**。

---

## 一、核心属性及参数详解（逐词读懂）

### 1.1 Text 常用属性

```csharp
Text text = GetComponent<Text>();
text.text = "普通文本";                                    // 显示内容
text.font = Resources.GetBuiltinResource<Font>("Arial.ttf"); // 字体
text.fontSize = 24;                                       // 字体大小
text.color = Color.red;                                   // 文字颜色
text.alignment = TextAnchor.MiddleCenter;                  // 对齐方式（居中）
text.horizontalOverflow = HorizontalWrapMode.Wrap;         // 水平溢出：换行
text.verticalOverflow = VerticalWrapMode.Truncate;         // 垂直溢出：截断
text.supportRichText = true;                              // 启用富文本
```

| 属性 | 类型 | 含义 |
|------|------|------|
| `text` | string | 显示的文本内容 |
| `font` | Font | 字体资源 |
| `fontSize` | int | 字体大小（像素） |
| `color` | Color | 文字颜色 |
| `alignment` | TextAnchor | 对齐方式 |
| `horizontalOverflow` | HorizontalWrapMode | 水平溢出处理（Wrap/Overflow） |
| `verticalOverflow` | VerticalWrapMode | 垂直溢出处理（Truncate/Overflow） |
| `supportRichText` | bool | 是否支持富文本标签 |

### 1.2 富文本标签

```csharp
text.text = "<color=red>红色</color>普通<size=30>大号</size>文字";
text.text = "<b>粗体</b><i>斜体</i><u>下划线</u>";
text.text = "<color=#FF5500>十六进制颜色</color>";
```

| 标签 | 效果 | 示例 |
|------|------|------|
| `<color=red>` | 红色文字 | `<color=red>警告</color>` |
| `<color=#RRGGBB>` | 十六进制颜色 | `<color=#FF5500>橙色</color>` |
| `<size=30>` | 字号 30 | `<size=30>标题</size>` |
| `<b>` | 粗体 | `<b>重要</b>` |
| `<i>` | 斜体 | `<i>强调</i>` |
| `<u>` | 下划线 | `<u>链接</u>` |

**整行人话**：用 HTML 风格的标签在一段文字里混合不同颜色、大小、样式。

### 1.3 Image 常用属性

```csharp
Image image = GetComponent<Image>();
image.sprite = mySprite;                                  // 设置 Sprite
image.color = new Color(1f, 0.5f, 0.5f);                 // 颜色叠加（粉色）
image.type = Image.Type.Sliced;                           // 图片类型：九宫格拉伸
image.preserveAspect = true;                              // 保持宽高比
image.fillAmount = 0.5f;                                 // 填充量（0~1，Filled 模式）
image.fillMethod = Image.FillMethod.Horizontal;           // 填充方向：水平
```

| 属性 | 类型 | 含义 |
|------|------|------|
| `sprite` | Sprite | 要显示的精灵图片 |
| `color` | Color | 颜色叠加（白色=原图，其他颜色会混合） |
| `type` | Image.Type | 图片类型（Simple/Sliced/Tiled/Filled） |
| `preserveAspect` | bool | 是否保持宽高比 |
| `fillAmount` | float | 填充比例（0~1，仅 Filled 模式） |
| `fillMethod` | Image.FillMethod | 填充方向（Horizontal/Vertical/Radial90/Radial180/Radial360） |

### 1.4 Image Type 四种模式

| 模式 | 效果 | 适用 |
|------|------|------|
| **Simple** | 正常显示，拉伸填充 | 普通图片、图标 |
| **Sliced** | 九宫格拉伸，边角不变形 | 按钮背景、面板边框 |
| **Tiled** | 平铺重复，不拉伸 | 纹理背景、图案填充 |
| **Filled** | 按比例填充（进度条） | 血条、进度条、冷却图标 |

### 1.5 Button 常用属性

```csharp
Button button = GetComponent<Button>();
button.interactable = true;                               // 是否可交互
button.onClick.AddListener(OnClick);                      // 添加点击回调
button.onClick.RemoveListener(OnClick);                   // 移除点击回调
button.onClick.RemoveAllListeners();                      // 移除所有回调
```

| 属性 | 类型 | 含义 |
|------|------|------|
| `interactable` | bool | 是否可交互（false 时变灰，点不动） |
| `onClick` | UnityEvent | 点击事件列表 |
| `transition` | Selectable.Transition | 状态过渡方式 |

---

## 二、标准使用步骤

```
步骤1  在 Canvas 下创建控件（右键 UI → Text/Image/Button）
步骤2  Inspector 设置属性（Text 的字体/大小、Image 的 Sprite、Button 的 Transition）
步骤3  脚本获取控件引用（GetComponent 或拖拽 SerializeField）
步骤4  代码控制属性或绑定事件
步骤5  运行测试效果
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

**语法拆解的标准格式**（遇到 `[SerializeField]`、`UnityEvent`、`Sprite` 等不熟悉的写法时使用）：

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

### 案例 1：动态更新分数显示

**功能**：Text 控件实时显示分数，分数变化时用颜色变化提醒玩家。

```csharp
using UnityEngine;
using UnityEngine.UI;

public class ScoreDisplay : MonoBehaviour
{
    [SerializeField] private Text _scoreText;      // 分数文本，Inspector 拖入
    [SerializeField] private Text _comboText;      // 连击文本，Inspector 拖入
    
    private int _score = 0;
    private int _combo = 0;

    void Start()
    {
        UpdateScoreText();
    }

    public void AddScore(int points)
    {
        _score += points;
        _combo++;
        
        UpdateScoreText();
        ShowComboEffect();
    }

    void UpdateScoreText()
    {
        _scoreText.text = $"分数：<color=yellow>{_score}</color>";
        
        if (_score >= 1000)
        {
            _scoreText.color = Color.green;
            _scoreText.fontSize = 32;
        }
        else if (_score >= 500)
        {
            _scoreText.color = Color.blue;
            _scoreText.fontSize = 28;
        }
        else
        {
            _scoreText.color = Color.white;
            _scoreText.fontSize = 24;
        }
    }

    void ShowComboEffect()
    {
        _comboText.text = $"{_combo} 连击！";
        _comboText.color = _combo >= 5 ? Color.red : Color.orange;
        
        CancelInvoke("HideCombo");
        _comboText.gameObject.SetActive(true);
        Invoke("HideCombo", 1f);
    }

    void HideCombo()
    {
        _comboText.gameObject.SetActive(false);
    }
}
```

#### 语法拆解

##### `$"分数：<color=yellow>{_score}</color>"` 是什么？

```csharp
_scoreText.text = $"分数：<color=yellow>{_score}</color>";
```

| 部分 | 含义 |
|------|------|
| `$"..."` | C# 字符串插值，`{变量}` 会被替换成变量值 |
| `<color=yellow>` | 富文本标签：黄色文字 |
| `{_score}` | 插入分数变量的值 |
| `</color>` | 结束颜色标签 |

**整行人话**：显示「分数：100」，其中数字是黄色的。

---

##### `Invoke("HideCombo", 1f)` 是什么？

```csharp
Invoke("HideCombo", 1f);
```

| 部分 | 含义 |
|------|------|
| `Invoke` | Unity 延迟调用方法，指定时间后执行 |
| `"HideCombo"` | 要调用的方法名（字符串） |
| `1f` | 延迟时间（秒） |

**整行人话**：1 秒后自动调用 HideCombo 方法，隐藏连击提示。

---

#### 逐行详解

| 行 | 代码 | 含义 |
|----|------|------|
| 5~6 | `[SerializeField] Text` | 公开引用，Inspector 拖入控件 |
| 8~9 | `_score / _combo` | 分数和连击数变量 |
| 11 | `Start()` | 初始化时更新显示 |
| 14 | `AddScore(int points)` | 外部调用加分 |
| 18~20 | 更新分数和连击，刷新显示 | — |
| 22 | `UpdateScoreText()` | 更新分数文本显示 |
| 24 | 富文本显示分数（黄色数字） | — |
| 26~38 | 根据分数改变颜色和字号 | — |
| 40 | `ShowComboEffect()` | 显示连击效果 |
| 42 | 连击数 >= 5 变红，否则橙色 | — |
| 44 | `CancelInvoke` | 取消之前的延迟调用（避免重叠） |
| 46 | `Invoke("HideCombo", 1f)` | 1 秒后隐藏连击 |

#### 操作提示

1. Canvas 下创建两个 Text：ScoreText 和 ComboText  
2. 把脚本挂到任意 GameObject（如 Canvas）  
3. Inspector 拖入两个 Text 引用  
4. 在其他脚本中调用 `GetComponent<ScoreDisplay>().AddScore(100)` 测试

---

### 案例 2：血条 Fill 模式实现

**功能**：用 Image 的 Filled 模式实现血条，血量变化时平滑更新。

```csharp
using UnityEngine;
using UnityEngine.UI;

public class HealthBar : MonoBehaviour
{
    [SerializeField] private Image _healthFill;      // 血量填充图片（Foreground）
    [SerializeField] private Text _healthText;       // 血量文字
    
    public float maxHealth = 100f;
    private float _currentHealth;
    private float _targetHealth;

    void Start()
    {
        _currentHealth = maxHealth;
        _targetHealth = maxHealth;
        UpdateHealthBar();
    }

    void Update()
    {
        _currentHealth = Mathf.Lerp(_currentHealth, _targetHealth, Time.deltaTime * 5f);
        UpdateHealthBar();
    }

    public void TakeDamage(float damage)
    {
        _targetHealth = Mathf.Max(0f, _targetHealth - damage);
    }

    public void Heal(float amount)
    {
        _targetHealth = Mathf.Min(maxHealth, _targetHealth + amount);
    }

    void UpdateHealthBar()
    {
        float fillPercent = _currentHealth / maxHealth;
        _healthFill.fillAmount = fillPercent;
        
        _healthText.text = $"{Mathf.Ceil(_currentHealth)}/{maxHealth}";
        
        if (fillPercent > 0.6f)
            _healthFill.color = Color.green;
        else if (fillPercent > 0.3f)
            _healthFill.color = Color.yellow;
        else
            _healthFill.color = Color.red;
    }
}
```

#### 语法拆解

##### `_healthFill.fillAmount = fillPercent;` 是什么？

```csharp
float fillPercent = _currentHealth / maxHealth;
_healthFill.fillAmount = fillPercent;
```

| 部分 | 含义 |
|------|------|
| `fillAmount` | Image 的填充比例（0~1），仅 Filled 模式有效 |
| `fillPercent` | 当前血量 / 最大血量，结果 0~1 |

**整行人话**：按比例填充血条——满血时 fillAmount=1（全满），没血时 fillAmount=0（空）。

---

##### `Mathf.Lerp(a, b, t)` 是什么？

```csharp
_currentHealth = Mathf.Lerp(_currentHealth, _targetHealth, Time.deltaTime * 5f);
```

| 部分 | 含义 |
|------|------|
| `Mathf.Lerp` | 线性插值：从 a 向 b 按 t 比例靠近 |
| `_currentHealth` | 当前显示的血量 |
| `_targetHealth` | 目标血量 |
| `Time.deltaTime * 5f` | 每帧推进 5%，实现平滑过渡 |

**整行人话**：血量变化不是瞬间跳变，而是平滑过渡，看起来更舒服。

---

#### 逐行详解

| 行 | 代码 | 含义 |
|----|------|------|
| 5~6 | Image/Text 引用 | Inspector 拖入 |
| 8 | `maxHealth = 100` | 最大血量 |
| 9~10 | 当前血量和目标血量 | — |
| 12~16 | 初始化，满血 | — |
| 18~21 | Update 中平滑插值血量 | — |
| 23 | `TakeDamage(float damage)` | 扣血方法 |
| 25 | `Mathf.Max(0, ...)` | 血量最低为 0 |
| 28 | `Heal(float amount)` | 加血方法 |
| 30 | `Mathf.Min(maxHealth, ...)` | 血量最高为 maxHealth |
| 32 | `UpdateHealthBar()` | 更新血条显示 |
| 34 | 计算填充比例 | — |
| 35 | 设置 fillAmount | — |
| 37 | 显示血量文字 | — |
| 39~44 | 根据血量改变颜色 | — |

#### 操作提示

1. Canvas 下创建血条：  
   - 创建一个 Image 作为背景（灰色）  
   - 在背景下创建一个 Image 作为前景（红色，Image Type 设为 Filled，Fill Method 设为 Horizontal）  
2. 创建 Text 显示数字  
3. 脚本挂到背景或 Canvas 上，拖入前景 Image 和 Text  
4. 调用 `TakeDamage(20)` 或 `Heal(30)` 测试

---

### 案例 3：按钮事件绑定与状态控制

**功能**：多个按钮控制 UI 面板的显隐，按钮点击后切换状态。

```csharp
using UnityEngine;
using UnityEngine.UI;

public class PanelController : MonoBehaviour
{
    [SerializeField] private Button _btnOpen;        // 打开按钮
    [SerializeField] private Button _btnClose;       // 关闭按钮
    [SerializeField] private Button _btnToggle;      // 切换按钮
    [SerializeField] private GameObject _panel;       // 要控制的面板

    void Start()
    {
        _btnOpen.onClick.AddListener(OpenPanel);
        _btnClose.onClick.AddListener(ClosePanel);
        _btnToggle.onClick.AddListener(TogglePanel);
        
        ClosePanel();
    }

    void OpenPanel()
    {
        _panel.SetActive(true);
        _btnOpen.interactable = false;
        _btnClose.interactable = true;
    }

    void ClosePanel()
    {
        _panel.SetActive(false);
        _btnOpen.interactable = true;
        _btnClose.interactable = false;
    }

    void TogglePanel()
    {
        bool isActive = _panel.activeSelf;
        _panel.SetActive(!isActive);
    }

    public void OnButtonPressed()
    {
        Debug.Log("按钮被按下！");
    }
}
```

#### 语法拆解

##### `_btnOpen.onClick.AddListener(OpenPanel)` 是什么？

```csharp
_btnOpen.onClick.AddListener(OpenPanel);
```

| 部分 | 含义 |
|------|------|
| `_btnOpen` | Button 组件引用 |
| `.onClick` | 点击事件列表（UnityEvent） |
| `.AddListener` | 添加回调方法 |
| `OpenPanel` | 回调方法名（无参数的 void 方法） |

**整行人话**：告诉打开按钮「点击时执行 OpenPanel 方法」。

---

##### `_btnOpen.interactable = false` 是什么？

```csharp
_btnOpen.interactable = false;
```

| 部分 | 含义 |
|------|------|
| `interactable` | bool 属性：是否可交互 |
| `false` | 不可交互，按钮变灰，点不动 |

**整行人话**：打开面板后，打开按钮变灰不可点，避免重复打开。

---

#### 逐行详解

| 行 | 代码 | 含义 |
|----|------|------|
| 5~8 | 按钮和面板引用 | Inspector 拖入 |
| 10 | `Start()` | 初始化绑定事件 |
| 12~14 | 三个按钮绑定各自回调 | — |
| 16 | `ClosePanel()` | 初始状态关闭面板 |
| 18 | `OpenPanel()` | 打开面板 |
| 20~21 | 设置按钮状态 | — |
| 24 | `ClosePanel()` | 关闭面板 |
| 26~27 | 设置按钮状态 | — |
| 30 | `TogglePanel()` | 切换面板显隐 |
| 32 | `_panel.activeSelf` | 获取当前激活状态 |
| 33 | `!isActive` | 取反切换 |
| 36 | `OnButtonPressed()` | 通用按钮回调（可在 Inspector 绑定） |

#### 操作提示

1. Canvas 下创建三个 Button：Open、Close、Toggle  
2. 创建一个 Panel（GameObject + Image）作为要控制的面板  
3. 脚本挂到任意 GameObject  
4. Inspector 拖入三个按钮和面板引用  
5. 也可在 Inspector 的 Button OnClick 中绑定 `OnButtonPressed` 方法

---

## 【入门阶段小结】

| 维度 | 要点 |
|------|------|
| **Text** | `text.text` 修改内容，富文本标签，颜色/字号控制 |
| **Image** | `image.sprite` 设置图片，`fillAmount` 控制填充，四种 Image Type |
| **Button** | `onClick.AddListener` 绑定事件，`interactable` 控制状态 |
| **案例** | 分数显示、血条、按钮控制面板 |

---

# 第三阶段：进阶篇

## 【阶段总述】

进阶阶段：**按钮事件系统深入**、**图文混排**、**性能优化**、**Selectable 基类**、**常见踩坑清单**。

---

## 一、按钮事件系统深入

### 1.1 UnityEvent — 可序列化事件

```csharp
using UnityEngine.Events;

public class CustomButton : MonoBehaviour
{
    public UnityEvent onCustomEvent;
    
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            onCustomEvent?.Invoke();
        }
    }
}
```

| 概念 | 说明 |
|------|------|
| `UnityEvent` | 可在 Inspector 中配置的事件列表 |
| `?.Invoke()` | 安全调用：事件不为空时才执行 |
| **优点** | 设计师可在 Inspector 中绑定方法，无需写代码 |

### 1.2 带参数的 UnityEvent

```csharp
public UnityEvent<int> onScoreChanged;

void AddScore(int points)
{
    _score += points;
    onScoreChanged?.Invoke(_score);
}
```

| 参数类型 | 泛型 |
|----------|------|
| float | `UnityEvent<float>` |
| int | `UnityEvent<int>` |
| string | `UnityEvent<string>` |
| Object | `UnityEvent<UnityEngine.Object>` |

---

## 二、图文混排 — Text + Image 组合

### 2.1 图文并排

```
Panel（水平布局组）
├── Image（图标）
└── Text（文字说明）
```

步骤：
1. 创建 Panel，添加 **Horizontal Layout Group**
2. 在 Panel 下创建 Image 和 Text
3. 调整布局组的 spacing 和 padding

### 2.2 文字背景高亮

```
Panel（带 Image 背景）
└── Text（文字）
```

步骤：
1. 创建 Panel（自带 Image），设为半透明背景
2. 在 Panel 下创建 Text
3. Panel 的锚点自适应 Text 大小（加 ContentSizeFitter）

---

## 三、性能优化

### 3.1 Text 性能注意事项

| 因素 | 影响 | 优化 |
|------|------|------|
| 频繁修改 text | 每帧重建字符网格 | 减少修改频率，缓存字符串 |
| 长文本 | 字符网格大，渲染开销高 | 用 TextMeshPro，或分段显示 |
| 富文本 | 解析标签有开销 | 避免过多嵌套标签 |
| 字体切换 | 切换字体重建网格 | 尽量不切换字体 |

### 3.2 Image 性能注意事项

| 因素 | 影响 | 优化 |
|------|------|------|
| 频繁切换 Sprite | 每帧重建网格 | 用 Sprite Atlas 合并图集 |
| Mask 嵌套 | 裁剪开销大 | 减少嵌套，用 RectMask2D |
| 过大图片 | 显存占用高 | 压缩纹理，合理分辨率 |

---

## 四、Selectable — 交互控件基类

Button/Toggle/Slider/Scrollbar 都继承自 Selectable，共享以下属性：

| 属性 | 说明 |
|------|------|
| `interactable` | 是否可交互 |
| `transition` | 状态过渡方式 |
| `targetGraphic` | 目标图形（状态变化影响的 Image） |
| `colors` | 各状态颜色（Normal/Highlighted/Pressed/Disabled） |

```csharp
Selectable selectable = GetComponent<Selectable>();
selectable.colors.normalColor = Color.white;
selectable.colors.highlightedColor = Color.gray;
selectable.colors.pressedColor = Color.darkGray;
selectable.colors.disabledColor = Color.grey;
```

---

## 五、常见误区与最佳实践

| 误区 | 正确做法 |
|------|----------|
| Text 显示中文乱码 | 使用中文字体，或用 TextMeshPro |
| Button 点不动 | 检查 EventSystem、GraphicRaycaster 是否存在 |
| 频繁修改 text 属性 | 缓存字符串，减少不必要的修改 |
| Image 拉伸变形 | 使用 Sliced 模式（九宫格）或开启 preserveAspect |
| 按钮事件重复绑定 | 每次绑定前先 RemoveAllListeners |
| 代码绑定和 Inspector 绑定混用 | 统一一种方式，避免混乱 |
| RawImage 显示 Sprite | 不要用 Sprite，用 Texture2D |
| 血条 fillAmount 没效果 | 确认 Image Type 设为 Filled |

---

## 【进阶阶段小结】

| 维度 | 要点 |
|------|------|
| 事件系统 | UnityEvent 可序列化事件，支持带参数 |
| 图文混排 | Layout Group + Panel + Text/Image |
| 性能 | 减少频繁修改、使用 Sprite Atlas、TextMeshPro |
| Selectable | Button/Toggle/Slider 共享基类属性 |
| 避坑 | 中文字体、EventSystem、九宫格拉伸 |

---

# 【全文总结】

## 最重要的一行代码

```csharp
button.onClick.AddListener(() => { Debug.Log("点击了！"); });
```

| 部分 | 含义 |
|------|------|
| `button.onClick` | 按钮点击事件列表 |
| `AddListener` | 添加回调 |
| `() => { ... }` | Lambda 表达式：匿名方法 |

## 三阶段对照

| 阶段 | 代表案例 |
|------|----------|
| 零基础 | 认识四个控件、读懂基本代码 |
| 入门 | 分数显示、血条、按钮控制面板 |
| 进阶 | UnityEvent、图文混排、性能优化 |

## API 速查

| 控件 | 常用代码 |
|------|----------|
| Text | `text.text = "内容"` / `text.color = Color.red` / `text.fontSize = 24` |
| Image | `image.sprite = sprite` / `image.fillAmount = 0.5f` / `image.color = color` |
| RawImage | `rawImage.texture = texture` / `rawImage.uvRect = rect` |
| Button | `button.onClick.AddListener(method)` / `button.interactable = false` |

## 学习自检

- [ ] Text/Image/RawImage/Button 各自的用途？
- [ ] Image 和 RawImage 的核心区别？
- [ ] Image 的四种 Type 各用在什么场景？
- [ ] Button 的点击事件如何绑定？
- [ ] 什么是富文本？有哪些常用标签？
- [ ] 为什么 Button 点不动？怎么排查？

---

## 参考资料

| 类型 | 链接 |
|------|------|
| Text 官方 Manual | https://docs.unity3d.com/Manual/script-Text.html |
| Image 官方 Manual | https://docs.unity3d.com/Manual/script-Image.html |
| Button 官方 Manual | https://docs.unity3d.com/Manual/script-Button.html |
| RawImage 官方 Manual | https://docs.unity3d.com/Manual/script-RawImage.html |
| Selectable API | https://docs.unity3d.com/ScriptReference/UI.Selectable.html |
| UnityEvent | https://docs.unity3d.com/ScriptReference/Events.UnityEvent.html |

---

*文档版本：与 major3/01_PlayerPrefs.md ~ 05_DoTween.md、Week2_Xmind、Week3_Xmind 同系列模板。*