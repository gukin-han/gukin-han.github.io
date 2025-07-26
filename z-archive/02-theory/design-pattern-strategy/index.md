# Design Pattern Strategy

## 전략 + 지연(Lazy) 파라미터

```java
// ① 전략 정의 — <C, R> : Context 타입과 반환 타입
@FunctionalInterface
public interface Strategy<C extends AlgorithmContext, R> {
    R execute(C context);
}

// ② 공통 컨텍스트 — 최소한의 마커용
public interface AlgorithmContext { }

// ③ 지연값 래퍼 (필요하면 Guava Suppliers.memoize()도 사용 가능)
public final class Lazy<T> implements Supplier<T> {
    private final Supplier<T> delegate;
    private T cached;
    private boolean evaluated = false;

    private Lazy(Supplier<T> delegate) { this.delegate = delegate; }

    public static <T> Lazy<T> of(Supplier<T> supplier) {
        return new Lazy<>(supplier);
    }

    @Override public synchronized T get() {
        if (!evaluated) {
            cached = delegate.get();
            evaluated = true;
        }
        return cached;
    }
}
```

### 2-A. 예시 컨텍스트 1 – FastAlgoContext

```java
public record FastAlgoContext(int a, int b) implements AlgorithmContext { }
```

### 2-B. 예시 컨텍스트 2 – HeavyAlgoContext (지연값 포함)

```java
public record HeavyAlgoContext(
        int iterations,
        Lazy<Double> exchangeRate,     // ❶ 지연 계산
        Lazy<List<BigDecimal>> rawData // ❷ 대용량 데이터
) implements AlgorithmContext { }
```


### 2-C. 전략 구현 두 가지

```java
// 빠른 알고리즘 — 모든 파라미터 즉시 사용
public class FastAlgo implements Strategy<FastAlgoContext, Integer> {
    @Override
    public Integer execute(FastAlgoContext ctx) {
        return ctx.a() + ctx.b();
    }
}

// 무거운 알고리즘 — 지연값을 ‘필요할 때’만 꺼내 씀
public class HeavyAlgo implements Strategy<HeavyAlgoContext, BigDecimal> {
    @Override
    public BigDecimal execute(HeavyAlgoContext ctx) {
        double rate = ctx.exchangeRate().get();         // 여기서만 평가
        List<BigDecimal> data = ctx.rawData().get();    // 역시 한 번만 평가
        return data.stream()
                   .reduce(BigDecimal.ZERO, (acc, d) -> acc.add(d.multiply(BigDecimal.valueOf(rate))));
    }
}
```

### 2-D. 클라이언트 / 컨텍스트 조립

```java
public class AlgoExecutor {
    public static void main(String[] args) {
        // 1) 즉시 수행하는 예
        Strategy<FastAlgoContext, Integer> fast = new FastAlgo();
        int result1 = fast.execute(new FastAlgoContext(3, 7));

        // 2) Heavy 예 — Supplier 안에 ‘진짜로 무거운’ 로직 캡슐화
        HeavyAlgoContext heavyCtx = new HeavyAlgoContext(
            1_000_000,
            Lazy.of(() -> fetchExchangeRateFromRemote()),          // API 호출
            Lazy.of(() -> loadBigCsv("/huge.csv"))                 // 파일 읽기
        );
        Strategy<HeavyAlgoContext, BigDecimal> heavy = new HeavyAlgo();
        BigDecimal result2 = heavy.execute(heavyCtx);
    }
}
```

### 확장 & 실전 팁

- DTO 수 많아질 때
   - 공통 필드를 BaseContext 로 묶고 전략별 extends 로 세분화.
   - 혹은 제네릭 + sealed interface(Java 21) 로 컴파일 타임 검증.
- 지연 요청 취소/타임아웃
   - CompletableFuture<T> 를 Supplier 안에서 사용한 뒤 .get(timeout)으로 제어.
- DI 프레임워크 활용
   - Spring + @Component 스캔 후 Map<String, Strategy> 주입으로 런타임 선택.
- 테스트
   - Supplier 안에서는 사이드 이펙트 최소화, Mockito로 Supplier 목 주입 가능.
- 읽기 편한 코드
   - Lazy<Double> rate = Lazy.of(this::expensiveCall) 형식으로 builder 패턴과 함께 쓰면 가독성↑.

