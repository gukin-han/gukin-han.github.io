# Java Spring Security

## `addFilterBefore` + 수동등록

- 필터는 Spring Security Chain의 순서가 중요하지만 `@Component` 로 자동등록 시에 순서 제어가 불가능
- SecurityConfig에서 명시적으로 보여주는것이 실무에 적합
- 설정값(environment, secret)은 대부분 application.yml에서 주입받는데, SecurityConfig가 그런 설정을 쉽게 관리할 수 있는 좋은 위치

### application.yml

```yaml
jwt:
  secret: my-secret-key
```

### JwtTokenFilter

```java
public class JwtTokenFilter extends OncePerRequestFilter {

    private final String secretKey;
    private final Key SECRET_KEY;

    public JwtTokenFilter(String secretKey) {
        this.secretKey = secretKey;
        this.SECRET_KEY = new SecretKeySpec(
                java.util.Base64.getDecoder().decode(secretKey),
                SignatureAlgorithm.HS512.getJcaName());
    }

    // doFilterInternal 그대로
}
```

- 빈으로 등록하지 않고 POJO로 유지

### SecurityConfig

```java
import org.springframework.beans.factory.annotation.Value;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Value("${jwt.secret}")
    private String secretKey;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {

        JwtTokenFilter jwtTokenFilter = new JwtTokenFilter(secretKey);

        http
            .csrf().disable()
            .authorizeHttpRequests()
                .anyRequest().authenticated()
            .and()
            .addFilterBefore(jwtTokenFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
```

- 단순한 자바 객체로 넘겨도 괜찮다
