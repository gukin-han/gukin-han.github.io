#!/usr/bin/env python3
"""
자동으로 _sidebar.md 파일을 생성하는 스크립트
프로젝트 구조를 스캔하여 모든 index.md 파일을 찾고 사이드바를 생성합니다.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

def get_title_from_markdown(file_path: Path) -> str:
    """마크다운 파일에서 첫 번째 # 제목을 추출합니다."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 첫 번째 # 제목을 찾습니다
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
            # 제목이 없으면 파일명을 사용합니다
            return file_path.stem.replace('-', ' ').title()
    except Exception:
        return file_path.stem.replace('-', ' ').title()

def scan_directory(directory: Path, base_path: str = "") -> List[Tuple[str, str, str]]:
    """디렉토리를 스캔하여 index.md 파일들을 찾습니다."""
    items = []
    
    # 디렉토리 내의 모든 항목을 가져옵니다
    try:
        dir_items = sorted([item for item in directory.iterdir() if item.is_dir()])
    except PermissionError:
        return items
    
    for item in dir_items:
        # .git 디렉토리는 건너뜁니다
        if item.name.startswith('.'):
            continue
            
        # index.md 파일이 있는지 확인합니다
        index_file = item / "index.md"
        if index_file.exists():
            title = get_title_from_markdown(index_file)
            relative_path = f"{base_path}/{item.name}/index.md" if base_path else f"{item.name}/index.md"
            items.append((item.name, title, relative_path))
    
    return items

def generate_sidebar_content() -> str:
    """사이드바 내용을 생성합니다."""
    content = []
    
    # 01-index 디렉토리 처리
    index_dir = Path("01-index")
    if index_dir.exists():
        index_items = scan_directory(index_dir, "01-index")
        if index_items:
            content.append("- 01 Index")
            for _, title, path in index_items:
                content.append(f"  - [{title}](/{path})")
            content.append("")
    
    # 02-solutions 디렉토리 처리
    solutions_dir = Path("02-solutions")
    if solutions_dir.exists():
        solutions_items = scan_directory(solutions_dir, "02-solutions")
        if solutions_items:
            content.append("- 02 Solutions")
            for _, title, path in solutions_items:
                content.append(f"  - [{title}](/{path})")
            content.append("")
    
    # 03-concepts 디렉토리 처리
    concepts_dir = Path("03-concepts")
    if concepts_dir.exists():
        concepts_items = scan_directory(concepts_dir, "03-concepts")
        if concepts_items:
            content.append("- 03 Concepts")
            for _, title, path in concepts_items:
                content.append(f"  - [{title}](/{path})")
            content.append("")
    
    # 기타 디렉토리들 처리 (01, 02, 03으로 시작하지 않는 디렉토리)
    for item in sorted(Path(".").iterdir()):
        if (item.is_dir() and 
            not item.name.startswith('.') and 
            not item.name.startswith(('01-', '02-', '03-')) and
            item.name not in ['01-index', '02-solutions', '03-concepts']):
            
            items = scan_directory(item, item.name)
            if items:
                # 디렉토리명을 제목으로 사용
                section_title = item.name.replace('-', ' ').title()
                content.append(f"- {section_title}")
                for _, title, path in items:
                    content.append(f"  - [{title}](/{path})")
                content.append("")
    
    return '\n'.join(content).strip()

def main():
    """메인 함수"""
    print("사이드바 생성을 시작합니다...")
    
    # 현재 작업 디렉토리를 확인합니다
    current_dir = Path.cwd()
    print(f"현재 디렉토리: {current_dir}")
    
    # 사이드바 내용을 생성합니다
    sidebar_content = generate_sidebar_content()
    
    # _sidebar.md 파일에 쓰기
    sidebar_file = Path("_sidebar.md")
    with open(sidebar_file, 'w', encoding='utf-8') as f:
        f.write(sidebar_content)
    
    print(f"사이드바가 생성되었습니다: {sidebar_file}")
    print("생성된 내용:")
    print("-" * 40)
    print(sidebar_content)
    print("-" * 40)

if __name__ == "__main__":
    main() 