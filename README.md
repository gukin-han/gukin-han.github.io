# 문서 정리 가이드라인 (Notes System v1)

> 목적: **빨리 찾고, 바로 쓰고, 오래 남기는** 구조. 기술은 *태그*, 폴더는 *문서 타입/작업 목적* 기준.

- [문서 정리 가이드라인 (Notes System v1)](#문서-정리-가이드라인-notes-system-v1)
  - [1. 폴더 구조 (기본 트리)](#1-폴더-구조-기본-트리)
  - [2. 번호 붙이기 원칙](#2-번호-붙이기-원칙)
  - [3. 폴더 깊이(depth) 원칙](#3-폴더-깊이depth-원칙)
  - [4. 태그 스키마](#4-태그-스키마)
  - [5. 파일명 규칙](#5-파일명-규칙)
  - [6. 공통 상단 5줄 템플릿](#6-공통-상단-5줄-템플릿)
  - [7. MOC(Map of Content)](#7-mocmap-of-content)
    - [7.1 언제 쓰나](#71-언제-쓰나)
    - [7.2 작성 원칙](#72-작성-원칙)
    - [7.3 템플릿](#73-템플릿)
    - [7.4 반자동 생성 스크립트(옵션)](#74-반자동-생성-스크립트옵션)
  - [8. 자동 목차(TOC) 운용](#8-자동-목차toc-운용)
  - [9. 에셋(Asset) 관리](#9-에셋asset-관리)
    - [9.1 배치 전략](#91-배치-전략)
    - [9.2 VS Code 설정](#92-vs-code-설정)
    - [9.3 Obsidian 설정(선택)](#93-obsidian-설정선택)
    - [9.4 용량/품질 관리](#94-용량품질-관리)
    - [9.5 고아 에셋 청소](#95-고아-에셋-청소)
  - [10. Kafka 예시(허브 → 분리)](#10-kafka-예시허브--분리)
  - [11. 운영 규칙(스케일 가드레일)](#11-운영-규칙스케일-가드레일)
  - [12. 마이그레이션 최소비용 플랜](#12-마이그레이션-최소비용-플랜)
  - [부록 A. 추천 .vscode/settings.json](#부록-a-추천-vscodesettingsjson)
  - [부록 B. pre-commit 훅(이미지 최적화 예시)](#부록-b-pre-commit-훅이미지-최적화-예시)
  - [부록 C. .gitignore 예외(점 폴더 쓸 때)](#부록-c-gitignore-예외점-폴더-쓸-때)

---


## 1. 폴더 구조 (기본 트리)

```text
notes/
├─ 00-inbox/                    # 급히 메모(주 1회 비우기)
├─ 10-drafts/                   # (옵션) 작성 중 초안함
├─ concepts/                    # 기술 불문 개념(원리·정의·보장)
├─ patterns/                    # 설계/아키텍처 패턴(트레이드오프 포함)
├─ recipes/                     # 구현 레시피(복붙 중심)
│  ├─ java/
│  ├─ spring/
│  ├─ redis/
│  ├─ kafka/
│  └─ db/
├─ experiments/                 # 실험/벤치마크/POC (환경·수치·결론)
├─ decisions/                   # ADR/RFC 의사결정 기록
├─ operations/                  # 운영/장애 대응 플레이북·체크리스트
├─ 90-projects/                 # 프로젝트 문맥(스펙/회의록 등)
│  └─ hr-sync/
├─ assets/                      # 공용 에셋(2회↑ 재사용)
└─ 99-z-archive/                # 휴면/폐기 (검색엔 걸리게)
````

* **폴더 = 작업 목적/문서 타입.**
* **기술(Java/Redis/Kafka) = 태그** 또는 `recipes/` 하위 폴더.

---

## 2. 번호 붙이기 원칙

* **전부 번호 금지.** 위치 고정이 필요한 **핵심만 번호**:

  * 상단 고정: `00-inbox/`, `10-drafts/`
  * 하단 고정: `90-projects/`, `99-z-archive/`
* 콘텐츠 폴더(`concepts/`, `patterns/`, `recipes/`…)는 **비번호** 유지.
* 리네임 노이즈·깨진 링크 최소화.

---

## 3. 폴더 깊이(depth) 원칙

* **기본 2단계.** 예외적으로 3단계(대형 프로젝트, 폭증한 레시피)만 허용.
* **20개 룰**: 한 폴더 문서가 20개↑면 하위 분화 또는 **MOC** 추가.

---

## 4. 태그 스키마

* 기술: `#tech/java #tech/redis #tech/kafka #tech/spring`
* 개념/주제: `#concept/idempotency #concept/concurrency`
* 레이어: `#layer/api #layer/service #layer/data`
* 도메인/프로젝트: `#domain/leave #proj/hr-sync`
* 문서 타입: `#type/concept|pattern|recipe|experiment|adr|playbook`
* 상태: `#status/capture|draft|final|verified`

> 폴더는 목적, **태그로 횡단 검색**.

---

## 5. 파일명 규칙

* `kebab-case`, 핵심 명사 우선.
* `experiments/`: `EXP-YYYY-MM-DD-key.md`
* `decisions/`: `ADR-YYYY-MM-DD-key.md`
* `operations/`: `playbook-thing.md`, `runbook-thing.md`
* 기타: `topic-keyword.md` (`idempotency.md`, `outbox.md` 등)

---

## 6. 공통 상단 5줄 템플릿

모든 문서 첫 블록(5줄) — 검색·재사용률 상승.

```md
Why  : (문제/배경 한 줄)
What : (핵심 결론 한 줄)
How  : (절차·핵심 코드·도식)
Result: (증거/수치/근거 링크)
Next : (관련 노트 링크)
```

---

## 7. MOC(Map of Content)

### 7.1 언제 쓰나

* 주제 노트 10–20개↑, 또는 폴더를 가로지르는 주제일 때 `MOC-<topic>.md`.

### 7.2 작성 원칙

* **큐레이션** 위주(섹션별 5–8개 링크). 장문 금지.
* 섹션 구분은 문서 타입(Concepts/Patterns/Recipes/Operations/Decisions/Experiments).
* **정의는 한 곳**(중복 금지). MOC는 링크 허브.

### 7.3 템플릿

```md
# MOC – Kafka
_Last updated: 2025-07-27_

## Concepts
- [Partition & Ordering](concepts/kafka-topic-partition-and-ordering.md) — 한줄 요약
- [Delivery Semantics](concepts/kafka-delivery-semantics-atleast-atmost-exactly-once.md)

## Patterns
- [Outbox](patterns/outbox.md)
- [Retry & DLQ](patterns/retry-dlq-pattern.md)
- [Keying Strategy](patterns/keying-strategy-for-partitioning.md)

## Recipes
- [Create Topic (Retention/Compaction)](recipes/kafka/topic-create-retention-compact-cli.md)
- [Idempotent Producer & acks](recipes/kafka/producer-idempotence-and-acks.md)
- [Spring Kafka – Retry/DLQ](recipes/spring/spring-kafka-retry-dlq-with-deadletter-pubsub.md)

## Operations
- [Consumer Lag Playbook](operations/playbook-consumer-lag.md)

## Decisions
- [ADR – Keying Strategy](decisions/ADR-2025-08-10-kafka-keying-strategy.md)

## Experiments
- [acks/batch/linger 성능](experiments/EXP-2025-08-12-producer-acks-batch-latency.md)
```

### 7.4 반자동 생성 스크립트(옵션)

태그(`#tech/kafka`) 기반으로 MOC를 뽑는 간단 쉘:

```bash
#!/usr/bin/env bash
set -euo pipefail
TOPIC="${1:-kafka}"              # 사용: ./gen-moc.sh kafka
ROOT="notes"
OUT="$ROOT/MOC-$TOPIC.md"
SECTIONS=(concepts patterns recipes operations decisions experiments)

{
  echo "# MOC – $TOPIC"
  echo
  echo "_Last updated: $(date +%F)_"
  for s in "${SECTIONS[@]}"; do
    echo
    echo "## ${s^}"
    echo
    mapfile -t files < <(grep -RIl --include="*.md" "#tech/$TOPIC" "$ROOT/$s" 2>/dev/null | sort || true)
    for f in "${files[@]:-}"; do
      title="$(grep -m1 '^# ' "$f" | sed 's/^# //')"
      [[ -z "$title" ]] && title="$(basename "$f" .md)"
      rel="${f#$ROOT/}"
      echo "- [$title]($rel)"
    done
  done
} > "$OUT"

echo "Wrote $OUT"
```

---

## 8. 자동 목차(TOC) 운용

* VS Code: 확장 **Markdown All in One**

  * 커맨드: `Markdown: Create Table of Contents`
  * 저장 시 자동 갱신:

    ```json
    "markdown.extension.toc.updateOnSave": true,
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 700
    ```
* Obsidian: **Outline 패널**은 라이브. 문서 내 고정 TOC는 플러그인 선택.

---

## 9. 에셋(Asset) 관리

### 9.1 배치 전략

* **기본(추천)**: **per-note** — `노트이름.assets/`

  * 예:

    ```
    recipes/redis/rate-limit-fixed-window.md
    recipes/redis/rate-limit-fixed-window.assets/fig01-ttl-flow.svg
    ```
* **공용(2회↑ 재사용)**: `assets/<topic>/…`

  * 예: `assets/architecture/outbox-seq.svg`

> “숨기고 싶다”가 1순위면 점 폴더(`.assets/`) 사용 가능. 단, 일부 빌드/ignore 규칙과 충돌 가능.

### 9.2 VS Code 설정

```json
{
  "editor.wordWrap": "on",
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 700,
  "markdown.extension.toc.updateOnSave": true,

  "pasteImage.path": "${currentFileDir}/${currentFileNameWithoutExt}.assets",
  "pasteImage.insertPattern": "![](${imagePath})",
  "pasteImage.defaultName": "${currentFileNameWithoutExt}-${currentDate}${currentTime}"
}
```

### 9.3 Obsidian 설정(선택)

* Files & Links → New attachments: **In subfolder under current folder**
* Subfolder: `_assets` (폴더 공용이 필요할 때)
* New link format: **Relative path**
* 내부 링크 자동 업데이트: Off(표준 Markdown 유지 목적이면)

### 9.4 용량/품질 관리

* **SVG 우선**(도표/아이콘). 스크린샷/사진은 **WebP**.
* 단일 파일 **5MB↑**: Git LFS 또는 외부 스토리지 링크.
* 다이어그램 원본 보존: `.drawio`/`.excalidraw` + 내보낸 `.svg` 동시 보관.

### 9.5 고아 에셋 청소

```bash
# 미참조 이미지 후보 나열 (macOS)
find . -type f \( -name "*.png" -o -name "*.webp" -o -name "*.svg" \) \
| while read f; do
  grep -Rqs -- "$f" ./*.md */*.md */*/*.md || echo "$f"
done
```

---

## 10. Kafka 예시(허브 → 분리)

* 초기: `concepts/kafka.md` **한 파일**에 섹션(##)으로 모음.
* 섹션 커지면 **개별 파일**로 승격, `kafka.md`는 **요약+링크 허브**만 유지.
* **고정 앵커**로 안정 링크:

```md
# Kafka Concepts (MOC)
<!-- TOC -->

<a id="kafka-append-only-log"></a>
## Append-only Log
요약 3–5줄…

<a id="kafka-partition-ordering"></a>
## Topic, Partition, Ordering
…

<a id="kafka-delivery-semantics"></a>
## Delivery Semantics (At-least/At-most/Exactly-once)
…
```

분리 예:

* `concepts/kafka-delivery-semantics-atleast-atmost-exactly-once.md`
* `kafka.md` 해당 섹션엔 5줄 요약 + “자세히 보기” 링크만.

---

## 11. 운영 규칙(스케일 가드레일)

* **30초 룰**: 재방문 30초 내 못 찾으면 파일명/태그/링크 보강.
* **20개 룰**: 폴더 20개↑ → 하위 분화 or MOC 추가.
* **주간 정리**: `00-inbox/` **주 1회 비우기**.
* **중복 금지**: 개념은 한 곳에만. 나머지는 링크로 재사용.

---

## 12. 마이그레이션 최소비용 플랜

1. 현 구조 유지. 위 트리만 추가.
2. **새 문서부터** 새 구조에 저장.
3. 기존 문서 상단에 **태그만** 먼저 부여.
4. 한 달 동안 자주 여는 문서만 단계적 이동.
5. 링크는 상대경로. 구조 변경 PR은 **이동 전용**으로 분리.

---

## 부록 A. 추천 .vscode/settings.json

```json
{
  "editor.wordWrap": "on",
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 700,

  "[markdown]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "markdown.extension.toc.updateOnSave": true,

  "pasteImage.path": "${currentFileDir}/${currentFileNameWithoutExt}.assets",
  "pasteImage.insertPattern": "![](${imagePath})",
  "pasteImage.defaultName": "${currentFileNameWithoutExt}-${currentDate}${currentTime}",

  "files.trimTrailingWhitespace": true
}
```

---

## 부록 B. pre-commit 훅(이미지 최적화 예시)

```bash
#!/usr/bin/env bash
set -e
changed=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(png|jpg|jpeg)$' || true)
for f in $changed; do
  [ -f "$f" ] || continue
  # WebP 생성
  command -v cwebp >/dev/null 2>&1 && cwebp -q 82 "$f" -o "${f%.*}.webp" >/dev/null 2>&1 || true
  # PNG 압축
  if [[ "$f" == *.png ]]; then
    command -v pngquant >/dev/null 2>&1 && pngquant --force --ext .png "$f" >/dev/null 2>&1 || true
  fi
  git add "${f%.*}.webp" "$f" || true
done
```

---

## 부록 C. .gitignore 예외(점 폴더 쓸 때)

`.gitignore`에 `.*`가 있다면 점 폴더 예외 추가:

```gitignore
!.assets/
!.assets/**
```

---

**핵심 요약**

* 폴더=목적, 기술=태그.
* 기본 depth=2, MOC로 주제 큐레이션.
* per-note 에셋 + 공용 승격.
* `kafka.md` 같은 허브 문서로 시작 → 커지면 분리.
* 30초/20개 룰로 지속 개선.


