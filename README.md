# Notes System v3: 개발자를 위한 노트 시스템

> 목적: **빠르게 찾고, 바로 쓰고, 오래 남기는** 실용적인 2-Depth 노트 구조.

- [Notes System v3: 개발자를 위한 노트 시스템](#notes-system-v3-개발자를-위한-노트-시스템)
  - [1. 폴더 구조 (v3, Type & Tech 2-Depth)](#1-폴더-구조-v3-type--tech-2-depth)
  - [2. 핵심 원칙](#2-핵심-원칙)
  - [3. 노트 작성 워크플로우](#3-노트-작성-워크플ow)
  - [4. 파일명 규칙](#4-파일명-규칙)
  - [5. 태그 스키마](#5-태그-스키마)
  - [6. MOC(Map of Content)](#6-mocmap-of-content)
    - [6.1 언제 쓰나](#61-언제-쓰나)
    - [6.2 작성 원칙](#62-작성-원칙)
    - [6.3 템플릿 예시](#63-템플릿-예시)
    - [6.4 반자동 생성 스크립트(옵션)](#64-반자동-생성-스크립트옵션)
  - [7. 에셋(Asset) 관리](#7-에셋asset-관리)
  - [8. VS Code 추천 설정](#8-vs-code-추천-설정)
  - [부록 A: pre-commit 훅 (이미지 최적화)](#부록-a-pre-commit-훅-이미지-최적화)

---

## 1. 폴더 구조 (v3, Type & Tech 2-Depth)

```text
/
├── 10-inbox/              # (1-depth) 모든 아이디어의 시작점
├── 20-concepts/           # (1-depth) 개념, 원리
│   └── general/           # (2-depth) 특정 기술에 국한되지 않는 일반 개념
├── 30-patterns/           # (1-depth) 설계/아키텍처 패턴
│   └── architecture/      # (2-depth) 특정 프레임워크/기술을 넘어선 패턴
├── 40-recipes/            # (1-depth) 코드 조각, 설정, 명령어, 플레이북
│   ├── git/
│   └── java/
├── 50-decisions/          # (1-depth) 의사결정 기록 (ADR)
├── 60-experiments/        # (1-depth) 기술 실험, POC
├── 70-projects/           # (1-depth) 프로젝트 관련 문서
├── 80-resources/          # (1-depth) 재사용 자원
│   ├── assets/
│   └── templates/
└── 99-archive/            # (1-depth) 보관소
```

---

## 2. 핵심 원칙

*   **폴더는 2-Depth를 엄격히 유지한다.**
    *   **1-depth (최상위 폴더)**: 노트의 **종류** (컨셉, 패턴, 레시피 등)를 정의한다.
    *   **2-depth (하위 폴더)**: **기술 스택** (Java, Redis 등) 또는 일반 주제 (General, Architecture)로 분류한다.
    *   모든 노트(`.md`)는 2-depth 폴더 아래에 위치하여, `타입/기술/노트.md` 구조를 유지한다.
*   **폴더 번호는 순서 고정이 필요한 경우에만 사용한다.**
    *   `10-inbox` (최상단), `99-archive` (최하단)처럼 위치가 중요한 폴더에만 번호를 붙여 관리 부담을 줄인다.
*   **한 폴더에 파일이 20개 이상 쌓이면 MOC(Map of Content) 생성을 고려한다.**
    *   무한한 depth 대신, 링크 기반의 허브 페이지로 복잡도를 관리한다.
*   **개념 정의는 단 한 곳에서만 한다 (Single Source of Truth).**
    *   동일한 개념을 여러 노트에 중복해서 쓰지 않는다. 항상 링크를 사용해 참조한다.

---

## 3. 노트 작성 워크플로우

1.  **캡처 (Capture)**: 어떤 생각이든 일단 `10-inbox/`에 빠르게 메모한다. (예: `untitled.md`, `새로운 인증 방식 아이디어.md`)
2.  **정리 (Organize)**: 매주 시간을 내어 `10-inbox/`의 노트들을 검토한다.
    *   **단순 정보/레시피인가?** -> `40-recipes/기술/주제.md`로 이동 및 정리
    *   **깊은 학습이 필요한 개념인가?** -> `20-concepts/기술/주제.md`로 이동 및 정리
    *   **프로젝트 관련 내용인가?** -> `70-projects/프로젝트명/회의록.md` 등으로 이동
    *   **더 이상 필요 없는 내용인가?** -> 과감히 삭제하거나 `99-archive/`로 이동
3.  **연결 (Connect)**: 노트를 작성하면서 기존의 다른 노트와 연결될 만한 부분을 찾아 `[[위키 링크]]`나 일반 마크다운 링크로 연결한다. 이 과정을 통해 지식이 네트워크를 형성한다.

---

## 4. 파일명 규칙

*   **`kebab-case`** 사용을 원칙으로 한다. (예: `rate-limiter-with-redis.md`)
*   **핵심 명사를 앞에** 두어 파일 목록에서 찾기 쉽게 한다.
*   **날짜 기반 접두사**는 특정 타입에만 사용한다.
    *   `60-experiments/`: `exp-YYYY-MM-DD-주제.md`
    *   `50-decisions/`: `adr-YYYY-MM-DD-주제.md`

---

## 5. 태그 스키마

> 폴더로 1차 분류하고, 태그로 2차 횡단 검색을 가능하게 한다.

*   **기술**: `#tech/java`, `#tech/spring`, `#tech/kafka`
*   **레이어**: `#layer/api`, `#layer/service`, `#layer/data`
*   **프로젝트**: `#proj/hr-sync`, `#proj/order-system`
*   **상태**: `#status/idea`, `#status/draft`, `#status/complete`
*   **문서 타입**: `#type/concept`, `#type/pattern`, `#type/recipe`, `#type/adr` (폴더와 중복되지만, 검색 편의를 위해 사용)

---

## 6. MOC(Map of Content)

### 6.1 언제 쓰나

*   특정 기술(예: Kafka)이나 주제(예: 인증)에 대한 노트가 여러 폴더에 흩어져 10개 이상 쌓였을 때.
*   `MOC-kafka.md` 와 같은 파일을 `20-concepts/`나 `30-patterns/` 등 가장 관련 있는 폴더의 `general` 이나 `architecture` 하위에 만든다.

### 6.2 작성 원칙

*   **큐레이션**이 핵심. 관련된 노트로 가는 링크 허브 역할에 집중한다.
*   섹션은 노트 타입(`## Concepts`, `## Patterns`, `## Recipes`)으로 나눈다.

### 6.3 템플릿 예시

```md
# MOC – Kafka
_Last updated: 2025-07-27_

## Concepts
- [Partition & Ordering](20-concepts/kafka/partition-and-ordering.md)
- [Delivery Semantics](20-concepts/kafka/delivery-semantics.md)

## Patterns
- [Outbox Pattern](30-patterns/architecture/outbox-pattern.md)
- [Retry & DLQ](30-patterns/spring/retry-dlq-with-kafka.md)

## Recipes
- [Create Topic CLI](40-recipes/kafka/create-topic-cli.md)
- [Spring Kafka Idempotent Producer](40-recipes/spring/kafka-idempotent-producer.md)
```

### 6.4 반자동 생성 스크립트(옵션)

태그(`-- #tech/kafka`) 기반으로 MOC 초안을 생성하는 쉘 스크립트:

```bash
#!/usr/bin/env bash
set -euo pipefail
TOPIC="${1:-kafka}" # 사용법: ./gen-moc.sh kafka
ROOT_DIR="."
OUT_FILE="MOC-$TOPIC.md"
SECTIONS=(20-concepts 30-patterns 40-recipes 50-decisions 60-experiments)

{
  echo "# MOC – $TOPIC"
  echo
  echo "_Last updated: $(date +%F)_"
  for s in "${SECTIONS[@]}"; do
    # 섹션 이름에서 숫자 접두사 제거하고 첫 글자 대문자로
    section_name=$(echo "$s" | sed 's/^[0-9]*-//' | sed 's/./\u&/')
    echo
    echo "## $section_name"
    echo
    # 해당 섹션 폴더 내에서 태그를 포함하는 마크다운 파일 검색
    mapfile -t files < <(grep -RIl --include="*.md" "#tech/$TOPIC" "$ROOT_DIR/$s/" 2>/dev/null | sort || true)
    for f in "${files[@]:-}"; do
      # 파일 경로에서 './' 제거
      rel_path="${f#./}"
      # 파일 첫 줄에서 제목 추출
      title=$(grep -m1 '^# ' "$f" | sed 's/^# //')
      # 제목이 없으면 파일명을 제목으로 사용
      [[ -z "$title" ]] && title="$(basename "$f" .md)"
      echo "- [$title]($rel_path)"
    done
  done
} > "$OUT_FILE"

echo "Generated MOC file: $OUT_FILE"
```

---

## 7. 에셋(Asset) 관리

*   **기본 전략: Per-note assets**
    *   노트와 동일한 위치에 `노트파일명.assets/` 폴더를 만들어 관련된 이미지를 모두 넣는다.
    *   예: `40-recipes/redis/rate-limiter.md` 와 `40-recipes/redis/rate-limiter.assets/flow-diagram.svg`
*   **공용 전략: Global assets**
    *   여러 노트에서 재사용될 에셋은 `80-resources/assets/` 에 보관한다.
    *   예: `80-resources/assets/architecture/microservice-communication.svg`

---

## 8. VS Code 추천 설정

`.vscode/settings.json` 파일에 아래 설정을 추가하면 노트 작성 경험이 향상됩니다.

```json
{
  "editor.wordWrap": "on",
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,

  "[markdown]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    // 위키 링크 [[...]] 자동 완성 활성화
    "editor.quickSuggestions": {
      "other": true,
      "comments": false,
      "strings": true
    }
  },

  // Markdown All in One 확장 기능
  "markdown.extension.toc.updateOnSave": true,

  // Paste Image 확장 기능 (클립보드 이미지 붙여넣기)
  "pasteImage.path": "${currentFileDir}/${currentFileNameWithoutExt}.assets",
  "pasteImage.insertPattern": "![](${imagePath})",
  "pasteImage.defaultName": "img-${currentDate}${currentTime}"

  "files.trimTrailingWhitespace": true
}
```

---

## 부록 A: pre-commit 훅 (이미지 최적화)

Git에 커밋하기 전, 이미지를 자동으로 최적화하는 pre-commit 훅입니다. `.git/hooks/pre-commit` 에 저장하고 실행 권한을 주세요 (`chmod +x .git/hooks/pre-commit`).

```bash
#!/usr/bin/env bash
set -e

# WebP, PNG 최적화 도구가 설치되어 있는지 확인
if ! command -v cwebp >/dev/null || ! command -v pngquant >/dev/null; then
  echo "Info: cwebp or pngquant not found. Skipping image optimization."
  exit 0
fi

# 스테이징된 이미지 파일 목록 가져오기
changed_images=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\\.(png|jpe?g)$' || true)

[ -z "$changed_images" ] && exit 0

echo "Optimizing images..."

for f in $changed_images; do
  [ -f "$f" ] || continue
  
  # WebP로 변환 (JPEG, PNG 모두)
  ext="${f##*.}"
  webp_file="${f%.*}.webp"
  cwebp -q 80 "$f" -o "$webp_file" >/dev/null 2>&1
  
  # 원본이 PNG이면 압축
  if [[ "$ext" == "png" ]]; then
    pngquant --force --ext .png --skip-if-larger "$f" >/dev/null 2>&1
  fi
  
  # 최적화된 파일들을 스테이징에 추가
  git add "$webp_file" "$f"
  echo "  - Optimized $f"
done

echo "Image optimization complete."
```