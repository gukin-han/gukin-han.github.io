# Java Naming Convention

## find vs. get

- 자바 언어나 스프링이 **강제**하는 컨벤션은 아님
- 다만 다음과 같은 관습이 널리 퍼져 있죠.

1. **getXXX() → 반드시 값을 돌려준다, 없으면 예외를 던진다**

   * 예: `User getUserById(Long id)`

     ```java
     User u = repo.getUserById(999L); // 해당 ID가 없으면 곧바로 NotFoundException
     ```
   * 장점: 호출하는 쪽에서는 “반드시 있다”를 전제하고 흐름을 구성할 수 있음.
   * 단점: 예외를 던지는 지점을 찾기 어렵고, 비즈니스 로직에서 흐름 제어용으로 예외를 과도하게 쓰기 쉽다.

2. **findXXX() → 값이 있으면 반환, 없으면 Optional.empty() 또는 null**

   * 예: `Optional<User> findUserById(Long id)`

     ```java
     repo.findUserById(999L)
         .ifPresentOrElse(user -> doSomething(user),
                          ()     -> log.warn("사용자 없음"));
     ```
   * 장점: 호출 쪽에서 “없을 수도 있다”를 명확히 처리하도록 강제.
   * 단점: 매번 `isPresent()`/`orElseThrow()`/`orElse()` 등을 처리해야 하는 번거로움.




