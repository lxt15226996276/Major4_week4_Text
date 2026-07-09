# Unity UGUI 常用控件（三）详解

> 参照：[Unity 官方 Manual - InputField](https://docs.unity3d.com/Manual/script-InputField.html) · [Dropdown](https://docs.unity3d.com/Manual/script-Dropdown.html) · [EventSystem](https://docs.unity3d.com/Manual/EventSystem.html)  
> 关联文档：[02_UGUI常用控件（一）.md](./02_UGUI常用控件（一）.md)（Text/Image/Button）· [03_UGUI常用控件（二）.md](./03_UGUI常用控件（二）.md)（Toggle/Slider/ScrollRect）· [../major3/01_PlayerPrefs.md](../major3/01_PlayerPrefs.md)（PlayerPrefs 保存）  
> 学习路径：**零基础 → 入门 → 进阶**，每阶段采用 **总—分—总** 结构。  
> 讲解维度：**定义 → 本质 → 特点 → 适用场景 → 原理 → API → 步骤 → 案例 → 避坑**（进阶含自定义输入验证 / Dropdown 动态选项 / 事件接口扩展）。  
> 案例讲解：遵循 **案例代码讲解模板**（功能 → 代码 → 语法拆解 → 逐行详解 → 操作提示）。  
> API 讲解：入门/进阶 API 章节均采用 **逐词读懂** 格式（与 [../major3/01_PlayerPrefs.md](../major3/01_PlayerPrefs.md) 一致：类型 → 参数 → 整行人话）。

---

## 【全文总述】

**InputField（输入框）** 是 UGUI 的「文本输入控件」：允许用户输入文字，支持密码隐藏、占位符、输入验证等功能。  
**Dropdown（下拉框）** 是 UGUI 的「多选一控件」：点击展开选项列表，选择一个选项后收起，适合选项较多但互斥的场景。  
**EventSystem（事件系统）** 是 UGUI 的「事件中枢」：负责分发用户输入事件（点击、拖动、滚动等）到相应的控件。  
**UGUI 事件接口** 是 UGUI 的「事件回调机制」：通过实现接口或注册事件，响应各种交互操作（点击、拖拽、指针进入等）。  
本文从输入和选择控件的用法，到事件系统的原理，逐层展开。

### 思维导图总览

```
Unity UGUI 常用控件（三）
│
├── InputField（输入框控件 — 文本输入）
│   │
│   ├── 【知识维度】（讲师框架 — 完整版）
│   │   │
│   │   ├── 定义：允许用户输入文本的控件
│   │   │   └── 官方描述：A text input field where users can type
│   │   │       创建方式：右键 UI → Input Field
│   │   │
│   │   ├── 本质：Text + 光标 + 输入检测 + 事件触发
│   │   │   ├── 组件模型：InputField + Text（Placeholder）+ Text（Text）+ Image（Background）
│   │   │   ├── 获取方式：GetComponent<InputField>()
│   │   │   └── 状态链路：输入 → text 更新 → OnValueChanged 事件 → 光标移动
│   │   │
│   │   ├── 官方定位：用户文本输入
│   │   │   ├── 设计用途：用户名输入、密码输入、搜索框、聊天输入
│   │   │   └── 核心能力：输入、编辑、验证、提交
│   │   │
│   │   ├── 特点
│   │   │   ├── 优势：支持多种输入类型、占位符、密码隐藏、输入验证、事件驱动
│   │   │   └── 局限：中文输入支持需注意、自定义光标样式复杂、移动端键盘适配
│   │   │
│   │   ├── 适用场景
│   │   │   ├── ✅ 适用：用户名/密码登录、搜索框、聊天输入、数值输入、表单填写
│   │   │   └── ❌ 不适用：连续值调节（用 Slider）、选项选择（用 Dropdown）
│   │   │
│   │   ├── 核心属性及参数（Inspector 常用）
│   │   │   ├── Text：当前输入的文本
│   │   │   ├── Placeholder：未输入时显示的提示文字
│   │   │   ├── Character Limit：最大字符数（0=不限）
│   │   │   ├── Content Type：输入类型（Standard/Password/Integer Number/Decimal Number）
│   │   │   ├── Line Type：换行方式（Single Line/Multi Line Submit/Multi Line Newline）
│   │   │   └── On Value Changed：文本变化事件
│   │   │   └── On End Edit：编辑结束事件（回车/失去焦点）
│   │   │
│   │   ├── 核心 API
│   │   │   ├── text：获取/设置输入文本（最常用）
│   │   │   ├── placeholder：占位符 Text 组件
│   │   │   ├── characterLimit：最大字符数
│   │   │   ├── contentType：输入类型
│   │   │   ├── onValueChanged：文本变化事件
│   │   │   └── onEndEdit：编辑结束事件
│   │   │
│   │   └── 标准使用步骤
│   │       ├── 步骤1 创建 InputField（右键 UI → Input Field）
│   │       ├── 步骤2 设置 Placeholder、ContentType、Character Limit
│   │       ├── 步骤3 代码监听 onValueChanged 和 onEndEdit 事件
│   │       └── 步骤4 运行测试输入效果
│   │
│   ├── Dropdown（下拉框控件 — 多选一）
│   │   │
│   │   │
│   │   ├── 定义：点击展开选项列表，选择一个选项后收起
│   │   │   ├── Options：选项列表（List\<Dropdown.OptionData\>）
│   │   │   ├── Value：当前选中的选项索引（从 0 开始）
│   │   │   ├── Caption Text：显示当前选中选项的文字
│   │   │   └── Template：下拉列表模板（展开时显示）
│   │   │
│   │   ├── 本质：Button + ScrollRect + 选项管理 + 事件触发
│   │   │
│   │   ├── 核心属性：options / value / captionText / template
│   │   │
│   │   └── 适用：选择职业、选择服务器、选择难度、筛选条件
│   │
│   ├── EventSystem（事件系统 — 事件中枢）
│   │   │
│   │   │
│   │   ├── 定义：管理和分发用户输入事件的核心组件
│   │   │   ├── Event System：场景中必须有且仅有一个
│   │   │   ├── Input Module：输入模块（StandaloneInputModule/TouchInputModule）
│   │   │   └── Selected Object：当前选中的 UI 对象
│   │   │
│   │   ├── 本质：事件分发器 + 输入检测 + 焦点管理
│   │   │
│   │   ├── 核心属性：firstSelectedGameObject / sendNavigationEvents
│   │   │
│   │   └── 适用：所有 UGUI 交互控件都依赖它
│   │
│   └── UGUI 事件接口（事件回调 — 扩展交互）
│       │
│       │
│       ├── 定义：通过实现接口响应特定交互事件
│       │   ├── IPointerEnterHandler：指针进入
│       │   ├── IPointerExitHandler：指针离开
│       │   ├── IPointerDownHandler：指针按下
│       │   ├── IPointerUpHandler：指针抬起
│       │   ├── IPointerClickHandler：点击
│       │   ├── IBeginDragHandler：开始拖拽
│       │   ├── IDragHandler：拖拽中
│       │   ├── IEndDragHandler：结束拖拽
│       │   └── IDropHandler：放置
│       │
│       ├── 本质：消息分发 + 接口回调
│       │
│       ├── 核心接口：上述 9 个常用接口
│       │
│       └── 适用：自定义控件、复杂交互、拖拽系统
```

| 学习阶段 | 学习目标 |
|----------|----------|
| **零基础** | 说清四个概念各自是什么；读懂 `inputField.text = ""` |
| **入门** | 掌握 InputField/Dropdown 常用属性、代码控制；完成 3 个交互案例 |
| **进阶** | 会自定义输入验证、Dropdown 动态选项、事件接口扩展、拖拽系统 |

### 讲师知识框架速览（全文脉络）

| 维度 | 零基础讲 | 入门讲 | 进阶讲 |
|------|----------|--------|--------|
| 定义 | ✅ | 回顾 | 回顾 |
| 本质 | ✅ | — | — |
| 特点 | ✅ | — | 性能补充 |
| 适用场景 | ✅ | — | 选型（输入方案） |
| 核心原理 | 控件用途 | ✅ 属性与 API | 事件机制原理 |
| 核心 API | 读懂 text/value | ✅ 常用属性 | 事件接口 |
| 使用步骤 | Inspector 创建 | ✅ 代码控制 | 进阶案例 |
| 调用时机 | — | ✅ Start/Update | — |
| 避坑 | — | 初步 | ✅ |

---

# 第一阶段：零基础篇

## 【阶段总述】

零基础阶段建立**正确认知**：InputField/Dropdown/EventSystem/事件接口各自是什么、分别用来做什么、有什么区别。  
同时学会**读懂** `inputField.text = "Hello";` 和 `dropdown.value = 0;`，并认识每个控件的 Inspector 核心参数。

---

## 一、四个概念定义对照

| 概念 | 一句话定义 | 核心作用 | 类比 |
|------|-----------|----------|------|
| **InputField** | 输入框控件，允许用户输入文字 | 文本输入、密码输入、搜索 | 登录框、搜索框 |
| **Dropdown** | 下拉框控件，多选一 | 从多个选项中选择一个 | 选择职业、选择地区 |
| **EventSystem** | 事件系统，管理用户输入事件 | 分发点击、拖动等事件 | 交通指挥中心 |
| **事件接口** | 通过实现接口响应交互事件 | 自定义交互逻辑 | 监听门铃、电话 |

---

## 二、本质 — 它们怎么工作？

```
InputField 工作流程：
  用户输入 → text 属性更新 → OnValueChanged 事件 → 光标移动 → 失去焦点/回车 → OnEndEdit 事件

Dropdown 工作流程：
  点击 → 展开模板（ScrollRect）→ 点击选项 → value 更新 → OnValueChanged 事件 → 收起模板

EventSystem 工作流程：
  用户操作（点击/拖动）→ InputModule 检测 → 找到目标控件 → 调用对应事件接口/UnityEvent
```

| 概念 | 说明 |
|------|------|
| **InputModule** | EventSystem 的输入模块，处理具体的输入检测（Standalone=鼠标键盘，Touch=触摸） |
| **GraphicRaycaster** | Canvas 上的射线检测组件，用来找到被点击的 UI 控件 |
| **选项索引** | Dropdown 的 value 是从 0 开始的索引，不是选项的文字 |

---

## 三、InputField 的 Content Type

| 类型 | 效果 | 适用 |
|------|------|------|
| **Standard** | 标准文本，允许任何字符 | 用户名、备注 |
| **Password** | 密码模式，显示为星号 | 密码输入 |
| **Integer Number** | 只允许整数 | 年龄、数量 |
| **Decimal Number** | 只允许小数 | 金额、评分 |
| **Email Address** | 邮箱格式 | 邮箱输入 |
| **Phone Number** | 电话号码格式 | 手机号输入 |

---

## 四、核心一课：如何读懂一行代码

### 4.1 InputField — 设置输入文本

```csharp
inputField.text = "Hello World";
```

| 部分 | 含义 |
|------|------|
| `inputField` | InputField 组件引用（变量名） |
| `.text` | 属性名：当前输入的文本 |
| `"Hello World"` | 赋值：设置输入框显示的文字 |

**整行人话**：把输入框的内容设为「Hello World」。

### 4.2 Dropdown — 设置选中项

```csharp
dropdown.value = 2;
```

| 部分 | 含义 |
|------|------|
| `dropdown` | Dropdown 组件引用（变量名） |
| `.value` | 属性名：当前选中选项的索引（从 0 开始） |
| `2` | 赋值：选中第 3 个选项（索引 0=第一个） |

**整行人话**：选中下拉框的第 3 个选项（索引从 0 开始）。

---

## 【零基础阶段小结】

| 维度 | 要点 |
|------|------|
| **InputField** | 输入框，用 `text` 控制内容，`contentType` 控制输入类型 |
| **Dropdown** | 下拉框，用 `value` 控制选中索引，`options` 管理选项列表 |
| **EventSystem** | 事件中枢，场景中必须有一个，管理所有交互事件 |
| **事件接口** | 通过实现接口响应特定交互，如 IPointerClickHandler |
| **区别** | InputField 是输入，Dropdown 是选择，EventSystem 是事件管理 |

**阶段检验**：能说出四个概念各自的用途；能解释 EventSystem 的作用。

---

# 第二阶段：入门篇

## 【阶段总述】

入门阶段掌握 **InputField/Dropdown/EventSystem/事件接口** 的常用属性和代码控制方式，学会绑定事件和实现常用交互功能。  
重点：**InputField 的输入验证、Dropdown 的动态选项、事件接口的基本用法**。

---

## 一、核心属性及参数详解（逐词读懂）

### 1.1 InputField 常用属性

```csharp
InputField inputField = GetComponent<InputField>();
inputField.text = "默认文本";                                 // 当前输入文本
inputField.placeholder.GetComponent<Text>().text = "请输入";   // 占位符文字
inputField.characterLimit = 20;                               // 最大字符数（0=不限）
inputField.contentType = InputField.ContentType.Password;      // 输入类型
inputField.lineType = InputField.LineType.SingleLine;          // 换行方式
inputField.onValueChanged.AddListener(OnInputChanged);         // 文本变化事件
inputField.onEndEdit.AddListener(OnInputEnd);                  // 编辑结束事件
```

| 属性 | 类型 | 含义 |
|------|------|------|
| `text` | string | 当前输入的文本 |
| `placeholder` | Graphic | 占位符（通常是 Text 组件） |
| `characterLimit` | int | 最大字符数（0=不限） |
| `contentType` | InputField.ContentType | 输入类型（Standard/Password 等） |
| `lineType` | InputField.LineType | 换行方式（SingleLine/MultiLine） |
| `onValueChanged` | UnityEvent\<string\> | 文本变化时的事件（参数为新文本） |
| `onEndEdit` | UnityEvent\<string\> | 编辑结束时的事件（参数为最终文本） |

### 1.2 Dropdown 常用属性

```csharp
Dropdown dropdown = GetComponent<Dropdown>();
dropdown.value = 0;                                           // 当前选中索引
dropdown.options.Clear();                                     // 清空选项列表
dropdown.options.Add(new Dropdown.OptionData("选项1"));       // 添加选项
dropdown.options.Add(new Dropdown.OptionData("选项2"));
dropdown.RefreshShownValue();                                 // 刷新显示
dropdown.onValueChanged.AddListener(OnDropdownChanged);       // 选项变化事件
```

| 属性 | 类型 | 含义 |
|------|------|------|
| `value` | int | 当前选中选项的索引（从 0 开始） |
| `options` | List\<Dropdown.OptionData\> | 选项列表 |
| `captionText` | Text | 显示当前选中选项的文字 |
| `template` | RectTransform | 下拉列表模板 |
| `onValueChanged` | UnityEvent\<int\> | 选项变化时的事件（参数为新索引） |

### 1.3 UGUI 事件接口对照

| 接口 | 触发时机 | 参数 |
|------|----------|------|
| `IPointerEnterHandler` | 指针进入控件 | PointerEventData |
| `IPointerExitHandler` | 指针离开控件 | PointerEventData |
| `IPointerDownHandler` | 指针按下 | PointerEventData |
| `IPointerUpHandler` | 指针抬起 | PointerEventData |
| `IPointerClickHandler` | 点击（按下+抬起） | PointerEventData |
| `IBeginDragHandler` | 开始拖拽 | PointerEventData |
| `IDragHandler` | 拖拽中 | PointerEventData |
| `IEndDragHandler` | 结束拖拽 | PointerEventData |
| `IDropHandler` | 拖拽放置到目标上 | PointerEventData |

---

## 二、标准使用步骤

### 2.1 InputField 使用步骤

```
步骤1  创建 InputField（右键 UI → Input Field）
步骤2  设置 Placeholder、ContentType、Character Limit
步骤3  设置 Line Type（单行/多行）
步骤4  代码监听 onValueChanged 和 onEndEdit 事件
步骤5  运行测试输入效果
```

### 2.2 Dropdown 使用步骤

```
步骤1  创建 Dropdown（右键 UI → Dropdown）
步骤2  在 Inspector 中添加/修改选项
步骤3  设置 Caption Text 显示样式
步骤4  代码监听 onValueChanged 事件
步骤5  运行测试选择效果
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

**语法拆解的标准格式**（遇到 `Dropdown.OptionData`、`IPointerClickHandler`、`PointerEventData` 等不熟悉的写法时使用）：

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

### 案例 1：登录界面 — InputField 输入验证

**功能**：用户名和密码输入框，支持输入验证（非空、长度限制），回车提交登录。

```csharp
using UnityEngine;
using UnityEngine.UI;

public class LoginPanel : MonoBehaviour
{
    [SerializeField] private InputField _usernameInput;    // 用户名输入框
    [SerializeField] private InputField _passwordInput;    // 密码输入框
    [SerializeField] private Text _errorText;              // 错误提示
    [SerializeField] private Button _loginButton;          // 登录按钮
    
    private const string USERNAME_KEY = "SavedUsername";

    void Start()
    {
        _usernameInput.text = PlayerPrefs.GetString(USERNAME_KEY, "");
        
        _usernameInput.onEndEdit.AddListener(OnUsernameEndEdit);
        _passwordInput.onEndEdit.AddListener(OnPasswordEndEdit);
        _loginButton.onClick.AddListener(OnLogin);
    }

    void OnUsernameEndEdit(string text)
    {
        if (!string.IsNullOrEmpty(text))
        {
            PlayerPrefs.SetString(USERNAME_KEY, text);
            PlayerPrefs.Save();
        }
    }

    void OnPasswordEndEdit(string text)
    {
        if (text == "\n")
        {
            _loginButton.onClick.Invoke();
        }
    }

    void OnLogin()
    {
        string username = _usernameInput.text.Trim();
        string password = _passwordInput.text;
        
        _errorText.text = "";
        
        if (string.IsNullOrEmpty(username))
        {
            _errorText.text = "请输入用户名";
            _usernameInput.Select();
            return;
        }
        
        if (password.Length < 6)
        {
            _errorText.text = "密码至少需要6位";
            _passwordInput.Select();
            return;
        }
        
        Debug.Log($"登录成功！用户名：{username}");
    }
}
```

#### 语法拆解

##### `inputField.onEndEdit.AddListener(OnUsernameEndEdit)` 是什么？

```csharp
_usernameInput.onEndEdit.AddListener(OnUsernameEndEdit);
```

| 部分 | 含义 |
|------|------|
| `onEndEdit` | 编辑结束事件（回车或失去焦点时触发） |
| `AddListener` | 添加回调方法 |
| `OnUsernameEndEdit` | 回调方法（参数 string：最终输入文本） |

**整行人话**：输入框编辑结束时，执行 OnUsernameEndEdit 方法。

---

##### `inputField.Select()` 是什么？

```csharp
_usernameInput.Select();
```

| 部分 | 含义 |
|------|------|
| `Select()` | 方法：让输入框获得焦点，弹出键盘 |

**整行人话**：让输入框获得焦点，准备输入。

---

#### 逐行详解

| 行 | 代码 | 含义 |
|----|------|------|
| 5~8 | InputField、Text、Button 引用 | Inspector 拖入 |
| 10 | `USERNAME_KEY` | PlayerPrefs 存档 Key |
| 12 | `Start()` | 初始化 |
| 14 | 读取上次保存的用户名 | — |
| 16~18 | 绑定事件 | — |
| 21 | `OnUsernameEndEdit` | 用户名编辑结束，保存到 PlayerPrefs |
| 23 | 非空判断 | — |
| 25~27 | 保存用户名 | — |
| 30 | `OnPasswordEndEdit` | 密码编辑结束 |
| 32 | 判断是否按了回车 | — |
| 34 | 触发登录按钮的点击事件 | — |
| 37 | `OnLogin()` | 登录逻辑 |
| 39~40 | 获取输入内容（Trim 去除空格） | — |
| 42 | 清空错误提示 | — |
| 44~48 | 验证用户名非空 | — |
| 50~54 | 验证密码长度 | — |
| 57 | 登录成功 | — |

#### 操作提示

1. Canvas 下创建两个 InputField（用户名、密码）  
2. 密码输入框的 Content Type 设为 Password  
3. 创建 Text 显示错误提示（初始为空）  
4. 创建 Button 作为登录按钮  
5. 脚本挂到任意 GameObject，拖入引用  
6. Play 测试：输入用户名和密码，回车或点击按钮登录

---

### 案例 2：角色选择 — Dropdown 动态选项

**功能**：下拉框选择角色职业，动态添加选项，选择后显示角色描述。

```csharp
using UnityEngine;
using UnityEngine.UI;

public class CharacterSelect : MonoBehaviour
{
    [SerializeField] private Dropdown _classDropdown;      // 职业下拉框
    [SerializeField] private Text _descriptionText;         // 职业描述
    
    private string[] _classNames = { "战士", "法师", "弓箭手", "牧师" };
    private string[] _classDescriptions = {
        "战士：近战物理职业，高血量高防御，适合冲锋陷阵",
        "法师：远程魔法职业，高伤害低血量，擅长范围攻击",
        "弓箭手：远程物理职业，高攻速高暴击，擅长放风筝",
        "牧师：辅助治疗职业，能治疗队友，提供增益效果"
    };

    void Start()
    {
        PopulateDropdown();
        
        _classDropdown.onValueChanged.AddListener(OnClassChanged);
        
        OnClassChanged(0);
    }

    void PopulateDropdown()
    {
        _classDropdown.options.Clear();
        
        for (int i = 0; i < _classNames.Length; i++)
        {
            _classDropdown.options.Add(new Dropdown.OptionData(_classNames[i]));
        }
        
        _classDropdown.RefreshShownValue();
    }

    void OnClassChanged(int index)
    {
        if (index >= 0 && index < _classDescriptions.Length)
        {
            _descriptionText.text = _classDescriptions[index];
        }
    }
}
```

#### 语法拆解

##### `dropdown.options.Add(new Dropdown.OptionData(name))` 是什么？

```csharp
_classDropdown.options.Add(new Dropdown.OptionData(_classNames[i]));
```

| 部分 | 含义 |
|------|------|
| `options` | Dropdown 的选项列表（List\<Dropdown.OptionData\>） |
| `Add` | 添加选项 |
| `new Dropdown.OptionData(name)` | 创建一个新选项（参数为选项文字） |

**整行人话**：向下拉框添加一个新选项，显示文字为职业名称。

---

##### `dropdown.RefreshShownValue()` 是什么？

```csharp
_classDropdown.RefreshShownValue();
```

| 部分 | 含义 |
|------|------|
| `RefreshShownValue()` | 方法：刷新显示当前选中的选项 |

**整行人话**：刷新下拉框的显示，确保选中的选项正确显示。

---

#### 逐行详解

| 行 | 代码 | 含义 |
|----|------|------|
| 5~6 | Dropdown 和 Text 引用 | Inspector 拖入 |
| 8~13 | 职业名称和描述数组 | — |
| 15 | `Start()` | 初始化 |
| 17 | `PopulateDropdown()` | 填充下拉框选项 |
| 19 | 绑定选项变化事件 | — |
| 21 | 初始化显示第一个职业描述 | — |
| 24 | `PopulateDropdown()` | 动态填充选项 |
| 26 | 清空原有选项 | — |
| 28 | for 循环添加选项 | — |
| 30 | 添加选项到列表 | — |
| 33 | 刷新显示 | — |
| 36 | `OnClassChanged(int index)` | 职业变化回调 |
| 38 | 索引范围检查 | — |
| 40 | 更新描述文字 | — |

#### 操作提示

1. Canvas 下创建 Dropdown 和 Text  
2. 确保 Dropdown 的 Options 为空（会在代码中动态添加）  
3. 脚本挂到任意 GameObject，拖入引用  
4. Play 测试：选择不同职业，描述文字实时更新

---

### 案例 3：交互反馈 — 事件接口实现

**功能**：实现 IPointerEnter/IPointerExit 接口，鼠标悬停时改变按钮颜色，离开时恢复。

```csharp
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

public class HoverButton : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler
{
    [SerializeField] private Image _buttonImage;       // 按钮图片
    [SerializeField] private Color _normalColor = Color.white;      // 正常颜色
    [SerializeField] private Color _hoverColor = Color.gray;        // 悬停颜色

    void Start()
    {
        _buttonImage.color = _normalColor;
    }

    public void OnPointerEnter(PointerEventData eventData)
    {
        _buttonImage.color = _hoverColor;
    }

    public void OnPointerExit(PointerEventData eventData)
    {
        _buttonImage.color = _normalColor;
    }
}
```

#### 语法拆解

##### `public class HoverButton : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler` 是什么？

```csharp
public class HoverButton : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler
```

| 部分 | 含义 |
|------|------|
| `MonoBehaviour` | 继承自 MonoBehaviour（Unity 脚本基类） |
| `IPointerEnterHandler` | 实现指针进入接口 |
| `IPointerExitHandler` | 实现指针离开接口 |

**整行人话**：这个脚本同时实现了「指针进入」和「指针离开」两个接口。

---

##### `public void OnPointerEnter(PointerEventData eventData)` 是什么？

```csharp
public void OnPointerEnter(PointerEventData eventData)
```

| 部分 | 含义 |
|------|------|
| `public` | 公开方法（接口要求） |
| `void` | 返回值为空 |
| `OnPointerEnter` | 接口方法名（指针进入时调用） |
| `PointerEventData` | 参数：包含指针事件的详细信息 |

**整行人话**：鼠标进入控件时，自动调用这个方法。

---

#### 逐行详解

| 行 | 代码 | 含义 |
|----|------|------|
| 5 | Image 引用和颜色变量 | Inspector 拖入 |
| 9 | `Start()` | 初始化颜色 |
| 11 | 设置正常颜色 | — |
| 14 | `OnPointerEnter` | 指针进入时调用 |
| 16 | 设置悬停颜色 | — |
| 19 | `OnPointerExit` | 指针离开时调用 |
| 21 | 恢复正常颜色 | — |

#### 操作提示

1. Canvas 下创建一个 Image（或 Button）  
2. 脚本挂到该 Image 上  
3. 在 Inspector 中设置 Normal Color 和 Hover Color  
4. Play 测试：鼠标悬停时颜色变化，离开时恢复

---

## 【入门阶段小结】

| 维度 | 要点 |
|------|------|
| **InputField** | `text` 控制内容，`onEndEdit` 事件，`contentType` 输入类型 |
| **Dropdown** | `value` 控制选中索引，`options` 管理选项，`RefreshShownValue` 刷新显示 |
| **EventSystem** | 场景中必须有一个，管理所有交互事件 |
| **事件接口** | 通过实现接口响应交互，如 IPointerEnterHandler |
| **案例** | 登录验证、角色选择、悬停反馈 |

---

# 第三阶段：进阶篇

## 【阶段总述】

进阶阶段：**自定义输入验证**、**Dropdown 动态选项管理**、**拖拽系统实现**、**事件优先级**、**常见踩坑清单**。

---

## 一、自定义输入验证

### 1.1 限制输入格式（正则表达式）

```csharp
using System.Text.RegularExpressions;

public void OnInputChanged(string text)
{
    string pattern = @"^[a-zA-Z0-9_]*$";
    if (!Regex.IsMatch(text, pattern))
    {
        inputField.text = Regex.Replace(text, @"[^a-zA-Z0-9_]", "");
    }
}
```

### 1.2 实时搜索过滤

```csharp
public void OnSearchChanged(string keyword)
{
    foreach (var item in allItems)
    {
        item.SetActive(item.name.Contains(keyword));
    }
}
```

---

## 二、Dropdown 高级用法

### 2.1 带图标的选项

```csharp
Sprite warriorIcon = Resources.Load<Sprite>("Icons/Warrior");
dropdown.options.Add(new Dropdown.OptionData("战士", warriorIcon));
```

### 2.2 多级下拉（模拟）

```csharp
public Dropdown mainDropdown;
public Dropdown subDropdown;

void OnMainChanged(int index)
{
    subDropdown.options.Clear();
    
    switch (index)
    {
        case 0: // 战士
            subDropdown.options.Add(new Dropdown.OptionData("狂暴"));
            subDropdown.options.Add(new Dropdown.OptionData("防御"));
            break;
        case 1: // 法师
            subDropdown.options.Add(new Dropdown.OptionData("火法"));
            subDropdown.options.Add(new Dropdown.OptionData("冰法"));
            break;
    }
    
    subDropdown.RefreshShownValue();
}
```

---

## 三、拖拽系统实现

### 3.1 拖拽源（实现 IBeginDragHandler、IDragHandler、IEndDragHandler）

```csharp
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

public class DragItem : MonoBehaviour, IBeginDragHandler, IDragHandler, IEndDragHandler
{
    private RectTransform _rectTransform;
    private CanvasGroup _canvasGroup;
    
    void Awake()
    {
        _rectTransform = GetComponent<RectTransform>();
        _canvasGroup = GetComponent<CanvasGroup>();
    }

    public void OnBeginDrag(PointerEventData eventData)
    {
        _canvasGroup.alpha = 0.5f;
        _canvasGroup.blocksRaycasts = false;
    }

    public void OnDrag(PointerEventData eventData)
    {
        _rectTransform.anchoredPosition += eventData.delta;
    }

    public void OnEndDrag(PointerEventData eventData)
    {
        _canvasGroup.alpha = 1f;
        _canvasGroup.blocksRaycasts = true;
        
        if (eventData.pointerCurrentRaycast.gameObject != null)
        {
            Debug.Log("拖放到了：" + eventData.pointerCurrentRaycast.gameObject.name);
        }
    }
}
```

### 3.2 拖拽目标（实现 IDropHandler）

```csharp
public class DropTarget : MonoBehaviour, IDropHandler
{
    public void OnDrop(PointerEventData eventData)
    {
        GameObject draggedObject = eventData.pointerDrag;
        if (draggedObject != null)
        {
            draggedObject.transform.SetParent(transform);
            draggedObject.GetComponent<RectTransform>().anchoredPosition = Vector2.zero;
            Debug.Log("物品已放入目标区域");
        }
    }
}
```

---

## 四、事件优先级

### 4.1 UnityEvent vs 事件接口

| 方式 | 优点 | 缺点 |
|------|------|------|
| **UnityEvent** | Inspector 绑定方便、无需写代码 | 灵活性差、不支持复杂逻辑 |
| **事件接口** | 灵活、支持复杂逻辑、可扩展 | 需要写代码、学习成本高 |

### 4.2 事件触发顺序

```
点击事件触发顺序：
  IPointerDownHandler → IPointerUpHandler → IPointerClickHandler
  
拖拽事件触发顺序：
  IPointerDownHandler → IBeginDragHandler → IDragHandler（多次）→ IEndDragHandler
```

---

## 五、常见误区与最佳实践

| 误区 | 正确做法 |
|------|----------|
| InputField 输入不显示 | 检查 Text 组件的 Font 是否正确；检查颜色是否与背景相同 |
| Dropdown 展开后不显示选项 | 检查 Template 是否正确设置；检查 Mask 组件是否遮挡 |
| 点击按钮没反应 | 检查 EventSystem 是否存在；检查 GraphicRaycaster 是否存在 |
| 拖拽时被其他控件遮挡 | 拖拽开始时设置 CanvasGroup.blocksRaycasts = false |
| InputField 回车不触发 onEndEdit | 检查 Line Type 是否为 Single Line |
| Dropdown 动态添加选项后显示异常 | 添加后调用 RefreshShownValue() |
| 事件接口不生效 | 确保脚本挂在有 Graphic 组件的 GameObject 上 |
| 多个控件重叠时事件冲突 | 调整 Canvas 的 Sort Order；使用 CanvasGroup 控制交互 |

---

## 【进阶阶段小结】

| 维度 | 要点 |
|------|------|
| 输入验证 | 正则表达式过滤、实时搜索 |
| Dropdown 高级 | 带图标选项、多级下拉 |
| 拖拽系统 | IBeginDragHandler/IDragHandler/IEndDragHandler/IDropHandler |
| 事件优先级 | UnityEvent vs 事件接口、触发顺序 |
| 避坑 | EventSystem、GraphicRaycaster、CanvasGroup |

---

# 【全文总结】

## 最重要的一行代码

```csharp
inputField.onEndEdit.AddListener(text => Debug.Log("输入完成：" + text));
```

| 部分 | 含义 |
|------|------|
| `onEndEdit` | 编辑结束事件 |
| `AddListener` | 添加回调 |
| `text => Debug.Log(...)` | Lambda 表达式：输入完成后打印文本 |

## 三阶段对照

| 阶段 | 代表案例 |
|------|----------|
| 零基础 | 认识四个概念、读懂基本代码 |
| 入门 | 登录验证、角色选择、悬停反馈 |
| 进阶 | 自定义验证、多级下拉、拖拽系统 |

## API 速查

| 控件/接口 | 常用代码 |
|-----------|----------|
| InputField | `inputField.text = ""` / `inputField.onEndEdit.AddListener` |
| Dropdown | `dropdown.value = 0` / `dropdown.options.Add()` / `dropdown.RefreshShownValue()` |
| IPointerEnterHandler | `OnPointerEnter(PointerEventData eventData)` |
| IPointerExitHandler | `OnPointerExit(PointerEventData eventData)` |
| IDragHandler | `OnDrag(PointerEventData eventData)` |
| IDropHandler | `OnDrop(PointerEventData eventData)` |

## 学习自检

- [ ] InputField 的 contentType 有哪些类型？分别适用于什么场景？
- [ ] Dropdown 的 value 是什么？怎么动态添加选项？
- [ ] EventSystem 的作用是什么？场景中可以有多个吗？
- [ ] IPointerEnterHandler 和 IPointerClickHandler 的区别？
- [ ] 拖拽系统需要实现哪些接口？各自的作用是什么？
- [ ] 为什么拖拽时需要设置 CanvasGroup.blocksRaycasts = false？

---

## 参考资料

| 类型 | 链接 |
|------|------|
| InputField 官方 Manual | https://docs.unity3d.com/Manual/script-InputField.html |
| Dropdown 官方 Manual | https://docs.unity3d.com/Manual/script-Dropdown.html |
| EventSystem 官方 Manual | https://docs.unity3d.com/Manual/EventSystem.html |
| 事件接口 API | https://docs.unity3d.com/ScriptReference/EventSystems.IPointerClickHandler.html |
| CanvasGroup | https://docs.unity3d.com/ScriptReference/UI.CanvasGroup.html |

---

*文档版本：与 major3/01_PlayerPrefs.md ~ 05_DoTween.md、Week2_Xmind、Week3_Xmind 同系列模板。*