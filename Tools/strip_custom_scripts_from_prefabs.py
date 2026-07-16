#!/usr/bin/env python3
"""Remove AnimationSystem custom MonoBehaviour scripts from Unity prefab YAML files."""

import re
import sys
from pathlib import Path

STRIP_GUIDS = {
    "d26e799ae5710cf43b51e0ce93cbdd91",  # Assassin
    "f08bf0305483ae24c8fcd5cb939a1f23",  # BladeItem
    "0131917d1e386944c8f60f2d3a846f96",  # Blademan
    "d0338a6ad7a746a4ab4984f3435b091d",  # Cage
    "55857324eeec59b49bee20f341dba6bc",  # CameraController
    "8f2730ff370b6a4468ef8f48a586959e",  # CharacterBaseController
    "2c6a5bd412e1c384c86a0a6ab2eb3243",  # EffectDestory
    "8cfbb7fa01a422747aba40256f5e1009",  # EnemyAI
    "c95d6c8a304fce74bb08794d01ac143f",  # GameController
    "75b0934a6ef99be40bfe06f3d9ba8ffd",  # InputController
    "d82d1fdf15994cb44a2e13a6bebf3dc9",  # Master
    "39fd0891a1c5fbb489585e65770b278d",  # PlayerInputStateController
    "267f277edfce5ca46a0e5bf1d6d47c92",  # PoolManager
    "440ca626bd783a441acfe3259f5eb830",  # Role
    "d4870ed2eb590bc4ea6dffc4641c6111",  # ShadowProjectileMega
    "4ced4f18d9b73db40baacbd86bdae93a",  # Shield
    "112aa1b3b592c6c42a7a76f871c115f0",  # Swordman
    "65080a54457f4b042814819f9744bc85",  # TestBehaviour
    "5f74c979b99b1844f9634313fdd54660",  # UIManager
    "f3c422220a2563b40b307dc956022443",  # Valkyrie
    "a807965ebb0f2834db0d32cbc05afe6c",  # ValkyrieAI
    "9df089d141d8dca4c9c2091075c918c8",  # Weapon
}

GUID_PATTERN = re.compile(
    r"m_Script:\s*\{fileID:\s*11500000,\s*guid:\s*([0-9a-f]+),\s*type:\s*3\}"
)
BLOCK_HEADER = re.compile(r"^--- !u!(\d+) &(-?\d+)", re.MULTILINE)
COMPONENT_REF = re.compile(
    r"^\s*-\s*component:\s*\{fileID:\s*(-?\d+)\}\s*$", re.MULTILINE
)


def strip_prefab(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("%YAML"):
        return 0

    parts = text.split("--- !u!")
    if not parts:
        return 0

    header = parts[0]
    blocks = parts[1:]
    remove_ids: set[str] = set()
    kept_blocks: list[str] = []

    for block in blocks:
        header_match = BLOCK_HEADER.match("--- !u!" + block)
        if not header_match:
            kept_blocks.append(block)
            continue

        type_id, local_id = header_match.group(1), header_match.group(2)
        guid_match = GUID_PATTERN.search(block)
        if type_id == "114" and guid_match and guid_match.group(1) in STRIP_GUIDS:
            remove_ids.add(local_id)
            continue

        kept_blocks.append(block)

    if not remove_ids:
        return 0

    cleaned_blocks: list[str] = []
    for block in kept_blocks:
        lines = block.splitlines(keepends=True)
        filtered = [
            line
            for line in lines
            if not (
                (m := COMPONENT_REF.match(line.rstrip("\r\n")))
                and m.group(1) in remove_ids
            )
        ]
        cleaned_blocks.append("".join(filtered))

    output = header + "".join("--- !u!" + b for b in cleaned_blocks)
    path.write_text(output, encoding="utf-8", newline="\n")
    return len(remove_ids)


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("Assets/Effects")
    total_removed = 0
    changed_files = 0

    for prefab in root.rglob("*.prefab"):
        removed = strip_prefab(prefab)
        if removed:
            changed_files += 1
            total_removed += removed
            print(f"stripped {removed} script(s): {prefab}")

    print(f"Done. {changed_files} prefab(s), {total_removed} component(s) removed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
