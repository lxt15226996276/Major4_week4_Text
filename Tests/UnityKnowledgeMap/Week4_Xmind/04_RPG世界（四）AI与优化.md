# 综合案例项目实例RPG世界（四）——AI与优化

> 参照：[Unity 官方 Manual - Animation](https://docs.unity3d.com/Manual/AnimationSection.html) · [NavMesh](https://docs.unity3d.com/Manual/NavMesh.html) · [Object Pooling](https://docs.unity3d.com/Manual/ObjectPooling.html) · [LOD Group](https://docs.unity3d.com/Manual/LODGroup.html)  
> 关联文档：[01_RPG世界（一）.md](./01_RPG世界（一）项目初始化与玩家基础.md) · [02_RPG世界（二）.md](./02_RPG世界（二）战斗系统与交互.md) · [03_RPG世界（三）.md](./03_RPG世界（三）任务与存档.md) · [05_综合复习.md](./05_综合复习.md)  
> 学习路径：**零基础 → 入门 → 进阶**，每阶段采用 **总—分—总** 结构。  
> 讲解维度：**定义 → 本质 → 特点 → 适用场景 → 原理 → API → 步骤 → 案例 → 避坑**（进阶含项目架构 / 模块化 / 性能优化）。  
> 案例讲解：遵循 **案例代码讲解模板**（功能 → 代码 → 语法拆解 → 逐行详解 → 操作提示）。  
> API 讲解：入门/进阶 API 章节均采用 **逐词读懂** 格式（与 [01_PlayerPrefs.md](../major3/01_PlayerPrefs.md) 一致：类型 → 参数 → 整行人话）。

---

## 【全文总述】

**RPG（角色扮演游戏）世界综合案例** 第四章，重点讲解 **怪物AI、状态机、性能优化** 三大核心模块。  
学习本案例，你将掌握：
- 如何设计和实现怪物AI行为
- 如何使用有限状态机管理AI状态
- 如何实现怪物寻路和追击
- 如何使用对象池优化性能
- 如何使用LOD和批处理优化渲染

### 思维导图总览

```
RPG 世界综合案例（四）——AI与优化
│
├── 怪物AI系统（智能对手 — 玩家的挑战）
│   │
│   ├── 定义：怪物自主决策和行动的系统，包含感知、决策、行动三个阶段
│   │
│   ├── 本质：感知环境 → 状态机决策 → 执行动作 → 更新状态
│   │   ├── 感知系统：检测玩家、检测距离、检测攻击范围
│   │   ├── 决策系统：有限状态机（Idle/Wander/Chase/Attack）
│   │   └── 行动系统：移动、攻击、受伤、死亡
│   │
│   ├── 核心原理：每帧更新感知 → 状态机判断转换条件 → 执行当前状态行为
│   │
│   ├── 核心 API 及参数
│   │   ├── NavMeshAgent：寻路组件
│   │   ├── Vector3.Distance：距离计算
│   │   └── Animator.SetFloat/SetBool：动画参数
│   │
│   └── 标准使用步骤
│       ├── 步骤1 设置 NavMesh 导航网格
│       ├── 步骤2 创建怪物状态机
│       ├── 步骤3 实现各状态行为
│       └── 步骤4 配置状态转换条件
│
├── 状态机系统（行为管理 — AI的大脑）
│   │
│   ├── 定义：管理对象状态及其转换的设计模式
│   │
│   ├── 本质：状态枚举 → 状态类 → 转换条件 → 状态机管理器
│   │   ├── 状态枚举：Idle、Wander、Chase、Attack、Hurt、Dead
│   │   ├── 状态类：每个状态封装自己的行为
│   │   ├── 转换条件：距离、血量、玩家位置等
│   │   └── 状态机：管理当前状态、处理转换
│   │
│   └── 实战：怪物状态机实现
│       ├── 定义状态枚举
│       ├── 创建状态基类
│       ├── 实现各状态类
│       └── 创建状态机管理器
│
├── 性能优化（流畅体验 — 游戏的保障）
│   │
│   ├── 定义：通过各种手段减少游戏资源消耗，提高运行流畅度
│   │
│   ├── 本质：减少计算量、减少内存分配、减少渲染开销
│   │   ├── 对象池：复用临时对象，避免频繁Instantiate/Destroy
│   │   ├── LOD：远距离显示低精度模型
│   │   ├── 批处理：合并渲染批次
│   │   └── 遮挡剔除：不渲染被挡住的物体
│   │
│   └── 实战：性能优化实现
│       ├── 实现对象池
│       ├── 设置 LOD Group
│       ├── 配置批处理
│       └── 开启遮挡剔除
│
├── 第一阶段：零基础（AI概念 + 状态机基础）
│   ├── 理解怪物AI和状态机的定义
│   ├── 逐词读懂：NavMeshAgent.SetDestination(target)
│   └── 完成NavMesh基础设置
│
├── 第二阶段：入门（AI实现 + 状态机 + 优化）
│   ├── 怪物AI完整实现
│   ├── 有限状态机实现
│   ├── 对象池优化
│   └── 实战案例：巡逻怪物、追击怪物、对象池
│
└── 第三阶段：进阶（架构设计 + 模块化 + 优化）
    ├── 状态机模块化封装
    ├── AI行为树简介
    ├── 高级优化技巧
    └── 常见误区与最佳实践
```

| 学习阶段 | 学习目标 |
|----------|----------|
| **零基础** | 理解AI与状态机概念；读懂NavMeshAgent核心代码；完成NavMesh设置 |
| **入门** | 实现怪物AI、状态机、对象池；掌握LOD基础；完成3个案例 |
| **进阶** | 理解行为树架构；会封装状态机；掌握高级优化技巧 |

### 讲师知识框架速览（全文脉络）

| 维度 | 零基础讲 | 入门讲 | 进阶讲 |
|------|----------|--------|--------|
| 定义 | ✅ | 回顾 | 回顾 |
| 本质 | ✅ | — | — |
| 特点 | ✅ | — | 架构特点 |
| 适用场景 | ✅ | — | 项目选型 |
| 核心原理 | AI流程 | ✅ 状态机机制 | 行为树设计 |
| 核心 API | 读懂 NavMesh | ✅ NavMeshAgent + 状态机 | 封装与优化 |
| 使用步骤 | NavMesh设置 | ✅ AI实现步骤 | 架构搭建 |
| 调用时机 | — | ✅ Update/状态切换 | 生命周期管理 |
| 避坑 | — | 初步 | ✅ |

---

# 第一阶段：零基础篇

## 【阶段总述】

零基础阶段建立**正确认知**：怪物AI是什么、状态机是什么、NavMesh怎么工作。  
同时学会**读懂** `NavMeshAgent.SetDestination(target)` 每个部分的含义，并完成NavMesh基础设置。

---

## 一、定义 — AI与状态机是什么？

| 项目 | 说明 |
|------|------|
| **怪物AI** | 怪物自主决策和行动的系统，包含感知、决策、行动 |
| **状态机** | 管理对象状态及其转换的设计模式 |
| **NavMesh** | Unity导航网格系统，用于AI寻路 |
| **有限状态机** | 有限个状态，状态间按条件转换 |
| **一句话** | AI=感知+决策+行动；状态机=管理这些行动的切换 |

```
怪物AI结构示例
EnemyAI
    ├── 感知系统
    │   ├── 检测玩家距离
    │   ├── 检测攻击范围
    │   └── 检测障碍物
    │
    ├── 状态机
    │   ├── 状态枚举（Idle/Wander/Chase/Attack）
    │   ├── 当前状态
    │   └── 状态转换
    │
    └── 行动系统
        ├── 移动（NavMeshAgent）
        ├── 攻击（动画事件）
        └── 受伤/死亡
```

---

## 二、本质 — AI与状态机如何工作？

### 2.1 AI系统本质

```
AI流程
感知（检测玩家）→ 决策（状态机判断）→ 行动（执行当前状态行为）→ 更新状态
```

| 环节 | 本质理解 |
|------|----------|
| **感知** | 检测玩家位置、距离、是否在视野内 |
| **决策** | 根据感知结果，状态机决定该做什么 |
| **行动** | 执行移动、攻击等具体行为 |
| **更新** | 每帧重复这个流程 |

### 2.2 状态机本质

```
状态机工作原理
当前状态 → 检查转换条件 → 条件满足 → 切换到新状态 → 执行新状态行为
```

| 环节 | 本质理解 |
|------|----------|
| **状态** | 怪物的行为模式（Idle=待机，Chase=追击） |
| **转换条件** | 触发状态切换的条件（距离足够近→攻击） |
| **状态行为** | 该状态下怪物做什么 |

---

## 三、特点与适用场景

### 3.1 AI系统特点

| 特点 | 说明 |
|------|------|
| **自主性** | 怪物自己做决策，不需要玩家控制 |
| **反应性** | 根据玩家行为做出反应 |
| **有限性** | AI行为是预设的，不是真正智能 |
| **性能敏感** | 大量AI会消耗性能 |

### 3.2 状态机特点

| 特点 | 说明 |
|------|------|
| **清晰** | 状态和转换一目了然 |
| **可扩展** | 新增状态只需加新类 |
| **解耦** | 每个状态独立，互不影响 |
| **可维护** | 逻辑分离，便于修改 |

### 3.3 适用场景

| 场景 | 是否适用 | 原因 |
|------|----------|------|
| 巡逻怪物 | ✅ | 状态机适合循环行为 |
| 追击怪物 | ✅ | 状态转换清晰 |
| Boss战 | ✅ | 多阶段状态切换 |
| 复杂行为 | ❌ | 考虑行为树 |

---

## 四、核心一课：如何读懂 NavMeshAgent

```csharp
navMeshAgent.SetDestination(target.position);
```

| 部分 | 含义 |
|------|------|
| `navMeshAgent` | NavMeshAgent组件引用 |
| `.SetDestination` | 方法名：设置寻路目标点 |
| `target.position` | 参数：目标位置（Vector3） |
| **效果** | AI自动规划路径并移动到目标 |

**整行人话**：告诉AI要去的地方，AI自己找路过去。

```csharp
// 完整的寻路代码
NavMeshAgent agent = GetComponent<NavMeshAgent>();
agent.SetDestination(player.position);
agent.isStopped = false;
```

| 行 | 含义 |
|----|------|
| `GetComponent<NavMeshAgent>()` | 获取寻路组件 |
| `SetDestination(player.position)` | 设置目标为玩家位置 |
| `isStopped = false` | 允许移动 |

---

## 五、零基础实战：NavMesh设置

### 5.1 步骤一：烘焙导航网格

1. 菜单 **Window → AI → Navigation**
2. 在Navigation窗口选择 **Bake** 选项卡
3. 设置参数：
   - **Radius**：0.5（角色半径）
   - **Height**：2（角色高度）
   - **Max Slope**：45（最大爬坡角度）
4. 点击 **Bake** 按钮

### 5.2 步骤二：设置可行走区域

1. 在Navigation窗口选择 **Object** 选项卡
2. 选择场景中的地面和平台
3. 设置 **Navigation Static** 为 true
4. 设置 **Area** 为 **Walkable**

### 5.3 步骤三：为怪物添加NavMeshAgent

1. 选择怪物GameObject
2. 菜单 **Component → AI → NavMeshAgent**
3. 设置参数：
   - **Speed**：移动速度
   - **Angular Speed**：转向速度
   - **Stopping Distance**：停止距离

---

## 【零基础阶段小结】

| 维度 | 要点 |
|------|------|
| **定义** | AI=自主决策；状态机=状态管理；NavMesh=寻路系统 |
| **本质** | AI=感知→决策→行动；状态机=条件→转换→行为 |
| **步骤** | Bake导航网格 → 设置可行走区域 → 添加NavMeshAgent |
| **读懂** | `navMeshAgent.SetDestination(target.position)` |

**阶段检验**：能说出AI流程；能画出状态机图；能读懂NavMeshAgent代码。

---

# 第二阶段：入门篇

## 【阶段总述】

入门阶段掌握 **怪物AI、有限状态机、性能优化** 三大核心模块，并完成 3 个实战案例。  
重点：**状态机设计模式**；**NavMesh寻路**；**对象池优化**。

---

## 一、怪物AI核心代码详解

### 1.1 NavMeshAgent API — 逐词读懂

#### `navMeshAgent.SetDestination(target)` 是什么？

```csharp
navMeshAgent.SetDestination(player.position);
```

| 部分 | 含义 |
|------|------|
| `navMeshAgent` | NavMeshAgent组件引用 |
| `.SetDestination` | **方法名**：设置寻路目标 |
| `player.position` | **参数**：目标位置（Vector3） |
| **效果** | AI自动规划路径并移动 |

**整行人话**：让AI去玩家所在的位置。

#### `navMeshAgent.isStopped = true` 是什么？

```csharp
navMeshAgent.isStopped = true;
```

| 部分 | 含义 |
|------|------|
| `isStopped` | **属性**：bool，是否停止移动 |
| `true` | 停止移动 |
| `false` | 允许移动 |

**整行人话**：让AI停下来。

#### `Vector3.Distance(a, b)` 是什么？

```csharp
float distance = Vector3.Distance(transform.position, player.position);
```

| 部分 | 含义 |
|------|------|
| `Vector3.Distance` | **静态方法**：计算两点间距离 |
| `a` | 点A位置 |
| `b` | 点B位置 |
| **返回值** | float，距离值 |

**整行人话**：算怪物和玩家之间隔了多远。

---

### 1.2 EnemyAI 完整代码

```csharp
using UnityEngine;
using UnityEngine.AI;

public enum EnemyState
{
    Idle,
    Wander,
    Chase,
    Attack,
    Hurt,
    Dead
}

public class EnemyAI : MonoBehaviour
{
    NavMeshAgent agent;
    Animator animator;
    Transform player;

    public EnemyState currentState;
    public float chaseRange = 10f;
    public float attackRange = 2f;
    public float wanderRadius = 5f;
    public float wanderTime = 3f;

    float wanderTimer;
    Vector3 wanderTarget;

    void Awake()
    {
        agent = GetComponent<NavMeshAgent>();
        animator = GetComponent<Animator>();
        player = GameObject.FindGameObjectWithTag("Player").transform;
    }

    void Update()
    {
        if (currentState == EnemyState.Dead) return;

        float distanceToPlayer = Vector3.Distance(transform.position, player.position);

        switch (currentState)
        {
            case EnemyState.Idle:
                HandleIdle(distanceToPlayer);
                break;
            case EnemyState.Wander:
                HandleWander(distanceToPlayer);
                break;
            case EnemyState.Chase:
                HandleChase(distanceToPlayer);
                break;
            case EnemyState.Attack:
                HandleAttack(distanceToPlayer);
                break;
        }
    }

    void HandleIdle(float distance)
    {
        animator.SetFloat("Speed", 0);

        if (distance < chaseRange)
        {
            ChangeState(EnemyState.Chase);
        }
        else
        {
            wanderTimer += Time.deltaTime;
            if (wanderTimer > wanderTime)
            {
                ChangeState(EnemyState.Wander);
            }
        }
    }

    void HandleWander(float distance)
    {
        if (distance < chaseRange)
        {
            ChangeState(EnemyState.Chase);
            return;
        }

        if (Vector3.Distance(transform.position, wanderTarget) < 1f)
        {
            SetNewWanderTarget();
        }

        agent.SetDestination(wanderTarget);
        animator.SetFloat("Speed", agent.velocity.magnitude);
    }

    void HandleChase(float distance)
    {
        if (distance > chaseRange)
        {
            ChangeState(EnemyState.Idle);
            return;
        }

        if (distance < attackRange)
        {
            ChangeState(EnemyState.Attack);
            return;
        }

        agent.SetDestination(player.position);
        animator.SetFloat("Speed", agent.velocity.magnitude);
    }

    void HandleAttack(float distance)
    {
        if (distance > attackRange)
        {
            ChangeState(EnemyState.Chase);
            return;
        }

        agent.isStopped = true;
        transform.LookAt(player);
        animator.SetTrigger("Attack");
        animator.SetFloat("Speed", 0);
    }

    void SetNewWanderTarget()
    {
        wanderTimer = 0;
        Vector3 randomDirection = Random.insideUnitSphere * wanderRadius;
        randomDirection += transform.position;
        NavMeshHit hit;
        NavMesh.SamplePosition(randomDirection, out hit, wanderRadius, NavMesh.AllAreas);
        wanderTarget = hit.position;
    }

    void ChangeState(EnemyState newState)
    {
        currentState = newState;
        agent.isStopped = false;
    }

    public void TakeDamage(int damage)
    {
        if (currentState == EnemyState.Dead) return;
        currentState = EnemyState.Hurt;
        animator.SetTrigger("Hurt");
        Invoke("ResumeState", 0.5f);
    }

    void ResumeState()
    {
        if (currentState != EnemyState.Dead)
        {
            currentState = EnemyState.Idle;
        }
    }

    public void Die()
    {
        currentState = EnemyState.Dead;
        agent.isStopped = true;
        animator.SetTrigger("Die");
    }
}
```

#### 语法拆解

##### `Random.insideUnitSphere` 是什么？

```csharp
Vector3 randomDirection = Random.insideUnitSphere * wanderRadius;
```

| 部分 | 含义 |
|------|------|
| `Random` | Unity随机数类 |
| `insideUnitSphere` | 静态属性：单位球内随机点 |
| `* wanderRadius` | 乘以巡逻半径 |

**整行人话**：在怪物周围随机找一个点。

##### `NavMesh.SamplePosition()` 是什么？

```csharp
NavMesh.SamplePosition(randomDirection, out hit, wanderRadius, NavMesh.AllAreas);
```

| 部分 | 含义 |
|------|------|
| `NavMesh.SamplePosition` | 静态方法：在导航网格上找最近点 |
| `randomDirection` | 随机位置 |
| `out hit` | 输出参数：找到的有效位置 |
| `wanderRadius` | 搜索半径 |
| `NavMesh.AllAreas` | 搜索所有区域 |

**整行人话**：确保随机点在可行走区域内。

---

## 二、有限状态机实现

### 2.1 State 基类

```csharp
public abstract class State
{
    protected EnemyAI enemy;

    public State(EnemyAI enemy)
    {
        this.enemy = enemy;
    }

    public abstract void Enter();
    public abstract void Update();
    public abstract void Exit();
}
```

### 2.2 IdleState 实现

```csharp
public class IdleState : State
{
    float wanderTimer;

    public IdleState(EnemyAI enemy) : base(enemy) { }

    public override void Enter()
    {
        enemy.agent.isStopped = true;
        enemy.animator.SetFloat("Speed", 0);
        wanderTimer = 0;
    }

    public override void Update()
    {
        float distance = Vector3.Distance(enemy.transform.position, enemy.player.position);

        if (distance < enemy.chaseRange)
        {
            enemy.ChangeState(new ChaseState(enemy));
            return;
        }

        wanderTimer += Time.deltaTime;
        if (wanderTimer > enemy.wanderTime)
        {
            enemy.ChangeState(new WanderState(enemy));
        }
    }

    public override void Exit() { }
}
```

### 2.3 StateMachine 状态机管理器

```csharp
public class StateMachine
{
    State currentState;

    public void ChangeState(State newState)
    {
        currentState?.Exit();
        currentState = newState;
        currentState.Enter();
    }

    public void Update()
    {
        currentState?.Update();
    }
}
```

### 2.4 使用状态机的 EnemyAI

```csharp
public class EnemyAI : MonoBehaviour
{
    StateMachine stateMachine;
    NavMeshAgent agent;
    Animator animator;
    public Transform player;

    void Awake()
    {
        agent = GetComponent<NavMeshAgent>();
        animator = GetComponent<Animator>();
        player = GameObject.FindGameObjectWithTag("Player").transform;
        stateMachine = new StateMachine();
        stateMachine.ChangeState(new IdleState(this));
    }

    void Update()
    {
        stateMachine.Update();
    }

    public void ChangeState(State newState)
    {
        stateMachine.ChangeState(newState);
    }
}
```

---

## 三、性能优化实现

### 3.1 对象池优化

```csharp
using UnityEngine;
using System.Collections.Generic;

public class ObjectPool : MonoBehaviour
{
    public static ObjectPool Instance;

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

    public GameObject Get(Vector3 position, Quaternion rotation)
    {
        GameObject obj = pool.Count > 0 ? pool.Dequeue() : Instantiate(prefab);
        obj.transform.position = position;
        obj.transform.rotation = rotation;
        obj.SetActive(true);
        return obj;
    }

    public void Return(GameObject obj)
    {
        obj.SetActive(false);
        pool.Enqueue(obj);
    }
}
```

### 3.2 LOD Group 设置

```csharp
using UnityEngine;

[RequireComponent(typeof(LODGroup))]
public class LODSetup : MonoBehaviour
{
    public Mesh[] lodMeshes;
    public float[] lodDistances = { 20, 50, 100 };

    void Awake()
    {
        LODGroup lodGroup = GetComponent<LODGroup>();
        LOD[] lods = new LOD[lodMeshes.Length];

        for (int i = 0; i < lodMeshes.Length; i++)
        {
            Renderer[] renderers = GetComponentsInChildren<Renderer>();
            lods[i] = new LOD(lodDistances[i], renderers);
        }

        lodGroup.SetLODs(lods);
    }
}
```

### 3.3 批处理与优化建议

| 优化手段 | 说明 |
|----------|------|
| **GPU Instancing** | 相同材质的物体批量渲染 |
| **LOD Group** | 远距离物体显示低精度模型 |
| **Occlusion Culling** | 遮挡剔除，不渲染被挡住的物体 |
| **Static Batching** | 静态物体合并批次 |
| **对象池** | 复用临时对象 |

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

### 案例 1：巡逻怪物AI

**功能**：怪物在范围内随机巡逻，发现玩家后追击并攻击。

```csharp
using UnityEngine;
using UnityEngine.AI;

public class PatrolEnemy : MonoBehaviour
{
    NavMeshAgent agent;
    Animator animator;
    Transform player;

    public float patrolRadius = 10f;
    public float chaseRange = 15f;
    public float attackRange = 2f;

    Vector3 patrolTarget;

    void Awake()
    {
        agent = GetComponent<NavMeshAgent>();
        animator = GetComponent<Animator>();
        player = GameObject.FindGameObjectWithTag("Player").transform;
        SetNewPatrolTarget();
    }

    void Update()
    {
        float distance = Vector3.Distance(transform.position, player.position);

        if (distance < attackRange)
        {
            Attack();
        }
        else if (distance < chaseRange)
        {
            Chase();
        }
        else
        {
            Patrol();
        }
    }

    void Patrol()
    {
        if (Vector3.Distance(transform.position, patrolTarget) < 1f)
        {
            SetNewPatrolTarget();
        }
        agent.SetDestination(patrolTarget);
        animator.SetFloat("Speed", agent.velocity.magnitude);
    }

    void Chase()
    {
        agent.SetDestination(player.position);
        animator.SetFloat("Speed", agent.velocity.magnitude);
    }

    void Attack()
    {
        agent.isStopped = true;
        transform.LookAt(player);
        animator.SetTrigger("Attack");
    }

    void SetNewPatrolTarget()
    {
        Vector3 randomPos = Random.insideUnitSphere * patrolRadius;
        randomPos += transform.position;
        NavMeshHit hit;
        NavMesh.SamplePosition(randomPos, out hit, patrolRadius, NavMesh.AllAreas);
        patrolTarget = hit.position;
    }
}
```

#### 语法拆解

##### `Random.insideUnitSphere` 是什么？

```csharp
Vector3 randomPos = Random.insideUnitSphere * patrolRadius;
```

| 部分 | 含义 |
|------|------|
| `Random.insideUnitSphere` | 单位球内随机点（x,y,z范围-1到1） |
| `* patrolRadius` | 缩放为巡逻半径 |

**整行人话**：在怪物周围随机选一个巡逻点。

##### `NavMesh.SamplePosition()` 是什么？

```csharp
NavMesh.SamplePosition(randomPos, out hit, patrolRadius, NavMesh.AllAreas);
```

| 部分 | 含义 |
|------|------|
| `SamplePosition` | 在导航网格上采样最近点 |
| `out hit` | 输出采样结果 |
| `patrolRadius` | 搜索半径 |

**整行人话**：确保巡逻点在可行走区域。

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 5~6 | 组件引用 | Agent和Animator |
| 7 | `Transform player` | 玩家引用 |
| 9~11 | 距离参数 | 巡逻/追击/攻击范围 |
| 13 | `patrolTarget` | 当前巡逻目标点 |
| 15~19 | 初始化 | 获取组件、找玩家、设初始目标 |
| 21 | `void Update()` | 每帧检测 |
| 23 | 计算距离 | 到玩家的距离 |
| 25 | `distance < attackRange` | 在攻击范围内 |
| 30 | `distance < chaseRange` | 在追击范围内 |
| 35 | 否则巡逻 | 默认行为 |
| 38 | Patrol() | 巡逻逻辑 |
| 46 | Chase() | 追击逻辑 |
| 52 | Attack() | 攻击逻辑 |
| 59 | SetNewPatrolTarget() | 设置新巡逻点 |

#### 操作提示

1. 怪物需有 **NavMeshAgent** 组件
2. 场景需已烘焙 **NavMesh**
3. 玩家Tag设为"Player"
4. Animator需有"Speed"和"Attack"参数

---

### 案例 2：有限状态机框架

**功能**：用状态机模式管理怪物行为，代码更清晰可扩展。

```csharp
using UnityEngine;

public abstract class BaseState
{
    protected Enemy enemy;

    public BaseState(Enemy enemy)
    {
        this.enemy = enemy;
    }

    public abstract void OnEnter();
    public abstract void OnUpdate();
    public abstract void OnExit();
}

public class Enemy : MonoBehaviour
{
    public BaseState currentState;

    void Update()
    {
        currentState?.OnUpdate();
    }

    public void ChangeState(BaseState newState)
    {
        currentState?.OnExit();
        currentState = newState;
        currentState?.OnEnter();
    }
}

public class IdleState : BaseState
{
    public IdleState(Enemy enemy) : base(enemy) { }

    public override void OnEnter()
    {
        Debug.Log("进入待机状态");
    }

    public override void OnUpdate()
    {
        if (IsPlayerNear())
        {
            enemy.ChangeState(new ChaseState(enemy));
        }
    }

    public override void OnExit()
    {
        Debug.Log("离开待机状态");
    }

    bool IsPlayerNear()
    {
        Transform player = GameObject.FindGameObjectWithTag("Player")?.transform;
        return player != null && Vector3.Distance(enemy.transform.position, player.position) < 10f;
    }
}

public class ChaseState : BaseState
{
    public ChaseState(Enemy enemy) : base(enemy) { }

    public override void OnEnter()
    {
        Debug.Log("进入追击状态");
    }

    public override void OnUpdate()
    {
        Transform player = GameObject.FindGameObjectWithTag("Player")?.transform;
        if (player != null)
        {
            enemy.transform.LookAt(player);
            enemy.transform.Translate(Vector3.forward * 2 * Time.deltaTime);
        }
    }

    public override void OnExit()
    {
        Debug.Log("离开追击状态");
    }
}
```

#### 语法拆解

##### `public abstract class BaseState` 是什么？

```csharp
public abstract class BaseState
{
    public abstract void OnEnter();
    public abstract void OnUpdate();
    public abstract void OnExit();
}
```

| 部分 | 含义 |
|------|------|
| `abstract` | 抽象类，不能直接实例化 |
| `abstract void` | 抽象方法，子类必须实现 |
| **作用** | 定义状态的标准接口 |

**整行人话**：定义所有状态都必须有的方法。

##### `currentState?.OnUpdate()` 是什么？

```csharp
currentState?.OnUpdate();
```

| 部分 | 含义 |
|------|------|
| `?.` | 空合并运算符，currentState不为null才调用 |
| `OnUpdate()` | 执行当前状态的更新方法 |

**整行人话**：安全地调用当前状态的更新方法。

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 1 | `abstract class BaseState` | 状态基类 |
| 4 | `protected Enemy enemy` | 持有敌人引用 |
| 8~10 | 抽象方法 | 进入/更新/退出 |
| 13 | `class Enemy` | 敌人控制器 |
| 15 | `currentState` | 当前状态 |
| 17 | `currentState?.OnUpdate()` | 更新当前状态 |
| 20 | `ChangeState()` | 切换状态 |
| 27 | `class IdleState` | 待机状态 |
| 28 | `: BaseState` | 继承基类 |
| 31~39 | OnEnter/OnUpdate/OnExit | 待机逻辑 |
| 47 | `class ChaseState` | 追击状态 |
| 52~62 | 追击逻辑 | 看向玩家并移动 |

#### 操作提示

1. 创建Enemy类挂到怪物上
2. Awake中初始化状态：`currentState = new IdleState(this)`
3. 新增状态只需继承BaseState

---

### 案例 3：对象池优化子弹

**功能**：用对象池管理子弹，避免频繁创建销毁。

```csharp
using UnityEngine;
using System.Collections.Generic;

public class BulletPool : MonoBehaviour
{
    public static BulletPool Instance;

    public GameObject bulletPrefab;
    public int poolSize = 20;

    Queue<GameObject> pool = new Queue<GameObject>();

    void Awake()
    {
        Instance = this;
        for (int i = 0; i < poolSize; i++)
        {
            GameObject bullet = Instantiate(bulletPrefab);
            bullet.SetActive(false);
            bullet.transform.SetParent(transform);
            pool.Enqueue(bullet);
        }
    }

    public GameObject GetBullet(Vector3 position, Quaternion rotation)
    {
        GameObject bullet = pool.Count > 0 ? pool.Dequeue() : Instantiate(bulletPrefab);
        bullet.transform.position = position;
        bullet.transform.rotation = rotation;
        bullet.SetActive(true);
        return bullet;
    }

    public void ReturnBullet(GameObject bullet)
    {
        bullet.SetActive(false);
        pool.Enqueue(bullet);
    }
}

public class Bullet : MonoBehaviour
{
    public float speed = 10f;
    public float lifetime = 2f;

    void OnEnable()
    {
        Invoke("ReturnToPool", lifetime);
    }

    void Update()
    {
        transform.Translate(Vector3.forward * speed * Time.deltaTime);
    }

    void OnCollisionEnter(Collision collision)
    {
        CancelInvoke();
        ReturnToPool();
    }

    void ReturnToPool()
    {
        BulletPool.Instance.ReturnBullet(gameObject);
    }
}
```

#### 语法拆解

##### `Queue<GameObject>` 是什么？

```csharp
Queue<GameObject> pool = new Queue<GameObject>();
```

| 部分 | 含义 |
|------|------|
| `Queue<T>` | 队列，先进先出（FIFO） |
| `pool` | 队列名 |

**整行人话**：存放闲置子弹的队列。

##### `pool.Dequeue()` 是什么？

```csharp
GameObject bullet = pool.Count > 0 ? pool.Dequeue() : Instantiate(bulletPrefab);
```

| 部分 | 含义 |
|------|------|
| `Dequeue()` | 出队：移除并返回队列首元素 |
| `pool.Count > 0` | 队列不为空 |

**整行人话**：从池中取出一颗子弹，没有就新建。

#### 逐行详解

| 行 | 代码 | 是什么意思 |
|----|------|------------|
| 5 | `static BulletPool Instance` | 单例 |
| 7~8 | 配置参数 | 预制体和池大小 |
| 10 | `Queue<GameObject> pool` | 对象池队列 |
| 12~19 | Awake | 初始化池 |
| 21 | `GetBullet()` | 获取子弹 |
| 27 | `ReturnBullet()` | 归还子弹 |
| 31 | `class Bullet` | 子弹脚本 |
| 33~34 | 速度和寿命 | 参数 |
| 36 | `OnEnable()` | 激活时调用 |
| 37 | `Invoke("ReturnToPool", lifetime)` | 延迟归还 |
| 40 | `Update()` | 移动子弹 |
| 44 | `OnCollisionEnter()` | 碰撞检测 |
| 45 | `CancelInvoke()` | 取消延迟 |

#### 操作提示

1. 创建子弹预制体，挂Bullet脚本
2. 创建空物体挂BulletPool脚本
3. Inspector拖入bulletPrefab
4. 发射子弹时调用 `BulletPool.Instance.GetBullet(pos, rot)`

---

## 【入门阶段小结】

| 维度 | 要点 |
|------|------|
| **AI** | NavMesh寻路 + 距离检测 + 状态切换 |
| **状态机** | 抽象基类 + 状态子类 + 状态管理器 |
| **优化** | 对象池 + LOD + 批处理 |
| **案例** | 巡逻怪物、状态机框架、子弹对象池 |

---

# 第三阶段：进阶篇

## 【阶段总述】

进阶阶段：**状态机模块化封装**、**AI行为树简介**、**高级优化技巧**、**常见误区与最佳实践**。

---

## 一、状态机进阶

### 1.1 泛型状态机

```csharp
public abstract class State<T>
{
    protected T owner;

    public State(T owner)
    {
        this.owner = owner;
    }

    public abstract void Enter();
    public abstract void Update();
    public abstract void Exit();
}

public class StateMachine<T>
{
    State<T> currentState;

    public void ChangeState(State<T> newState)
    {
        currentState?.Exit();
        currentState = newState;
        currentState.Enter();
    }

    public void Update() => currentState?.Update();
}

public class Enemy : MonoBehaviour
{
    StateMachine<Enemy> stateMachine;

    void Awake()
    {
        stateMachine = new StateMachine<Enemy>();
        stateMachine.ChangeState(new IdleState<Enemy>(this));
    }

    void Update() => stateMachine.Update();
}
```

### 1.2 状态转换表

```csharp
using System.Collections.Generic;

public class StateTransition<T>
{
    public State<T> from;
    public State<T> to;
    public System.Func<bool> condition;
}

public class StateMachine<T>
{
    List<StateTransition<T>> transitions = new List<StateTransition<T>>();
    State<T> currentState;

    public void AddTransition(State<T> from, State<T> to, System.Func<bool> condition)
    {
        transitions.Add(new StateTransition<T> { from = from, to = to, condition = condition });
    }

    void CheckTransitions()
    {
        foreach (var t in transitions)
        {
            if (t.from == currentState && t.condition())
            {
                ChangeState(t.to);
                break;
            }
        }
    }
}
```

---

## 二、行为树简介

### 2.1 行为树节点类型

```csharp
public enum NodeStatus
{
    Success,
    Failure,
    Running
}

public abstract class BehaviorNode
{
    protected Enemy enemy;

    public BehaviorNode(Enemy enemy)
    {
        this.enemy = enemy;
    }

    public abstract NodeStatus Evaluate();
}

public class Selector : BehaviorNode
{
    List<BehaviorNode> children;

    public Selector(Enemy enemy, params BehaviorNode[] children) : base(enemy)
    {
        this.children = new List<BehaviorNode>(children);
    }

    public override NodeStatus Evaluate()
    {
        foreach (var child in children)
        {
            switch (child.Evaluate())
            {
                case NodeStatus.Success:
                    return NodeStatus.Success;
                case NodeStatus.Running:
                    return NodeStatus.Running;
                case NodeStatus.Failure:
                    continue;
            }
        }
        return NodeStatus.Failure;
    }
}

public class Sequence : BehaviorNode
{
    List<BehaviorNode> children;

    public Sequence(Enemy enemy, params BehaviorNode[] children) : base(enemy)
    {
        this.children = new List<BehaviorNode>(children);
    }

    public override NodeStatus Evaluate()
    {
        bool isAnyChildRunning = false;
        foreach (var child in children)
        {
            switch (child.Evaluate())
            {
                case NodeStatus.Success:
                    continue;
                case NodeStatus.Running:
                    isAnyChildRunning = true;
                    continue;
                case NodeStatus.Failure:
                    return NodeStatus.Failure;
            }
        }
        return isAnyChildRunning ? NodeStatus.Running : NodeStatus.Success;
    }
}
```

### 2.2 行为树叶子节点

```csharp
public class CheckPlayerInRange : BehaviorNode
{
    float range;

    public CheckPlayerInRange(Enemy enemy, float range) : base(enemy)
    {
        this.range = range;
    }

    public override NodeStatus Evaluate()
    {
        float distance = Vector3.Distance(enemy.transform.position, enemy.player.position);
        return distance < range ? NodeStatus.Success : NodeStatus.Failure;
    }
}

public class MoveToPlayer : BehaviorNode
{
    public MoveToPlayer(Enemy enemy) : base(enemy) { }

    public override NodeStatus Evaluate()
    {
        enemy.agent.SetDestination(enemy.player.position);
        return NodeStatus.Running;
    }
}
```

### 2.3 使用行为树

```csharp
public class Enemy : MonoBehaviour
{
    BehaviorNode behaviorTree;

    void Awake()
    {
        behaviorTree = new Selector(this,
            new Sequence(this,
                new CheckPlayerInRange(this, 2f),
                new Attack(this)),
            new Sequence(this,
                new CheckPlayerInRange(this, 10f),
                new MoveToPlayer(this)),
            new Wander(this)
        );
    }

    void Update()
    {
        behaviorTree.Evaluate();
    }
}
```

---

## 三、高级优化技巧

### 3.1 对象池管理器

```csharp
using UnityEngine;
using System.Collections.Generic;

public class PoolManager : MonoBehaviour
{
    public static PoolManager Instance;

    Dictionary<string, Queue<GameObject>> pools = new Dictionary<string, Queue<GameObject>>();

    void Awake()
    {
        Instance = this;
    }

    public void CreatePool(string key, GameObject prefab, int size)
    {
        if (!pools.ContainsKey(key))
        {
            pools[key] = new Queue<GameObject>();
            for (int i = 0; i < size; i++)
            {
                GameObject obj = Instantiate(prefab);
                obj.SetActive(false);
                obj.transform.SetParent(transform);
                pools[key].Enqueue(obj);
            }
        }
    }

    public GameObject GetFromPool(string key)
    {
        if (pools.TryGetValue(key, out var pool))
        {
            if (pool.Count > 0)
            {
                GameObject obj = pool.Dequeue();
                obj.SetActive(true);
                return obj;
            }
        }
        return null;
    }

    public void ReturnToPool(string key, GameObject obj)
    {
        if (pools.TryGetValue(key, out var pool))
        {
            obj.SetActive(false);
            pool.Enqueue(obj);
        }
    }
}
```

### 3.2 性能监控

```csharp
using UnityEngine;
using UnityEngine.UI;

public class PerformanceMonitor : MonoBehaviour
{
    public Text fpsText;
    public Text memoryText;
    float deltaTime;

    void Update()
    {
        deltaTime += (Time.unscaledDeltaTime - deltaTime) * 0.1f;
        float fps = 1.0f / deltaTime;
        fpsText.text = $"FPS: {Mathf.Round(fps)}";

        long memory = System.GC.GetTotalMemory(false) / 1024 / 1024;
        memoryText.text = $"Memory: {memory} MB";
    }
}
```

---

## 四、常见误区与最佳实践

| 误区 | 正确做法 |
|------|----------|
| 每帧FindGameObjectWithTag | Awake缓存引用 |
| 不用NavMesh直接Translate | 复杂场景用NavMesh寻路 |
| 状态机逻辑写在Update | 用状态模式分离 |
| 频繁Instantiate/Destroy | 用对象池 |
| 不做距离检测直接追击 | 先检测距离再行动 |
| AI太多导致卡顿 | 用LOD和距离剔除 |
| 忘记处理Dead状态 | 死亡后停止所有行为 |

---

## 【进阶阶段小结】

| 维度 | 要点 |
|------|------|
| 状态机 | 泛型封装、转换表 |
| 行为树 | Selector/Sequence/叶子节点 |
| 优化 | 对象池管理器、性能监控 |
| 避坑 | 缓存引用、NavMesh寻路、死亡处理 |

---

# 【全文总结】

## 最重要的一行代码

```csharp
navMeshAgent.SetDestination(player.position);
```

| 部分 | 含义 |
|------|------|
| `navMeshAgent` | 寻路组件 |
| `SetDestination` | 设置目标 |
| `player.position` | 玩家位置 |

## 三阶段对照

| 阶段 | 代表案例 |
|------|----------|
| 零基础 | NavMesh设置、AI概念理解 |
| 入门 | 巡逻怪物、状态机框架、对象池 |
| 进阶 | 泛型状态机、行为树、高级优化 |

## API 速查

| 代码 | 作用 |
|------|------|
| `NavMeshAgent.SetDestination()` | 设置寻路目标 |
| `Vector3.Distance()` | 计算距离 |
| `Random.insideUnitSphere` | 随机位置 |
| `NavMesh.SamplePosition()` | 导航网格采样 |
| `Queue.Enqueue/Dequeue` | 对象池操作 |
| `LODGroup.SetLODs()` | 设置LOD |

## 学习自检

- [ ] 能实现巡逻和追击怪物AI
- [ ] 能使用有限状态机管理行为
- [ ] 能实现对象池优化
- [ ] 理解NavMesh寻路原理
- [ ] 了解行为树基本概念

---

## 参考资料

| 类型 | 链接 |
|------|------|
| NavMesh | https://docs.unity3d.com/Manual/NavMesh.html |
| NavMeshAgent | https://docs.unity3d.com/ScriptReference/AI.NavMeshAgent.html |
| LOD Group | https://docs.unity3d.com/Manual/LODGroup.html |

---

*文档版本：与 major3 系列、Week2_Xmind、Week3_Xmind、Week4_Xmind 同系列模板。*