# 小灶 03 · Exam07 Dictionary 登录 · 考试版 vs 商业四层（lixiaotong · S2-）

> **触发**：**§11.24** → 你回复 **`小灶：Dictionary`** → **本 Chat 独占**  
> **定位**：不占大步 Chat · 架构 / 模式 / API / 面试话 / 对照你自写 `AccountData` + `AuthController`  
> **双轨**：**交卷** 仍用 Exam07 P-L1（Dict + TryGetValue + 锁 3s + DDoL）· **理解/面试** 用本讲义商业分层  
> **吸收**：[`外部路线吸收库.md`](../外部路线吸收库.md) **§6.x F07-AUTH** · 手游账号体系通用实践 · U17 Dictionary

---

## 零、你现在该学什么

| 阶段 | 位置 | 本讲义 | 不必现在做 |
|------|------|--------|------------|
| **W2 Exam07 交卷** | 第 3 步 | **Dictionary + TryGetValue + 锁 3s + LoadScene** | OAuth / 服务端验密 |
| **S2- 理解力** | P 83* | **能画认证四层** · 口述 Dict 与 DB/缓存差距 | JWT 全套 |
| **S2+ 练手** | 阶段 02 | 拆 **IAccountRepository** · Session 独立 | 网易通行证 SDK |
| **S3 / 讲师** | 2027+ | 风控 · 设备指纹 · 合规隐私 | 阿里系统一账号 |

---

## 一、考试版 vs 商业版 · 核心差距

| 问题 | 考试写法（能得分） | 商业上线（手游/MMO 通用） |
|------|-------------------|---------------------------|
| 存储 | `Dictionary<string,string>` 明文密码 | **Repository** · 本地加密 / **服务端** 权威 · 永不明文 log |
| 结构 | `AccountData` Mono 包 Dict + 单例 | **数据 / 领域服务 / 表现 / 会话** 四层 |
| 注册 | `ContainsKey` + `Add` | **唯一性校验** · 格式规则 · 敏感词 · 频控 |
| 登录 | `TryGetValue` + 比字符串 | **AuthService.Login** · 失败码枚举 · **审计日志** |
| 锁 3s | 协程 + `interactable=false` | **RateLimiter / 冷却表** · 指数退避 · 验证码 |
| 会话 | `DontDestroyOnLoad` + 静态 Instance | **SessionService** · Token · 过期 · 踢下线 |
| UI | `AuthController` 读 Input 调 Dict | **View 只发命令** · Service 返回 **Result DTO** |
| 跨场景 | `CurrentUserName` 字段 | **UserSession** · 角色 ID · 服务器选服 |

**阅卷**：Dict + Trim + TryGetValue + 错登锁 3s + 进 Game = L1 够用；**商业分层是面试与主程视野，不是 W2 硬性交付**。

---

## 二、商业四层 + 两服务（对标大厂客户端通用）

```
[ 表现层 ]  AuthView / AuthController       ← 三屏切换 · Input/Button · TipText · 只调 Service
      ↑ AuthResult / AuthErrorCode
[ 领域层 ]  AuthService                     ← Register/Login/Logout · 不引用 InputField
      ↑ 读写
[ 数据层 ]  IAccountRepository              ← Dictionary 只是「内存实现」一种
      │         ├─ InMemoryAccountRepo      ← Exam07 考试版
      │         ├─ EncryptedLocalRepo       ← 阶段 02+
      │         └─ RemoteAccountRepo        ← HTTPS + 服务端
      ↑
[ 会话层 ]  SessionService (DDoL)           ← CurrentUserId/Name · Token · 跨场景
      ↑
[ 风控层 ]  LoginRateLimiter                ← 锁 3s / 5 次封 15min（卷面只考 3s）
```

**设计模式（面试能讲）**

| 模式 | 在认证模块里 |
|------|--------------|
| **仓储 Repository** | `IAccountRepository` 藏 Dict/SQL/HTTP |
| **单一职责** | AuthService 不 `SetActive` Panel · Controller 不 `Add` Dict |
| **门面 Facade** | `AuthService.Login()` 隐藏 TryGetValue 细节 |
| **DTO / Result** | `AuthResult { Ok, Code, Message }` 代替 scattered `out string` |
| **单例 + DDoL** | SessionService 跨场景（考试版 = AccountData Instance） |
| **策略** | `IPasswordHasher`：明文(禁) / SHA+Salt / 服务端 |

---

## 三、数据层 · IAccountRepository（Dict 的正确位置）

```csharp
using System.Collections.Generic;

/// <summary>
/// 账号持久化抽象：考试用 Dictionary 实现；商业换实现不改 AuthService。
/// </summary>
public interface IAccountRepository
{
    bool Exists(string account);
    void Add(string account, string passwordHash);
    bool TryGetPasswordHash(string account, out string passwordHash);
}

/// <summary>
/// Exam07 考试版：内存 Dictionary。禁止在 UI 脚本里 new 这个类。
/// </summary>
public sealed class InMemoryAccountRepository : IAccountRepository
{
    private readonly Dictionary<string, string> _map = new Dictionary<string, string>();

    public bool Exists(string account) => _map.ContainsKey(account);

    public void Add(string account, string passwordHash) => _map.Add(account, passwordHash);

    public bool TryGetPasswordHash(string account, out string passwordHash)
        => _map.TryGetValue(account, out passwordHash);
}
```

**API 要点**

| API | 考试 | 商业 |
|-----|------|------|
| `ContainsKey` | 注册前判重复 | 仍用 · 或 DB UNIQUE |
| `TryGetValue` | 登录查键 | **必须** · 禁 `dict[key]` |
| `Dictionary<,>` | 卷面考点 | 只是 Repo 一种后端 |

---

## 四、领域层 · AuthService（不写 MonoBehaviour）

```csharp
public enum AuthErrorCode
{
    None,
    EmptyField,
    AccountExists,
    AccountNotFound,
    WrongPassword,
    RateLimited
}

public readonly struct AuthResult
{
    public bool Ok { get; init; }
    public AuthErrorCode Code { get; init; }
    public string Message { get; init; }
}

/// <summary>
/// 认证领域逻辑：Trim/校验/比密/写会话；不知道 InputField 和 Panel。
/// </summary>
public class AuthService
{
    private readonly IAccountRepository _repo;
    private readonly SessionService _session;

    public AuthService(IAccountRepository repo, SessionService session)
    {
        _repo = repo;
        _session = session;
    }

    public AuthResult Register(string account, string password)
    {
        account = account.Trim();
        password = password.Trim();
        if (string.IsNullOrEmpty(account) || string.IsNullOrEmpty(password))
            return Fail(AuthErrorCode.EmptyField, "账号或密码不能为空");
        if (_repo.Exists(account))
            return Fail(AuthErrorCode.AccountExists, "账号已存在");

        // 商业：password = _hasher.Hash(password);
        _repo.Add(account, password);
        return Ok("注册成功");
    }

    public AuthResult Login(string account, string password)
    {
        account = account.Trim();
        password = password.Trim();
        if (!_repo.TryGetPasswordHash(account, out string stored))
            return Fail(AuthErrorCode.AccountNotFound, "账号不存在");
        if (stored != password)
            return Fail(AuthErrorCode.WrongPassword, "密码错误");

        _session.SetCurrentUser(account);
        return Ok("登录成功");
    }

    private static AuthResult Ok(string msg) => new() { Ok = true, Code = AuthErrorCode.None, Message = msg };
    private static AuthResult Fail(AuthErrorCode c, string msg) => new() { Ok = false, Code = c, Message = msg };
}
```

---

## 五、会话层 · SessionService（你 Exam07 的 DDoL + CurrentUserName）

```csharp
using UnityEngine;

/// <summary>
/// 跨场景会话：Exam07 Game 读用户名 · FollowNameUI 依赖此。
/// </summary>
public class SessionService : MonoBehaviour
{
    public static SessionService Instance { get; private set; }
    public string CurrentUserName { get; private set; }

    private void Awake()
    {
        if (Instance != null && Instance != this) { Destroy(gameObject); return; }
        Instance = this;
        DontDestroyOnLoad(gameObject);
    }

    public void SetCurrentUser(string userName) => CurrentUserName = userName;
}
```

**考试版合并**：`AccountData` = Repository + Session **合体 Mono** · W2 可交卷 · 面试要说「将来会拆」。

---

## 六、表现层 · AuthController 只做 UI（对照你现有代码）

**你已有亮点（P-L1 方向对）**

| 项 | 你的代码 | 评价 |
|----|----------|------|
| 三屏 `ShowPanel` | `SetActive` 互斥 | ✅ 清晰 |
| 锁 3s | `StopTressSeconds` 协程 + `interactable` | ✅ 考点 5 |
| 解绑 | `OnDestroy` RemoveListener 命名方法 | ✅ §11.19 |
| Back 钮 | `btnLoginBack` / `btnRegisterBack` | ✅ P+1 |

**建议 P-L1 校准（不影响小灶理解，交卷前建议改）**

| 项 | 现状 | 建议 |
|----|------|------|
| 单例名 | `Instacne` 拼写 | → `Instance` + `{ get; private set; }` |
| Register 重复键 | `ContainsKey(account)` 未 Trim | → `ContainsKey(accoutInput)` |
| 会话名 | TryLogin 未写 `CurrentUserName` | → Game 场景 FollowNameUI 要读 |
| 注册成功 log | message 含明文密码 | → 商业 **禁止** log 密码 · 卷面也别打 |
| Awake vs OnEnable | 订阅在 OnEnable | ✅ 可以 · 保证 Remove 对称 |

---

## 七、Exam07 交卷版 · 与四层的「最小映射」

| 商业层 | Exam07 P-L1 等价 | 你仓库 |
|--------|------------------|--------|
| Repository | `Dictionary` in AccountData | ✅ 有 |
| AuthService | Register / TryLogin 方法 | ✅ 有 · 合体在 Mono |
| Session | DDoL + Instance | ✅ Awake 有 DDoL |
| View | AuthController + Panel 切换 | ✅ 有 |
| RateLimiter | Lock 3s 协程 | ✅ 有 · 仅登录失败 |
| CurrentUserName | 跨场景用户名 | ⚠️ 待补属性 + Login 赋值 |

**P-L1 不必写 IAccountRepository 四文件**；**小灶要求你能说清「若上商业会拆成哪四层」**。

---

## 八、进阶扩展（阿里/网易/腾讯级 · 阶段 02+）

| 模块 | 行业扩展 |
|------|----------|
| **密码** | SHA256 + Salt · 永存 Hash |
| **Token** | Login 返回 JWT · Header 带 Authorization |
| **频控** | IP/设备 5 次失败 → 验证码 |
| **Dict 局限** | 重启丢数据 → PlayerPrefs/SQLite/服务端 |
| **并发** | 多线程写 Dict 要锁 · 手游客户端少见 |
| **合规** | 隐私协议 · 未成年人 · 实名 |
| **选服** | Exam02 Dropdown · Exam07 直连 Game |

---

## 九、面试 3 句话（讲师预备）

1. 「本地考试用 **Dictionary + TryGetValue** 做仓储；商业里 Dict 只是 **IAccountRepository 的内存实现**，登录逻辑在 **AuthService**，UI 不碰 Dict。」  
2. 「**ContainsKey 注册、TryGetValue 登录** 是 C# 字典安全用法；禁直接 `dict[key]` 防 KeyNotFoundException。」  
3. 「错登 **RateLimiter** 在考试是协程锁按钮；线上是 **服务端频控 + 风控**，客户端锁只是 UX。」

---

## 十、自检题（简讲师课后）

1. 为什么 UI 脚本里 **`new Dictionary`** 是反模式？Exam07 应该在哪一层 `new`？  
2. **`ContainsKey` + 索引器** vs **`TryGetValue`** — 登录为什么必须用后者？  
3. Exam07 若只加 **一个** 商业特性且不超 P-L1，你选 **补 CurrentUserName** 还是 **拆 IAccountRepository**？为什么？

---

## 十-A · 自检标准答案（2026-06-24 · lixiaotong）

1. **UI 里 new Dictionary？**  
   → UI 是表现层 · Dict 是数据源 · 应 **AccountData/Repository 一处 new** · UI 只调 `Register/TryLogin` · 否则难测、难换存储、难 DDoL。

2. **TryGetValue？**  
   → 键不存在时 **TryGetValue 返回 false** · `dict[key]` **抛异常** · 登录失败是常态路径 · 必须安全查键。

3. **只加一项选哪个？**  
   → **补 CurrentUserName + Login 成功赋值** · Game FollowNameUI **硬依赖** · 拆 Repository 是阶段 02 架构练手 · W2 交卷优先 **功能链闭环**。

---

**下一小灶**：**「小灶：UI分层」**（Exam07 第 4 步 GameCanvas）或 **「小灶：WorldToScreen」**（第 5 步跟随）  
**Exam07 映射**：锁 3s 只绑 **LoginPanel BtnLogin 提交** · Initial **BtnToLogin** 只切 Panel
