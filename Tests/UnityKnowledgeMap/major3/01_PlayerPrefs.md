# PlayerPrefs 存档详解

> 参照：[Unity 官方 Scripting API - PlayerPrefs](https://docs.unity3d.com/ScriptReference/PlayerPrefs.html)  
> 学习路径：**零基础 → 入门 → 进阶**，每阶段采用 **总—分—总** 结构。  
> 讲解维度：**定义 → 本质 → 特点 → 适用场景 → 原理 → API → 步骤 → 案例 → 避坑**（进阶含 JsonUtility）。  
> 案例讲解：遵循 **案例代码讲解模板**（功能 → 代码 → 语法拆解 → 逐行详解 → 操作提示）。

---

## 【全文总述】

Unity 持久化有两条主线：**PlayerPrefs**（少量简单设置）与 **JsonUtility + JSON 文件**（打包后正式存档）。本文按讲师知识框架，从概念到实战逐层展开。

### 思维导图总览

```
Unity 数据持久化
│
├── PlayerPrefs（UnityEngine 静态类 — 轻量键值对持久化）
│   │
│   ├── 【知识维度】（讲师框架 — 完整版）
│   │   │
│   │   ├── 定义：Unity 内置轻量级键值对持久化工具
│   │   │   └── 官方描述：在多次游戏会话之间存储 Player Preferences（玩家偏好）的类
│   │   │       可将 string、float、integer 存入用户平台注册表（platform registry）
│   │   │
│   │   ├── 本质：Unity 对各平台「本地偏好存储 API」的统一封装
│   │   │   ├── 数据模型：Key（字符串名字）→ Value（int / float / string）
│   │   │   ├── 调用方式：静态类，全局唯一，不能 new，直接 PlayerPrefs.xxx() 调用
│   │   │   └── 存储链路：Set 写内存缓存 → Save 写入磁盘 → Get 读取恢复
│   │   │
│   │   ├── 官方定位：存玩家偏好（Preferences），非完整游戏存档系统
│   │   │   ├── 设计用途：音量、画质、语言、开关、简单标记
│   │   │   └── 官方警告：本地注册表存储，无加密，勿存敏感数据
│   │   │
│   │   ├── 特点
│   │   │   ├── 优势：API 极简（10 个方法）、跨平台统一接口、无需管理路径、跨会话保留
│   │   │   └── 局限：仅 3 种类型、无加密易篡改、WebGL 约 1MB、Key 过多难维护、Editor 与 Build 不同份
│   │   │
│   │   ├── 适用场景
│   │   │   ├── ✅ 适用：音量/音效、音乐开关、语言画质、历史最高分、首次启动标记、新手引导步骤
│   │   │   └── ❌ 不适用：关卡进度、背包列表、大量 Key、金币内购、频繁大量写入
│   │   │
│   │   ├── 核心原理：内存缓存 + 磁盘持久化（两步模型）
│   │   │   ├── SetInt/SetFloat/SetString → 先写入内存
│   │   │   ├── Save() → 将所有修改持久化到本地注册表/平台存储
│   │   │   └── GetXxx → 从内存/磁盘读取对应 Key 的值
│   │   │
│   │   ├── 核心 API 及参数（10 个静态方法）
│   │   │   ├── 写入：SetInt(key,value) / SetFloat(key,value) / SetString(key,value)
│   │   │   ├── 读取：GetInt(key) 没存过→0 | GetInt(key,default) 没存过→default
│   │   │   │         GetFloat / GetString 同上规律
│   │   │   ├── 检测：HasKey(key) → true 存过 / false 未存过
│   │   │   ├── 落盘：Save() 无参数，写入磁盘
│   │   │   └── 删除：DeleteKey(key) 删一条 | DeleteAll() 删全部（慎用）
│   │   │
│   │   ├── 标准使用步骤（四步）
│   │   │   ├── 步骤1 启动读档：Start/Awake → GetXxx(key, default) → 恢复到变量
│   │   │   ├── 步骤2 应用到游戏：变量 → AudioListener / UI / 游戏逻辑
│   │   │   ├── 步骤3 运行中修改：玩家操作 → SetXxx(key, value)
│   │   │   └── 步骤4 关键时刻存盘：Save()（设置变更 / 退出 / 关卡结束）
│   │   │
│   │   ├── 生命周期与调用时机
│   │   │   ├── Start/Awake：读取 PlayerPrefs，恢复设置
│   │   │   ├── UI 事件回调：Set + Save（滑条、开关按钮）
│   │   │   ├── OnApplicationQuit：Save 双保险
│   │   │   └── OnApplicationPause(true)：移动端切后台时 Save
│   │   │
│   │   ├── 平台差异与存储路径（由 Company Name + Product Name 决定）
│   │   │   ├── Windows Build：注册表 HKCU\Software\公司\产品（Key 名哈希）
│   │   │   ├── Windows Editor：注册表带 UnityEditor 前缀（与 Build 不是同一份）
│   │   │   ├── Android：SharedPreferences XML
│   │   │   ├── iOS：NSUserDefaults
│   │   │   ├── macOS：~/Library/Preferences/...plist
│   │   │   └── WebGL：IndexedDB，总量上限约 1MB
│   │   │
│   │   ├── 性能 / 安全 / 调试
│   │   │   ├── 性能：Get/Set 低开销；Save 涉及磁盘 I/O，勿每帧调用
│   │   │   ├── 安全：明文无加密，玩家可篡改，不存金币/内购/密码
│   │   │   └── 调试：Editor 菜单 DeleteAll；Build 版本实测跨会话
│   │   │
│   │   └── 选型、封装、避坑
│   │       ├── 选型：设置/最高分 → PlayerPrefs；关卡/背包 → JsonUtility + JSON
│   │       ├── 封装：PrefsKeys 常量 + GameSettings 静态属性
│   │       └── 避坑：Set 后 Save、Key 大小写一致、Get 用两参数重载、Build 实测
│   │
│   ├── 第一阶段：零基础（建立认知 + 读懂代码）
│   │   ├── 理解定义、本质、特点、适用场景
│   │   ├── 逐词读懂：PlayerPrefs.SetInt("Score", 100) 每个部分的含义
│   │   └── 跑通 Demo：分数每次 +10，验证跨会话持久化
│   │
│   ├── 第二阶段：入门（API + 步骤 + 案例）
│   │   ├── 10 个 API 及参数详解（Get 两个重载行为不同）
│   │   ├── 标准四步流程 + 生命周期调用时机
│   │   └── 实战案例：音乐开关（SetInt 0/1）/ 音量滑条（SetFloat）/ 历史最高分
│   │
│   └── 第三阶段：进阶（封装 + 选型 + JsonUtility）
│       ├── bool/enum 扩展存法 + PrefsKeys + GameSettings 封装
│       ├── 平台差异、性能、安全、调试与 Build 测试清单
│       ├── 选型决策：PlayerPrefs vs JsonUtility 分工
│       └── JsonUtility 打包正式存档（见下方分支）
│
└── JsonUtility + JSON 文件（Unity 内置 JSON 序列化 — 打包正式存档）
    │
    ├── 定义：UnityEngine 静态类，提供 C# 对象与 JSON 字符串的互转能力
    │   └── 配合 System.IO.File 将 JSON 写入 Application.persistentDataPath 下的 .json 文件
    │
    ├── 本质：对象序列化（Object → JSON 文本 → 磁盘文件）与反序列化（磁盘 → JSON → Object）
    │   └── 与 PlayerPrefs 区别：一个 JSON 文件存整个 SaveData 对象，而非散列 Key-Value
    │
    ├── 官方定位：轻量级 JSON 序列化工具，适合中等复杂度存档结构
    │   └── 存档类需 [Serializable] 标记，字段必须 public
    │
    ├── 特点
    │   ├── 优势：可读（JSON 文本）、支持多字段和 List、persistentDataPath 打包可靠、Unity 内置
    │   └── 局限：只序列化 public 字段、不支持 Dictionary/多态、存档类不能继承 MonoBehaviour
    │
    ├── 适用场景
    │   ├── ✅ 适用：关卡进度、金币血量、背包列表、多字段游戏存档、打包后跨会话读档
    │   └── ❌ 不适用：单个音量值（PlayerPrefs 更简单）、超大型数据（考虑二进制方案）
    │
    ├── 核心 API 及参数
    │   ├── JsonUtility.ToJson(obj) → 对象转 JSON 紧凑字符串
    │   ├── JsonUtility.ToJson(obj, prettyPrint) → prettyPrint=true 格式化缩进（调试用）
    │   ├── JsonUtility.FromJson<T>(json) → JSON 字符串还原为 T 类型对象
    │   ├── Application.persistentDataPath → 各平台统一的打包后可读写存档根目录
    │   ├── File.WriteAllText(path, json) → 写入 .json 文件
    │   ├── File.ReadAllText(path) → 读取整个文件为字符串
    │   └── File.Exists(path) → 判断存档文件是否存在
    │
    ├── 标准使用步骤（六步）
    │   ├── 步骤1 定义 [Serializable] 的 SaveData 类（public 字段）
    │   ├── 步骤2 运行时维护 SaveData 实例（currentData）
    │   ├── 步骤3 启动 Load：Exists? → ReadAllText → FromJson → 恢复数据
    │   ├── 步骤4 无存档时：new SaveData() 创建默认新游戏数据
    │   ├── 步骤5 存档 Save：CollectFromGame → ToJson → WriteAllText
    │   └── 步骤6 ApplyToGame：将 currentData 应用到游戏逻辑与 UI
    │
    ├── persistentDataPath（打包路径 — 必用）
    │   ├── 正确：Application.persistentDataPath + "/save.json"（打包后可读写）
    │   └── 错误：Application.dataPath（游戏安装目录，打包后只读，无法存档）
    │
    ├── 与 PlayerPrefs 配合使用
    │   ├── PlayerPrefs → 音量、语言、开关等少量设置
    │   └── JsonUtility + File → 关卡、金币、背包等完整游戏进度
    │
    └── 限制 + 打包测试清单
        ├── 限制：public 字段 only、无 Dictionary、无多态、SaveData 非 MonoBehaviour
        └── 测试：Build 版 Save→关游戏→Load；Debug.Log 路径；首次无存档走新游戏分支
```

| 学习阶段 | 学习目标 |
|----------|----------|
| **零基础** | 说清定义、本质、特点；逐词读懂 `PlayerPrefs.SetInt("Score", 100);` |
| **入门** | 掌握 API 参数差异、标准步骤、调用时机；独立完成 3 个案例 |
| **进阶** | 会封装、会选型、会调试；掌握 JsonUtility 打包存档全流程 |

### 讲师知识框架速览（全文脉络）

| 维度 | 零基础讲 | 入门讲 | 进阶讲 |
|------|----------|--------|--------|
| 定义 | ✅ | 回顾 | 回顾 |
| 本质 | ✅ | — | — |
| 特点 | ✅ | — | 性能/安全补充 |
| 适用场景 | ✅ | — | 选型决策 |
| 核心原理 | 初步 | ✅ 存储机制 | 平台路径 |
| 核心 API | 读懂一行 | ✅ 10 个全讲 | 封装 |
| 使用步骤 | Demo | ✅ 标准流程 | SaveManager |
| 调用时机 | — | ✅ | OnApplicationQuit 等 |
| 避坑/最佳实践 | — | 初步 | ✅ |

---

# 第一阶段：零基础篇

## 【阶段总述】

零基础阶段建立**正确认知**：PlayerPrefs 是什么、本质是什么、有什么特点、适合存什么。  
同时学会**逐词读懂** `PlayerPrefs.SetInt("Score", 100);`，并跑通第一个 Demo。

---

## 一、定义 — PlayerPrefs 是什么？

| 项目 | 说明 |
|------|------|
| **类名** | `PlayerPrefs` |
| **命名空间** | `UnityEngine` |
| **类型** | **静态类**（不能 `new`，直接 `PlayerPrefs.xxx()` 调用） |
| **官方定义** | 一个在**多次游戏会话之间**存储玩家偏好（Preferences）的类 |
| **存储模型** | **键值对（Key-Value）**：字符串 Key → 值（int / float / string） |
| **一句话** | Unity 内置的「本地小账本」，关游戏后数据仍在 |

```csharp
// PlayerPrefs 的标准调用形式
PlayerPrefs.SetInt("Score", 100);
//  ↑类名      ↑方法   ↑Key  ↑Value
```

---

## 二、本质 — 底层到底是什么？

### 2.1 与普通变量的本质区别

| 对比项 | 普通变量 | PlayerPrefs |
|--------|----------|-------------|
| 存储位置 | 内存（RAM） | 内存缓存 + 本地持久化存储 |
| 关游戏后 | 清空 | **保留** |
| 跨场景 | 需 DontDestroyOnLoad 等 | 任意场景可直接读写 |
| 数据形式 | C# 任意类型 | 仅 int / float / string |

### 2.2 本质：键值对 + 平台本地存储

```
你的代码：PlayerPrefs.SetInt("MusicOn", 1)
                    │
                    ▼
            Unity 内存缓存（运行时读写）
                    │
                    ▼ Save()
            平台本地存储（跨会话保留）
            ├── Windows → 注册表
            ├── Android → SharedPreferences XML
            ├── iOS     → NSUserDefaults
            └── WebGL   → IndexedDB（约 1MB 上限）
```

**本质理解**：PlayerPrefs 是 Unity 对「各平台本地偏好存储 API」的**统一封装**，你只管 Key-Value，Unity 负责适配平台。

### 2.3 键值对规则

| 你起的名字（Key） | 要存的值（Value） | 含义 |
|-------------------|-------------------|------|
| `"MusicOn"` | `1` | 音乐开 |
| `"Volume"` | `0.8f` | 音量 80% |
| `"Score"` | `100` | 分数 100 |

**规则**：读写 Key 必须**完全一致**（大小写敏感）。

---

## 三、官方定位 — 设计来干什么？

Unity 官方将其定位为 **Player Preferences（玩家偏好）**，不是完整游戏存档系统。

| 官方意图 | 说明 |
|----------|------|
| ✅ 设计目的 | 音量、画质、语言、开关、简单标记 |
| ❌ 非设计目的 | 关卡进度、背包、任务链、大量游戏数据 |
| 官方原话 | 本地存储，**无加密**，不要存敏感数据 |

> **说明**：PlayerPrefs 的设计用途是存玩家偏好（Preferences），不宜当作完整游戏存档。复杂进度应使用 JsonUtility + JSON 文件（进阶篇）。

---

## 四、特点 — 优势与局限

### 4.1 优势

| 特点 | 说明 |
|------|------|
| **极简 API** | 10 个静态方法，上手快 |
| **跨平台统一** | 同一套代码，Unity 适配各平台存储 |
| **无需路径管理** | 不用自己找文件夹，Unity 自动处理 |
| **跨会话** | 关游戏再开，数据仍在 |
| **小数据读写快** | 几个设置项读写几乎无感 |

### 4.2 局限

| 特点 | 说明 |
|------|------|
| **仅 3 种类型** | int / float / string，无 bool / Vector3 / 自定义类 |
| **无加密** | 明文存储，玩家可篡改 |
| **数据量有限** | WebGL 约 1MB；Key 过多难维护 |
| **非正式存档** | 不适合复杂游戏进度 |
| **Editor ≠ Build** | 编辑器与打包后存储路径不同 |

---

## 五、适用场景 vs 不适用场景

### ✅ 适用场景

| 场景 | 示例 Key | 存法 |
|------|----------|------|
| 音量 / 音效 | `"MasterVolume"` | SetFloat |
| 音乐 / 音效开关 | `"MusicOn"` | SetInt(0/1) |
| 语言 / 画质 | `"Language"` | SetString / SetInt |
| 历史最高分 | `"HighScore"` | SetInt |
| 首次启动标记 | `"HasLaunched"` | HasKey + SetInt |
| 新手引导步骤 | `"TutorialStep"` | SetInt |

### ❌ 不适用场景

| 场景 | 原因 | 应改用 |
|------|------|--------|
| 关卡 + 背包 + 任务 | 字段多、结构复杂 | JsonUtility + JSON |
| 100+ 个独立 Key | 维护噩梦 | 一个 JSON 文件 |
| 金币 / 内购凭证 | 无加密，易篡改 | 服务端校验 + 本地缓存 |
| 大量频繁写入 | I/O 有开销 | 内存缓存 + 定时 Save |

---

## 六、核心一课：如何读懂一行代码

```csharp
PlayerPrefs.SetInt("Score", 100);
```

```
PlayerPrefs . SetInt ( "Score" , 100 ) ;
    ①      ②   ③      ④       ⑤    ⑥
```

| 序号 | 部分 | 含义 |
|:----:|------|------|
| ① | `PlayerPrefs` | 类名：Unity 存档工具箱 |
| ② | `.` | 调用该类的方法 |
| ③ | `SetInt` | Set（写入）+ Int（整数） |
| ④ | `"Score"` | 参数1 Key：数据名字 |
| ⑤ | `100` | 参数2 Value：要存的整数 |
| ⑥ | `;` | C# 语句结束 |

**翻译**：在账本里把 `"Score"` 设为 `100`（先写内存，需 `Save()` 才落盘）。

```csharp
PlayerPrefs.SetInt("Score", 100);   // 记账
PlayerPrefs.Save();                 // 存银行
```

### 读数据的代码

```csharp
int score = PlayerPrefs.GetInt("Score", 0);
//  ↑变量  ↑工具箱  ↑读整数  ↑Key  ↑默认值（没存过时用）
```

### 静态类 — 不能 new

```csharp
// ❌ PlayerPrefs p = new PlayerPrefs();
// ✅ 
PlayerPrefs.SetInt("Score", 100);
```

---

## 七、零基础第一个案例

**功能**：每次运行给分数 +10，验证 PlayerPrefs 跨会话持久化。

```csharp
using UnityEngine;                              // 引入 Unity 核心库（PlayerPrefs、MonoBehaviour 都在里面）

public class FirstPrefsDemo : MonoBehaviour     // 定义脚本类，继承 MonoBehaviour 才能挂到物体上
{
    void Start()                                // Start：物体启用后、第一帧 Update 前自动执行一次
    {
        int score = PlayerPrefs.GetInt("MyScore", 0);   // 读存档：Key="MyScore"，没存过则默认 0
        score += 10;                            // 在原有分数上加 10
        PlayerPrefs.SetInt("MyScore", score);  // 写存档：把新分数存回 Key="MyScore"
        PlayerPrefs.Save();                    // 落盘：写入硬盘，关游戏后再开还在
        Debug.Log("当前分数：" + score);       // 在 Console 窗口打印日志
    }
}
```

#### 语法拆解

##### `: MonoBehaviour` 是什么？

```csharp
public class FirstPrefsDemo : MonoBehaviour
```

| 部分 | 含义 |
|------|------|
| `public class FirstPrefsDemo` | 声明公开类，类名须与 `.cs` 文件名一致 |
| `: MonoBehaviour` | 继承 MonoBehaviour，脚本可挂载到 Hierarchy 中的 GameObject |

**整行人话**：把脚本变成可挂载组件，Unity 才会调用其中的 `Start()` 等方法。

---

##### `score += 10;` 是什么？

```csharp
score += 10;
```

| 部分 | 含义 |
|------|------|
| `score` | 变量名 |
| `+=` | 复合赋值：先加再赋回，等价于 `score = score + 10` |
| `10` | 加的整数 |

**整行人话**：在当前分数基础上加 10 分。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用 Unity 引擎命名空间 |
| 3 | `public class FirstPrefsDemo : MonoBehaviour` | 见上方语法拆解 |
| 5 | `void Start()` | 生命周期函数，游戏开始时自动调用一次 |
| 7 | `GetInt("MyScore", 0)` | 读 Key；没存过返回 0 |
| 8 | `score += 10` | 见上方语法拆解 |
| 9 | `SetInt("MyScore", score)` | 写入 PlayerPrefs |
| 10 | `Save()` | 持久化到磁盘 |
| 11 | `Debug.Log(...)` | Console 输出调试信息 |

| 运行次数 | 输出 | 说明 |
|----------|------|------|
| 第 1 次 | 10 | 默认 0 → +10 |
| 第 2 次 | 20 | 读到 10 → +10 |
| 第 3 次 | 30 | 跨会话持久化成功 |

---

## 【零基础阶段小结】

| 维度 | 要点 |
|------|------|
| **定义** | 静态类，Key-Value 本地存储 |
| **本质** | Unity 对各平台偏好存储的统一封装 |
| **特点** | 简单跨平台，但仅 3 类型、无加密、非正式存档 |
| **适用** | 设置、开关、最高分；**不适用**复杂进度 |
| **代码** | `SetInt("Score",100)` = Key 名字 + Value 值 |

**阶段检验**：能回答定义/本质/特点/适用场景，并逐词读懂 `SetInt("Score", 100)`。

---

# 第二阶段：入门篇

## 【阶段总述】

入门阶段深入 **核心原理、10 个 API 及参数、标准使用步骤、调用时机**，并完成 3 个实战案例。  
需掌握：**Get 两个重载的参数不同，行为就不同**。

---

## 一、核心原理 — 内存与磁盘两步模型

```
SetInt("Score", 100)
       │
       ▼
  ┌──────────┐
  │ 内存缓存  │ ← GetInt 从这里读（即时）
  └────┬─────┘
       │ Save()
       ▼
  ┌──────────┐
  │ 磁盘持久化 │ ← 关游戏后再开从这里恢复
  └──────────┘
```

| 操作 | 作用 | 是否跨会话 |
|------|------|------------|
| Set | 写内存 | 本次运行内有效；崩溃可能丢 |
| Save | 内存 → 磁盘 | ✅ 关游戏仍在 |
| Get | 读内存（或首次从磁盘加载到内存） | — |

**口诀**：Set 记账，Save 存银行。

---

## 二、核心 API 及参数详解

### API 全景

```
PlayerPrefs（10 个静态方法）
├── 写入：SetInt / SetFloat / SetString       参数：(key, value)
├── 读取：GetInt / GetFloat / GetString       1 参数 or 2 参数（行为不同！）
├── 检测：HasKey(key)
├── 落盘：Save()
└── 删除：DeleteKey(key) / DeleteAll()
```

---

### 2.1 写入 API — Set 系列

三个方法结构相同：**参数1 = key（名字），参数2 = value（值）**。

#### SetInt

```csharp
PlayerPrefs.SetInt(string key, int value);
```

```csharp
PlayerPrefs.SetInt("Score", 100);
//                 ↑Key     ↑Value（int）
PlayerPrefs.SetInt("MusicOn", 1);    // 开关：1=开
PlayerPrefs.Save();
```

#### SetFloat

```csharp
PlayerPrefs.SetFloat(string key, float value);
```

```csharp
PlayerPrefs.SetFloat("Volume", 0.8f);
//                   ↑Key      ↑Value（必须加 f）
PlayerPrefs.Save();
```

#### SetString

```csharp
PlayerPrefs.SetString(string key, string value);
```

```csharp
PlayerPrefs.SetString("Language", "zh-CN");
//                     ↑Key        ↑Value（双引号字符串）
PlayerPrefs.Save();
```

| 方法 | 参数1 key | 参数2 value | 类型要求 |
|------|-----------|-------------|----------|
| SetInt | 数据名字 | 整数值 | int |
| SetFloat | 数据名字 | 小数值 | float（加 `f`） |
| SetString | 数据名字 | 文字内容 | string（双引号） |

**注意**：同一 Key 多次 Set，**后者覆盖前者**（不是累加）。

---

### 2.2 读取 API — Get 系列（两个重载，行为不同）

#### GetInt — 两个重载

```csharp
// 重载1：只有 key
int a = PlayerPrefs.GetInt("Score");        // 没存过 → 固定返回 0

// 重载2：key + defaultValue（推荐）
int b = PlayerPrefs.GetInt("Score", 0);     // 没存过 → 返回 0（你指定的）
int c = PlayerPrefs.GetInt("Level", 1);     // 没存过 → 返回 1（首次从第1关开始）
```

| 对比 | `GetInt(key)` | `GetInt(key, defaultValue)` |
|------|---------------|----------------------------|
| 参数 | 1 个 | 2 个 |
| Key 不存在 | 固定返回 `0` | 返回 `defaultValue` |
| Key 存在 | 返回存的值 | 返回存的值（忽略 default） |
| 推荐 | 确定 0 合理时 | **大多数情况** |

```csharp
// 对比案例
// 从未存过 "Coins"：
GetInt("Coins")      → 0
GetInt("Coins", 100) → 100

// 已 SetInt("Coins", 50)：
GetInt("Coins")      → 50
GetInt("Coins", 100) → 50（100 被忽略）
```

#### GetFloat / GetString — 同样规律

| 方法 | 1 参数（没存过） | 2 参数（没存过） |
|------|------------------|------------------|
| GetFloat | → `0.0f` | → 你指定的 default |
| GetString | → `""` | → 你指定的 default |

```csharp
float vol = PlayerPrefs.GetFloat("Volume", 1.0f);      // 默认满音量
string lang = PlayerPrefs.GetString("Language", "en"); // 默认英文
```

---

### 2.3 HasKey — 检测是否存过

```csharp
bool exists = PlayerPrefs.HasKey("Score");
//                              ↑参数：Key 名字
// 返回 true = 存过；false = 从没存过
```

| 用法 | 场景 |
|------|------|
| `GetInt(key, default)` | 只需默认值，简单场景 |
| `HasKey(key)` | 区分「首次启动」vs「老玩家」 |

---

### 2.4 Save — 落盘

```csharp
PlayerPrefs.Save();   // 无参数：所有 Set 的修改写入磁盘
```

| 调用时机 | 说明 |
|----------|------|
| 设置变更后 | 玩家改音量/开关后立即 Save |
| 关卡结束 | 更新分数后 Save |
| 退出游戏 | `OnApplicationQuit` 中 Save（双保险） |
| ❌ 不要 | 每帧 Save（I/O 开销大） |

---

### 2.5 DeleteKey / DeleteAll — 删除

```csharp
PlayerPrefs.DeleteKey("Score");   // 参数：Key → 删一条
PlayerPrefs.DeleteAll();          // 无参数 → 删全部
PlayerPrefs.Save();
```

---

## 三、标准使用步骤

### 3.1 四步流程

```
步骤1【启动读档】 Start/Awake  →  GetXxx(key, default)  →  恢复到变量
步骤2【应用到游戏】           →  把变量赋给 AudioListener / UI 等
步骤3【运行中修改】           →  玩家操作  →  SetXxx(key, value)
步骤4【关键时刻存盘】         →  Save()
```

### 3.2 流程图

```
游戏启动 → Get 读取 → 应用到游戏
              ↓
         玩家改设置 → Set 写内存
              ↓
    设置变更 / 退出 / 关卡结束 → Save 落盘
```

---

## 四、生命周期与调用时机

| Unity 回调 | 适合做什么 | 示例 |
|------------|------------|------|
| `Awake()` / `Start()` | **读取** PlayerPrefs，恢复设置 | `GetFloat("Volume", 1f)` |
| UI 事件 / 按钮回调 | **写入** + **Save** | 滑条 OnValueChanged |
| `OnDisable()` | 可选：保存当前状态 | 场景切换前 |
| `OnApplicationQuit()` | **Save** 双保险 | 退出时再存一次 |
| `OnApplicationPause(true)`（移动端） | 切后台时 Save | 防杀进程丢数据 |

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

**语法拆解的标准格式**（遇到 `[Range]`、`? :`、`const` 等不熟悉的写法时使用）：

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

### 案例 1：音乐开关

**功能**：点击按钮切换音乐开/关，关游戏后再开仍然记住状态。

```csharp
using UnityEngine;                              // 引用 Unity 库

public class MusicSwitch : MonoBehaviour        // 脚本类，可挂载到场景物体
{
    public bool isMusicOn;                      // 公开 bool 变量：当前音乐是否开启（Inspector 可见）
    private const string KEY = "MusicOn";       // 私有常量：PlayerPrefs 里用的 Key 名字，防止写错

    void Start()                                // 游戏启动时执行
    {
        int saved = PlayerPrefs.GetInt(KEY, 1); // 读整数：Key="MusicOn"，默认 1（首次默认开）
        isMusicOn = (saved != 0);               // 转换：saved 不等于 0 → true（开），等于 0 → false（关）
    }

    public void OnToggleClick()                 // 公开方法：可绑定到 UI 按钮的 OnClick 事件
    {
        isMusicOn = !isMusicOn;                 // 取反：开变关，关变开
        PlayerPrefs.SetInt(KEY, isMusicOn ? 1 : 0);  // 写入：开→1，关→0
        PlayerPrefs.Save();                     // 落盘保存
    }
}
```

#### 语法拆解

##### `private const string KEY = "MusicOn";` 是什么？

```csharp
private const string KEY = "MusicOn";
```

| 部分 | 含义 |
|------|------|
| `private` | 仅本脚本内部可用，外部类不能直接访问 |
| `const` | 常量，编译后值固定，运行中不能修改 |
| `string` | 字符串类型 |
| `KEY` | 变量名，惯例用大写表示「存档 Key 常量」 |
| `= "MusicOn"` | 赋值为字符串 `"MusicOn"`，读写 PlayerPrefs 时都用此名字 |

**整行人话**：定义一个本脚本专用的、不可改的存档 Key 名字，避免 `"MusicOn"` 在代码里散落拼错。

---

##### `(saved != 0)` 是什么？

```csharp
isMusicOn = (saved != 0);
```

| 部分 | 含义 |
|------|------|
| `saved` | 从 PlayerPrefs 读出的 int 值（1 或 0） |
| `!=` | 不等于比较运算符 |
| `0` | 整数零 |
| `(saved != 0)` | 表达式结果为 bool：saved 为 1 时 true，为 0 时 false |
| `isMusicOn = ...` | 把 bool 结果赋给开关变量 |

**整行人话**：把 PlayerPrefs 里的 1/0 转换成 bool 类型的开/关状态。

---

##### `isMusicOn ? 1 : 0` 是什么？

```csharp
PlayerPrefs.SetInt(KEY, isMusicOn ? 1 : 0);
```

| 部分 | 含义 |
|------|------|
| `isMusicOn ? 1 : 0` | 三元运算符：条件 ? 真时的值 : 假时的值 |
| `isMusicOn` | 条件：true 或 false |
| `? 1` | 条件为 true 时，整个表达式结果是 1 |
| `: 0` | 条件为 false 时，整个表达式结果是 0 |

**整行人话**：音乐开则存 1，关则存 0，一行完成 bool → int 转换。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 4 | `public bool isMusicOn` | 声明 bool 变量，表示音乐开关状态 |
| 5 | `private const string KEY` | 存档 Key 常量，见上方语法拆解 |
| 7 | `void Start()` | 进入 Play 模式后调用一次 |
| 9 | `GetInt(KEY, 1)` | 读 Key；第二个参数 1 = 首次默认开 |
| 10 | `(saved != 0)` | int 转 bool，见上方语法拆解 |
| 13 | `public void OnToggleClick()` | 按钮 OnClick 绑定的方法 |
| 15 | `!isMusicOn` | 逻辑非，取反开/关 |
| 16 | `isMusicOn ? 1 : 0` | 三元运算，见上方语法拆解 |
| 17 | `Save()` | 写入硬盘 |

#### 操作提示

在 UI Button 的 On Click 事件中添加 `MusicSwitch.OnToggleClick`，并拖入挂有此脚本的物体。

---

### 案例 2：音量滑条

**功能**：拖动 UI 滑条调节音量，音量写入 PlayerPrefs，并同步到 `AudioListener`。

```csharp
using UnityEngine;                              // 引用 Unity 库

public class VolumeControl : MonoBehaviour      // 脚本类，挂到有 Slider 逻辑的物体上
{
    [Range(0f, 1f)] public float volume = 1f;  // 见下方语法拆解
    private const string KEY = "MasterVolume";  // PlayerPrefs 的 Key：主音量

    void Start()                                // 游戏启动时：先读存档，再应用到声音
    {
        volume = PlayerPrefs.GetFloat(KEY, 1.0f);  // 读小数：默认 1.0f = 100% 音量
        AudioListener.volume = volume;          // 设置全局音量（0=静音，1=最大）
    }

    public void OnSliderChanged(float newValue) // UI Slider 拖动时调用，newValue 是滑条当前值
    {
        volume = newValue;                      // 更新内存里的音量变量
        PlayerPrefs.SetFloat(KEY, volume);      // 写入 PlayerPrefs（Key + float 值）
        PlayerPrefs.Save();                     // 落盘
        AudioListener.volume = volume;          // 立刻听到音量变化
    }
}
```

#### 语法拆解

##### `[Range(0f, 1f)] public float volume = 1f;` 是什么？

```csharp
[Range(0f, 1f)] public float volume = 1f;
```

| 部分 | 含义 |
|------|------|
| `[Range(0f, 1f)]` | Unity 特性（Attribute），写在字段上一行，给 Inspector 面板加显示效果 |
| `Range` | 「范围」：限制数值在最小值与最大值之间 |
| `0f` | 最小值 0.0（float 类型，数字后的 `f` 不能省） |
| `1f` | 最大值 1.0 |
| **Inspector 效果** | `volume` 显示为 0~1 的滑动条，而非普通输入框 |
| `public float volume` | 公开的小数变量，名为 volume（音量） |
| `= 1f` | 默认值 1.0，即 100% 音量 |

**整行人话**：声明一个 0~1 之间的音量变量，默认满音量；Inspector 中用滑条便于调试。

**说明**：`[Range]` 仅影响 Editor 中 Inspector 的显示，不影响 PlayerPrefs 读写；打包后玩家通过 UI Slider 调音量，走 `OnSliderChanged` 方法。

---

##### `AudioListener.volume = volume;` 是什么？

```csharp
AudioListener.volume = volume;
```

| 部分 | 含义 |
|------|------|
| `AudioListener` | Unity 全局音频监听类，控制整个游戏的音量 |
| `.volume` | 音量属性，取值 0.0（静音）~ 1.0（最大） |
| `= volume` | 把脚本里的 volume 变量赋给全局音量 |

**整行人话**：把存档/滑条里的音量值应用到游戏实际声音输出。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 4 | `[Range(0f, 1f)] public float volume = 1f` | 见上方语法拆解 |
| 5 | `KEY = "MasterVolume"` | 存档 Key，与 SetFloat/GetFloat 对应 |
| 9 | `GetFloat(KEY, 1.0f)` | 读音量；没存过 → 默认 1.0f |
| 10 | `AudioListener.volume = volume` | 见上方语法拆解 |
| 13 | `OnSliderChanged(float newValue)` | Slider 的 OnValueChanged 传入当前值 |
| 15~17 | SetFloat + Save + AudioListener | 更新变量、写存档、立刻生效 |

#### 操作提示

在 Slider 的 On Value Changed 里添加 `VolumeControl.OnSliderChanged`，并拖入挂有此脚本的物体。

---

### 案例 3：历史最高分

**功能**：本局结束时，若分数超过历史最高，则更新并保存。

```csharp
using UnityEngine;                              // 引用 Unity 库

public class HighScore : MonoBehaviour          // 脚本类
{
    private const string KEY = "HighScore";     // PlayerPrefs Key：历史最高分

    public void OnGameOver(int currentScore)    // 本局结束时外部调用，传入本局得分
    {
        int best = PlayerPrefs.GetInt(KEY, 0);  // 读历史最高分，默认 0（从没玩过）
        if (currentScore > best)                // if：条件为真才执行大括号里的代码
        {
            PlayerPrefs.SetInt(KEY, currentScore);  // 本局更高，写入新纪录
            PlayerPrefs.Save();                 // 落盘
        }
    }
}
```

#### 语法拆解

##### `public void OnGameOver(int currentScore)` 是什么？

```csharp
public void OnGameOver(int currentScore)
```

| 部分 | 含义 |
|------|------|
| `public` | 公开方法，其他脚本可调用 |
| `void` | 无返回值 |
| `OnGameOver` | 方法名，表示「游戏结束时」 |
| `(int currentScore)` | 参数：调用时必须传入一个 int，代表本局得分 |

**整行人话**：定义一个接收本局分数的公开方法，供 GameManager 在游戏结束时调用。

---

##### `if (currentScore > best)` 是什么？

```csharp
if (currentScore > best)
{
    // ...
}
```

| 部分 | 含义 |
|------|------|
| `if` | 条件判断：只有条件为 true 才执行 `{ }` 内代码 |
| `currentScore > best` | 本局分数是否大于历史最高分 |
| `{ }` | 条件成立时执行的代码块 |

**整行人话**：只有破纪录时才更新 PlayerPrefs，避免无效写入。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 5 | `private const string KEY` | 常量 Key `"HighScore"` |
| 7 | `OnGameOver(int currentScore)` | 见上方语法拆解 |
| 9 | `GetInt(KEY, 0)` | 读历史最高分，默认 0 |
| 10 | `if (currentScore > best)` | 见上方语法拆解 |
| 12~13 | SetInt + Save | 写入新纪录并落盘 |

#### 操作提示

在 GameManager 游戏结束时调用：`GetComponent<HighScore>().OnGameOver(本局分数);`

---

## 【入门阶段小结】

| 维度 | 要点 |
|------|------|
| **原理** | Set → 内存；Save → 磁盘；Get 从内存读 |
| **API** | Set(key,value)；Get(key) vs Get(key,default)；HasKey；Save；Delete |
| **步骤** | 启动读 → 应用 → 修改 Set → 关键节点 Save |
| **时机** | Start 读；UI 事件写+Save；Quit 双保险 |

---

# 第三阶段：进阶篇

## 【阶段总述】

进阶阶段补齐讲师框架的剩余维度：**工程化封装、平台差异、性能、安全、调试、选型**，并完整讲解 **JsonUtility 打包存档**（同样按定义→本质→特点→API→步骤展开）。

---

## 一、PlayerPrefs 进阶维度

### 1.1 类型扩展：bool 与 enum

```csharp
// bool → int（PlayerPrefs 无 SetBool）
PlayerPrefs.SetInt("MusicOn", isOn ? 1 : 0);
bool isOn = PlayerPrefs.GetInt("MusicOn", 1) != 0;

// enum → int
PlayerPrefs.SetInt("Difficulty", (int)Difficulty.Hard);
Difficulty d = (Difficulty)PlayerPrefs.GetInt("Difficulty", 0);
```

### 1.2 工程化封装

**Key 常量** — 防止 `"Score"` / `"score"` 变成两个 Key：

```csharp
public static class PrefsKeys
{
    public const string Score   = "Score";
    public const string Volume  = "MasterVolume";
    public const string MusicOn = "MusicOn";
}
```

**静态属性** — 读写 + Save 一体化：

```csharp
public static class GameSettings
{
    public static float MasterVolume
    {
        get => PlayerPrefs.GetFloat(PrefsKeys.Volume, 1.0f);
        set { PlayerPrefs.SetFloat(PrefsKeys.Volume, value); PlayerPrefs.Save(); }
    }
}
```

### 1.3 平台差异与存储路径

由 **Edit → Project Settings → Player** 的 Company Name + Product Name 决定：

| 平台 | 存储位置 |
|------|----------|
| Windows Build | 注册表 `HKCU\Software\公司\产品` |
| Windows Editor | 注册表带 `UnityEditor`（**与 Build 不同**） |
| Android | SharedPreferences XML |
| iOS | NSUserDefaults |
| WebGL | IndexedDB（**约 1MB 上限**） |

### 1.4 性能考量

| 操作 | 性能影响 | 建议 |
|------|----------|------|
| Get | 低（内存读） | 可频繁调用 |
| Set | 低（内存写） | 正常 |
| Save | **中偏高**（磁盘 I/O） | 只在关键节点调用，**不要每帧** |
| 大量 Key | 维护成本高 | 换 JSON 文件 |

### 1.5 安全性

| 事实 | 应对 |
|------|------|
| 本地明文，无加密 | 不存金币、内购、密码 |
| 客户端可篡改 | 单机休闲影响小；联网需服务端校验 |
| Windows Key 名哈希 | 调试用代码 Log，勿手动改注册表 |

### 1.6 调试与测试

```csharp
#if UNITY_EDITOR
using UnityEditor;
public static class PrefsEditorTool
{
    [MenuItem("Tools/清除全部 PlayerPrefs")]
    static void ClearAll()
    {
        PlayerPrefs.DeleteAll();
        Debug.Log("PlayerPrefs 已清空");
    }
}
#endif
```

**测试清单**：

- [ ] Editor Play 测功能逻辑
- [ ] **Build 版本**测跨会话（Editor 与 Build 存档不互通）
- [ ] 首次运行（无 Key）默认值是否正确
- [ ] 杀进程后数据是否丢失（没 Save 的情况）

### 1.7 选型决策

```
需要持久化？
  ├─ 仅跨场景 → DontDestroyOnLoad / 静态变量
  └─ 跨会话
       ├─ 少量简单值（设置/最高分）→ PlayerPrefs
       └─ 复杂进度（关卡/背包）→ JsonUtility + JSON 文件
```

| 要存什么 | 方案 |
|----------|------|
| 音量、语言、开关 | PlayerPrefs |
| 关卡、金币、背包 | JsonUtility + persistentDataPath |

### 1.8 常见误区与最佳实践

| 误区 | 正确做法 |
|------|----------|
| Set 后不 Save | 关键操作后立刻 Save |
| Key 大小写不一致 | 用 PrefsKeys 常量 |
| 用 PlayerPrefs 存完整进度 | 换 JSON 文件 |
| 只在 Editor 测存档 | Build 后实测 |
| 每帧 Save | 仅在变更/退出时 Save |

---

## 二、JsonUtility 打包存档（完整知识框架）

PlayerPrefs 边界之外，正式游戏进度用 **JsonUtility + JSON 文件 + persistentDataPath**。

---

### 2.1 定义 — JsonUtility 是什么？

| 项目 | 说明 |
|------|------|
| **类名** | `JsonUtility`（UnityEngine 命名空间） |
| **类型** | 静态类 |
| **官方定义** | Unity 内置的 **JSON 序列化/反序列化** 工具 |
| **一句话** | 把 C# 对象 ↔ JSON 字符串互转，再配合 File 写入磁盘 |

---

### 2.2 本质 — 与 PlayerPrefs 的本质区别

| 对比 | PlayerPrefs | JsonUtility + File |
|------|-------------|---------------------|
| 数据形式 | Key-Value 散列 | **一个 JSON 文件**存整个对象 |
| 数据类型 | int/float/string | **可序列化类的多个字段** |
| 路径 | Unity 自动管理 | 你指定 `persistentDataPath` |
| 适用 | 几个设置项 | **完整存档结构** |

```
SaveData 对象  →  ToJson  →  JSON 字符串  →  WriteAllText  →  save.json
save.json  →  ReadAllText  →  JSON 字符串  →  FromJson  →  SaveData 对象
```

---

### 2.3 特点 — 优势与局限

**优势**：可读（JSON 文本）、支持多字段和 List、打包后 persistentDataPath 可靠、Unity 内置无需第三方。

**局限**：

| 限制 | 说明 |
|------|------|
| 只序列化 **public** 字段 | private 不进 JSON |
| 不支持 Dictionary | 改用 List |
| 不支持多态 | 扁平化结构 |
| 存档类不能继承 MonoBehaviour | SaveData 用纯 C# 类 |

---

### 2.4 适用场景

| ✅ 适用 | ❌ 不适用 |
|---------|-----------|
| 关卡、金币、血量、背包 | 单个音量值（用 PlayerPrefs 更简单） |
| 多字段游戏进度 | 超大型数据（考虑二进制/MessagePack） |
| 需要打包后读档 | 纯内存运行时状态 |

---

### 2.5 核心 API 及参数

#### JsonUtility.ToJson — 对象 → JSON

```csharp
string json = JsonUtility.ToJson(object obj);
string json = JsonUtility.ToJson(object obj, bool prettyPrint);
```

| 参数 | 含义 |
|------|------|
| `obj` | 要序列化的对象（如 SaveData 实例） |
| `prettyPrint` | `true` = 格式化缩进（调试用）；`false` = 紧凑 |

#### JsonUtility.FromJson — JSON → 对象

```csharp
SaveData data = JsonUtility.FromJson<SaveData>(string json);
```

| 参数 | 含义 |
|------|------|
| `json` | JSON 字符串 |
| `<SaveData>` | 目标类型 |
| **返回值** | 还原后的对象 |

#### File 读写 + 路径

```csharp
string path = Application.persistentDataPath + "/save.json";
File.WriteAllText(path, json);    // 写入
string json = File.ReadAllText(path);  // 读取
bool exists = File.Exists(path);       // 是否存在
```

| API | 参数 | 作用 |
|-----|------|------|
| `persistentDataPath` | 无 | 打包后安全的存档根目录 |
| `WriteAllText(path, json)` | 路径 + 内容 | 写入文件 |
| `ReadAllText(path)` | 路径 | 读取整个文件 |
| `Exists(path)` | 路径 | 文件是否存在 |

**persistentDataPath vs dataPath**：

| 路径 | 打包后可写 | 用途 |
|------|------------|------|
| `Application.dataPath` | ❌ 只读 | 游戏安装目录 |
| `Application.persistentDataPath` | ✅ | **存档目录** |

---

### 2.6 使用步骤（六步）

```
步骤1  定义 [Serializable] 的 SaveData 类（public 字段）
步骤2  游戏运行时维护 SaveData 实例（currentData）
步骤3  启动时：File.Exists? → ReadAllText → FromJson → 恢复
步骤4  无存档时：new SaveData() 默认值（新游戏）
步骤5  存档时：CollectFromGame → ToJson → WriteAllText
步骤6  ApplyToGame：把 currentData 应用到游戏逻辑/UI
```

---

### 2.7 SaveData 类定义

```csharp
using System;                                 // 提供 [Serializable] 特性
using System.Collections.Generic;             // 提供 List<T> 泛型列表

[Serializable]                                // Unity 特性：标记此类可被 JsonUtility 序列化
public class SaveData                           // 纯 C# 类，不继承 MonoBehaviour
{
    public int level;                           // public 字段：当前关卡（会被写入 JSON）
    public int gold;                            // public 字段：金币
    public int hp;                              // public 字段：血量
    public List<string> items;                  // public 字段：背包物品列表（string 字符串列表）
}
```

#### 语法拆解

##### `[Serializable]` 是什么？

```csharp
[Serializable]
public class SaveData
```

| 部分 | 含义 |
|------|------|
| `[Serializable]` | .NET 特性，标记类可被序列化（转成 JSON 等格式） |
| 作用 | JsonUtility.ToJson / FromJson 要求类必须带此标记 |

**整行人话**：告诉 Unity 这个类可以转成 JSON 字符串。

**说明**：没有 `[Serializable]`，JsonUtility 无法正常工作。

---

##### `public List<string> items;` 是什么？

```csharp
public List<string> items;
```

| 部分 | 含义 |
|------|------|
| `public` | 公开字段，JsonUtility 才能序列化 |
| `List<string>` | 字符串列表，表示多个物品名 |
| `items` | 字段名，会出现在 JSON 的 `"items": [...]` 中 |

**整行人话**：公开的物品列表字段，存档时会写入 JSON 数组。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using System;` | 引用系统库，使用 `[Serializable]` |
| 2 | `using System.Collections.Generic;` | 引用泛型集合，使用 `List<string>` |
| 4 | `[Serializable]` | 见上方语法拆解 |
| 5 | `public class SaveData` | 纯 C# 存档类，不继承 MonoBehaviour |
| 7~10 | `public int level` 等 | 必须 public；`items` 见上方语法拆解 |

生成 JSON 示例：

```json
{ "level": 3, "gold": 500, "hp": 80, "items": ["Sword", "Potion"] }
```

---

### 2.8 完整 SaveManager 案例

**功能**：启动自动读档，支持手动存档与退出存档，JSON 文件保存在 persistentDataPath。

```csharp
using System.IO;                                // 提供 File 读写：WriteAllText、ReadAllText、Exists
using UnityEngine;

public class SaveManager : MonoBehaviour
{
    private const string SAVE_FILE = "save.json";  // 存档文件名（常量）
    public SaveData currentData;                   // 当前内存里持有的存档数据对象

    void Start() { LoadGame(); }                   // 启动时自动读档

    public void LoadGame()                          // 读档方法
    {
        string path = Application.persistentDataPath + "/" + SAVE_FILE;
        // persistentDataPath = 打包后可读写的存档目录；+ 拼接文件名

        if (File.Exists(path))                      // 文件存在吗？
        {
            string json = File.ReadAllText(path);   // 把整个 .json 文件读成一个字符串
            currentData = JsonUtility.FromJson<SaveData>(json);
            // FromJson：JSON 字符串 → SaveData 对象
            Debug.Log("读档：关卡 " + currentData.level);
        }
        else                                        // 第一次玩，没有存档文件
        {
            currentData = new SaveData { level = 1, gold = 0, hp = 100,
                items = new System.Collections.Generic.List<string>() };
            // new SaveData { ... }：创建对象并初始化字段（对象初始化器）
            Debug.Log("新游戏");
        }
        ApplyToGame();                              // 把数据应用到游戏（UI、角色属性等）
    }

    public void SaveGame()                          // 存档方法
    {
        CollectFromGame();                          // 先从游戏里收集最新数据到 currentData
        string json = JsonUtility.ToJson(currentData, true);
        // ToJson：对象 → JSON 字符串；true = 格式化缩进，方便调试
        string path = Application.persistentDataPath + "/" + SAVE_FILE;
        File.WriteAllText(path, json);              // 把 JSON 字符串写入文件（覆盖旧文件）
        Debug.Log("存档：" + path);
    }

    void CollectFromGame() { /* 从 GameManager 等收集数据到 currentData */ }
    void ApplyToGame()     { /* 把 currentData 赋回游戏逻辑 */ }

    void OnApplicationQuit() { SaveGame(); }        // 退出游戏时再存一次（双保险）
}
```

#### 语法拆解

##### `Application.persistentDataPath + "/" + SAVE_FILE` 是什么？

```csharp
string path = Application.persistentDataPath + "/" + SAVE_FILE;
```

| 部分 | 含义 |
|------|------|
| `Application` | Unity 应用静态类 |
| `.persistentDataPath` | 各平台统一的、打包后可读写的持久化目录 |
| `+ "/" + SAVE_FILE` | 字符串拼接，得到完整文件路径，如 `.../save.json` |

**整行人话**：拼出跨平台合法的存档文件完整路径。

**说明**：不可用 `Application.dataPath`，打包后为只读安装目录。

---

##### `JsonUtility.FromJson<SaveData>(json)` 是什么？

```csharp
currentData = JsonUtility.FromJson<SaveData>(json);
```

| 部分 | 含义 |
|------|------|
| `JsonUtility.FromJson` | 静态方法，JSON 字符串 → C# 对象 |
| `<SaveData>` | 泛型参数，指定还原成 SaveData 类型 |
| `(json)` | 参数：从文件读出的 JSON 字符串 |
| `currentData = ...` | 把还原的对象赋给运行时变量 |

**整行人话**：把 JSON 文本变回 SaveData 对象，用于恢复游戏进度。

---

##### `new SaveData { level = 1, gold = 0, ... }` 是什么？

```csharp
currentData = new SaveData { level = 1, gold = 0, hp = 100, items = new List<string>() };
```

| 部分 | 含义 |
|------|------|
| `new SaveData` | 创建 SaveData 实例 |
| `{ level = 1, ... }` | 对象初始化器：创建同时给字段赋初值 |
| `items = new List<string>()` | 初始化空列表，避免 null 引用 |

**整行人话**：无存档文件时，创建一份默认的新游戏数据。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using System.IO;` | 文件读写库 |
| 5 | `SAVE_FILE = "save.json"` | 存档文件名，最终路径如 `.../save.json` |
| 6 | `public SaveData currentData` | 运行时内存里的存档对象 |
| 8 | `LoadGame()` in Start | 一进游戏就读档 |
| 12 | `persistentDataPath + "/" + SAVE_FILE` | 各平台合法存档完整路径 |
| 14 | `File.Exists(path)` | 有没有存档文件 |
| 16 | `ReadAllText(path)` | 读文件全部内容为 string |
| 17 | `FromJson<SaveData>(json)` | JSON 字符串还原成 SaveData |
| 22~24 | `new SaveData { level=1, ... }` | 无存档时创建默认新游戏数据 |
| 31 | `ToJson(currentData, true)` | 对象转 JSON；true=带换行缩进 |
| 33 | `WriteAllText(path, json)` | 写入磁盘 |
| 39 | `OnApplicationQuit()` | Unity 退出时回调，适合最后 Save |

#### 关键代码翻译

| 代码 | 含义 |
|------|------|
| `persistentDataPath + "/save.json"` | 打包后合法存档路径 |
| `File.Exists(path)` | 有没有存档文件 |
| `JsonUtility.FromJson<SaveData>(json)` | JSON → 对象 |
| `JsonUtility.ToJson(data, true)` | 对象 → JSON |
| `File.WriteAllText(path, json)` | 写入磁盘 |

---

### 2.9 PlayerPrefs 与 JsonUtility 配合

```csharp
// 设置 → PlayerPrefs
PlayerPrefs.SetFloat("MasterVolume", 0.8f);
PlayerPrefs.Save();

// 进度 → JSON 文件
saveManager.currentData.level = 5;
saveManager.SaveGame();
```

同一项目：**GameSettings（PlayerPrefs）+ SaveManager（JSON）** 分工明确。

---

### 2.10 JsonUtility 打包测试清单

- [ ] 路径用 `persistentDataPath`，不是 `dataPath`
- [ ] SaveData 有 `[Serializable]`，字段 public
- [ ] **Build 版本**测试 Save → 关游戏 → Load
- [ ] `Debug.Log(path)` 确认文件位置
- [ ] 无存档时走新游戏分支

---

## 三、进阶综合案例：SettingsManager

**功能**：统一管理音乐开关与音量，启动读档、修改时写档并应用到 AudioListener。

```csharp
using UnityEngine;

public class SettingsManager : MonoBehaviour      // 统一管理音量、音乐开关的设置类
{
    private const string KEY_MUSIC  = "MusicOn";    // 音乐开关的 PlayerPrefs Key
    private const string KEY_VOLUME = "MasterVolume"; // 音量的 PlayerPrefs Key

    public bool musicOn;                            // 运行时：音乐是否开启
    public float volume;                            // 运行时：音量 0~1

    void Start()                                    // 启动：读存档 → 应用到声音
    {
        musicOn = PlayerPrefs.GetInt(KEY_MUSIC, 1) != 0;  // 读开关，默认 1=开
        volume  = PlayerPrefs.GetFloat(KEY_VOLUME, 1.0f); // 读音量，默认满
        Apply();                                    // 应用到 AudioListener
    }

    public void SetMusic(bool on)                   // 外部/UI 调用：设置音乐开关
    {
        musicOn = on;
        PlayerPrefs.SetInt(KEY_MUSIC, on ? 1 : 0);
        PlayerPrefs.Save();
        Apply();
    }

    public void SetVolume(float v)                  // 外部/UI 调用：设置音量
    {
        volume = v;
        PlayerPrefs.SetFloat(KEY_VOLUME, v);
        PlayerPrefs.Save();
        Apply();
    }

    void Apply() { AudioListener.volume = musicOn ? volume : 0f; }
}
```

#### 语法拆解

##### `musicOn ? volume : 0f` 是什么？

```csharp
AudioListener.volume = musicOn ? volume : 0f;
```

| 部分 | 含义 |
|------|------|
| `musicOn ? volume : 0f` | 三元运算符：音乐开用 volume，关则 0（静音） |
| `musicOn` | 条件：true = 音乐开启 |
| `? volume` | 开启时使用 volume 作为全局音量 |
| `: 0f` | 关闭时音量为 0 |

**整行人话**：音乐关则强制静音，音乐开则使用当前音量值。

---

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 5~6 | 两个 `KEY` 常量 | 分别对应音乐开关和音量，避免字符串写错 |
| 8~9 | `musicOn` / `volume` | 游戏运行时的当前状态（内存变量） |
| 13 | `GetInt(KEY_MUSIC, 1) != 0` | 读开关，默认开 |
| 14 | `GetFloat(KEY_VOLUME, 1.0f)` | 读音量，默认满 |
| 15 | `Apply()` | 读完后立刻让声音生效 |
| 17~22 | `SetMusic(bool on)` | UI Toggle 可绑此方法；改内存 → 写 PlayerPrefs → Save → Apply |
| 24~29 | `SetVolume(float v)` | Slider 可绑此方法；同上流程 |
| 31 | `musicOn ? volume : 0f` | 音乐关则全局音量 0；音乐开则用 volume 值 |

---

## 【进阶阶段小结】

| 维度 | PlayerPrefs | JsonUtility |
|------|-------------|-------------|
| 定义 | Key-Value 偏好存储 | JSON 序列化工具 |
| 本质 | 平台偏好 API 封装 | 对象 ↔ JSON 字符串 |
| 适用 | 设置、开关、最高分 | 关卡、背包、完整进度 |
| 路径 | Unity 自动 | persistentDataPath |
| 封装 | PrefsKeys + GameSettings | SaveData + SaveManager |
| 测试 | Editor + Build | **必须 Build 实测** |

---

# 【全文总结】

## 讲师知识框架回顾

| 维度 | 核心结论 |
|------|----------|
| **定义** | PlayerPrefs = 静态 Key-Value 本地存储；JsonUtility = JSON 序列化 |
| **本质** | PlayerPrefs 是平台偏好 API 的统一封装；JsonUtility 是对象与 JSON 互转 |
| **特点** | 简单跨平台 vs 仅 3 类型无加密；JSON 可读 vs 只 public 字段 |
| **适用** | 设置/开关 → PlayerPrefs；完整进度 → JSON 文件 |
| **原理** | Set → 内存 → Save → 磁盘 |
| **API** | Set/Get/HasKey/Save/Delete；ToJson/FromJson/File |
| **步骤** | 启动读 → 应用 → 修改 → Save；Load/Save 六步流程 |
| **时机** | Start 读；UI 写+Save；Quit 双保险 |
| **避坑** | Save、Key 常量、Build 实测、dataPath vs persistentDataPath |

## 最重要的一行代码

```csharp
PlayerPrefs.SetInt("Score", 100);
```

| 部分 | 含义 |
|------|------|
| `PlayerPrefs` | 工具箱（静态类） |
| `SetInt` | 写入整数 |
| `"Score"` | Key：名字 |
| `100` | Value：值 |
| 后续 | `Save()` 才真正落盘 |

## 三阶段对照

| 阶段 | 掌握维度 | 代表案例 |
|------|----------|----------|
| 零基础 | 定义/本质/特点/适用 + 读懂代码 | 分数 +10 Demo |
| 入门 | 原理/API/步骤/时机 | 音乐、音量、最高分 |
| 进阶 | 封装/平台/性能/安全/选型 + JsonUtility | SaveManager |

## API 速查

**PlayerPrefs**

| 代码 | 参数 | 作用 |
|------|------|------|
| `SetInt("Score", 100)` | key, value | 存整数 |
| `GetInt("Score", 0)` | key, default | 读整数 |
| `HasKey("Score")` | key | 是否存过 |
| `Save()` | 无 | 落盘 |
| `DeleteKey("Score")` | key | 删一条 |

**JsonUtility**

| 代码 | 参数 | 作用 |
|------|------|------|
| `ToJson(obj, true)` | 对象, 格式化 | 对象→JSON |
| `FromJson<SaveData>(json)` | JSON 字符串 | JSON→对象 |
| `WriteAllText(path, json)` | 路径, 内容 | 写文件 |
| `persistentDataPath` | 无 | 存档根目录 |

## 学习自检

**PlayerPrefs**：定义/本质/特点/适用？能读懂 SetInt？Get 两参数区别？Save 时机？

**JsonUtility**：SaveData 怎么写？ToJson/FromJson？为何用 persistentDataPath？Build 测过吗？

---

## 参考资料

| 类型 | 链接 |
|------|------|
| PlayerPrefs 官方 API | https://docs.unity3d.com/ScriptReference/PlayerPrefs.html |
| JsonUtility 官方 API | https://docs.unity3d.com/ScriptReference/JsonUtility.html |
| persistentDataPath | https://docs.unity3d.com/ScriptReference/Application-persistentDataPath.html |
| Unity Learn 跨会话持久化 | https://learn.unity.com/pathway/junior-programmer/unit/manage-scene-flow-and-data/tutorial/implement-data-persistence-between-sessions?version=2021.3 |
