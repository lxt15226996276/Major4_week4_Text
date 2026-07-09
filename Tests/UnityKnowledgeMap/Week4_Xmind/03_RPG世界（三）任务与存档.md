# 综合案例项目实例RPG世界（三）——任务与存档

> 参照：[Unity 官方 Scripting API - PlayerPrefs](https://docs.unity3d.com/ScriptReference/PlayerPrefs.html) · [JsonUtility](https://docs.unity3d.com/ScriptReference/JsonUtility.html) · [ScriptableObject](https://docs.unity3d.com/ScriptReference/ScriptableObject.html)  
> 关联文档：[01_RPG世界（一）.md](./01_RPG世界（一）项目初始化与玩家基础.md) · [02_RPG世界（二）.md](./02_RPG世界（二）战斗系统与交互.md) · [04_RPG世界（四）.md](./04_RPG世界（四）AI与优化.md) · [05_综合复习.md](./05_综合复习.md)  
> 学习路径：**零基础 → 入门 → 进阶**，每阶段采用 **总—分—总** 结构。  
> 讲解维度：**定义 → 本质 → 特点 → 适用场景 → 原理 → API → 步骤 → 案例 → 避坑**（进阶含项目架构 / 模块化 / 性能优化）。  
> 案例讲解：遵循 **案例代码讲解模板**（功能 → 代码 → 语法拆解 → 逐行详解 → 操作提示）。  
> API 讲解：入门/进阶 API 章节均采用 **逐词读懂** 格式（与 [01_PlayerPrefs.md](../major3/01_PlayerPrefs.md) 一致：类型 → 参数 → 整行人话）。

---

## 【全文总述】

**RPG（角色扮演游戏）世界综合案例** 第三章，重点讲解 **任务系统、存档系统、背包系统** 三大核心模块。  
学习本案例，你将掌握：
- 如何设计和实现任务系统
- 如何用 PlayerPrefs 存简单设置
- 如何用 JsonUtility 存完整游戏进度
- 如何实现背包系统
- 如何制作任务和背包UI

### 思维导图总览

```
RPG 世界综合案例（三）——任务与存档
│
├── 任务系统（游戏引导 — 玩家成长的主线）
│   │
│   ├── 定义：游戏中引导玩家完成特定目标的任务机制，包含接取、执行、交付、奖励流程
│   │
│   ├── 本质：数据驱动的任务模板 → 运行时实例 → 状态追踪 → 触发条件检测 → 奖励发放
│   │   ├── 任务类型：击杀任务、收集任务、对话任务、探索任务
│   │   ├── 任务状态：未接取、进行中、已完成、已领取
│   │   ├── 任务条件：目标数量、目标类型、完成条件
│   │   └── 任务奖励：金币、经验、道具
│   │
│   ├── 核心原理：任务管理器加载配置 → 玩家接取任务 → 监听条件变化 → 完成检测 → 发放奖励
│   │
│   ├── 核心 API 及参数
│   │   ├── ScriptableObject：任务数据配置
│   │   ├── PlayerPrefs.SetInt/GetInt：简单状态存储
│   │   └── JsonUtility.ToJson/FromJson：复杂数据序列化
│   │
│   └── 标准使用步骤
│       ├── 步骤1 创建任务数据配置（ScriptableObject）
│       ├── 步骤2 创建任务管理器（QuestManager）
│       ├── 步骤3 实现任务接取与追踪
│       └── 步骤4 制作任务UI
│
├── 存档系统（进度保存 — 玩家劳动的结晶）
│   │
│   ├── 定义：将游戏运行时数据保存到磁盘，下次启动时恢复的机制
│   │
│   ├── 本质：运行时数据 → 序列化 → 文件写入 → 文件读取 → 反序列化 → 恢复数据
│   │   ├── PlayerPrefs：简单键值对，适合设置、开关、最高分
│   │   ├── JsonUtility + File：复杂对象，适合完整游戏进度
│   │   └── ScriptableObject：游戏配置数据
│   │
│   ├── 核心原理：数据收集 → 序列化 → 写入 persistentDataPath → 读取 → 反序列化 → 应用到游戏
│   │
│   ├── 核心 API 及参数
│   │   ├── PlayerPrefs.SetXxx/GetXxx/Save：简单存档
│   │   ├── JsonUtility.ToJson/FromJson：对象序列化
│   │   ├── File.WriteAllText/ReadAllText：文件读写
│   │   └── Application.persistentDataPath：跨平台存档路径
│   │
│   └── 标准使用步骤
│       ├── 步骤1 定义存档数据类（SaveData）
│       ├── 步骤2 创建存档管理器（SaveManager）
│       ├── 步骤3 实现存档和读档方法
│       └── 步骤4 绑定UI按钮
│
├── 背包系统（物品管理 — 玩家收集的仓库）
│   │
│   ├── 定义：管理玩家收集物品的系统，包含物品存储、查看、使用、丢弃
│   │
│   ├── 本质：物品数据结构 → 容量限制 → 物品操作（添加/移除/使用）→ UI展示
│   │   ├── 物品类型：消耗品、装备、材料、任务道具
│   │   ├── 背包容量：固定格子数
│   │   └── 物品堆叠：相同物品可叠加
│   │
│   └── 实战：背包系统实现
│       ├── 创建物品数据（ScriptableObject）
│       ├── 实现背包管理器
│       └── 制作背包UI
│
├── 第一阶段：零基础（任务与存档概念）
│   ├── 理解任务系统与存档系统的定义
│   ├── 逐词读懂：PlayerPrefs.SetInt("Key", value)
│   └── 完成任务UI基础搭建
│
├── 第二阶段：入门（任务实现 + 存档操作 + 背包）
│   ├── 任务系统完整实现
│   ├── PlayerPrefs 与 JsonUtility 存档
│   ├── 背包系统实现
│   └── 实战案例：任务接取、存档读档、背包操作
│
└── 第三阶段：进阶（架构设计 + 模块化 + 优化）
    ├── 任务系统模块化封装
    ├── 存档系统安全与性能
    ├── 背包系统优化
    └── 常见误区与最佳实践
```

| 学习阶段 | 学习目标 |
|----------|----------|
| **零基础** | 理解任务与存档概念；读懂 PlayerPrefs 核心代码；完成任务UI基础搭建 |
| **入门** | 实现任务系统、存档系统、背包系统；掌握 JsonUtility；完成 3 个案例 |
| **进阶** | 理解数据驱动架构；会封装存档系统；掌握性能优化技巧 |

### 讲师知识框架速览（全文脉络）

| 维度 | 零基础讲 | 入门讲 | 进阶讲 |
|------|----------|--------|--------|
| 定义 | ✅ | 回顾 | 回顾 |
| 本质 | ✅ | — | — |
| 特点 | ✅ | — | 架构特点 |
| 适用场景 | ✅ | — | 项目选型 |
| 核心原理 | 任务流程 | ✅ 存档链路 | 数据驱动设计 |
| 核心 API | 读懂 PlayerPrefs | ✅ PlayerPrefs + JsonUtility | 封装与优化 |
| 使用步骤 | UI搭建 | ✅ 任务实现步骤 | 架构搭建 |
| 调用时机 | — | ✅ 启动读档/退出存档 | 生命周期管理 |
| 避坑 | — | 初步 | ✅ |

---

# 第一阶段：零基础篇

## 【阶段总述】

零基础阶段建立**正确认知**：任务系统是什么、存档系统是什么、PlayerPrefs 怎么工作。  
同时学会**读懂** `PlayerPrefs.SetInt("Key", value)` 每个部分的含义，并完成任务UI基础搭建。

---

## 一、定义 — 任务与存档是什么？

| 项目 | 说明 |
|------|------|
| **任务系统** | 引导玩家完成特定目标的机制，包含接取、执行、交付、奖励 |
| **存档系统** | 将游戏数据保存到磁盘，下次启动恢复的机制 |
| **背包系统** | 管理玩家收集物品的系统 |
| **PlayerPrefs** | Unity内置轻量级键值对存储，适合简单设置 |
| **JsonUtility** | Unity内置JSON序列化工具，适合复杂数据 |
| **一句话** | 任务=目标+奖励；存档=数据持久化；背包=物品仓库 |

```
任务系统结构示例
QuestManager
    ├── 任务配置（ScriptableObject）
    │   ├── 任务ID
    │   ├── 任务名称
    │   ├── 任务描述
    │   ├── 任务类型（击杀/收集/对话）
    │   ├── 目标数量
    │   └── 奖励
    │
    ├── 任务状态管理
    │   ├── 未接取
    │   ├── 进行中
    │   └── 已完成
    │
    └── 任务UI
        ├── 任务列表
        ├── 当前任务
        └── 任务进度
```

---

## 二、本质 — 任务与存档如何工作？

### 2.1 任务系统本质

```
任务流程
接取任务 → 更新状态为进行中 → 监听目标条件 → 条件满足 → 更新状态为完成 → 交付领取奖励
```

| 环节 | 本质理解 |
|------|----------|
| **接取** | 玩家与NPC交互，领取任务 |
| **追踪** | 实时检测任务目标完成情况 |
| **完成** | 目标达成，可交付任务 |
| **奖励** | 交付后获得金币、经验、道具 |

### 2.2 存档系统本质

```
存档流程
数据收集 → 序列化(ToJson) → 写入文件 → 读取文件 → 反序列化(FromJson) → 恢复到游戏
```

| 环节 | 本质理解 |
|------|----------|
| **收集** | 从游戏对象中读取当前数据 |
| **序列化** | 将对象转为JSON字符串 |
| **写入** | 将JSON写入磁盘文件 |
| **读取** | 从磁盘读取JSON文件 |
| **反序列化** | 将JSON转为游戏对象 |
| **恢复** | 将数据应用到游戏 |

---

## 三、特点与适用场景

### 3.1 任务系统特点

| 特点 | 说明 |
|------|------|
| **数据驱动** | 任务内容由配置数据决定，无需改代码 |
| **状态追踪** | 需要记录每个任务的当前状态 |
| **条件触发** | 任务进度由游戏事件触发更新 |
| **奖励驱动** | 奖励激励玩家完成任务 |

### 3.2 存档系统特点

| 特点 | 说明 |
|------|------|
| **跨会话** | 关游戏再开，数据仍在 |
| **平台兼容** | 不同平台有不同的存储路径 |
| **性能考虑** | 磁盘IO有开销，不宜频繁调用 |
| **安全性** | 本地存档易被篡改 |

### 3.3 适用场景

| 场景 | PlayerPrefs | JsonUtility |
|------|-------------|-------------|
| 音量设置 | ✅ | ❌（太大材小用） |
| 语言选择 | ✅ | ❌ |
| 关卡进度 | ❌ | ✅ |
| 背包物品 | ❌ | ✅ |
| 任务状态 | ❌ | ✅ |
| 角色属性 | ❌ | ✅ |

---

## 四、核心一课：如何读懂 PlayerPrefs

```csharp
PlayerPrefs.SetInt("Quest_001", 1);
PlayerPrefs.Save();
```

| 部分 | 含义 |
|------|------|
| `PlayerPrefs` | Unity存档工具箱，静态类 |
| `.SetInt` | 方法名：设置整数 |
| `"Quest_001"` | 参数1：Key，数据名字 |
| `1` | 参数2：Value，要存的值 |
| `.Save()` | 方法名：写入磁盘 |

**整行人话**：把"Quest_001"这个任务标记设为1（进行中），然后保存到硬盘。

```csharp
// 完整的读写代码
PlayerPrefs.SetInt("Coins", 100);  // 存金币
PlayerPrefs.Save();                 // 写入磁盘
int coins = PlayerPrefs.GetInt("Coins", 0);  // 读金币，默认0
```

| 行 | 含义 |
|----|------|
| `SetInt("Coins", 100)` | 把金币设为100 |
| `Save()` | 写入磁盘，关游戏不丢 |
| `GetInt("Coins", 0)` | 读金币，没存过返回0 |

---

## 五、零基础实战：任务UI搭建

### 5.1 步骤一：创建任务面板

1. 右键 Canvas → **UI → Panel**，命名为 `QuestPanel`
2. 设置 Panel 位置和大小（居中偏右）
3. 设置初始状态为隐藏

### 5.2 步骤二：创建任务列表

1. 右键 QuestPanel → **UI → ScrollRect**，命名为 `QuestScroll`
2. 设置 ScrollRect 参数：
   - **Movement Type**：Clamped
   - **Horizontal**：false
   - **Vertical**：true
3. 删除 Content 下的 Image，添加 **Vertical Layout Group**
4. 设置 **Child Force Expand**：Width=true，Height=false

### 5.3 步骤三：创建任务项预制体

1. 右键 Content → **UI → Text**，命名为 `QuestItem`
2. 设置字体大小、颜色
3. 拖入 Prefabs 文件夹，命名为 `QuestItem.prefab`
4. 删除场景中的 QuestItem

### 5.4 步骤四：创建存档按钮

1. 右键 Canvas → **UI → Button**，命名为 `SaveBtn`
2. 设置按钮文本为"保存游戏"
3. 调整位置到右下角

---

## 【零基础阶段小结】

| 维度 | 要点 |
|------|------|
| **定义** | 任务=目标+奖励；存档=数据持久化；背包=物品仓库 |
| **本质** | 任务=数据驱动+状态追踪；存档=序列化+文件IO |
| **步骤** | 创建QuestPanel → ScrollRect → QuestItem → SaveBtn |
| **读懂** | `PlayerPrefs.SetInt("Key", value)` |

**阶段检验**：能说出任务流程；能画出存档流程图；能读懂 PlayerPrefs 代码。

---

# 第二阶段：入门篇

## 【阶段总述】

入门阶段掌握 **任务系统、存档系统、背包系统** 三大核心模块，并完成 3 个实战案例。  
重点：**ScriptableObject配置任务**；**JsonUtility序列化存档**；**List管理背包物品**。

---

## 一、任务系统核心代码详解

### 1.1 ScriptableObject API — 逐词读懂

#### `CreateAssetMenu(fileName, menuName)` 是什么？

```csharp
[CreateAssetMenu(fileName = "NewQuest", menuName = "RPG/Quest")]
public class Quest : ScriptableObject
```

| 部分 | 含义 |
|------|------|
| `[CreateAssetMenu]` | 特性：让类可以在Project窗口右键创建 |
| `fileName` | 默认文件名 |
| `menuName` | 菜单路径（RPG → Quest） |
| `ScriptableObject` | 可创建资产的基类 |

**整行人话**：让这个任务配置类可以在Unity编辑器中右键创建。

#### `JsonUtility.ToJson(obj, prettyPrint)` 是什么？

```csharp
string json = JsonUtility.ToJson(saveData, true);
```

| 部分 | 含义 |
|------|------|
| `JsonUtility` | Unity内置JSON工具类 |
| `.ToJson` | 方法名：对象转JSON字符串 |
| `obj` | 参数1：要序列化的对象 |
| `prettyPrint` | 参数2：是否格式化（true=带换行） |

**整行人话**：把游戏数据对象变成可读的JSON文本。

---

### 1.2 Quest 数据配置

```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "NewQuest", menuName = "RPG/Quest")]
public class Quest : ScriptableObject
{
    public string questID;
    public string questName;
    public string description;
    public QuestType questType;
    public int targetCount;
    public int currentCount;
    public QuestState state;
    public Reward reward;
}

public enum QuestType
{
    Kill,
    Collect,
    Talk,
    Explore
}

public enum QuestState
{
    NotAccepted,
    InProgress,
    Completed,
    Claimed
}

[System.Serializable]
public class Reward
{
    public int gold;
    public int experience;
    public Item item;
}
```

#### 语法拆解

##### `public enum QuestType` 是什么？

```csharp
public enum QuestType
{
    Kill,
    Collect,
    Talk,
    Explore
}
```

| 部分 | 含义 |
|------|------|
| `enum` | 枚举类型，定义一组命名常量 |
| `QuestType` | 枚举名 |
| `Kill/Collect/Talk/Explore` | 枚举值，表示不同任务类型 |

**整行人话**：定义任务的四种类型，代码里用名字而不是数字，更易读。

##### `[System.Serializable]` 是什么？

```csharp
[System.Serializable]
public class Reward
```

| 部分 | 含义 |
|------|------|
| `[Serializable]` | 特性：标记类可被序列化 |
| **作用** | JsonUtility和Inspector需要这个标记才能正常工作 |

**整行人话**：告诉Unity这个奖励类可以转成JSON，也能在Inspector中显示。

---

### 1.3 QuestManager 完整代码

```csharp
using UnityEngine;
using System.Collections.Generic;

public class QuestManager : MonoBehaviour
{
    public static QuestManager Instance { get; private set; }

    public List<Quest> allQuests = new List<Quest>();
    public List<Quest> activeQuests = new List<Quest>();

    void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(gameObject);
    }

    public void AcceptQuest(string questID)
    {
        Quest quest = allQuests.Find(q => q.questID == questID);
        if (quest != null && quest.state == QuestState.NotAccepted)
        {
            quest.state = QuestState.InProgress;
            quest.currentCount = 0;
            activeQuests.Add(quest);
            Debug.Log("接取任务：" + quest.questName);
        }
    }

    public void UpdateQuestProgress(string questID, int count)
    {
        Quest quest = activeQuests.Find(q => q.questID == questID);
        if (quest != null)
        {
            quest.currentCount += count;
            if (quest.currentCount >= quest.targetCount)
            {
                quest.state = QuestState.Completed;
                Debug.Log("任务完成：" + quest.questName);
            }
        }
    }

    public void ClaimReward(string questID)
    {
        Quest quest = activeQuests.Find(q => q.questID == questID);
        if (quest != null && quest.state == QuestState.Completed)
        {
            PlayerStats.Instance.AddGold(quest.reward.gold);
            PlayerStats.Instance.AddExp(quest.reward.experience);
            quest.state = QuestState.Claimed;
            activeQuests.Remove(quest);
            Debug.Log("领取奖励：金币+" + quest.reward.gold);
        }
    }
}
```

#### 语法拆解

##### `allQuests.Find(q => q.questID == questID)` 是什么？

```csharp
Quest quest = allQuests.Find(q => q.questID == questID);
```

| 部分 | 含义 |
|------|------|
| `allQuests` | 任务列表 |
| `.Find()` | 查找方法，返回第一个满足条件的元素 |
| `q => q.questID == questID` | Lambda表达式：筛选条件 |
| **效果** | 在列表中找到ID匹配的任务 |

**整行人话**：在所有任务中找到指定ID的任务。

##### `PlayerStats.Instance.AddGold()` 是什么？

```csharp
PlayerStats.Instance.AddGold(quest.reward.gold);
```

| 部分 | 含义 |
|------|------|
| `PlayerStats.Instance` | 单例，全局唯一的玩家状态 |
| `.AddGold()` | 方法：增加金币 |

**整行人话**：给玩家增加任务奖励的金币。

---

## 二、存档系统实现

### 2.1 SaveData 存档数据类

```csharp
using UnityEngine;
using System.Collections.Generic;

[System.Serializable]
public class SaveData
{
    public int level;
    public int gold;
    public int experience;
    public int health;
    public Vector3 position;
    public List<QuestData> quests = new List<QuestData>();
    public List<InventoryItem> inventory = new List<InventoryItem>();
}

[System.Serializable]
public class QuestData
{
    public string questID;
    public int currentCount;
    public QuestState state;
}

[System.Serializable]
public class InventoryItem
{
    public string itemID;
    public int quantity;
}
```

#### 语法拆解

##### `public List<QuestData> quests` 是什么？

```csharp
public List<QuestData> quests = new List<QuestData>();
```

| 部分 | 含义 |
|------|------|
| `List<QuestData>` | QuestData类型的列表 |
| `quests` | 字段名 |
| `= new List<QuestData>()` | 初始化空列表 |

**整行人话**：存档中的任务进度列表。

##### `public Vector3 position` 是什么？

```csharp
public Vector3 position;
```

| 部分 | 含义 |
|------|------|
| `Vector3` | 三维向量（x,y,z） |
| `position` | 玩家位置 |

**整行人话**：存档时记录玩家位置，读档时恢复。

---

### 2.2 SaveManager 完整代码

```csharp
using UnityEngine;
using System.IO;

public class SaveManager : MonoBehaviour
{
    public static SaveManager Instance { get; private set; }

    private const string SAVE_FILE = "save.json";
    public SaveData currentData;

    void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(gameObject);
    }

    void Start()
    {
        LoadGame();
    }

    public void SaveGame()
    {
        CollectData();
        string json = JsonUtility.ToJson(currentData, true);
        string path = Application.persistentDataPath + "/" + SAVE_FILE;
        File.WriteAllText(path, json);
        Debug.Log("存档成功：" + path);
    }

    public void LoadGame()
    {
        string path = Application.persistentDataPath + "/" + SAVE_FILE;
        if (File.Exists(path))
        {
            string json = File.ReadAllText(path);
            currentData = JsonUtility.FromJson<SaveData>(json);
            ApplyData();
            Debug.Log("读档成功");
        }
        else
        {
            currentData = CreateDefaultData();
            Debug.Log("新游戏");
        }
    }

    void CollectData()
    {
        currentData.level = PlayerStats.Instance.level;
        currentData.gold = PlayerStats.Instance.gold;
        currentData.experience = PlayerStats.Instance.experience;
        currentData.health = PlayerStats.Instance.health;
        currentData.position = PlayerController.Instance.transform.position;
    }

    void ApplyData()
    {
        PlayerStats.Instance.level = currentData.level;
        PlayerStats.Instance.gold = currentData.gold;
        PlayerStats.Instance.experience = currentData.experience;
        PlayerStats.Instance.health = currentData.health;
        PlayerController.Instance.transform.position = currentData.position;
    }

    SaveData CreateDefaultData()
    {
        return new SaveData
        {
            level = 1,
            gold = 0,
            experience = 0,
            health = 100,
            position = Vector3.zero,
            quests = new List<QuestData>(),
            inventory = new List<InventoryItem>()
        };
    }

    void OnApplicationQuit()
    {
        SaveGame();
    }
}
```

#### 语法拆解

##### `Application.persistentDataPath` 是什么？

```csharp
string path = Application.persistentDataPath + "/" + SAVE_FILE;
```

| 部分 | 含义 |
|------|------|
| `Application` | Unity应用静态类 |
| `.persistentDataPath` | 各平台统一的可读写目录 |
| `+ "/" + SAVE_FILE` | 拼接文件名 |

**整行人话**：拼出跨平台合法的存档文件路径。

**重要**：不可用 `Application.dataPath`，打包后为只读。

##### `File.WriteAllText(path, json)` 是什么？

```csharp
File.WriteAllText(path, json);
```

| 部分 | 含义 |
|------|------|
| `File` | System.IO命名空间下的文件操作类 |
| `.WriteAllText` | 方法：将字符串写入文件（覆盖） |
| `path` | 文件完整路径 |
| `json` | 要写入的JSON字符串 |

**整行人话**：把JSON数据写入存档文件。

---

## 三、背包系统实现

### 3.1 Item 物品数据

```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "NewItem", menuName = "RPG/Item")]
public class Item : ScriptableObject
{
    public string itemID;
    public string itemName;
    public Sprite icon;
    public ItemType itemType;
    public int maxStack = 99;
    public int value;
    public string description;
}

public enum ItemType
{
    Consumable,
    Equipment,
    Material,
    QuestItem
}
```

### 3.2 InventoryManager 完整代码

```csharp
using UnityEngine;
using System.Collections.Generic;

public class InventoryManager : MonoBehaviour
{
    public static InventoryManager Instance { get; private set; }

    public int inventorySize = 20;
    public List<InventoryItem> items = new List<InventoryItem>();

    void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(gameObject);
    }

    public bool AddItem(Item item, int quantity = 1)
    {
        InventoryItem existingItem = items.Find(i => i.itemID == item.itemID);

        if (existingItem != null && existingItem.quantity < item.maxStack)
        {
            existingItem.quantity += quantity;
            return true;
        }

        if (items.Count < inventorySize)
        {
            items.Add(new InventoryItem { itemID = item.itemID, quantity = quantity });
            return true;
        }

        return false;
    }

    public void RemoveItem(string itemID, int quantity = 1)
    {
        InventoryItem item = items.Find(i => i.itemID == itemID);
        if (item != null)
        {
            item.quantity -= quantity;
            if (item.quantity <= 0)
            {
                items.Remove(item);
            }
        }
    }

    public void UseItem(string itemID)
    {
        InventoryItem item = items.Find(i => i.itemID == itemID);
        if (item != null)
        {
            Item data = Resources.Load<Item>("Items/" + itemID);
            if (data != null && data.itemType == ItemType.Consumable)
            {
                PlayerStats.Instance.Heal(data.value);
                RemoveItem(itemID, 1);
            }
        }
    }
}
```

#### 语法拆解

##### `Resources.Load<Item>("Items/" + itemID)` 是什么？

```csharp
Item data = Resources.Load<Item>("Items/" + itemID);
```

| 部分 | 含义 |
|------|------|
| `Resources.Load<T>` | 从Resources文件夹加载资源 |
| `<Item>` | 泛型参数：要加载的类型 |
| `"Items/" + itemID` | 资源路径（相对于Resources） |

**整行人话**：根据物品ID从Resources文件夹加载物品配置数据。

##### `items.Find(i => i.itemID == itemID)` 是什么？

```csharp
InventoryItem existingItem = items.Find(i => i.itemID == itemID);
```

| 部分 | 含义 |
|------|------|
| `items` | 背包物品列表 |
| `.Find()` | 查找方法 |
| `i => i.itemID == itemID` | Lambda：按ID查找 |

**整行人话**：在背包中找到指定ID的物品。

---

## 四、入门三个案例

### 案例代码讲解模板

每个案例统一按以下结构组织：

| 顺序 | 板块 | 内容 |
|:----:|------|------|
| 1 | **功能** | 案例实现什么业务 |
| 2 | **完整代码** | 带行内注释的完整脚本 |
| 3 | **语法拆解** | 对案例中较生僻的语法，逐个说明 |
| 4 | **逐行详解** | 表格：每行代码的含义 |
| 5 | **操作提示** | Unity 绑定、调用方式等 |

---

### 案例 1：任务接取与追踪

**功能**：与NPC对话接取任务，击杀敌人更新任务进度，完成后领取奖励。

```csharp
using UnityEngine;

public class QuestGiver : MonoBehaviour, IInteractable
{
    public Quest quest;

    public void Interact()
    {
        switch (quest.state)
        {
            case QuestState.NotAccepted:
                AcceptQuest();
                break;
            case QuestState.InProgress:
                ShowProgress();
                break;
            case QuestState.Completed:
                ClaimReward();
                break;
            case QuestState.Claimed:
                Debug.Log("任务已完成");
                break;
        }
    }

    void AcceptQuest()
    {
        QuestManager.Instance.AcceptQuest(quest.questID);
        Debug.Log("接取任务：" + quest.questName);
        Debug.Log(quest.description);
    }

    void ShowProgress()
    {
        Debug.Log($"进度：{quest.currentCount}/{quest.targetCount}");
    }

    void ClaimReward()
    {
        QuestManager.Instance.ClaimReward(quest.questID);
        Debug.Log($"获得奖励：金币{quest.reward.gold}，经验{quest.reward.experience}");
    }
}
```

#### 语法拆解

##### `switch (quest.state)` 是什么？

```csharp
switch (quest.state)
{
    case QuestState.NotAccepted:
        // 接取任务
        break;
    case QuestState.InProgress:
        // 显示进度
        break;
}
```

| 部分 | 含义 |
|------|------|
| `switch` | 多条件分支语句 |
| `quest.state` | 要判断的值 |
| `case` | 匹配的情况 |
| `break` | 跳出switch |

**整行人话**：根据任务当前状态执行不同逻辑。

##### `$"{quest.currentCount}/{quest.targetCount}"` 是什么？

```csharp
Debug.Log($"进度：{quest.currentCount}/{quest.targetCount}");
```

| 部分 | 含义 |
|------|------|
| `$""` | 字符串插值语法 |
| `{quest.currentCount}` | 嵌入变量值 |

**整行人话**：把变量值直接嵌入字符串中。

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 5 | `public Quest quest` | 要给予的任务配置 |
| 7 | `Interact()` | 实现IInteractable接口 |
| 9 | `switch (quest.state)` | 根据任务状态分支 |
| 11 | `NotAccepted` | 未接取时接取任务 |
| 15 | `InProgress` | 进行中时显示进度 |
| 19 | `Completed` | 完成时领取奖励 |
| 23 | `Claimed` | 已领取时提示 |
| 27 | `AcceptQuest()` | 调用QuestManager接取 |
| 32 | `ShowProgress()` | 显示当前进度 |
| 36 | `ClaimReward()` | 调用QuestManager领奖励 |

#### 操作提示

1. 创建Quest配置资产（右键 → RPG → Quest）
2. 配置任务ID、名称、描述、类型、目标数量、奖励
3. NPC挂QuestGiver脚本，Inspector拖入Quest配置
4. 击杀敌人时调用 `QuestManager.Instance.UpdateQuestProgress()`

---

### 案例 2：存档与读档

**功能**：点击按钮保存游戏，启动时自动读档，退出时自动保存。

```csharp
using UnityEngine;
using UnityEngine.UI;

public class SaveLoadUI : MonoBehaviour
{
    public Button saveBtn;
    public Button loadBtn;

    void Awake()
    {
        saveBtn.onClick.AddListener(SaveGame);
        loadBtn.onClick.AddListener(LoadGame);
    }

    void SaveGame()
    {
        SaveManager.Instance.SaveGame();
        Debug.Log("游戏已保存");
    }

    void LoadGame()
    {
        SaveManager.Instance.LoadGame();
        Debug.Log("游戏已读取");
    }
}
```

#### 语法拆解

##### `saveBtn.onClick.AddListener(SaveGame)` 是什么？

```csharp
saveBtn.onClick.AddListener(SaveGame);
```

| 部分 | 含义 |
|------|------|
| `saveBtn` | Button组件引用 |
| `.onClick` | 按钮点击事件 |
| `.AddListener()` | 添加回调方法 |
| `SaveGame` | 点击时执行的方法 |

**整行人话**：按钮被点击时，执行SaveGame方法。

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 5~6 | 按钮引用 | Inspector拖入按钮 |
| 8 | `void Awake()` | 初始化 |
| 10 | 绑定保存按钮 | 点击保存游戏 |
| 11 | 绑定读档按钮 | 点击读取游戏 |
| 14 | `SaveGame()` | 调用SaveManager保存 |
| 19 | `LoadGame()` | 调用SaveManager读取 |

#### 操作提示

1. 创建两个Button：SaveBtn和LoadBtn
2. 创建空物体挂SaveLoadUI脚本
3. Inspector将按钮拖入对应字段

---

### 案例 3：背包物品拾取与使用

**功能**：拾取场景中的物品放入背包，点击背包物品使用消耗品。

```csharp
using UnityEngine;

public class ItemPickup : MonoBehaviour, IInteractable
{
    public Item item;
    public int quantity = 1;

    public void Interact()
    {
        bool success = InventoryManager.Instance.AddItem(item, quantity);
        if (success)
        {
            Debug.Log("拾取：" + item.itemName + " x" + quantity);
            Destroy(gameObject);
        }
        else
        {
            Debug.Log("背包已满");
        }
    }
}
```

#### 语法拆解

##### `InventoryManager.Instance.AddItem(item, quantity)` 是什么？

```csharp
bool success = InventoryManager.Instance.AddItem(item, quantity);
```

| 部分 | 含义 |
|------|------|
| `InventoryManager.Instance` | 背包管理器单例 |
| `.AddItem()` | 添加物品方法 |
| `item` | 物品配置 |
| `quantity` | 数量 |
| **返回值** | bool，true=成功，false=失败 |

**整行人话**：尝试把物品加入背包，返回是否成功。

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 5 | `public Item item` | 物品配置（ScriptableObject） |
| 6 | `public int quantity` | 拾取数量 |
| 8 | `Interact()` | 实现接口方法 |
| 10 | `AddItem(item, quantity)` | 尝试加入背包 |
| 11 | `if (success)` | 判断是否成功 |
| 13 | `Destroy(gameObject)` | 成功则销毁道具 |
| 16 | `Debug.Log("背包已满")` | 失败则提示 |

#### 操作提示

1. 创建Item配置资产（右键 → RPG → Item）
2. 场景中创建道具物体，挂ItemPickup脚本
3. Inspector拖入Item配置
4. 背包UI需显示物品列表，点击调用UseItem

---

## 【入门阶段小结】

| 维度 | 要点 |
|------|------|
| **任务** | ScriptableObject配置 + QuestManager管理 |
| **存档** | JsonUtility序列化 + persistentDataPath |
| **背包** | List管理物品 + ScriptableObject配置 |
| **案例** | 任务接取、存档读档、物品拾取 |

---

# 第三阶段：进阶篇

## 【阶段总述】

进阶阶段：**任务系统模块化封装**、**存档系统安全与性能**、**背包系统优化**、**常见误区与最佳实践**。

---

## 一、任务系统进阶

### 1.1 条件触发系统

```csharp
using UnityEngine;
using System;

public class GameEventManager : MonoBehaviour
{
    public static GameEventManager Instance { get; private set; }

    public event Action<string, int> OnEnemyKilled;
    public event Action<string, int> OnItemCollected;
    public event Action<string> OnTalkedToNPC;

    void Awake()
    {
        Instance = this;
    }

    public void EnemyKilled(string enemyID, int count = 1)
    {
        OnEnemyKilled?.Invoke(enemyID, count);
    }

    public void ItemCollected(string itemID, int count = 1)
    {
        OnItemCollected?.Invoke(itemID, count);
    }

    public void TalkedToNPC(string npcID)
    {
        OnTalkedToNPC?.Invoke(npcID);
    }
}
```

### 1.2 任务自动追踪

```csharp
public class QuestTracker : MonoBehaviour
{
    void OnEnable()
    {
        GameEventManager.Instance.OnEnemyKilled += HandleEnemyKilled;
        GameEventManager.Instance.OnItemCollected += HandleItemCollected;
    }

    void OnDisable()
    {
        GameEventManager.Instance.OnEnemyKilled -= HandleEnemyKilled;
        GameEventManager.Instance.OnItemCollected -= HandleItemCollected;
    }

    void HandleEnemyKilled(string enemyID, int count)
    {
        foreach (var quest in QuestManager.Instance.activeQuests)
        {
            if (quest.questType == QuestType.Kill && 
                quest.targetID == enemyID)
            {
                QuestManager.Instance.UpdateQuestProgress(quest.questID, count);
            }
        }
    }

    void HandleItemCollected(string itemID, int count)
    {
        foreach (var quest in QuestManager.Instance.activeQuests)
        {
            if (quest.questType == QuestType.Collect && 
                quest.targetID == itemID)
            {
                QuestManager.Instance.UpdateQuestProgress(quest.questID, count);
            }
        }
    }
}
```

---

## 二、存档系统进阶

### 2.1 多存档位

```csharp
using UnityEngine;
using System.IO;

public class MultiSaveManager : MonoBehaviour
{
    public static MultiSaveManager Instance { get; private set; }

    public int saveSlots = 3;

    void Awake()
    {
        Instance = this;
    }

    public void SaveGame(int slot)
    {
        SaveData data = CollectData();
        string json = JsonUtility.ToJson(data, true);
        string path = GetSavePath(slot);
        File.WriteAllText(path, json);
    }

    public bool LoadGame(int slot)
    {
        string path = GetSavePath(slot);
        if (File.Exists(path))
        {
            string json = File.ReadAllText(path);
            SaveData data = JsonUtility.FromJson<SaveData>(json);
            ApplyData(data);
            return true;
        }
        return false;
    }

    string GetSavePath(int slot)
    {
        return Application.persistentDataPath + $"/save_{slot}.json";
    }

    SaveData CollectData() { /* ... */ return null; }
    void ApplyData(SaveData data) { /* ... */ }
}
```

### 2.2 存档加密

```csharp
using UnityEngine;
using System.IO;
using System.Security.Cryptography;
using System.Text;

public class SecureSaveManager
{
    private static readonly string KEY = "YourSecretKey16";
    private static readonly string IV = "YourIV16Bytes!";

    public static void SaveEncrypted(string path, SaveData data)
    {
        string json = JsonUtility.ToJson(data);
        byte[] encrypted = EncryptString(json);
        File.WriteAllBytes(path, encrypted);
    }

    public static SaveData LoadEncrypted(string path)
    {
        if (!File.Exists(path)) return null;
        byte[] encrypted = File.ReadAllBytes(path);
        string json = DecryptString(encrypted);
        return JsonUtility.FromJson<SaveData>(json);
    }

    static byte[] EncryptString(string plainText)
    {
        using (Aes aes = Aes.Create())
        {
            aes.Key = Encoding.UTF8.GetBytes(KEY);
            aes.IV = Encoding.UTF8.GetBytes(IV);
            ICryptoTransform encryptor = aes.CreateEncryptor(aes.Key, aes.IV);
            using (MemoryStream ms = new MemoryStream())
            using (CryptoStream cs = new CryptoStream(ms, encryptor, CryptoStreamMode.Write))
            using (StreamWriter sw = new StreamWriter(cs))
            {
                sw.Write(plainText);
            }
            return ms.ToArray();
        }
    }

    static string DecryptString(byte[] cipherText)
    {
        using (Aes aes = Aes.Create())
        {
            aes.Key = Encoding.UTF8.GetBytes(KEY);
            aes.IV = Encoding.UTF8.GetBytes(IV);
            ICryptoTransform decryptor = aes.CreateDecryptor(aes.Key, aes.IV);
            using (MemoryStream ms = new MemoryStream(cipherText))
            using (CryptoStream cs = new CryptoStream(ms, decryptor, CryptoStreamMode.Read))
            using (StreamReader sr = new StreamReader(cs))
            {
                return sr.ReadToEnd();
            }
        }
    }
}
```

---

## 三、背包系统进阶

### 3.1 背包UI优化

```csharp
using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;

public class InventoryUI : MonoBehaviour
{
    public GameObject slotPrefab;
    public Transform slotParent;

    void OnEnable()
    {
        UpdateUI();
    }

    public void UpdateUI()
    {
        foreach (Transform child in slotParent)
        {
            Destroy(child.gameObject);
        }

        foreach (var item in InventoryManager.Instance.items)
        {
            GameObject slot = Instantiate(slotPrefab, slotParent);
            Item data = Resources.Load<Item>("Items/" + item.itemID);
            slot.GetComponent<Image>().sprite = data.icon;
            slot.GetComponentInChildren<Text>().text = item.quantity.ToString();
        }
    }
}
```

### 3.2 对象池优化

```csharp
using UnityEngine;
using System.Collections.Generic;

public class SlotPool : MonoBehaviour
{
    public static SlotPool Instance;
    public GameObject prefab;
    public int poolSize = 20;

    Queue<GameObject> pool = new Queue<GameObject>();

    void Awake()
    {
        Instance = this;
        for (int i = 0; i < poolSize; i++)
        {
            GameObject obj = Instantiate(prefab);
            obj.SetActive(false);
            obj.transform.SetParent(transform);
            pool.Enqueue(obj);
        }
    }

    public GameObject Get()
    {
        return pool.Count > 0 ? pool.Dequeue() : Instantiate(prefab);
    }

    public void Return(GameObject obj)
    {
        obj.SetActive(false);
        pool.Enqueue(obj);
    }
}
```

---

## 四、常见误区与最佳实践

| 误区 | 正确做法 |
|------|----------|
| 用PlayerPrefs存完整进度 | 用JsonUtility + JSON文件 |
| 存档路径用dataPath | 用persistentDataPath |
| 频繁Save() | 只在关键节点Save |
| 任务进度硬编码 | 用ScriptableObject配置 |
| 背包直接存ScriptableObject | 存ID，运行时加载 |
| 忘记处理空存档 | Load时检查文件是否存在 |
| 存档类缺[Serializable] | 必须加Serializable标记 |

---

## 【进阶阶段小结】

| 维度 | 要点 |
|------|------|
| 任务 | 事件驱动自动追踪、条件系统 |
| 存档 | 多存档位、加密、性能优化 |
| 背包 | 对象池、UI优化 |
| 避坑 | persistentDataPath、Serializable、事件清理 |

---

# 【全文总结】

## 最重要的一行代码

```csharp
string json = JsonUtility.ToJson(currentData, true);
File.WriteAllText(Application.persistentDataPath + "/save.json", json);
```

| 部分 | 含义 |
|------|------|
| `JsonUtility.ToJson` | 对象转JSON |
| `currentData` | 存档数据对象 |
| `File.WriteAllText` | 写入文件 |
| `persistentDataPath` | 跨平台存档路径 |

## 三阶段对照

| 阶段 | 代表案例 |
|------|----------|
| 零基础 | 任务UI搭建、PlayerPrefs理解 |
| 入门 | 任务系统、存档系统、背包系统 |
| 进阶 | 事件驱动、多存档位、加密 |

## API 速查

| 代码 | 作用 |
|------|------|
| `PlayerPrefs.SetInt()` | 简单存档 |
| `JsonUtility.ToJson()` | 对象转JSON |
| `JsonUtility.FromJson()` | JSON转对象 |
| `File.WriteAllText()` | 写入文件 |
| `persistentDataPath` | 存档路径 |
| `Resources.Load()` | 加载资源 |
| `ScriptableObject` | 数据配置 |

## 学习自检

- [ ] 能创建任务配置并实现任务系统
- [ ] 能用JsonUtility实现存档读档
- [ ] 能实现背包物品拾取与使用
- [ ] 理解persistentDataPath的作用
- [ ] 掌握ScriptableObject数据配置

---

## 参考资料

| 类型 | 链接 |
|------|------|
| PlayerPrefs | https://docs.unity3d.com/ScriptReference/PlayerPrefs.html |
| JsonUtility | https://docs.unity3d.com/ScriptReference/JsonUtility.html |
| ScriptableObject | https://docs.unity3d.com/ScriptReference/ScriptableObject.html |

---

*文档版本：与 major3 系列、Week2_Xmind、Week3_Xmind、Week4_Xmind 同系列模板。*