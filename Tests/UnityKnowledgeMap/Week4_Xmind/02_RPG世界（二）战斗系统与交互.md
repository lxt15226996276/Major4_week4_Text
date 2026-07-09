# 综合案例项目实例RPG世界（二）——战斗系统与交互

> 参照：[Unity 官方 Manual - Physics.Raycast](https://docs.unity3d.com/ScriptReference/Physics.Raycast.html) · [DOTween](https://dotween.demigiant.com/) · [UI System](https://docs.unity3d.com/Manual/UISystem.html)  
> 关联文档：[01_RPG世界（一）.md](./01_RPG世界（一）项目初始化与玩家基础.md) · [03_RPG世界（三）.md](./03_RPG世界（三）任务与存档.md) · [04_RPG世界（四）.md](./04_RPG世界（四）AI与优化.md) · [05_综合复习.md](./05_综合复习.md)  
> 学习路径：**零基础 → 入门 → 进阶**，每阶段采用 **总—分—总** 结构。  
> 讲解维度：**定义 → 本质 → 特点 → 适用场景 → 原理 → API → 步骤 → 案例 → 避坑**（进阶含项目架构 / 模块化 / 性能优化）。  
> 案例讲解：遵循 **案例代码讲解模板**（功能 → 代码 → 语法拆解 → 逐行详解 → 操作提示）。  
> API 讲解：入门/进阶 API 章节均采用 **逐词读懂** 格式（与 [01_PlayerPrefs.md](../major3/01_PlayerPrefs.md) 一致：类型 → 参数 → 整行人话）。

---

## 【全文总述】

**RPG（角色扮演游戏）世界综合案例** 第二章，重点讲解 **战斗系统、交互系统、射线检测、UI界面** 四大核心模块。  
学习本案例，你将掌握：
- 如何实现玩家攻击与伤害计算
- 如何制作血条和战斗UI
- 如何用射线检测实现点击交互
- 如何实现物品拾取与对话系统
- 如何用DOTween做UI动画

### 思维导图总览

```
RPG 世界综合案例（二）——战斗系统与交互
│
├── 战斗系统（核心玩法 — 玩家与敌人的对抗）
│   │
│   ├── 定义：玩家攻击、敌人受伤、血量管理、战斗判定的完整逻辑体系
│   │
│   ├── 本质：碰撞体/射线检测 → 伤害计算 → 血量更新 → UI反馈 → 状态变化
│   │   ├── 攻击检测：Raycast / Collider.OnTriggerEnter
│   │   ├── 伤害公式：攻击力 - 防御力 = 实际伤害
│   │   ├── 血量系统：当前血量 vs 最大血量
│   │   └── 战斗状态：攻击中、受伤、死亡
│   │
│   ├── 核心原理：输入触发 → 动画播放 → 帧检测 → 命中判定 → 伤害结算
│   │
│   ├── 核心 API 及参数
│   │   ├── Physics.Raycast(ray, out hit, distance)：射线检测
│   │   ├── Animator.SetTrigger("Attack")：触发攻击动画
│   │   └── Mathf.Clamp(value, min, max)：数值限制
│   │
│   └── 标准使用步骤
│       ├── 步骤1 创建攻击脚本（PlayerAttack）
│       ├── 步骤2 配置伤害公式与属性系统
│       ├── 步骤3 制作血条 UI
│       └── 步骤4 实现死亡逻辑
│
├── 交互系统（世界互动 — 玩家与环境的交流）
│   │
│   ├── 定义：玩家通过点击/按键与场景物体、NPC、道具进行互动的机制
│   │
│   ├── 本质：射线检测 → 判定目标类型 → 执行对应交互逻辑
│   │   ├── 物品拾取：检测道具 → 添加到背包 → 销毁道具
│   │   ├── NPC对话：检测NPC → 显示对话框 → 播放对话
│   │   └── 物体交互：检测可交互物体 → 触发机关/开门
│   │
│   ├── 核心原理：Input.GetMouseButtonDown → ScreenPointToRay → Raycast → 回调
│   │
│   ├── 核心 API 及参数
│   │   ├── Camera.ScreenPointToRay(mousePos)：屏幕点转射线
│   │   ├── Physics.RaycastAll(ray, distance)：检测所有命中
│   │   └── LayerMask：按层过滤检测
│   │
│   └── 标准使用步骤
│       ├── 步骤1 创建交互管理器（InteractionManager）
│       ├── 步骤2 为可交互物体添加组件
│       ├── 步骤3 实现点击检测逻辑
│       └── 步骤4 制作交互UI反馈
│
├── UI界面系统（信息展示 — 玩家查看数据的窗口）
│   │
│   ├── 定义：Canvas + UI元素（Image、Text、Button）组成的用户界面
│   │
│   ├── 本质：RectTransform布局 → Canvas渲染 → 事件系统交互
│   │   ├── Canvas：UI渲染容器
│   │   ├── Image：图片显示（血条、图标）
│   │   ├── Text：文字显示（血量、提示）
│   │   └── Button：交互按钮
│   │
│   └── 实战：战斗UI与交互UI
│       ├── 血条制作（Slider/Image.fillAmount）
│       ├── 伤害数字弹出
│       └── 对话面板
│
├── DOTween动画（流畅体验 — UI与物体的动效）
│   │
│   ├── 定义：第三方补间动画库，实现平滑移动、缩放、淡入淡出等效果
│   │
│   ├── 本质：数值插值 → 每帧更新目标属性 → 动画完成回调
│   │   ├── DOMove：位置动画
│   │   ├── DOScale：缩放动画
│   │   ├── DOFade：透明度动画
│   │   └── Sequence：动画序列
│   │
│   └── 实战：战斗特效与UI动画
│       ├── 攻击动作缓冲
│       ├── 受伤抖动
│       └── UI面板淡入淡出
│
├── 第一阶段：零基础（战斗基础 + 交互概念）
│   ├── 理解战斗系统与交互系统的定义
│   ├── 逐词读懂：Physics.Raycast(ray, out hit)
│   └── 完成战斗UI基础搭建
│
├── 第二阶段：入门（战斗逻辑 + 交互实现 + UI）
│   ├── PlayerAttack 攻击脚本详解
│   ├── 血条系统制作
│   ├── 交互管理器实现
│   ├── 拾取与对话案例
│   └── DOTween 基础用法
│
└── 第三阶段：进阶（架构设计 + 模块化 + 优化）
    ├── 战斗系统模块化封装
    ├── 事件驱动架构
    ├── 性能优化：对象池、批处理
    └── 常见误区与最佳实践
```

| 学习阶段 | 学习目标 |
|----------|----------|
| **零基础** | 理解战斗与交互概念；读懂 Raycast 核心代码；完成战斗UI基础搭建 |
| **入门** | 实现攻击、血条、拾取、对话；掌握 DOTween 基础；完成 3 个案例 |
| **进阶** | 理解模块化战斗架构；会封装交互系统；掌握性能优化技巧 |

### 讲师知识框架速览（全文脉络）

| 维度 | 零基础讲 | 入门讲 | 进阶讲 |
|------|----------|--------|--------|
| 定义 | ✅ | 回顾 | 回顾 |
| 本质 | ✅ | — | — |
| 特点 | ✅ | — | 架构特点 |
| 适用场景 | ✅ | — | 项目选型 |
| 核心原理 | 战斗流程 | ✅ 攻击检测链路 | 模块化设计 |
| 核心 API | 读懂 Raycast | ✅ Physics + Animator + DOTween | 封装与优化 |
| 使用步骤 | UI搭建 | ✅ 战斗实现步骤 | 架构搭建 |
| 调用时机 | — | ✅ Update/动画事件 | 生命周期管理 |
| 避坑 | — | 初步 | ✅ |

---

# 第一阶段：零基础篇

## 【阶段总述】

零基础阶段建立**正确认知**：战斗系统是什么、交互系统是什么、射线检测怎么工作。  
同时学会**读懂** `Physics.Raycast(ray, out hit)` 每个部分的含义，并完成战斗UI基础搭建。

---

## 一、定义 — 战斗与交互是什么？

| 项目 | 说明 |
|------|------|
| **战斗系统** | 玩家攻击、敌人受伤、血量管理、战斗判定的完整逻辑 |
| **交互系统** | 玩家与场景物体、NPC、道具进行互动的机制 |
| **射线检测** | 从相机发出射线，检测场景中碰撞体的技术 |
| **血条** | 显示角色血量的UI元素 |
| **一句话** | 战斗 = 攻击检测 + 伤害计算；交互 = 点击检测 + 执行动作 |

```
战斗系统结构示例
PlayerAttack
    ├── 攻击输入（鼠标左键/空格键）
    ├── 攻击动画（SetTrigger）
    ├── 攻击检测（Raycast/Trigger）
    │   ├── 检测范围
    │   ├── Layer过滤
    │   └── 命中判定
    ├── 伤害计算（攻击力 - 防御力）
    └── 伤害反馈（UI血条、数字弹出）
```

---

## 二、本质 — 战斗与交互如何工作？

### 2.1 战斗系统本质

```
攻击流程
输入（左键）→ 播放攻击动画 → 动画事件触发检测 → Raycast检测 → 命中敌人 → 伤害计算 → 更新血条
```

| 环节 | 本质理解 |
|------|----------|
| **输入检测** | 监听用户点击，判断是否可以攻击 |
| **动画播放** | 通过 Animator 播放攻击动作 |
| **攻击检测** | 用射线或碰撞体检测前方敌人 |
| **伤害计算** | 根据属性算出实际伤害值 |
| **反馈更新** | 更新敌人血量和UI显示 |

### 2.2 交互系统本质

```
交互流程
输入（点击）→ 屏幕点转射线 → Raycast检测 → 获取交互组件 → 执行交互逻辑 → UI反馈
```

| 环节 | 本质理解 |
|------|----------|
| **点击检测** | 检测鼠标点击的屏幕位置 |
| **射线转换** | 将屏幕点转换为3D空间射线 |
| **物体检测** | 检测射线命中的物体 |
| **交互执行** | 根据物体类型执行对应动作 |

---

## 三、特点与适用场景

### 3.1 战斗系统特点

| 特点 | 说明 |
|------|------|
| **状态依赖** | 攻击、受伤、死亡等状态相互影响 |
| **帧敏感** | 攻击判定需要精确到帧 |
| **动画同步** | 攻击动作与伤害判定需同步 |
| **反馈及时** | 玩家需要即时看到伤害效果 |

### 3.2 交互系统特点

| 特点 | 说明 |
|------|------|
| **点击触发** | 通过鼠标点击触发 |
| **距离限制** | 只能与一定范围内的物体交互 |
| **类型多样** | 拾取、对话、机关等多种交互类型 |
| **优先级** | 多个物体重叠时需确定优先顺序 |

### 3.3 适用场景

| 场景 | 是否适用 | 原因 |
|------|----------|------|
| 近战攻击 | ✅ | Raycast检测前方敌人 |
| 远程攻击 | ✅ | 子弹飞行检测 |
| 物品拾取 | ✅ | 点击地面物品 |
| NPC对话 | ✅ | 点击NPC触发对话 |
| 开门/开关 | ✅ | 点击可交互物体 |

---

## 四、核心一课：如何读懂射线检测

```csharp
Physics.Raycast(ray, out hit);
```

| 部分 | 含义 |
|------|------|
| `Physics` | Unity物理类，提供射线检测等静态方法 |
| `.Raycast` | 方法名：发射射线检测碰撞体 |
| `ray` | 参数1：Ray类型，包含起点和方向 |
| `out hit` | 参数2：输出参数，命中时存储碰撞信息 |
| **返回值** | bool，true=命中，false=未命中 |

**整行人话**：发射一条射线，如果碰到碰撞体就返回true，并把碰撞信息存到hit里。

```csharp
// 完整的射线检测代码片段
Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
if (Physics.Raycast(ray, out RaycastHit hit))
{
    Debug.Log("命中：" + hit.collider.name);
}
```

| 行 | 含义 |
|----|------|
| `ScreenPointToRay(mousePos)` | 将鼠标屏幕坐标转换为世界射线 |
| `Physics.Raycast(ray, out hit)` | 发射射线检测碰撞 |
| `hit.collider.name` | 获取被命中物体的名称 |

---

## 五、零基础实战：战斗UI搭建

### 5.1 步骤一：创建Canvas

1. 菜单 **GameObject → UI → Canvas**
2. 右键 Canvas → **UI → Panel**，命名为 `HUD`

### 5.2 步骤二：创建血条

1. 右键 HUD → **UI → Slider**，命名为 `HealthBar`
2. 设置 Slider 参数：
   - **Direction**：Left to Right
   - **Min Value**：0
   - **Max Value**：100
   - **Whole Numbers**：false
3. 删除 Handle Slide Area（可选）
4. 调整背景色为红色，填充色为绿色

### 5.3 步骤三：创建伤害数字预制体

1. 右键 HUD → **UI → Text**，命名为 `DamageText`
2. 设置字体大小、颜色（红色）
3. 拖入 Prefabs 文件夹，命名为 `DamageText.prefab`
4. 删除场景中的 DamageText

### 5.4 步骤四：创建对话框

1. 右键 HUD → **UI → Panel**，命名为 `DialogPanel`
2. 右键 DialogPanel → **UI → Text**，命名为 `DialogText`
3. 设置 DialogPanel 初始状态为隐藏

---

## 【零基础阶段小结】

| 维度 | 要点 |
|------|------|
| **定义** | 战斗=攻击+伤害；交互=点击+动作；射线=检测工具 |
| **本质** | 战斗=输入→动画→检测→计算→反馈；交互=点击→射线→检测→执行 |
| **步骤** | 创建Canvas → 血条 → 伤害数字 → 对话框 |
| **读懂** | `Physics.Raycast(ray, out hit)` |

**阶段检验**：能说出战斗流程；能画出交互流程图；能读懂射线检测代码。

---

# 第二阶段：入门篇

## 【阶段总述】

入门阶段掌握 **攻击逻辑、血条系统、交互管理器、DOTween** 四大核心模块，并完成 3 个实战案例。  
重点：**动画事件触发攻击检测**；**Raycast实现点击交互**；**DOTween做UI动画**。

---

## 一、PlayerAttack 核心代码详解

### 1.1 Raycast API — 逐词读懂

#### `Physics.Raycast(ray, out hit, distance)` 是什么？

```csharp
Physics.Raycast(ray, out hit, distance);
```

| 部分 | 含义 |
|------|------|
| `Physics` | Unity物理静态类 |
| `.Raycast` | **方法名**：发射射线检测碰撞体 |
| `ray` | **参数1**：Ray，射线（起点+方向） |
| `out hit` | **参数2**：输出参数，命中时填充 RaycastHit |
| `distance` | **参数3**：射线最大距离（可选，默认无限远） |
| **返回值** | bool，true=命中 |

**整行人话**：从射线起点朝方向发射，最多检测distance距离内的碰撞体，命中就返回true。

#### `Camera.ScreenPointToRay(mousePos)` 是什么？

```csharp
Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
```

| 部分 | 含义 |
|------|------|
| `ScreenPointToRay` | **方法名**：屏幕像素坐标转换为世界射线 |
| `Input.mousePosition` | **参数**：鼠标屏幕坐标（像素） |
| **返回值** | Ray，从相机穿过鼠标点的射线 |

**整行人话**：把鼠标点击的2D屏幕点，变成3D世界里的一条激光。

#### `LayerMask.GetMask("Enemy")` 是什么？

```csharp
LayerMask enemyLayer = LayerMask.GetMask("Enemy");
```

| 部分 | 含义 |
|------|------|
| `LayerMask` | 层掩码类型，用于过滤射线检测 |
| `GetMask("Enemy")` | **静态方法**：获取名为"Enemy"的层掩码 |
| **用途** | 只检测指定层的物体 |

**整行人话**：告诉射线检测只看Enemy层的物体，其他层忽略。

---

### 1.2 PlayerAttack 完整代码

```csharp
using UnityEngine;

public class PlayerAttack : MonoBehaviour
{
    CharacterController controller;
    Animator animator;
    public float attackRange = 3f;
    public int attackDamage = 20;
    public LayerMask enemyLayer;

    bool isAttacking;

    void Awake()
    {
        controller = GetComponent<CharacterController>();
        animator = GetComponent<Animator>();
    }

    void Update()
    {
        if (Input.GetMouseButtonDown(0) && !isAttacking)
        {
            Attack();
        }
    }

    void Attack()
    {
        isAttacking = true;
        animator.SetTrigger("Attack");
    }

    public void OnAttackHit()
    {
        Ray ray = new Ray(transform.position + Vector3.up, transform.forward);
        if (Physics.Raycast(ray, out RaycastHit hit, attackRange, enemyLayer))
        {
            EnemyHealth enemy = hit.collider.GetComponent<EnemyHealth>();
            if (enemy != null)
            {
                enemy.TakeDamage(attackDamage);
            }
        }
        isAttacking = false;
    }
}
```

#### 语法拆解

##### `new Ray(origin, direction)` 是什么？

```csharp
Ray ray = new Ray(transform.position + Vector3.up, transform.forward);
```

| 部分 | 含义 |
|------|------|
| `Ray` | 射线结构体，包含起点和方向 |
| `transform.position + Vector3.up` | 起点：玩家位置向上偏移（从胸口发出） |
| `transform.forward` | 方向：玩家正前方 |

**整行人话**：从玩家胸口向前方发射一条射线。

##### `hit.collider.GetComponent<EnemyHealth>()` 是什么？

```csharp
EnemyHealth enemy = hit.collider.GetComponent<EnemyHealth>();
```

| 部分 | 含义 |
|------|------|
| `hit.collider` | 被命中物体的碰撞体 |
| `GetComponent<EnemyHealth>()` | 获取碰撞体所在物体上的 EnemyHealth 组件 |

**整行人话**：拿到被打中的敌人的血量组件。

---

## 二、血条系统制作

### 2.1 EnemyHealth 完整代码

```csharp
using UnityEngine;
using UnityEngine.UI;

public class EnemyHealth : MonoBehaviour
{
    public int maxHealth = 100;
    public int currentHealth;
    public Slider healthSlider;
    public Transform damageTextPrefab;

    void Awake()
    {
        currentHealth = maxHealth;
        healthSlider.maxValue = maxHealth;
        healthSlider.value = currentHealth;
    }

    public void TakeDamage(int damage)
    {
        currentHealth = Mathf.Max(0, currentHealth - damage);
        healthSlider.value = currentHealth;
        ShowDamageText(damage);

        if (currentHealth <= 0)
        {
            Die();
        }
    }

    void ShowDamageText(int damage)
    {
        Transform text = Instantiate(damageTextPrefab, transform.position + Vector3.up, Quaternion.identity);
        text.GetComponent<Text>().text = "-" + damage;
        Destroy(text.gameObject, 1f);
    }

    void Die()
    {
        Debug.Log(gameObject.name + " 死亡");
        Destroy(gameObject, 0.5f);
    }
}
```

#### 语法拆解

##### `Mathf.Max(0, currentHealth - damage)` 是什么？

```csharp
currentHealth = Mathf.Max(0, currentHealth - damage);
```

| 部分 | 含义 |
|------|------|
| `Mathf.Max` | 取两个数中较大的值 |
| `0` | 最小值，防止血量变成负数 |
| `currentHealth - damage` | 扣除伤害后的血量 |

**整行人话**：扣血但不低于0。

##### `Instantiate(prefab, position, rotation)` 是什么？

```csharp
Transform text = Instantiate(damageTextPrefab, transform.position + Vector3.up, Quaternion.identity);
```

| 部分 | 含义 |
|------|------|
| `Instantiate` | 创建预制体实例 |
| `damageTextPrefab` | 要创建的预制体 |
| `transform.position + Vector3.up` | 创建位置：敌人位置上方 |
| `Quaternion.identity` | 旋转：无旋转 |

**整行人话**：在敌人头顶创建一个伤害数字。

---

## 三、交互管理器实现

### 3.1 InteractionManager 完整代码

```csharp
using UnityEngine;

public class InteractionManager : MonoBehaviour
{
    Camera mainCam;
    public float interactDistance = 5f;
    public LayerMask interactLayer;

    void Awake()
    {
        mainCam = Camera.main;
    }

    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            CheckInteraction();
        }
    }

    void CheckInteraction()
    {
        Ray ray = mainCam.ScreenPointToRay(Input.mousePosition);
        if (Physics.Raycast(ray, out RaycastHit hit, interactDistance, interactLayer))
        {
            IInteractable interactable = hit.collider.GetComponent<IInteractable>();
            if (interactable != null)
            {
                interactable.Interact();
            }
        }
    }
}

public interface IInteractable
{
    void Interact();
}
```

#### 语法拆解

##### `public interface IInteractable` 是什么？

```csharp
public interface IInteractable
{
    void Interact();
}
```

| 部分 | 含义 |
|------|------|
| `interface` | 接口定义，声明一组方法签名 |
| `IInteractable` | 接口名，约定交互行为 |
| `void Interact()` | 接口方法，所有可交互物体必须实现 |

**整行人话**：定义一个"可交互"的标准，所有想被点击的物体都要实现这个方法。

##### `hit.collider.GetComponent<IInteractable>()` 是什么？

```csharp
IInteractable interactable = hit.collider.GetComponent<IInteractable>();
```

| 部分 | 含义 |
|------|------|
| `GetComponent<IInteractable>()` | 获取实现了 IInteractable 接口的组件 |
| **效果** | 不管是道具还是NPC，只要实现了接口就能交互 |

**整行人话**：拿到被点击物体的交互组件，执行交互。

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

### 案例 1：玩家攻击系统

**功能**：鼠标左键触发攻击，射线检测前方敌人并造成伤害。

```csharp
using UnityEngine;

public class PlayerAttackSystem : MonoBehaviour
{
    Animator animator;
    public float attackRange = 3f;
    public int damage = 20;
    public LayerMask enemyLayer;

    void Awake()
    {
        animator = GetComponent<Animator>();
    }

    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            animator.SetTrigger("Attack");
        }
    }

    public void OnAttackFrame()
    {
        Vector3 startPos = transform.position + Vector3.up * 1.5f;
        Ray ray = new Ray(startPos, transform.forward);
        
        Debug.DrawRay(startPos, transform.forward * attackRange, Color.red, 0.1f);

        if (Physics.Raycast(ray, out RaycastHit hit, attackRange, enemyLayer))
        {
            EnemyHealth enemy = hit.collider.GetComponent<EnemyHealth>();
            if (enemy != null)
            {
                enemy.TakeDamage(damage);
            }
        }
    }
}
```

#### 语法拆解

##### `animator.SetTrigger("Attack")` 是什么？

```csharp
animator.SetTrigger("Attack");
```

| 部分 | 含义 |
|------|------|
| `animator` | Animator组件引用 |
| `SetTrigger` | 设置触发器参数（触发后自动重置） |
| `"Attack"` | 参数名，须与Animator Controller中定义一致 |

**整行人话**：触发攻击动画一次。

##### `Debug.DrawRay(start, direction, color, duration)` 是什么？

```csharp
Debug.DrawRay(startPos, transform.forward * attackRange, Color.red, 0.1f);
```

| 部分 | 含义 |
|------|------|
| `Debug.DrawRay` | 在Scene视图绘制射线（仅调试） |
| `startPos` | 起点 |
| `direction * attackRange` | 方向和长度 |
| `Color.red` | 颜色 |
| `0.1f` | 显示时长（秒） |

**整行人话**：在Scene视图画出射线，方便调试攻击范围。

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 5 | `Animator animator` | 动画器引用 |
| 6~8 | 攻击参数 | 范围、伤害、敌人层 |
| 10~12 | 初始化 | 获取Animator组件 |
| 14 | `void Update()` | 每帧检测输入 |
| 16 | `GetMouseButtonDown(0)` | 鼠标左键按下 |
| 17 | `SetTrigger("Attack")` | 触发攻击动画 |
| 21 | `OnAttackFrame()` | 动画事件调用 |
| 22 | `startPos` | 射线起点（胸口高度） |
| 23 | 创建射线 | 从胸口向前方 |
| 25 | `DrawRay` | 调试绘制射线 |
| 27 | `Raycast` | 射线检测敌人 |
| 29 | `GetComponent<EnemyHealth>()` | 获取敌人血量组件 |
| 31 | `TakeDamage(damage)` | 造成伤害 |

#### 操作提示

1. 在 Animator Controller 的 Attack 动画中添加 **Animation Event**
2. 事件函数名填 `OnAttackFrame`
3. 敌人Layer设为"Enemy"，脚本中 enemyLayer 勾选 Enemy
4. 敌人需有 **Collider** 和 **EnemyHealth** 组件

---

### 案例 2：物品拾取系统

**功能**：点击场景中的道具，自动拾取到背包。

```csharp
using UnityEngine;

public class ItemPickup : MonoBehaviour, IInteractable
{
    public string itemName = "金币";
    public int amount = 10;

    public void Interact()
    {
        Debug.Log("拾取：" + itemName + " x" + amount);
        Destroy(gameObject);
    }

    void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(transform.position, 0.5f);
    }
}
```

#### 语法拆解

##### `: IInteractable` 是什么？

```csharp
public class ItemPickup : MonoBehaviour, IInteractable
```

| 部分 | 含义 |
|------|------|
| `: MonoBehaviour` | 继承MonoBehaviour，可挂载到物体 |
| `, IInteractable` | 实现IInteractable接口 |
| **义务** | 必须实现接口中的 `Interact()` 方法 |

**整行人话**：这个脚本既能挂到物体上，又符合"可交互"标准。

##### `OnDrawGizmosSelected()` 是什么？

```csharp
void OnDrawGizmosSelected()
{
    Gizmos.color = Color.yellow;
    Gizmos.DrawWireSphere(transform.position, 0.5f);
}
```

| 部分 | 含义 |
|------|------|
| `OnDrawGizmosSelected` | 选中物体时在Scene视图绘制Gizmo |
| `Gizmos.DrawWireSphere` | 绘制空心球体 |

**整行人话**：选中道具时显示黄色范围球，方便编辑。

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `using UnityEngine;` | 引用Unity命名空间 |
| 3 | `: MonoBehaviour, IInteractable` | 继承并实现接口 |
| 5~6 | 物品参数 | 名称和数量 |
| 8 | `public void Interact()` | 实现接口方法 |
| 10 | `Debug.Log` | 打印拾取信息 |
| 11 | `Destroy(gameObject)` | 销毁道具 |
| 14 | `OnDrawGizmosSelected()` | 选中时绘制Gizmo |

#### 操作提示

1. 创建空物体命名为 `Coin`
2. 添加 **SphereCollider**（勾选 IsTrigger）
3. 添加 **ItemPickup** 脚本
4. 将物体Layer设为"Interactable"
5. InteractionManager 的 interactLayer 勾选 Interactable

---

### 案例 3：NPC对话系统

**功能**：点击NPC弹出对话框，显示对话内容。

```csharp
using UnityEngine;
using UnityEngine.UI;

public class NPCDialogue : MonoBehaviour, IInteractable
{
    public string[] dialogues = { "欢迎来到这个世界！", "你看起来很强壮。", "小心森林里的怪物。" };
    public Text dialogueText;
    public GameObject dialoguePanel;

    int currentIndex = 0;

    public void Interact()
    {
        currentIndex = 0;
        ShowDialogue();
    }

    void ShowDialogue()
    {
        dialoguePanel.SetActive(true);
        dialogueText.text = dialogues[currentIndex];
    }

    public void NextDialogue()
    {
        currentIndex++;
        if (currentIndex < dialogues.Length)
        {
            dialogueText.text = dialogues[currentIndex];
        }
        else
        {
            dialoguePanel.SetActive(false);
        }
    }
}
```

#### 语法拆解

##### `public string[] dialogues` 是什么？

```csharp
public string[] dialogues = { "欢迎来到这个世界！", "你看起来很强壮。" };
```

| 部分 | 含义 |
|------|------|
| `string[]` | 字符串数组，存储多个对话 |
| `{ ... }` | 初始化列表，包含多条对话 |

**整行人话**：一个装着多句话的盒子。

##### `dialoguePanel.SetActive(true)` 是什么？

```csharp
dialoguePanel.SetActive(true);
```

| 部分 | 含义 |
|------|------|
| `SetActive` | 设置物体激活/禁用 |
| `true` | 激活，显示对话框 |
| `false` | 禁用，隐藏对话框 |

**整行人话**：显示/隐藏对话框。

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 5 | `string[] dialogues` | 对话数组 |
| 6~7 | UI引用 | 对话文字和面板 |
| 9 | `currentIndex` | 当前对话索引 |
| 11 | `Interact()` | 实现接口方法 |
| 12 | `currentIndex = 0` | 重置到第一句 |
| 13 | `ShowDialogue()` | 显示对话框 |
| 16 | `SetActive(true)` | 显示面板 |
| 17 | `dialogueText.text = ...` | 设置对话内容 |
| 20 | `NextDialogue()` | 下一句（按钮调用） |
| 21 | `currentIndex++` | 索引加1 |
| 22 | 判断是否还有对话 | 没说完继续 |
| 26 | `SetActive(false)` | 说完隐藏面板 |

#### 操作提示

1. 在DialogPanel上添加 **Button**，命名为 `NextBtn`
2. Button的OnClick事件绑定 `NPCDialogue.NextDialogue`
3. NPC需有 **Collider** 和 **NPCDialogue** 脚本
4. Layer设为"Interactable"

---

## 五、DOTween 基础用法

### 5.1 DOTween 安装

1. 菜单 **Window → Package Manager**
2. 点击 **+ → Add package from git URL**
3. 输入：`com.unity.nuget.newtonsoft-json`（如需要）
4. 从 Asset Store 下载 DOTween 并导入

### 5.2 常用 DOTween 方法

| 方法 | 作用 | 示例 |
|------|------|------|
| `transform.DOMove(target, duration)` | 移动到目标位置 | `transform.DOMove(new Vector3(0,0,5), 1f)` |
| `transform.DOScale(target, duration)` | 缩放到目标大小 | `transform.DOScale(Vector3.one * 2, 0.5f)` |
| `transform.DORotate(target, duration)` | 旋转到目标角度 | `transform.DORotate(new Vector3(0,180,0), 1f)` |
| `image.DOFade(alpha, duration)` | 淡入淡出 | `image.DOFade(0, 0.5f)` |
| `text.DOText(text, duration)` | 打字机效果 | `text.DOText("Hello", 2f)` |

### 5.3 战斗UI动画示例

```csharp
using UnityEngine;
using UnityEngine.UI;
using DG.Tweening;

public class DamagePopup : MonoBehaviour
{
    Text damageText;

    void Awake()
    {
        damageText = GetComponent<Text>();
    }

    public void ShowDamage(int damage)
    {
        damageText.text = "-" + damage;
        transform.localScale = Vector3.zero;
        
        transform.DOScale(Vector3.one, 0.2f).SetEase(Ease.OutBack);
        transform.DOMove(transform.position + Vector3.up * 1f, 0.8f);
        damageText.DOFade(0, 0.8f).OnComplete(() => Destroy(gameObject));
    }
}
```

#### 语法拆解

##### `transform.DOScale(Vector3.one, 0.2f)` 是什么？

```csharp
transform.DOScale(Vector3.one, 0.2f).SetEase(Ease.OutBack);
```

| 部分 | 含义 |
|------|------|
| `DOScale` | DOTween扩展方法：缩放动画 |
| `Vector3.one` | 目标缩放（1倍） |
| `0.2f` | 动画时长（秒） |
| `SetEase(Ease.OutBack)` | 设置缓动函数（回弹效果） |

**整行人话**：0.2秒内放大到1倍，带回弹效果。

##### `.OnComplete(() => Destroy(gameObject))` 是什么？

```csharp
damageText.DOFade(0, 0.8f).OnComplete(() => Destroy(gameObject));
```

| 部分 | 含义 |
|------|------|
| `DOFade(0, 0.8f)` | 0.8秒内透明度变为0 |
| `OnComplete(callback)` | 动画完成后执行回调 |
| `() => Destroy(gameObject)` | Lambda表达式：销毁物体 |

**整行人话**：淡出后自动销毁物体。

---

## 【入门阶段小结】

| 维度 | 要点 |
|------|------|
| **攻击** | Raycast检测 + 动画事件触发 |
| **血条** | Slider控制 + 伤害数字弹出 |
| **交互** | IInteractable接口 + 射线检测 |
| **DOTween** | DOMove / DOFade / SetEase |
| **案例** | 攻击系统、物品拾取、NPC对话 |

---

# 第三阶段：进阶篇

## 【阶段总述】

进阶阶段：**战斗系统模块化封装**、**事件驱动架构**、**性能优化**、**常见误区与最佳实践**。

---

## 一、战斗系统模块化封装

### 1.1 BattleSystem 封装

```csharp
using UnityEngine;

public class BattleSystem : MonoBehaviour
{
    public static BattleSystem Instance { get; private set; }

    public delegate void DamageEvent(int damage, GameObject target);
    public event DamageEvent OnDamage;

    void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(gameObject);
    }

    public void DealDamage(GameObject attacker, GameObject target, int baseDamage)
    {
        Stats attackerStats = attacker.GetComponent<Stats>();
        Stats targetStats = target.GetComponent<Stats>();

        if (targetStats == null) return;

        int attack = attackerStats != null ? attackerStats.attack : baseDamage;
        int defense = targetStats.defense;
        int damage = Mathf.Max(1, attack - defense);

        targetStats.TakeDamage(damage);

        OnDamage?.Invoke(damage, target);
    }
}

public class Stats : MonoBehaviour
{
    public int maxHealth = 100;
    public int currentHealth;
    public int attack = 10;
    public int defense = 5;

    void Awake()
    {
        currentHealth = maxHealth;
    }

    public void TakeDamage(int damage)
    {
        currentHealth = Mathf.Max(0, currentHealth - damage);
        if (currentHealth <= 0)
            OnDeath();
    }

    void OnDeath()
    {
        Destroy(gameObject, 0.5f);
    }
}
```

### 1.2 事件驱动架构

```csharp
public class DamageUI : MonoBehaviour
{
    public Text damageText;

    void OnEnable()
    {
        BattleSystem.Instance.OnDamage += ShowDamage;
    }

    void OnDisable()
    {
        BattleSystem.Instance.OnDamage -= ShowDamage;
    }

    void ShowDamage(int damage, GameObject target)
    {
        damageText.text = "-" + damage;
        damageText.DOFade(1, 0.1f);
        damageText.DOFade(0, 0.8f).SetDelay(0.2f);
    }
}
```

---

## 二、性能优化

### 2.1 对象池优化伤害数字

```csharp
using UnityEngine;
using System.Collections.Generic;
using DG.Tweening;

public class DamageTextPool : MonoBehaviour
{
    public static DamageTextPool Instance;
    public GameObject prefab;
    public int poolSize = 10;

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

    public GameObject Get(Vector3 position, int damage)
    {
        GameObject obj = pool.Count > 0 ? pool.Dequeue() : Instantiate(prefab);
        obj.transform.position = position;
        obj.GetComponent<Text>().text = "-" + damage;
        obj.SetActive(true);

        obj.transform.DOMove(position + Vector3.up * 1f, 0.8f);
        obj.GetComponent<Text>().DOFade(0, 0.8f).OnComplete(() =>
        {
            obj.SetActive(false);
            pool.Enqueue(obj);
        });

        return obj;
    }
}
```

### 2.2 批处理与优化建议

| 优化手段 | 说明 |
|----------|------|
| **对象池** | 重复使用伤害数字、特效等临时对象 |
| **LayerMask过滤** | 减少射线检测范围 |
| **距离限制** | 只检测近距离物体 |
| **静态批处理** | 合并静态物体渲染 |

---

## 三、常见误区与最佳实践

| 误区 | 正确做法 |
|------|----------|
| Update里频繁Instantiate | 用对象池 |
| 攻击判定写在Update | 用动画事件触发 |
| 直接访问Camera.main | Awake缓存 |
| 不做LayerMask过滤 | 检测时指定Layer |
| 血量可能为负 | 用Mathf.Max限制 |
| 交互系统耦合严重 | 用IInteractable接口 |
| 忘记清理事件订阅 | OnDisable中取消订阅 |

---

## 【进阶阶段小结】

| 维度 | 要点 |
|------|------|
| 架构 | 模块化封装、事件驱动 |
| 封装 | BattleSystem单例、Stats属性 |
| 优化 | 对象池、LayerMask过滤 |
| 避坑 | 动画事件、事件清理、缓存引用 |

---

# 【全文总结】

## 最重要的一行代码

```csharp
if (Physics.Raycast(ray, out RaycastHit hit, range, layerMask))
```

| 部分 | 含义 |
|------|------|
| `Physics.Raycast` | 发射射线检测 |
| `ray` | 射线（起点+方向） |
| `out hit` | 命中信息 |
| `range` | 检测距离 |
| `layerMask` | 层过滤 |

## 三阶段对照

| 阶段 | 代表案例 |
|------|----------|
| 零基础 | 战斗UI搭建、射线检测理解 |
| 入门 | 攻击系统、物品拾取、NPC对话 |
| 进阶 | 模块化封装、事件驱动、对象池 |

## API 速查

| 代码 | 作用 |
|------|------|
| `Physics.Raycast()` | 射线检测 |
| `ScreenPointToRay()` | 屏幕→射线 |
| `LayerMask.GetMask()` | 获取层掩码 |
| `animator.SetTrigger()` | 触发动画 |
| `Mathf.Max()` | 最大值限制 |
| `transform.DOMove()` | DOTween移动 |
| `image.DOFade()` | DOTween淡入淡出 |

## 学习自检

- [ ] 能实现玩家攻击与伤害计算
- [ ] 能制作血条和伤害数字弹出
- [ ] 能实现物品拾取和NPC对话
- [ ] 理解IInteractable接口的作用
- [ ] 掌握DOTween基础用法

---

## 参考资料

| 类型 | 链接 |
|------|------|
| Physics.Raycast | https://docs.unity3d.com/ScriptReference/Physics.Raycast.html |
| DOTween | https://dotween.demigiant.com/ |
| UI System | https://docs.unity3d.com/Manual/UISystem.html |

---

*文档版本：与 major3 系列、Week2_Xmind、Week3_Xmind、Week4_Xmind 同系列模板。*