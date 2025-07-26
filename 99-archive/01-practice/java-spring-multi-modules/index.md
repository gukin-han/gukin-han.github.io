# Gradle 멀티 모듈 프로젝트 구성 가이드

이 문서는 현재 프로젝트와 유사한 Gradle 멀티 모듈 구조를 설정하는 방법을 안내합니다. 이 가이드를 따르면 재현성 높게 모듈화된 프로젝트를 구성할 수 있습니다.

## 1. 프로젝트 구조

본 프로젝트는 다음과 같은 계층적 구조를 가집니다.

```
.
├── apps
│   └── commerce-api
├── modules
│   └── jpa
└── supports
    ├── jackson
    ├── logging
    └── monitoring
```

- **`apps`**: 실제 실행 가능한 애플리케이션 모듈이 위치합니다. (예: Spring Boot 애플리케이션)
- **`modules`**: 도메인 또는 비즈니스 로직과 관련된 공통 모듈이 위치합니다. 다른 모듈에서 재사용 가능한 코드의 집합입니다.
- **`supports`**: 프로젝트 전반에 걸쳐 사용되는 기술적인 지원 모듈이 위치합니다. (예: 로깅, 모니터링, 직렬화 설정)

## 2. `settings.gradle.kts` 설정

프로젝트의 최상단 `settings.gradle.kts` 파일은 전체 프로젝트의 구성과 포함될 하위 모듈을 정의합니다.

```kotlin
rootProject.name = "your-project-name"

include(
    ":apps:commerce-api",
    ":modules:jpa",
    ":supports:jackson",
    ":supports:logging",
    ":supports:monitoring",
)

// ... (pluginManagement 설정)
```

- **`rootProject.name`**: 루트 프로젝트의 이름을 지정합니다.
- **`include(...)`**: 프로젝트에 포함할 모든 하위 모듈의 경로를 콜론(`:`)으로 구분하여 나열합니다.

**주의사항**:
- 새로운 모듈을 추가할 때마다 `include`에 해당 모듈의 경로를 반드시 추가해야 합니다.

## 3. 루트 `build.gradle.kts` 설정

루트 `build.gradle.kts` 파일은 모든 하위 프로젝트에 공통으로 적용될 설정을 정의합니다.

### 3.1. 플러그인과 공통 설정

```kotlin
plugins {
    java
    id("org.springframework.boot") apply false
    id("io.spring.dependency-management")
}

allprojects {
    // group, version 등 공통 설정
    repositories {
        mavenCentral()
    }
}

subprojects {
    apply(plugin = "java")
    apply(plugin = "org.springframework.boot")
    apply(plugin = "io.spring.dependency-management")

    dependencies {
        // 모든 하위 모듈에 공통으로 필요한 의존성 추가
        implementation("org.projectlombok:lombok")
        annotationProcessor("org.projectlombok:lombok")
        testImplementation("org.springframework.boot:spring-boot-starter-test")
    }

    // ... (Jar, BootJar, test 태스크 설정)
}
```

- **`plugins`**: `apply false`를 사용하여 플러그인을 직접 적용하지 않고, 하위 모듈에서 필요에 따라 적용할 수 있도록 설정합니다.
- **`allprojects`**: 루트 프로젝트를 포함한 모든 프로젝트에 적용될 설정을 정의합니다.
- **`subprojects`**: 모든 하위 프로젝트에 공통으로 적용될 설정을 정의합니다. 공통 의존성이나 플러그인을 여기에 추가하면 중복을 줄일 수 있습니다.

### 3.2. `apps` 모듈 특별 취급

```kotlin
configure(allprojects.filter { it.parent?.name.equals("apps") }) {
    tasks.withType<Jar> { enabled = false }
    tasks.withType<BootJar> { enabled = true }
}
```

- `apps` 디렉토리 아래의 모듈들은 실행 가능한 애플리케이션이므로, 일반 `Jar` 파일 대신 실행 가능한 `BootJar` 파일을 생성하도록 설정합니다.

### 3.3. 컨테이너 모듈 Task 비활성화

```kotlin
project("apps") { tasks.configureEach { enabled = false } }
project("modules") { tasks.configureEach { enabled = false } }
project("supports") { tasks.configureEach { enabled = false } }
```

- `apps`, `modules`, `supports`와 같이 다른 모듈을 담기만 하는 컨테이너 성격의 디렉토리(모듈)들은 직접 빌드되거나 테스트될 필요가 없으므로 모든 태스크를 비활성화하여 빌드 성능을 향상시킵니다.

## 4. 하위 모듈 `build.gradle.kts` 설정

각 하위 모듈의 `build.gradle.kts` 파일은 해당 모듈에만 필요한 의존성과 설정을 정의합니다.

### 4.1. `apps` 모듈 (예: `commerce-api`)

```kotlin
// apps/commerce-api/build.gradle.kts

dependencies {
    // 다른 모듈 참조
    implementation(project(":modules:jpa"))
    implementation(project(":supports:jackson"))

    // 웹 관련 의존성
    implementation("org.springframework.boot:spring-boot-starter-web")
}
```

- `implementation(project(":..."))` 구문을 사용하여 다른 내부 모듈에 대한 의존성을 추가합니다.
- 애플리케이션 실행에 필요한 의존성(예: `spring-boot-starter-web`)을 추가합니다.

### 4.2. `modules` 또는 `supports` 모듈 (예: `jpa`)

```kotlin
// modules/jpa/build.gradle.kts

plugins {
    `java-library`
}

dependencies {
    // 외부에 노출할 API
    api("org.springframework.boot:spring-boot-starter-data-jpa")

    // 내부에서만 사용할 구현체
    implementation("com.querydsl:querydsl-jpa::jakarta")
}
```

- **`plugins { 'java-library' }`**: 이 모듈이 다른 모듈에게 API를 제공하는 라이브러리임을 명시합니다.
- **`api(...)`**: 이 모듈을 의존하는 다른 모듈에게 전이(transitive) 의존성을 제공합니다. 즉, `jpa` 모듈을 의존하는 모듈은 `spring-boot-starter-data-jpa`를 직접 의존하지 않아도 사용할 수 있게 됩니다.
- **`implementation(...)`**: 이 모듈 내부에서만 사용되는 의존성을 추가합니다.

## 5. 재현을 위한 프로세스

1.  **디렉토리 구조 생성**: `apps`, `modules`, `supports` 디렉토리를 생성하고, 그 안에 필요한 하위 모듈 디렉토리를 생성합니다.
2.  **`settings.gradle.kts` 작성**: `rootProject.name`을 설정하고 `include`에 모든 하위 모듈 경로를 추가합니다.
3.  **루트 `build.gradle.kts` 작성**: 위 가이드에 따라 공통 설정을 추가합니다.
4.  **하위 모듈 `build.gradle.kts` 작성**: 각 모듈의 역할에 맞게 플러그인과 의존성을 설정합니다.
    - 라이브러리 모듈은 `java-library` 플러그인을 사용하고 `api`와 `implementation`을 구분하여 의존성을 관리합니다.
    - 애플리케이션 모듈은 필요한 내부 모듈들을 `project("...")`로 참조합니다.
5.  **Gradle 프로젝트 새로고침**: IDE(예: IntelliJ)에서 "Reload All Gradle Projects"를 실행하여 변경사항을 적용합니다.

## 6. 주의해야 할 점

- **순환 의존성 금지**: 모듈 간에 서로를 참조하는 순환 의존성(circular dependency)이 발생하지 않도록 주의해야 합니다. 예를 들어, `module-a`가 `module-b`를 의존하고, `module-b`가 다시 `module-a`를 의존하는 상황을 피해야 합니다.
- **`api` vs `implementation`**: `java-library` 플러그인을 사용할 때, 모듈의 API로 외부에 노출해야 하는 의존성은 `api`로, 내부 구현에만 필요한 의존성은 `implementation`으로 명확히 구분해야 합니다. 이는 불필요한 의존성 전파를 막고 빌드 성능을 향상시킵니다.
- **버전 관리**: `gradle.properties` 또는 루트 `build.gradle.kts`의 `ext` 블록을 사용하여 의존성 버전을 한 곳에서 관리하면 일관성을 유지하고 업데이트를 용이하게 할 수 있습니다.
- **테스트 의존성**: `testFixtures`를 사용하면 모듈 간 테스트 코드를 공유할 수 있어 유용합니다.
