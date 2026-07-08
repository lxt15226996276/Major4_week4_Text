# 教练规范与文档模板 · 索引

> **规范文件物理位置**：`Assets/Exams/Docs/`（与 Unity Exam 工程同目录，方便相对路径引用）  
> **本文件夹**：统一索引 + 结构说明 · **不重复拷贝正文**

---

## 一、教练宪法（AI 开讲必读）

| 文件 | 路径 | 用途 |
|------|------|------|
| **教学规范** | [`Assets/Exams/Docs/教学规范.md`](../../Assets/Exams/Docs/教学规范.md) | v7.16.3 · **§11.28 Doc 双遍对照** · §11.14 九块 · §11.25 布局矩阵 · §11.27 审计 |
| **阶段修改说明** | [`Assets/Exams/Docs/阶段修改说明.md`](../../Assets/Exams/Docs/阶段修改说明.md) | 版本变更记录 |
| **UI 布局矩阵** | [`Assets/Exams/Docs/UI布局举一反三矩阵.md`](../../Assets/Exams/Docs/UI布局举一反三矩阵.md) | U1～U7 · Button/Input/Image/Text/Grid |

---

## 二、开套模板（复制到 ExamXX/Docs/）

| 模板 | 路径 | 产出 |
|------|------|------|
| **分步教程模板** | [`Assets/Exams/Docs/分步教程模板.md`](../../Assets/Exams/Docs/分步教程模板.md) | `ExamXX/Docs/分步教程.md` |
| **教程模板** | [`Assets/Exams/Docs/教程模板.md`](../../Assets/Exams/Docs/教程模板.md) | `ExamXX/Docs/教程.md` |

---

## 三、成长体系模板（复制到 Docs/01 或 02）

| 模板 | 路径 |
|------|------|
| 成长路线 | [`../01-成长路线/模板-成长路线.md`](../01-成长路线/模板-成长路线.md) |
| **IC 职级全景** | [`../01-成长路线/职级全景_L0-F1_Unity客户端_lixiaotong.md`](../01-成长路线/职级全景_L0-F1_Unity客户端_lixiaotong.md) |
| 学员档案 | [`../01-成长路线/模板-学员档案.md`](../01-成长路线/模板-学员档案.md) |
| 排课 | [`../03-排课与考纲/一周十日排课模板.md`](../03-排课与考纲/一周十日排课模板.md) |

---

## 四、Lab 讲义约定

| 项 | 约定 |
|----|------|
| 位置 | `Assets/Labs/Stage01_WX/Lab_XX.md` · `Assets/Stage01_W4/StageX/` |
| 结构 | 目标 · 验收 · 操作表 · 📌A · 🔷B（同 Exam 大步） |
| 规范 | 遵守 [`教学规范.md`](../../Assets/Exams/Docs/教学规范.md) · **不代写脚本** |

---

## 五、文档三层关系

```
Docs/00～04          学员路线 · 档案 · 排课（本总目录）
Assets/Exams/Docs/   教练规范 + 模板（宪法）
Assets/Exams/ExamXX/Docs/   每套题讲义（教程 + 分步教程）
Assets/Labs/         Lab 讲义 + 你的实验场景
```
