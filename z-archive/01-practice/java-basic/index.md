# Java Basic

## static

### 인스턴스 vs. 클래스를 통한 static 변수 접근- [Java Basic](#java-basic)

```java
public class Data3 {
    public String name;
    public static int count; // static

    public Data3(String name) {
        this.name = name;
//        Data3.count++; // Data3 생략가능
        Data3.count++;
    }
}
```

```java
//추가
//인스턴스를 통한 접근
Data3 data4 = new Data3("D");
System.out.println(data4.count);
//클래스를 통합 접근
System.out.println(Data3.count);
```

- 둘다 결과적으로 정적 변수에 접근 가능
- 비교
  - `data4.count` : (비추천) 인스턴스 변수에 접근하는것 처럼 오해할 수 있기 때문
  - `Data3.count` : (추천) 클래스 통해서 접근하는 것이 더 명확
