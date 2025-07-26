# Java Spring AOP

## 핵심 비즈니스 로직

```java
@Service
public class SimpleService {
    public void sayHello() {
        System.out.println("안녕하세요! 저는 스프링 서비스입니다.");
    }
}
```


## AOP 클래스

```java
@Aspect
@Component
public class LoggingAspect {

    // SimpleService의 모든 메서드 실행 전후로 동작
    @Around("execution(* com.example.demo.SimpleService.*(..))")
    public Object logAround(ProceedingJoinPoint joinPoint) throws Throwable {
        System.out.println("[AOP] 메서드 실행 전: " + joinPoint.getSignature().getName());

        Object result = joinPoint.proceed(); // 실제 메서드 실행

        System.out.println("[AOP] 메서드 실행 후: " + joinPoint.getSignature().getName());

        return result;
    }
}
```

- `@Around`가 InvocationHandler 역할을 대신한다
- `ProceedingJoinPoint.proceed()` 호출 = 실제 메서드 실행


## AOP 활성화

```java
@SpringBootApplication
@EnableAspectJAutoProxy
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

- `@EnableAspectJAutoProxy` -> Spring에게 프록시 사용