# Unity 动画专题 · 知识点详解

本目录格式与 [`00_Unity常用类.md`](../00_Unity常用类.md) 一致。

## 参照来源体系

每篇文档的 **参照来源** 分三层（比 00 更细，因动画专题需要）：

| 层级 | 内容 |
|------|------|
| **课程教材（六本）** | 与 `00_Unity常用类.md` 相同书目，但按**各篇动画主题**摘取对应章节 |
| **动画专项权威** | Parent / Gregory / Dean / Cookbook / Hocking 等动画或 Mecanim 专项书 |
| **Unity 官方** | Manual + Scripting API（**最终标准**） |

文末均有 **「课程六教材 · 本专题贡献对照」** 表，标明六本教材在本篇的精读要点与优先级。

## 文档列表

| 文件 | 内容 | 核心类/概念 |
|------|------|------------|
| [01_Animation动画深入.md](01_Animation动画深入.md) | Legacy 动画系统 | Animation, AnimationClip, AnimationState |
| [02_Animator动画.md](02_Animator动画.md) | Mecanim 现代动画 | Animator, Avatar, Controller, Parameters |
| [03_动画状态机一.md](03_动画状态机一.md) | 状态切换与分层 | State, Transition, Layer, AvatarMask |
| [04_动画状态机二.md](04_动画状态机二.md) | 混合树与 IK | BlendTree, IK, MatchTarget, Retarget |
| [05_常见游戏动画设置.md](05_常见游戏动画设置.md) | 三类游戏实战 | 射击 / RPG / 2D 流程与选型 |

## 学习顺序

```
01 Animation Legacy → 02 Animator → 03 状态机(一) → 04 状态机(二) → 05 游戏实战
```

## 与 00 的关系

- **00**：Unity 常用类总览，六本教材覆盖全局
- **Animation/**：在六本教材基础上 **+ 动画专项书 + 更细官方链接 + 本专题对照表**
