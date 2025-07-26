# 아키텍처 및 코드 스타일 가이드라인

이 문서는 `example` 도메인을 기준으로 프로젝트의 아키텍처와 코드 스타일 가이드라인을 설명합니다. 새로운 도메인 기능을 추가할 때 이 가이드라인을 따라주세요.

## 1. 계층형 아키텍처 (Layered Architecture)

본 프로젝트는 일반적인 계층형 아키텍처를 따르며, 각 계층은 명확한 책임과 역할을 가집니다. 패키지 구조를 통해 계층을 구분합니다.

- **`interfaces`**: 외부 세계와의 상호작용을 담당합니다. (예: REST API Controller)
- **`application`**: `interfaces`와 `domain` 계층을 연결하고, 트랜잭션 관리 등 애플리케이션의 흐름을 제어합니다.
- **`domain`**: 핵심 비즈니스 로직과 도메인 모델을 포함합니다.
- **`infrastructure`**: 데이터베이스 연동, 외부 시스템 호출 등 기술적인 구현을 담당합니다.

### 1.1. 패키지 구조

하나의 도메인(`example`)은 각 계층에 걸쳐 다음과 같은 패키지 구조를 가집니다.

```
com.loopers
├── interfaces.api.example
│   ├── ExampleV1ApiSpec.java
│   ├── ExampleV1Controller.java
│   └── ExampleV1Dto.java
├── application.example
│   ├── ExampleFacade.java
│   └── ExampleInfo.java
├── domain.example
│   ├── ExampleModel.java
│   ├── ExampleRepository.java
│   └── ExampleService.java
└── infrastructure.example
    ├── ExampleJpaRepository.java
    └── ExampleRepositoryImpl.java
```

## 2. 클래스별 역할과 책임 및 코드 스타일

### 2.1. `interfaces` 계층

- **`ExampleV1Controller.java`**: 
    - 역할: REST API 엔드포인트를 정의하고, HTTP 요청을 받아 처리합니다.
    - 책임: 요청 파라미터 유효성 검사, `application` 계층으로 요청 전달, 결과(DTO)를 `ApiResponse`로 감싸 반환합니다.
    - 스타일:
        - `@RestController`, `@RequestMapping` 어노테이션을 사용합니다.
        - 생성자 주입을 위해 `@RequiredArgsConstructor`를 사용합니다.
        - API 명세 인터페이스(`ExampleV1ApiSpec`)를 구현합니다.
    ```java
    @RequiredArgsConstructor
    @RestController
    @RequestMapping("/api/v1/examples")
    public class ExampleV1Controller implements ExampleV1ApiSpec {

        private final ExampleFacade exampleFacade;

        @GetMapping("/{exampleId}")
        @Override
        public ApiResponse<ExampleV1Dto.ExampleResponse> getExample(
            @PathVariable(value = "exampleId") Long exampleId
        ) {
            ExampleInfo info = exampleFacade.getExample(exampleId);
            ExampleV1Dto.ExampleResponse response = ExampleV1Dto.ExampleResponse.from(info);
            return ApiResponse.success(response);
        }
    }
    ```
- **`ExampleV1Dto.java`**: 
    - 역할: API 요청(Request) 및 응답(Response)에 사용되는 데이터 전송 객체(DTO)를 정의합니다.
    - 책임: `record` 타입을 사용하여 불변 객체로 정의하고, `application` 계층의 `Info` 객체로부터 DTO를 생성하는 정적 팩토리 메서드(`from`)를 제공합니다.
    - 스타일:
        - 외부 클래스(`ExampleV1Dto`) 안에 static `record`로 요청/응답 DTO를 정의하여 관련된 DTO들을 그룹화합니다.
        - `record`를 사용하여 `getter`, `equals`, `hashCode`, `toString`을 자동으로 생성합니다.
    ```java
    public class ExampleV1Dto {
        public record ExampleResponse(Long id, String name, String description) {
            public static ExampleResponse from(ExampleInfo info) {
                return new ExampleResponse(
                    info.id(),
                    info.name(),
                    info.description()
                );
            }
        }
    }
    ```
- **`ExampleV1ApiSpec.java`**: 
    - 역할: API 명세를 정의하는 인터페이스입니다. (Swagger/OpenAPI)
    - 책임: `@Tag`, `@Operation` 등 어노테이션을 사용하여 API 문서를 명확하게 기술합니다. `Controller`는 이 인터페이스를 구현합니다.
    - 스타일:
        - `@Tag`로 API 그룹을 정의하고, `@Operation`으로 각 API의 요약과 설명을 추가합니다.
        - 파라미터에는 `@Schema`를 사용하여 상세 설명을 추가합니다.
    ```java
    @Tag(name = "Example V1 API", description = "Loopers 예시 API 입니다.")
    public interface ExampleV1ApiSpec {

        @Operation(
            summary = "예시 조회",
            description = "ID로 예시를 조회합니다."
        )
        ApiResponse<ExampleV1Dto.ExampleResponse> getExample(
            @Schema(name = "예시 ID", description = "조회할 예시의 ID")
            Long exampleId
        );
    }
    ```

### 2.2. `application` 계층

- **`ExampleFacade.java`**: 
    - 역할: `interfaces`와 `domain` 계층을 연결하는 퍼사드(Facade)입니다.
    - 책임: `domain` 계층의 여러 서비스를 조합하여 하나의 비즈니스 유스케이스를 완성하고, 그 결과를 `Info` 객체로 변환하여 반환합니다.
    - 스타일:
        - `@Component` 또는 `@Service` 어노테이션을 사용합니다.
        - `@RequiredArgsConstructor`를 통한 생성자 주입을 사용합니다.
    ```java
    @RequiredArgsConstructor
    @Component
    public class ExampleFacade {
        private final ExampleService exampleService;

        public ExampleInfo getExample(Long id) {
            ExampleModel example = exampleService.getExample(id);
            return ExampleInfo.from(example);
        }
    }
    ```
- **`ExampleInfo.java`**: 
    - 역할: `application` 계층과 `interfaces` 계층 사이에서 데이터를 전달하는 데 사용되는 객체입니다.
    - 책임: `domain` 계층의 `Model` 객체로부터 `Info` 객체를 생성하는 정적 팩토리 메서드(`from`)를 제공합니다. `record` 타입을 사용하여 불변성을 유지합니다.
    - 스타일:
        - `record`를 사용하여 불변 데이터 객체를 간결하게 표현합니다.
        - `Model`을 `Info`로 변환하는 정적 팩토리 메서드 `from`을 제공합니다.
    ```java
    public record ExampleInfo(Long id, String name, String description) {
        public static ExampleInfo from(ExampleModel model) {
            return new ExampleInfo(
                model.getId(),
                model.getName(),
                model.getDescription()
            );
        }
    }
    ```

### 2.3. `domain` 계층

- **`ExampleService.java`**: 
    - 역할: 핵심 비즈니스 로직을 수행합니다.
    - 책임: 도메인 모델(`ExampleModel`)을 사용하여 비즈니스 규칙을 처리합니다. 트랜잭션 경계는 이 계층에서 설정하는 것을 권장합니다. (`@Transactional`)
    - 스타일:
        - `@Service` 또는 `@Component` 어노테이션을 사용합니다.
        - `@RequiredArgsConstructor`를 통한 생성자 주입을 사용합니다.
        - 조회 메서드에는 `@Transactional(readOnly = true)`를 사용하여 성능을 최적화합니다.
    ```java
    @RequiredArgsConstructor
    @Component
    public class ExampleService {

        private final ExampleRepository exampleRepository;

        @Transactional(readOnly = true)
        public ExampleModel getExample(Long id) {
            return exampleRepository.find(id)
                .orElseThrow(() -> new CoreException(ErrorType.NOT_FOUND, "[id = " + id + "] 예시를 찾을 수 없습니다."));
        }
    }
    ```
- **`ExampleModel.java`**: 
    - 역할: 도메인의 핵심 데이터와 비즈니스 행위를 가지는 객체(JPA Entity)입니다.
    - 책임: 객체의 일관성을 유지하기 위한 유효성 검사 로직을 생성자나 메서드 내에 포함합니다. (예: `name`은 비어있을 수 없다는 규칙)
    - 스타일:
        - `@Entity` 어노테이션으로 JPA 엔티티임을 명시합니다.
        - `protected` 기본 생성자를 두어 JPA의 프록시 생성을 지원합니다.
        - 생성자와 비즈니스 메서드 내에서 `Guard Clause`를 사용하여 유효성 검사를 수행하고, 실패 시 `CoreException`을 발생시킵니다.
    ```java
    @Entity
    @Table(name = "example")
    public class ExampleModel extends BaseEntity {

        private String name;
        private String description;

        protected ExampleModel() {}

        public ExampleModel(String name, String description) {
            if (name == null || name.isBlank()) {
                throw new CoreException(ErrorType.BAD_REQUEST, "이름은 비어있을 수 없습니다.");
            }
            if (description == null || description.isBlank()) {
                throw new CoreException(ErrorType.BAD_REQUEST, "설명은 비어있을 수 없습니다.");
            }

            this.name = name;
            this.description = description;
        }

        // ... getters and other business methods
    }
    ```
- **`ExampleRepository.java`**: 
    - 역할: `domain` 계층이 `infrastructure` 계층에 의존하지 않도록 추상화된 리포지토리 인터페이스입니다. (의존성 역전 원칙, DIP)
    - 책임: `ExampleModel`의 영속성을 처리하기 위한 메서드를 정의합니다. (예: `find`, `save`)
    - 스타일:
        - 특정 기술에 종속되지 않는 순수한 Java 인터페이스로 작성합니다.
        - `Optional`을 사용하여 조회 결과가 없을 수 있음을 명시적으로 표현합니다.
    ```java
    public interface ExampleRepository {
        Optional<ExampleModel> find(Long id);
    }
    ```

### 2.4. `infrastructure` 계층

- **`ExampleRepositoryImpl.java`**: 
    - 역할: `domain.ExampleRepository` 인터페이스의 구현체입니다.
    - 책임: Spring Data JPA, QueryDSL 등 특정 데이터 접근 기술을 사용하여 실제 데이터베이스 작업을 수행합니다.
    - 스타일:
        - `@Repository` 또는 `@Component` 어노테이션을 사용합니다.
        - `@RequiredArgsConstructor`를 통한 생성자 주입을 사용합니다.
        - `domain`의 리포지토리 인터페이스를 구현합니다.
    ```java
    @RequiredArgsConstructor
    @Component
    public class ExampleRepositoryImpl implements ExampleRepository {
        private final ExampleJpaRepository exampleJpaRepository;

        @Override
        public Optional<ExampleModel> find(Long id) {
            return exampleJpaRepository.findById(id);
        }
    }
    ```
- **`ExampleJpaRepository.java`**: 
    - 역할: Spring Data JPA가 제공하는 리포지토리 인터페이스입니다.
    - 책임: `JpaRepository`를 상속받아 기본적인 CRUD 메서드를 제공받습니다.
    - 스타일:
        - `JpaRepository<EntityType, IdType>`를 상속받습니다.
        - 필요한 경우 쿼리 메서드를 추가로 정의할 수 있습니다.
    ```java
    public interface ExampleJpaRepository extends JpaRepository<ExampleModel, Long> {}
    ```

## 3. 에러 처리 전략

- **`CoreException`**: 비즈니스 로직에서 발생하는 예외는 `CoreException`을 사용합니다. `ErrorType`과 커스텀 메시지를 가질 수 있습니다.
- **`ApiControllerAdvice`**: `@RestControllerAdvice`를 사용하여 전역적으로 예외를 처리합니다.
    - `CoreException`을 받아서 `ApiResponse.fail` 형태로 변환하여 클라이언트에게 일관된 에러 응답을 제공합니다.
    - `MethodArgumentTypeMismatchException`, `HttpMessageNotReadableException` 등 Spring의 기본 예외들도 처리하여 사용자 친화적인 에러 메시지를 반환합니다.
    ```java
    @RestControllerAdvice
    @Slf4j
    public class ApiControllerAdvice {
        @ExceptionHandler
        public ResponseEntity<ApiResponse<?>> handle(CoreException e) {
            log.warn("CoreException : {}", e.getCustomMessage() != null ? e.getCustomMessage() : e.getMessage(), e);
            return failureResponse(e.getErrorType(), e.getCustomMessage());
        }

        // ... other exception handlers

        private ResponseEntity<ApiResponse<?>> failureResponse(ErrorType errorType, String errorMessage) {
            return ResponseEntity.status(errorType.getStatus())
                .body(ApiResponse.fail(errorType.getCode(), errorMessage != null ? errorMessage : errorType.getMessage()));
        }
    }
    ```

## 4. 테스트 전략 및 매칭

각 계층의 역할에 맞는 테스트를 작성하여 코드의 안정성을 보장합니다.

- **단위 테스트 (Unit Test)**
    - **대상**: `domain.ExampleModel`
    - **목표**: 외부 의존성 없이 순수 비즈니스 로직(유효성 검사 등)을 테스트합니다.
    - **파일명**: `ExampleModelTest.java`
    - **스타일**:
        - `@DisplayName`, `@Nested`를 사용하여 테스트 구조를 명확하게 표현합니다.
        - `assertAll`을 사용하여 여러 검증을 그룹화합니다.
    ```java
    class ExampleModelTest {
        @DisplayName("예시 모델을 생성할 때, ")
        @Nested
        class Create {
            @DisplayName("제목과 설명이 모두 주어지면, 정상적으로 생성된다.")
            @Test
            void createsExampleModel_whenNameAndDescriptionAreProvided() {
                // arrange
                String name = "제목";
                String description = "설명";

                // act
                ExampleModel exampleModel = new ExampleModel(name, description);

                // assert
                assertAll(
                    () -> assertThat(exampleModel.getId()).isNotNull(),
                    () -> assertThat(exampleModel.getName()).isEqualTo(name),
                    () -> assertThat(exampleModel.getDescription()).isEqualTo(description)
                );
            }
            // ...
        }
    }
    ```

- **통합 테스트 (Integration Test)**
    - **대상**: `domain.ExampleService`
    - **목표**: `Service`가 `Repository` 등 다른 컴포넌트와 올바르게 상호작용하는지 검증합니다.
    - **파일명**: `ExampleServiceIntegrationTest.java`
    - **스타일**:
        - `@SpringBootTest`를 사용하여 스프링 컨텍스트를 로드합니다.
        - `@Autowired`로 테스트에 필요한 빈을 주입받습니다.
        - `@AfterEach`와 `DatabaseCleanUp`을 사용하여 테스트 간 격리를 보장합니다.
    ```java
    @SpringBootTest
    class ExampleServiceIntegrationTest {
        @Autowired
        private ExampleService exampleService;

        @Autowired
        private ExampleJpaRepository exampleJpaRepository;

        @Autowired
        private DatabaseCleanUp databaseCleanUp;

        @AfterEach
        void tearDown() {
            databaseCleanUp.truncateAllTables();
        }

        // ... test methods
    }
    ```

- **E2E 테스트 (End-to-End Test)**
    - **대상**: `interfaces.api.ExampleV1Controller`
    - **목표**: 실제 API 요청부터 응답까지 전체 흐름을 테스트합니다.
    - **파일명**: `ExampleV1ApiE2ETest.java`
    - **스타일**:
        - `@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)`를 사용합니다.
        - `TestRestTemplate`을 사용하여 실제 HTTP 요청을 보냅니다.
        - `ParameterizedTypeReference`를 사용하여 제네릭을 포함한 응답을 받습니다.
    ```java
    @SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
    class ExampleV1ApiE2ETest {

        private final TestRestTemplate testRestTemplate;
        // ...

        @DisplayName("GET /api/v1/examples/{id}")
        @Nested
        class Get {
            @DisplayName("존재하는 예시 ID를 주면, 해당 예시 정보를 반환한다.")
            @Test
            void returnsExampleInfo_whenValidIdIsProvided() {
                // arrange
                ExampleModel exampleModel = exampleJpaRepository.save(/* ... */);
                String requestUrl = "/api/v1/examples/" + exampleModel.getId();

                // act
                ParameterizedTypeReference<ApiResponse<ExampleV1Dto.ExampleResponse>> responseType = new ParameterizedTypeReference<>() {};
                ResponseEntity<ApiResponse<ExampleV1Dto.ExampleResponse>> response =
                    testRestTemplate.exchange(requestUrl, HttpMethod.GET, null, responseType);

                // assert
                // ...
            }
        }
    }
    ```

## 5. 재현을 위한 프로세스

1.  새로운 도메인(예: `product`)에 대한 기능을 추가할 경우, 위 패키지 구조에 따라 각 계층에 `product` 패키지를 생성합니다.
2.  각 클래스의 역할과 책임, 코드 스타일에 맞게 `ProductController`, `ProductDto`, `ProductFacade`, `ProductInfo`, `ProductService`, `ProductModel`, `ProductRepository` 등을 작성합니다.
3.  각 클래스에 매칭되는 테스트 코드를 위 테스트 전략에 따라 작성합니다. (`ProductModelTest`, `ProductServiceIntegrationTest`, `ProductApiE2ETest`)
4.  의존성 주입은 생성자 주입(`@RequiredArgsConstructor`)을 사용하고, 각 클래스는 역할에 맞는 어노테이션(`@RestController`, `@Service`, `@Repository` 등)을 사용합니다.
5.  비즈니스 예외는 `CoreException`을, 전역 예외 처리는 `ApiControllerAdvice`를 활용합니다.
