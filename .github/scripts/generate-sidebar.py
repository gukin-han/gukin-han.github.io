#!/usr/bin/env python3
"""
자동으로 _sidebar.md 파일을 생성하는 스크립트
루트부터 재귀 스캔하여 index.md를 찾고, 계층 구조대로 사이드바를 만듭니다.
"""

from pathlib import Path
from typing import List

# ─── 설정 ───────────────────────────────────────────────────────────
HOME_LINK = "/"   # 루트 URL
EXCLUDE_DIRS = {"assets"}  # 제외할 디렉토리명 (소문자)
# ─────────────────────────────────────────────────────────────────────

def get_title(fp: Path) -> str:
    """마크다운에서 첫 번째 '# ' 제목을 뽑고, 없으면 파일명 기반으로."""
    try:
        for line in fp.open(encoding='utf-8'):
            if line.startswith('# '):
                return line[2:].strip()
    except:
        pass
    return fp.stem.replace('-', ' ').title()

def process_dir(dir_path: Path, rel_prefix: Path, depth: int) -> List[str]:
    """
    디렉토리를 재귀 처리하여 리스트 항목을 생성.
    - dir_path: 현재 디렉토리
    - rel_prefix: 루트 대비 상대 경로 프리픽스
    - depth: 들여쓰기 깊이
    """
    lines: List[str] = []
    index_md = dir_path / 'index.md'

    # 디렉토리 헤더 (index.md 있으면 링크, 없으면 텍스트)
    if index_md.exists():
        title = get_title(index_md)
        link = (rel_prefix / dir_path.name / 'index.md').as_posix()
        lines.append(f"{'  '*depth}- [{title}](/{link})")
    else:
        section = dir_path.name.replace('-', ' ').title()
        lines.append(f"{'  '*depth}- {section}")

    # 자식 디렉토리 처리
    for child in sorted(dir_path.iterdir()):
        if (child.is_dir() and
            not child.name.startswith('.') and
            child.name.lower() not in EXCLUDE_DIRS):
            lines.extend(process_dir(child, rel_prefix / dir_path.name, depth + 1))
    return lines

def generate_sidebar() -> str:
    lines: List[str] = []

    # 1) Home 링크
    lines.append(f"- [Home]({HOME_LINK})")
    lines.append("")

    # 2) 루트 폴더의 서브디렉토리부터 생성
    root = Path.cwd()
    for child in sorted(root.iterdir()):
        if (child.is_dir() and
            not child.name.startswith('.') and
            child.name.lower() not in EXCLUDE_DIRS):
            lines.extend(process_dir(child, Path(), 0))

    # 최종 문자열
    return "\n".join(lines).rstrip() + "\n"

def main():
    sidebar = generate_sidebar()
    out = Path.cwd() / '_sidebar.md'
    out.write_text(sidebar, encoding='utf-8')
    print(f"✅ {out.name} 생성 완료")
    print(sidebar)

if __name__ == '__main__':
    main()
