# 新项目迁移 · 归档 · 删除判定

> **适用**：重建 Unity 项目 · 清理 `Tests/` 旧目录  
> **原则**：**W3 练习只依赖 `Docs/` + `Assets/Exams/Docs/` + `Assets/Labs/` + 你在 `Assets/Exams/` 的工程进度**

---

## 一、你问的 5 个文件夹 · 删了有没有影响？

| 文件夹 | 能否删 | 对 W3 成长路线 / 教练模板 | 说明 |
|--------|:------:|---------------------------|------|
| **`Tests/scripts`** | ✅ 可删 | **无影响** | 仅 `gen_short_answers.py` · 读的是根目录 **`QuizSite/`**（不是 QuizWeb） |
| **`Tests/QuizWeb`** | ✅ 可删 | **无影响** | 旧版刷题页 · 已被 **`QuizSite/`**（项目根）取代 |
| **`Tests/_extracted`** | ✅ 可删 | **无影响** | 试卷 txt 抽取副本 · 与 `Tests/考试试卷/` 重复 |
| **`Tests/Major3_week4_Exams`** | ✅ 可删* | **不影响 W3 Lab** · 断部分 **历史标杆链接** | 旧 Major3 工程/讲义 · 现行在 `Assets/Exams/` |
| **`Tests/Major4_week1_Exams`** | ✅ 可删* | **同上** | W1 旧拷贝 · Exam02/05/06/07 教程里 **Markdown 链接**会失效 · **Unity 不引用** |

\* 建议：删前先 **Zip 归档到 U 盘/网盘**（见 §四）。Coach 规范、W3 排课、模板 **不依赖** 这两目录里的任何 `.unity`/`.cs`。

### 删 Major* 后会断什么？（仅文档链接 · 可修可忽略）

| 引用位置 | 影响 |
|----------|------|
| `Assets/Exams/Exam02/Docs/教程.md` 等 | 「历史标杆」链接 404 · **不影响 Play** |
| `Assets/Exams/Docs/教学规范.md` | 文字提到 Major 路径 · **规范本身仍有效** |
| `Docs/01-成长路线/阶段01-本月配置.md` | 「历史基线」一行 · 可改文案 |

**结论**：下周 **Lab + 教练模板继承 = 零依赖** 这 5 个文件夹。

---

## 二、新建 Unity 项目 · 必拷清单（按优先级）

### A. 必拷（没有就无法按现路线练）

| 拷贝源 | 放到新项目 | 用途 |
|--------|------------|------|
| **`Docs/`** 整文件夹 | 项目根 `Docs/` | 成长路线 · 档案 · W3 排课 · 考纲 · 小灶 |
| **`Assets/Exams/Docs/`** | 同路径 | **教学规范 v7.16** · 分步/教程 **模板** · UI 矩阵 |
| **`Assets/Labs/Stage01_W3/`** | 同路径 | **W3 五 Lab 讲义** |
| **`Assets/Labs/Stage01_W3/README.md`** | 同路径 | Lab 索引 |

### B. 强烈建议拷（延续 W2 进度 · 非 W3 硬性）

| 拷贝源 | 用途 |
|--------|------|
| **`Assets/Exams/Exam01`～`Exam10/`**（或你做完的几套） | 场景 · 脚本 · Prefab · 分步教程 |
| **`Assets/Images/`**（若 Exam 引用美术） | UI 图集 |
| **`PPT/`** | 课堂单元对照 |

### C. 与 Unity 无关 · 按需拷

| 拷贝源 | 用途 |
|--------|------|
| **`QuizSite/`** | 刷题站（根目录 · **不是** Tests/QuizWeb） |
| **`Docs/03-排课与考纲/元宇宙专业四题库_精简答案.md`** | 理论复习 |
| **`Tests/考试试卷/`** 或 `.doc` 原件 | 试卷原文 · 开新套对照 |

### D. 不必拷到新 Unity 项目

| 路径 | 原因 |
|------|------|
| `Tests/Major3_week4_Exams/` | 已被 `Assets/Exams/` 取代 |
| `Tests/Major4_week1_Exams/` | 旧拷贝 + 错别字讲义 |
| `Tests/_extracted/` | 重复 txt |
| `Tests/QuizWeb/` | 旧刷题页 |
| `Tests/scripts/` | 可选；重建精简答案用 `QuizSite` 脚本即可 |
| `Tests/阶段性主程成长路线/` 残留 | 已迁到 `Docs/` · 只留跳转 README |
| `Library/` `Temp/` `Logs/` | Unity 生成 · 禁止拷 |

---

## 三、推荐的新项目目录（统一后）

```
新Unity项目/
├── Docs/                          ← 路线 + 档案 + 排课（总入口 README.md）
├── Assets/
│   ├── Exams/
│   │   ├── Docs/                  ← 教练宪法 + 模板（勿删）
│   │   └── ExamXX/                ← 周考工程
│   ├── Labs/
│   │   └── Stage01_W3/            ← W3 主力
│   └── Images/                    ← 按需
├── QuizSite/                      ← 可选 · 刷题
└── PPT/                           ← 可选 · 课堂
```

**不要再建** `Tests/Major4_week1_Exams/` 这类平行拷贝；历史代码只 **Zip 归档**，不放进新工程。

---

## 四、当前项目 · 安全清理顺序

1. **Zip 归档**（可选）：`Major3_week4_Exams` + `Major4_week1_Exams` → `Archive_Major_Exams_2026.zip`
2. **删除**：`Tests/_extracted` · `Tests/QuizWeb` · `Tests/scripts`
3. **删除**：`Major3_week4_Exams` · `Major4_week1_Exams`（确认 Zip 后）
4. **清理残留**：`Tests/阶段性主程成长路线/` 下除 `README.md` 外的 orphan 文件
5. **更新链接**（可选）：Exam02 等教程里 Major 标杆改指 `Assets/Exams/Exam02/`

---

## 五、W3 第一周打开顺序

1. [`Docs/README.md`](../README.md)
2. [`Docs/00-每日入口/lixiaotong_唯一执行入口.md`](../00-每日入口/lixiaotong_唯一执行入口.md)
3. [`Docs/01-成长路线/W3-Lab周-当前.md`](../01-成长路线/W3-Lab周-当前.md)
4. [`Assets/Labs/Stage01_W3/Lab_Animation_01.md`](../../Assets/Labs/Stage01_W3/Lab_Animation_01.md)
5. [`Assets/Exams/Docs/教学规范.md`](../../Assets/Exams/Docs/教学规范.md)

---

## 六、投喂 AI（新项目）

```
@Docs/00-每日入口/lixiaotong_唯一执行入口.md
@Docs/02-学员档案/学员能力档案_lixiaotong.md
@Docs/01-成长路线/W3-Lab周-当前.md
@Assets/Exams/Docs/教学规范.md
@Assets/Labs/Stage01_W3/Lab_XX.md
```

**不要**再 @ `Tests/Major4_week1_Exams/...`
