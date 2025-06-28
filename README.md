# HOME

# Notes

이 저장소는 Docify를 사용한 문서 사이트입니다.

## 자동 사이드바 생성

이 프로젝트는 GitHub Actions를 사용하여 `_sidebar.md` 파일을 자동으로 갱신합니다.

### 작동 방식

1. **GitHub Actions 워크플로우**: `.github/workflows/update-sidebar.yml`
   - main/master 브랜치에 푸시될 때 자동으로 실행됩니다
   - `_sidebar.md` 파일이 변경되지 않았을 때만 실행됩니다

2. **Python 스크립트**: `.github/scripts/generate-sidebar.py`
   - 프로젝트 구조를 스캔하여 모든 `index.md` 파일을 찾습니다
   - 각 `index.md` 파일의 첫 번째 `#` 제목을 추출합니다
   - 디렉토리 구조에 따라 사이드바를 자동 생성합니다

### 권한 설정

GitHub Actions가 저장소에 커밋을 푸시하려면 적절한 권한이 필요합니다.

1. GitHub 저장소 페이지에서 **Settings** 탭으로 이동
2. 왼쪽 메뉴에서 **Actions** → **General** 선택
3. **Workflow permissions** 섹션에서:
   - **Read and write permissions** 선택
   - **Allow GitHub Actions to create and approve pull requests** 체크
4. **Save** 클릭

### 디렉토리 구조

```
notes/
├── 01-index/          # 인덱스 문서들
├── 02-solutions/      # 솔루션 문서들
├── 03-concepts/       # 개념 문서들
└── _sidebar.md        # 자동 생성되는 사이드바
```

### 수동 실행

로컬에서 사이드바를 수동으로 생성하려면:

```bash
python3 .github/scripts/generate-sidebar.py
```

### 주의사항

- 각 문서 디렉토리에는 `index.md` 파일이 있어야 합니다
- `index.md` 파일의 첫 번째 `#` 제목이 사이드바에 표시됩니다
- 제목이 없으면 디렉토리명이 사용됩니다