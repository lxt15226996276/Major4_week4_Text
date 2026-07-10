# -*- coding: utf-8 -*-
"""
子步 5.1：把 MainCanvas.prefab 的 InventoryGrid 改造为 ScrollRect 体系。
- 删除 20 个静态 ItemSlot 及其组件
- InventoryGrid GO 改造为 ScrollRect（保留原 RectTransform 位置）
- 新建 Viewport(RectMask2D+Image) / Content(GridLayout+CSF) / Scrollbar / SlidingArea / Handle
- Content 内放 8 个样例格（2 行 x 4 列）便于看滚动效果
风格沿用现有 prefab：棕色主题、ItemSlot 用 UISprite(guid b90c18..)、关闭钮 sprite(51ce3c..)等。
"""
import re, random

PATH = "Assets/Exams/Exam01/Prefabs/MainCanvas.prefab"
with open(PATH, encoding="utf-8") as f:
    txt = f.read()

# ---------- GUID 常量（权威取自 Unity 2022.3 ugui built-in） ----------
G_IMAGE        = "fe87c0e1cc204ed48ad3b37840f39efc"  # Image
G_GRID         = "8a8695521f0d02e499659fee002a26c2"  # GridLayoutGroup（= 现有 InventoryGrid 用的）
G_CSF          = "3245ec927659c4140ac4f8d17403cc18"  # ContentSizeFitter
G_SCROLLRECT   = "1aa08ab6e0800fa44ae55d278d1423e3"  # ScrollRect
G_RECTMASK2D   = "3312d7739989d2b4e91e6319e9a96d76"  # RectMask2D
G_SCROLLBAR    = "2a4db7a114972834c8e4117be1d82ba3"  # Scrollbar
G_SPRITE_SLOT  = "b90c180d76d13ac43845ea5a1b0ae1a7"  # ItemSlot 用的 UISprite

# ---------- 现有 fileID（来自 prefab 体检） ----------
INV_GO = "7183490414185368192"
INV_RT = "9093643205188261330"
INV_GLG_MB = "8909113354142644186"   # InventoryGrid 上的 GridLayoutGroup MonoBehaviour（将删除）
PANELROOT_RT = "4619034392515744993"  # BackpackPanel/PanelRoot

# ---------- 生成不冲突的新 fileID ----------
existing = set(re.findall(r'&(\d+)', txt))
def new_id(seed):
    # 用稳定的大数 + seed，并避开 existing
    base = 8800000000000000000 + seed * 1117
    while str(base) in existing:
        base += 1
    existing.add(str(base))
    return str(base)

# 预分配所有新 fileID（seed 区分用途，便于阅读）
ids = {}
for key in ["SCROLLRECT_MB",       # ScrollRect MonoBehaviour on InventoryGrid GO
            "VP_GO", "VP_RT", "VP_IMG_MB", "VP_RECTMASK_MB",
            "CONTENT_GO", "CONTENT_RT", "CONTENT_GLG_MB", "CONTENT_CSF_MB",
            "SB_GO", "SB_RT", "SB_MB", "SB_IMG_MB",
            "SA_GO", "SA_RT",
            "HANDLE_GO", "HANDLE_RT", "HANDLE_IMG_MB",
            ]:
    pass
seed = 0
for key in ["SCROLLRECT_MB","VP_GO","VP_RT","VP_IMG_MB","VP_RECTMASK_MB",
            "CONTENT_GO","CONTENT_RT","CONTENT_GLG_MB","CONTENT_CSF_MB",
            "SB_GO","SB_RT","SB_MB","SB_IMG_MB",
            "SA_GO","SA_RT","HANDLE_GO","HANDLE_RT","HANDLE_CR","HANDLE_IMG_MB"]:
    seed += 1
    ids[key] = new_id(seed)

# 8 个样例格的 fileID
for i in range(8):
    seed += 1
    ids[f"SLOT{i}_GO"] = new_id(seed)
    seed += 1
    ids[f"SLOT{i}_RT"] = new_id(seed)
    seed += 1
    ids[f"SLOT{i}_CR"] = new_id(seed)
    seed += 1
    ids[f"SLOT{i}_IMG"] = new_id(seed)

# ============================================================
# 步骤 1：定位并删除 20 个 ItemSlot 的所有块
# ============================================================
# 每个 ItemSlot 涉及 4 类块：GameObject(!1) / RectTransform(!224) / CanvasRenderer(!222) / Image(!114)
# 先收集所有 ItemSlot 的 GO id
pat_rt = re.compile(r'--- !u!224 &(\d+)\nRectTransform:(.*?)(?=\n--- !u!)', re.S)
slot_go_ids = []
for m in pat_rt.finditer(txt):
    body = m.group(2)
    if re.search(r'm_Father: \{fileID: ' + INV_RT + r'\}', body):
        gm = re.search(r'm_GameObject: \{fileID: (\d+)\}', body)
        slot_go_ids.append(gm.group(1))
assert len(slot_go_ids) == 20, f"expect 20 slots, got {len(slot_go_ids)}"

# 收集要删除的所有块（按文件中的 "--- !u!CLASS &ID\n... 直到下一个 --- !u!"）
# 一个 GO 的组件块都引用该 GO id（m_GameObject）。删除所有引用 slot_go 的块。
blocks = re.split(r'(?=^--- !u!)', txt, flags=re.M)
def block_refs_go(block, go_id):
    # 组件块含 m_GameObject: {fileID: go_id}
    return re.search(r'm_GameObject: \{fileID: ' + go_id + r'\}', block) is not None
def block_is_go(block, go_id):
    # GameObject 块的 header 即 --- !u!1 &{go_id}
    return re.match(r'--- !u!1 &' + go_id + r'\nGameObject:', block) is not None

kept = []
removed = 0
for b in blocks:
    drop = False
    for go_id in slot_go_ids:
        if block_refs_go(b, go_id) or block_is_go(b, go_id):
            drop = True; break
    if not drop:
        kept.append(b)
    else:
        removed += 1
txt2 = "".join(kept)
print(f"[1] removed {removed} blocks for 20 ItemSlots")

# ============================================================
# 步骤 2：删除 InventoryGrid 上的旧 GridLayoutGroup MonoBehaviour（INV_GLG_MB）
# ============================================================
txt2 = re.sub(r'^--- !u!114 &' + INV_GLG_MB + r'\nMonoBehaviour:.*?(?=^--- !u!)', '', txt2, flags=re.M | re.S)
# 同时从 InventoryGrid GO 的 m_Component 列表中移除该组件引用
txt2 = re.sub(r'(  m_Component:\n(?:  - component: \{fileID: \d+\}\n)*?)  - component: \{fileID: ' + INV_GLG_MB + r'\}\n',
              r'\1', txt2)
print("[2] removed old GridLayoutGroup MonoBehaviour from InventoryGrid GO")

# 验证旧 GLG 块已删
assert INV_GLG_MB not in txt2, "old GLG block still referenced!"

# ============================================================
# 步骤 3：给 InventoryGrid GO 加上 ScrollRect 组件引用 + 改名
# ============================================================
# 在 m_Component 列表里追加 ScrollRect 组件引用（RectTransform 之后）
txt2 = txt2.replace(
    f"  - component: {{fileID: {INV_RT}}}\n  m_Layer: 5\n  m_Name: InventoryGrid",
    f"  - component: {{fileID: {INV_RT}}}\n  - component: {{fileID: {ids['SCROLLRECT_MB']}}}\n  m_Layer: 5\n  m_Name: ScrollRect"
)
# 改 InventoryGrid RectTransform 的 m_Children 为 [Viewport, Scrollbar]
old_children_line = "  m_Children:\n  m_Father: {fileID: 4619034392515744993}"
new_children_line = (f"  m_Children:\n"
                     f"  - {{fileID: {ids['VP_RT']}}}\n"
                     f"  - {{fileID: {ids['SB_RT']}}}\n"
                     f"  m_Father: {{fileID: {PANELROOT_RT}}}")
assert old_children_line in txt2, "InventoryGrid children anchor not found"
txt2 = txt2.replace(old_children_line, new_children_line)
print("[3] InventoryGrid -> ScrollRect (renamed + wired children)")

# ============================================================
# 步骤 4：追加 ScrollRect MonoBehaviour（在 InventoryGrid RectTransform 块之后）
# ============================================================
scrollrect_block = f"""--- !u!114 &{ids['SCROLLRECT_MB']}
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {INV_GO}}}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {{fileID: 11500000, guid: {G_SCROLLRECT}, type: 3}}
  m_Name:
  m_EditorClassIdentifier:
  m_Content: {{fileID: {ids['CONTENT_RT']}}}
  m_Horizontal: 0
  m_Vertical: 1
  m_MovementType: 2
  m_Elasticity: 0.1
  m_Inertia: 1
  m_DecelerationRate: 0.135
  m_ScrollSensitivity: 1
  m_Viewport: {{fileID: {ids['VP_RT']}}}
  m_HorizontalScrollbar: {{fileID: 0}}
  m_VerticalScrollbar: {{fileID: {ids['SB_MB']}}}
  m_HorizontalScrollbarVisibility: 0
  m_VerticalScrollbarVisibility: 2
  m_HorizontalScrollbarSpacing: 0
  m_VerticalScrollbarSpacing: -18
  m_OnValueChanged:
    m_PersistentCalls:
      m_Calls: []
"""
anchor = f"--- !u!224 &{INV_RT}\nRectTransform:"
idx = txt2.index(anchor)
# 找该块的结尾（下一个 --- !u!）
end = txt2.index("\n--- !u!", idx)
txt2 = txt2[:end] + "\n" + scrollrect_block + txt2[end:]
print("[4] appended ScrollRect MonoBehaviour")

# ============================================================
# 步骤 5：构建 Viewport / Content / Scrollbar / SlidingArea / Handle + 8 样例格
#   全部追加到文件末尾（PrefabAsset 末尾）
# ============================================================
# ItemSlot 样例格 sprite（沿用现有 UISprite guid b90c18..）
def slot_block(i):
    go = ids[f"SLOT{i}_GO"]; rt = ids[f"SLOT{i}_RT"]; cr = ids[f"SLOT{i}_CR"]; img = ids[f"SLOT{i}_IMG"]
    return f"""--- !u!1 &{go}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {rt}}}
  - component: {{fileID: {cr}}}
  - component: {{fileID: {img}}}
  m_Layer: 5
  m_Name: ItemSlot{i}
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!224 &{rt}
RectTransform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {go}}}
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalPosition: {{x: 0, y: 0, z: 0}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
  m_Children: []
  m_Father: {{fileID: {ids['CONTENT_RT']}}}
  m_LocalEulerAnglesHint: {{x: 0, y: 0, z: 0}}
  m_AnchorMin: {{x: 0, y: 0}}
  m_AnchorMax: {{x: 0, y: 0}}
  m_AnchoredPosition: {{x: 0, y: 0}}
  m_SizeDelta: {{x: 0, y: 0}}
  m_Pivot: {{x: 0.5, y: 0.5}}
--- !u!222 &{cr}
CanvasRenderer:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {go}}}
  m_CullTransparentMesh: 1
--- !u!114 &{img}
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {go}}}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {{fileID: 11500000, guid: {G_IMAGE}, type: 3}}
  m_Name:
  m_EditorClassIdentifier:
  m_Material: {{fileID: 0}}
  m_Color: {{r: 1, g: 1, b: 1, a: 1}}
  m_RaycastTarget: 1
  m_RaycastPadding: {{x: 0, y: 0, z: 0, w: 0}}
  m_Maskable: 1
  m_OnCullStateChanged:
    m_PersistentCalls:
      m_Calls: []
  m_Sprite: {{fileID: 21300000, guid: {G_SPRITE_SLOT}, type: 3}}
  m_Type: 1
  m_PreserveAspect: 0
  m_FillCenter: 1
  m_FillMethod: 4
  m_FillAmount: 1
  m_FillClockwise: 1
  m_FillOrigin: 0
  m_UseSpriteMesh: 0
  m_PixelsPerUnitMultiplier: 1
"""

appended = ""

# ---- Viewport ----
appended += f"""--- !u!1 &{ids['VP_GO']}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {ids['VP_RT']}}}
  - component: {{fileID: {ids['VP_IMG_MB']}}}
  - component: {{fileID: {ids['VP_RECTMASK_MB']}}}
  m_Layer: 5
  m_Name: Viewport
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!224 &{ids['VP_RT']}
RectTransform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {ids['VP_GO']}}}
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalPosition: {{x: 0, y: 0, z: 0}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
  m_Children:
  - {{fileID: {ids['CONTENT_RT']}}}
  m_Father: {{fileID: {INV_RT}}}
  m_LocalEulerAnglesHint: {{x: 0, y: 0, z: 0}}
  m_AnchorMin: {{x: 0, y: 0}}
  m_AnchorMax: {{x: 1, y: 1}}
  m_AnchoredPosition: {{x: 0, y: 0}}
  m_SizeDelta: {{x: -18, y: 0}}
  m_Pivot: {{x: 0.5, y: 0.5}}
--- !u!114 &{ids['VP_IMG_MB']}
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {ids['VP_GO']}}}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {{fileID: 11500000, guid: {G_IMAGE}, type: 3}}
  m_Name:
  m_EditorClassIdentifier:
  m_Material: {{fileID: 0}}
  m_Color: {{r: 1, g: 1, b: 1, a: 1}}
  m_RaycastTarget: 1
  m_RaycastPadding: {{x: 0, y: 0, z: 0, w: 0}}
  m_Maskable: 1
  m_OnCullStateChanged:
    m_PersistentCalls:
      m_Calls: []
  m_Sprite: {{fileID: 21300000, guid: {G_SPRITE_SLOT}, type: 3}}
  m_Type: 1
  m_PreserveAspect: 0
  m_FillCenter: 1
  m_FillMethod: 4
  m_FillAmount: 1
  m_FillClockwise: 1
  m_FillOrigin: 0
  m_UseSpriteMesh: 0
  m_PixelsPerUnitMultiplier: 1
--- !u!114 &{ids['VP_RECTMASK_MB']}
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {ids['VP_GO']}}}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {{fileID: 11500000, guid: {G_RECTMASK2D}, type: 3}}
  m_Name:
  m_EditorClassIdentifier:
  m_ShowMaskGraphic: 0
  m_Padding: {{x: 0, y: 0, z: 0, w: 0}}
  m_Softness: {{x: 0, y: 0}}
"""

# ---- Content ----
appended += f"""--- !u!1 &{ids['CONTENT_GO']}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {ids['CONTENT_RT']}}}
  - component: {{fileID: {ids['CONTENT_GLG_MB']}}}
  - component: {{fileID: {ids['CONTENT_CSF_MB']}}}
  m_Layer: 5
  m_Name: Content
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!224 &{ids['CONTENT_RT']}
RectTransform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {ids['CONTENT_GO']}}}
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalPosition: {{x: 0, y: 0, z: 0}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
  m_Children:
"""
for i in range(8):
    appended += f"  - {{fileID: {ids[f'SLOT{i}_RT']}}}\n"
appended += f"""  m_Father: {{fileID: {ids['VP_RT']}}}
  m_LocalEulerAnglesHint: {{x: 0, y: 0, z: 0}}
  m_AnchorMin: {{x: 0, y: 1}}
  m_AnchorMax: {{x: 0, y: 1}}
  m_AnchoredPosition: {{x: 0, y: 0}}
  m_SizeDelta: {{x: 0, y: 0}}
  m_Pivot: {{x: 0, y: 1}}
--- !u!114 &{ids['CONTENT_GLG_MB']}
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {ids['CONTENT_GO']}}}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {{fileID: 11500000, guid: {G_GRID}, type: 3}}
  m_Name:
  m_EditorClassIdentifier:
  m_Padding:
    m_Left: 6
    m_Right: 6
    m_Top: 6
    m_Bottom: 6
  m_ChildAlignment: 4
  m_StartCorner: 0
  m_StartAxis: 0
  m_CellSize: {{x: 98, y: 98}}
  m_Spacing: {{x: 10, y: 10}}
  m_Constraint: 1
  m_ConstraintCount: 4
--- !u!114 &{ids['CONTENT_CSF_MB']}
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {ids['CONTENT_GO']}}}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {{fileID: 11500000, guid: {G_CSF}, type: 3}}
  m_Name:
  m_EditorClassIdentifier:
  m_HorizontalFit: 0
  m_VerticalFit: 2
"""

# ---- Scrollbar (Vertical) ----
appended += f"""--- !u!1 &{ids['SB_GO']}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {ids['SB_RT']}}}
  - component: {{fileID: {ids['SB_IMG_MB']}}}
  - component: {{fileID: {ids['SB_MB']}}}
  m_Layer: 5
  m_Name: Scrollbar Vertical
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!224 &{ids['SB_RT']}
RectTransform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {ids['SB_GO']}}}
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalPosition: {{x: 0, y: 0, z: 0}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
  m_Children:
  - {{fileID: {ids['SA_RT']}}}
  m_Father: {{fileID: {INV_RT}}}
  m_LocalEulerAnglesHint: {{x: 0, y: 0, z: 0}}
  m_AnchorMin: {{x: 1, y: 0}}
  m_AnchorMax: {{x: 1, y: 1}}
  m_AnchoredPosition: {{x: 0, y: 0}}
  m_SizeDelta: {{x: 18, y: 0}}
  m_Pivot: {{x: 1, y: 1}}
--- !u!114 &{ids['SB_IMG_MB']}
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {ids['SB_GO']}}}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {{fileID: 11500000, guid: {G_IMAGE}, type: 3}}
  m_Name:
  m_EditorClassIdentifier:
  m_Material: {{fileID: 0}}
  m_Color: {{r: 0.2, g: 0.15, b: 0.1, a: 0.6}}
  m_RaycastTarget: 1
  m_RaycastPadding: {{x: 0, y: 0, z: 0, w: 0}}
  m_Maskable: 1
  m_OnCullStateChanged:
    m_PersistentCalls:
      m_Calls: []
  m_Sprite: {{fileID: 21300000, guid: {G_SPRITE_SLOT}, type: 3}}
  m_Type: 1
  m_PreserveAspect: 0
  m_FillCenter: 1
  m_FillMethod: 4
  m_FillAmount: 1
  m_FillClockwise: 1
  m_FillOrigin: 0
  m_UseSpriteMesh: 0
  m_PixelsPerUnitMultiplier: 1
--- !u!114 &{ids['SB_MB']}
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {ids['SB_GO']}}}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {{fileID: 11500000, guid: {G_SCROLLBAR}, type: 3}}
  m_Name:
  m_EditorClassIdentifier:
  m_Navigation:
    m_Mode: 3
    m_WrapAround: 0
    m_SelectOnUp: {{fileID: 0}}
    m_SelectOnDown: {{fileID: 0}}
    m_SelectOnLeft: {{fileID: 0}}
    m_SelectOnRight: {{fileID: 0}}
  m_Transition: 1
  m_Colors:
    m_NormalColor: {{r: 1, g: 1, b: 1, a: 1}}
    m_HighlightedColor: {{r: 0.9607843, g: 0.9607843, b: 0.9607843, a: 1}}
    m_PressedColor: {{r: 0.78431374, g: 0.78431374, b: 0.78431374, a: 1}}
    m_SelectedColor: {{r: 0.9607843, g: 0.9607843, b: 0.9607843, a: 1}}
    m_DisabledColor: {{r: 0.78431374, g: 0.78431374, b: 0.78431374, a: 0.5019608}}
    m_ColorMultiplier: 1
    m_FadeDuration: 0.1
  m_SpriteState:
    m_HighlightedSprite: {{fileID: 0}}
    m_PressedSprite: {{fileID: 0}}
    m_SelectedSprite: {{fileID: 0}}
    m_DisabledSprite: {{fileID: 0}}
  m_AnimationTriggers:
    m_NormalTrigger: Normal
    m_HighlightedTrigger: Highlighted
    m_PressedTrigger: Pressed
    m_SelectedTrigger: Selected
    m_DisabledTrigger: Disabled
  m_Interactable: 1
  m_TargetGraphic: {{fileID: {ids['HANDLE_IMG_MB']}}}
  m_HandleRect: {{fileID: {ids['HANDLE_RT']}}}
  m_Direction: 2
  m_Value: 1
  m_Size: 0.5
  m_NumberOfSteps: 0
  m_OnValueChanged:
    m_PersistentCalls:
      m_Calls: []
"""

# ---- Sliding Area ----
appended += f"""--- !u!1 &{ids['SA_GO']}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {ids['SA_RT']}}}
  m_Layer: 5
  m_Name: Sliding Area
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!224 &{ids['SA_RT']}
RectTransform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {ids['SA_GO']}}}
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalPosition: {{x: 0, y: 0, z: 0}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
  m_Children:
  - {{fileID: {ids['HANDLE_RT']}}}
  m_Father: {{fileID: {ids['SB_RT']}}}
  m_LocalEulerAnglesHint: {{x: 0, y: 0, z: 0}}
  m_AnchorMin: {{x: 0, y: 0}}
  m_AnchorMax: {{x: 1, y: 1}}
  m_AnchoredPosition: {{x: 0, y: 0}}
  m_SizeDelta: {{x: -20, y: -20}}
  m_Pivot: {{x: 0.5, y: 0.5}}
"""

# ---- Handle ----
appended += f"""--- !u!1 &{ids['HANDLE_GO']}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {ids['HANDLE_RT']}}}
  - component: {{fileID: {ids['HANDLE_CR']}}}
  - component: {{fileID: {ids['HANDLE_IMG_MB']}}}
  m_Layer: 5
  m_Name: Handle
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!224 &{ids['HANDLE_RT']}
RectTransform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {ids['HANDLE_GO']}}}
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalPosition: {{x: 0, y: 0, z: 0}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
  m_Children: []
  m_Father: {{fileID: {ids['SA_RT']}}}
  m_LocalEulerAnglesHint: {{x: 0, y: 0, z: 0}}
  m_AnchorMin: {{x: 0, y: 0}}
  m_AnchorMax: {{x: 1, y: 1}}
  m_AnchoredPosition: {{x: 0, y: 0}}
  m_SizeDelta: {{x: 0, y: 0}}
  m_Pivot: {{x: 0.5, y: 0.5}}
--- !u!222 &{ids['HANDLE_CR']}
CanvasRenderer:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {ids['HANDLE_GO']}}}
  m_CullTransparentMesh: 1
--- !u!114 &{ids['HANDLE_IMG_MB']}
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {ids['HANDLE_GO']}}}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {{fileID: 11500000, guid: {G_IMAGE}, type: 3}}
  m_Name:
  m_EditorClassIdentifier:
  m_Material: {{fileID: 0}}
  m_Color: {{r: 0.8, g: 0.65, b: 0.4, a: 1}}
  m_RaycastTarget: 1
  m_RaycastPadding: {{x: 0, y: 0, z: 0, w: 0}}
  m_Maskable: 1
  m_OnCullStateChanged:
    m_PersistentCalls:
      m_Calls: []
  m_Sprite: {{fileID: 21300000, guid: {G_SPRITE_SLOT}, type: 3}}
  m_Type: 1
  m_PreserveAspect: 0
  m_FillCenter: 1
  m_FillMethod: 4
  m_FillAmount: 1
  m_FillClockwise: 1
  m_FillOrigin: 0
  m_UseSpriteMesh: 0
  m_PixelsPerUnitMultiplier: 1
"""

# 8 个样例格
for i in range(8):
    appended += slot_block(i)

# 追加到文件末尾
txt2 = txt2.rstrip() + "\n" + appended
print("[5] appended Viewport/Content/Scrollbar/SlidingArea/Handle + 8 slots")

# ============================================================
# 写回
# ============================================================
with open(PATH, "w", encoding="utf-8") as f:
    f.write(txt2)
print(f"\nDONE. wrote {PATH}")
print(f"new fileIDs used: {len(ids)} + 8x3 slots")
