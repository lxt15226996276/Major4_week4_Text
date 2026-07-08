# Lab_Editor_01 · MenuItem 与 EditorWindow

> **关联考纲**：U15（Editor 扩展）  
> **预估**：3h · **W3 第 3 天**  
> **前置**：无；C# 基础即可

---

## 学习目标

| 层级 | 你要做到 |
|------|----------|
| **L1** | 区分运行时脚本 vs `Editor` 文件夹脚本 |
| **P-L1** | 自己写 **1 个 MenuItem** + **1 个简单 EditorWindow** |
| **P+1** | Window 里读 **Selection** 或改 **Prefab** 上一字段（带确认） |

---

## 目录结构（你必须自己建）

```
Assets/Labs/Stage01_W3/Lab_Editor_01/
├── Editor/                    ← 必须 Editor 文件夹
│   ├── LabMenuItems.cs
│   └── LabToolWindow.cs
└── Runtime/                   ← 可选测试用
    └── LabTestComponent.cs
```

> **注意**：`Editor` 下脚本 **不能** 被场景 GameObject 引用。

---

## 第 1 步：MenuItem

`LabMenuItems.cs`：

- `[MenuItem("Lab/Log Selection Count")]`
- 点击后在 Console 输出当前 `Selection.gameObjects.Length`

**检查**：菜单出现 · 点一次有日志

---

## 第 2 步：EditorWindow

`LabToolWindow.cs`：

- `[MenuItem("Lab/Open Lab Tool Window")]`
- `EditorWindow.GetWindow<LabToolWindow>()`
- Window 里一个 **Button**：「选中物体改名前缀 `Lab_`」
- 用 `Selection.activeGameObject` + `Undo.RecordObject`（P+1 推荐）

**P-L1 硬指标**：

- [ ] 继承 `EditorWindow`，不是 `MonoBehaviour`
- [ ] MenuItem 路径与窗口类分离或同文件均可
- [ ] 无 `DestroyImmediate` 乱删未确认对象

---

## 第 3 步：可选 P+1

- 读 `LabTestComponent` 的 public 字段在 Inspector 显示
- 或批量给选中物体加组件

---

## 与项目关系

- RPG 配表工具、打包前检查 → 都基于 U15
- W4 项目可用本 Lab 窗口改成「关卡列表刷新」

---

## 面试 2 题

1. `Editor` 文件夹脚本为什么进不了 Build？
2. `Undo.RecordObject` 解决什么问题？

---

## 完成打勾

- [ ] MenuItem 可用
- [ ] EditorWindow 可开、按钮有作用
- [ ] 档案 U15：**1→2**
