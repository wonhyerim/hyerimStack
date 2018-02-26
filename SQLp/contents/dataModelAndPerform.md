![logo](../../image/logo.png)



# SQLp - 국가공인 SQL 전문가 

   

###  **INDEX**

- #### 과목 1 - 데이터 모델링의 이해

  - ##### 데이터 모델링의 이해

  - ##### 데이터 모델과 성능

  ​


- #### *과목 2 - SQL 기본 및 활용*

  - ##### SQL 기본

  - ##### SQL 활용

  - ##### SQL 최적화 기본 원리

  ​


- #### 과목 3 - SQL 고급 활용 튜닝

  - ##### 아키텍처 기반 튜닝 원리

  - ##### Lock 과 트랜잭션 동시성 제어

  - ##### 옵티마이저 원리

  - ##### 인덱스와 조인

  - ##### 고급 SQL 튜닝


</br></br></br></br>

----




## **과목 2 - SQL 기본 및 활용**

</br>


### **1 . SQL 기본**  


### **1 . 데이터 모델링의 이해**  

- #### 관계형데이터베이스 개요
  1. SQL 의 종류
  
  - 데이터 조작어 (Data Manipulation Language)
  
    + SELECT , INSERT , UPDATE , DELETE 

  - 데이터 정의어 (Data Definition Language)
    + CREATE , ALTER , DROP, RENAME

  - 데이터 제어어 (Data Control Language)
    + GRANT, REVOKE

  - 트랜잭션 제어어 (Transaction Control Language)
    + COMMIT, ROLLBACK
    

- #### DDL (DATA DEFINITION LANGUAGE)
1. CREATE TABLE 

  - 구문 형식
    + 예시
     ~~~
      CREATE TABLE 테이블명 (
      
        칼럼명1 DATATYPE [DEFALT] [NOT NULL], 
        칼럼명2 DATATYPE [DEFALT], 
        칼럼명3 DATATYPE [DEFALT], 

        CONSTRAINT 제약조건명 PRIMARY KEY (칼럼명),
        CONSTRAINT 제약조건명 FOREIGN KEY (칼럼명) REFERENCES 테이블명 (칼럼명)
        
      );
    ~~~
    
    + 예약어는 사용할 수 없고 각각의 컬럼은 계층적 구조를 가진 전체 경로로 관리한다. 

  
  - 생성된 테이블 구조 확인  

    + ORACLE
     ~~~
      DESCRIBE 테이블명; 
        OR
      DESC 테이블명;
    ~~~
  
    + SQL Server
     ~~~
      exec sp_help 'dbo.테이블명'
      go    
    ~~~
  
    

  
  - CTAS : SELECT 를 이용한 테이블 생성  
           NOT NULL만 적용되고 다른 제약조건은 없어짐
    + ORACLE
     ~~~
      CREATE TABLE 테이블명 AS SELECT * FROM 테이블명 ;
    ~~~
  
    + SQL Server : Identity 속성도 적용
     ~~~
      SELECT * INTO 테이블명 FROM 테이블명     
    ~~~
  
    

2. ALTER TABLE 

  - ADD / DROP COLUMN 

    + 예시
    ~~~~
      ALTER TABLE 테이블명
      ADD 칼럼명 데이터 유형;
        -> ORACLE의 경우 (칼럼명 데이터유형)

      ALTER TABLE 테이블명
      DROP COLUMN 칼럼명 ; 
    ~~~~

    + 추가한 컬럼은 마지막에 위치하며 순서를 바꿀 수는 없다. 
 
  - MODIFY COLUMN

    + ORACLE
    ~~~
      ALTER TABLE 테이블명
      MODIFY (칼럼명 데이터유형 [DEFAULT] [NOT NULL], ...);
    ~~~
  
    + SQL Server
    ~~~
      ALTER TABLE 테이블명
      ALTER (칼럼명 데이터유형 [DEFAULT] [NOT NULL], ...);
    ~~~
  
    + NULL 값, 혹은 테이블에 아무 행도 없으면 칼럼의 크기를 줄일 수 있다. (데이터 타입 변경도 가능)
    
    + DEFAULT는 변경 이후에 데이터에만 반영

 - RENAME COLUMN

    + ORACLE
    ~~~
      ALTER TABLE 테이블명
      RENAME COLUMN 칼럼명  TO 칼럼명;
    ~~~
  
    + SQL Server
    ~~~
      sp_rename 전 칼럼명, 후 칼럼명, 'COLUMN';
    ~~~

    + 스크립트 및 저장 프로시저를 손상시킬 수 있다.  


 - DROP CONSTRAINT

    + 예시
    ~~~
      ALTER TABLE 테이블명
      DROP CONSTRAINT 제약조건명;
    ~~~

 - ADD CONSTRAINT

    + 예시
    ~~~
      ALTER TABLE 테이블명
      ADD CONSTRAINT 제약조건명 제약조건 (칼럼명);
    ~~~
  


3. RENAME /DROP / TRUNCATE TABLE 

  - RENAME TABLE
    + ORACLE
    ~~~
      RENAME 테이블명 TO 테이블명 ; 
    ~~~
  
    + SQL Server
    ~~~
      sp_rename 'dbo.전 테이블명' , 'dbo.후 테이블명'
      ~~~
  

  - DROP TABLE 

    + ORACLE
    ~~~
      DROP TABLE 테이블명 [CASCADE CONSTRAINT];
    ~~~
  
    + SQL Server
    ~~~
      DROP TABLE 테이블명;
    ~~~



  - TRUNCATE TABLE 
    + 예시
    ~~~
      TRUNCATE TABLE 테이블명 ;
    ~~~

    + 모든 행들이 제거, 저장 공간 재사용 가능

    + DELETE 문보다 시스템 부하는 적지만 정상적인 복구 불가능


**다음 설명부터는 불필요한 예제를 줄일 예정이다.**

- #### DML (DATA MANIPULATION LANGUAGE)
  1. DML 

    - INSERT / UPDATE / DELETE / SELECT 등이 있다.

    - DML 의 특징
      + DML은 입력 후에 COMMIT을 입력해야 한다. (SQL server 의 경우 auto commit)
      + 테이블 전체 데이터를 삭제하는 DELETE 는 전체 데이터의 로그를 저장하기 떄문에 TRUNCATE TABLE 권고 

    - SELECT 
      + DISTICT , ALL 명령어 사용 가능 (중복 데이터 조회 여부 결정)
      + ALIAS 를 통해 별명 지정 가능
      + 합성연산자로 오라클은 '||' , SQL Server 는 '+' 를 사용한다.



- #### TCL (TRANSACTION CONTROL LANGUAGE)
  1. 트랜잭션
  - 트랜잭션의 특성
    + 원자성 : 쪼갤 수 없는 최소 단위이다
    + 일관성
    + 고립성
    + 지속성

  - 트랜잭션의 종류
    + AUTO COMMIT : 일부 ORACLE 혹은 SQL Server 의 기본 옵션, 자동으로 COMMIT, ROLLBACK 실행

    + 암시적 트랜잭션 : 시작은 DBMS가 끝은 사용자 명령어로 트랜잭션 제어
    
    + 명시적 트랜잭션 : 시작과 끝을 모두 명시적으로 지정
  
  ***트랜잭션 제어를 통해 무결성 보장 가능***


- #### WHERE 절
  1. 연산자

    - 우선순위 
      
      + () -> NOT -> 비교 연산자 -> AND -> OR

    - NULL 값
      + NULL 과의 수치연산 : NULL
      + NULL 과의 비교연산 : FALSE

    - ROWNUM (오라클) != TOP(SQL Server)
      



- #### 함수 (FUNCTION)
  
  1. 단일행 함수 ( 단일행 값이 입력  / SELECT, WHERE, ORDER BY 절에서 사용 가능)
    - 데이터의 형식에 따라 분류
    
      + 문자형 함수

      + 숫자형 함수
      
      + 날짜형 함수
      
      + 변환형 함수 : 특정 데이터 타입을 다양한 형식으로 출력
        
      + NULL 관련 함수
        NULL 과의 연산은 결과값이 NULL 이기 때문에 NVL/ ISNULL 등과 같은 함수를 사용하는 것이 좋다. 그러나 다중행 함수의 인자일 경우에는 NVL 함수는 불필요한 부하를 발생시킬 수 있다. ( 다중행 함수의 경우엔 전체 건수가 NULL 일때에만 결과가 NULL 이기 때문 )
    2. GROUP BY, HAVING 절
    - GROUP BY 절
      + 데이터들을 작은 그룹으로 분류하여 소그룹에 대한 항목별로 통계 정보를 얻을 때 추가로 사용된다. 

    - 특징
      + 집계함수의 통계 정보는 NULL 값을 가진 행을 제외하고 수행한다. 

      + ALIAS 명을 사용할 수 없다. 

      + WHERE 절에는 올 수 없다. (집계함수를 사용할 수 있는 GROUP BY 절보다 WHERE 절이 먼저 수행된다. ) 

      + GROUP BY 절에 의한 소그룹 별로 만들어진 집계 데이터 중, HAVING 절에서 제한 조건을 두어 조건을 만족하는 내용만 출력한다. 

      + GROUP BY 절에서 그룹 단위를 표시해 주어야 집계 함수를 사용할 수 있다. 

      + FROM -> WHERE -> GROUP BY 순으로 데이터가 걸러지기 떄문에 역으로의 처리나 사용은 못한다.

    3. ORDER BY 절
    -  특정 칼럼을 기준으로 정렬하여 출력하는데 사용된다. 

    - 특징 
      + NULL 값을 Oracle 에서는 가장 큰 값으로 취급하고 SQL Server 에서는 가장 작은 값으로 취급한다. 

      + ORDER BY 절에서는 ALIAS명을 사용할 수 있다.

      + SELECT 절에 없는 칼럼을 사용 할 수 있다. 

      + 집계함수를 사용한 경우 GROUP BY 절에서 사용하지 않은 컬럼을 ORDER BY 절에서 사용할 수 없다. 

      + Oracle 에서는 ROWNUM 조건이 ORDER BY 보다 먼저 실행되기 때문에 ORDER BY 를 사용할 때에는 인라인 뷰에서 먼저 사용해야 한다. SQL Server 에서의 TOP절은 ORDER BY 결과가 그대로 반영된다. 

     4. SELECT 문장실행 순서
        
        1\) FROM

        2\) WHERE

        3\) GROUP BY

        4\) HAVING
        
        5\) SELECT

        6\) ORDER BY


- #### 조인 (JOIN)

  1. EQUI JOIN
    - 칼럼 값들이 서로 정확하게 일치할 때 사용

    - '=' 이나 'INNER JOIN' 사용

  **조인 조건은 적어도 대상 테이블의 개수에서 하나를 뺀 수 만큼이 필요하다.**


  2. NON EQUI JOIN

  - 두 개의 테이블 간에 칼럼 값들이 정확하게 일치하지 않는 경우 사용

    - 'BETWEEN' , '<' , '>' 사용 

  **조인 조건은 정규화를 통해 쪼개진 데이터들의 논리적 연관 관계를 구체적으로 표현한 것이다.**


- #### 정리

</br>



### **2 . SQL 활용** 


- #### 표준 조인 (STANDARD JOIN)
  
  1. 특징
  - INNER JOIN
    + 내부 JOIN 이라고 하며 JOIN 조건에서 동일한 값이 있는 행만 반환한다. 
    + USING, ON 조건절을 필수적으로 사용해야 한다. 
    + 첫 번째 테이블, 두 번째 테이블의 칼럼 순서대로 데이터가 출력된다. 
    + JOIN된 칼럼을 별개의 칼럼으로 처리한다. (출력한다)

  - NATURAL JOIN
    + 동일한 이름을 갖는 모든 칼럼들에 대해 EQUI(=) JOIN 을 수행한다. 
    + 추가로 USING, ON, WHERE 절에서 JOIN 조건을 정의할 수 없다. 
    + JOIN에 사용된 칼럼들은 같은 데이터 유형이어야 하며 ALIAS 나 테이블명과 같은 접두사를 붙일 수 없다. 
    + 별도의 칼럼 순서를 지정하지 않으면 JOIN의 기중니 되는 칼럼들이 먼저 출력된다. 
    

  - USING 조건절
    + FROM 절에서 사용된다. 
    + 같은 이름을 가진 칼럼들 중에서 원하는 칼럼에 대해서만 선택적으로 EQUI JOIN을 할 수 있다. 
    + ALIAS , 테이블 이름과 같은 접두사를 붙일 수 없다. 
    + 기준이 되는 칼럼이 먼저 출력된다. 
    

  - ON 조건절
    + JOIN 서술부와 비 JOIN 서술부인 WHERE 조건절을 분리하여 이해가 쉬우며 칼럼명이 달라도 JOIN조건을 사용할 수 있다. 
    + 임의의 JOIN 조건을 지정하거나 JOIN 칼럼을 명시할 수 있다. 
    + ALIAS 나 테이블 명과 같은 접두사를 사용하여 SELECT 에 사용하는 칼럼을 논리적으로 명확하게 지정해주어야 한다. 
  
  - CROSS JOIN
    + PRODUCT(곱집합) 의 개념으로 테이블 간 JOIN 조건이 없는 경우 생길 수 있는 모든 데이터의 조합
    + WHERE 절에 JOIN 조건을 걸어 INNER JOIN 과 같은 결과를 낼 수 있지만 그러면 CROSS JOIN의 의미가 없다. 
    
  - OUTER JOIN
    + JOIN 조건에서 동일한 값이 없는 행도 반환할 때 사용한다
    + LEFT, RIGHT JOIN 은 기준이 되는 테이블의 데이터(컬럼)는 모두 출력하며 , FULL OUTER JOIN은 합집합과 동일하다. 
    + 중복되는 데이터는 삭제한다는 점에서 UNION 가능과 같다. 

  **FROM 절에서 JOIN 형태는 INNER JOIN, NATURAL JOIN, USING 조건절, ON 조건절, CROSS JOIN, OUTER JOIN 등이 있다.**

- #### 집합 연산자 (SET OPERATOR)
  1. 집합 연산자
    - UNION
      + 합집합으로 중복된 행은 하나의 행으로 만든다.
    
    - UNION ALL
      + 여러 질의 결과가 상호 배타적일 떄 사용한다.
      + 중복 데이터도 그대로 표시한다.

    - INTERSECT
      + 교집합으로써 중복된 행을 하나의 행으로 출력한다. 

    - EXCEPT
      + 결과에 대한 차집합이다.
      + 일부 데이터베이스에서는 MINUS 를 사용한다. 
      + 중복된 행은 하나의 행으로 표시한다. 


- #### 계층형 질의와 셀프 조인
  1. Oracle 계층형 질의
  - 예시
    ~~~
    SELECT ...
    FROM table
    WHERE condition 
    START WITH condition2
    CONNECT BY [NO CYCLE] condition3
    [ORDER SIBLINGS BY column ... ]
    ~~~
    + START WITH 
      계층 구조 전개의 시작 위치를 지정/ 루트 데이터 지정

    + CONNECT BY : 다음에 전개될 자식 데이터를 지정하는 구문
      - CONNECT_BY_ISLEAF : 전개 과정에서 해당 데이터가 리프 데이터면 1 그렇지 않으면 0 반환
      - CONNECT_BY_ISCYCLE : 전개 과정에서 해당 데이터가 조상이면 1 아니면 0 QKSGHKS
      - LEVEL : 루트데이터면 1 하위로 갈수로 1씩 증가
    
    + PRIOR : CONNECT BY 절에서 사용되며 현재 읽은 칼럼을 지정

    + NOCYCLE : 이미 나타났던 데이터가 전개 중에 다시 나타나면 이를 싸이클이 형성되었다고 한다. NOCYCLE은 사이클이 발생한 이후의 데이터는 전개하지 않는다. 

    + ORDER SIBLINGS BY : 형재 노드 사이의 정렬을 수행한다. 

    + WHERE : 전개 후에 지정된 조건을 만족하는 데이터만 추출한다. 

    + SYS_CONNECT_BY_PATH :  루트 데이터부터 현재 데이터 까지의 경로를 표시 한다. 

    + CONNECT_BY_ROOT : 현재 전개할 데이터의 루트 데이터를 표시한다. 

  2. SQL Server 계층형 질의
  - 방법 
    + 쿼리 두개를 결합하여(UNION ALL) 위에 있는 쿼리를 '앵커멤버', 아래에 있는 쿼리를 '재귀멤버' 라고 한다. 

    + 앵커 멤버가 시작점이자 OUTER 집합이 되어 INNER 집합인 재귀 멤버와 조인을 시작한다. 반복하다 더 조인할 수 없으면 결과 집합을 모두 합하여 리턴한다
    
  3. 셀프 조인 
  - 동일 테이블 사이의 조인 
  - 식별을 위해 반드시 별칭을 사용해야 한다. 

- #### 서브쿼리
  1. 서브쿼리 : 메인쿼리가 서브쿼리를 포함하는 종속적인 관계
  - 단일행 서브쿼리 / 다중행 서브쿼리 (반환되는 데이터에 따라)
    + 단일행 서브쿼리 : 실행 결과가 항상 1건 이하인 서브쿼리
       
       Ex ) =, <,>,<>

    + 다중행 서브쿼리 : 실행 결과가 여러개

      Ex) IN, ALL, ANY, SOME, EXISTS
    
    + 다중 칼럼 서브쿼리 : 여러개의 칼럼이 반환되어 메인 쿼리의 조건과 동시에 비교

    
        
  - 비연관 서브쿼리 / 연관 서브쿼리
    + 연관 서브쿼리 : 서브쿼리 내에 메인 칼럼이 사용된 서브쿼리
      
      EXISTS 는 항상 연관 서브쿼리로 사용된다. 

    + 비연관 서브쿼리 : 메인 쿼리에 값을 제공하기 위한 목적으로 주로 사용된다. 

  - SQL 문에서의 서브쿼리 (위치에 따라)
    + SELECT : 스칼라 서브쿼리라고도 한다. 
   
    + FROM : 인라인 뷰 라고도 하며 임시적으로 생성되는 동적인 뷰이다. 
    + WHERE  
    + HAVING : 그룹핑된 결과에 대해 부가적인 조건을 주기 위해 사용된다. 
    + ORDER BY
    + INSERT 의 VALUES 
    + UPDATE 의 SET: 서브쿼리의 결과가 NULL 을 반환할 경우 해당 칼럼의 결과가 NULL이 될수 있음에 주의해야 한다. 

    ***뷰는 단지 뷰 정의만 갖고 있는 가상 테이블로써 독립성, 편리성, 보안성을 장점으로 갖고 있다. ***


- #### 그룹함수 (GROUP FUNCTION)
  1. AGGREGATE FUNCTION
    - COUNT, SUM, AVG, MAX, MIN등 각종 집계함수를 포함한다. 

  2. GROUP FUNCTION
    - ROLLUP : 소그룹 간의 소계를 계산
    - CUBE : GROUP BY 항목들 간 다차원적인 소계를 계산 할 수 있다
    - GROUPING SET : 원하는 소계만 손쉽게 추출 가능

  3. WINDOW FUNCTION 

- #### 윈도우 함수 (WINDOW FUNCTION)
  1. 순위 관련 함수
    - RANK 
      + ORDER BY 를 포함한 특정 항목에 대한 순위를 구하는 함수
     
    - DENSE_RANK 
      + 동일한 순위를 하나의 건수로 취급
   
    - ROW_NUMBER 
      + 동일한 값이라도 고유한 순위를 부여

  2. 집계 관련 함수
      - SUM / MAX / MIN / AVG / COUNT

  3. 행 순서 관련 함수
    - FIRST_VALUE 
      + 파티션 별 윈도우에서 가장 먼저 나온 값

    - LAST_VALUE 
      + 파티션 별 윈도우에서 가장 나중에 나온 값

    - LAG 함수
      + 파티션 별 윈도우에서 이전 몇 번째 행의 값을 가져올 수 있다. 

    - LEAD 함수
      + 윈도우에서 이후 몇 번째 행의 값을 가져올 수 있다.     

  4. 비율 관련 함수
    - RATIO_TO_REPORT
      + SUM 값에 대한 행별 칼럼 값의 백분을을 구할 수 있다. 
    
    - PERCENT_RANK
      + 윈도우에서 제일 먼저 나온 것을 0으로 , 제일 늦게 나온 것을 1로 행의 순서별 백분율을 구한다. 

    - CUME_DIST
      + 파티션 별 윈도우의 전체 건수에서 현재 행보다 작거나 같은 건수에 대한 누적 배분율을 구한다. 

    - NTILE 
      + 파티션 별 전체 건수를 ARGUMENT 값으로 N 등분한 결과를 구할 수 있다.   

  5. 선형 분석을 포함한 통계 분석 함수

- #### DCL (DATA CONTROL LANGUAGE)
  1. 정의 및 특징
    - 유저를 생성하고 권한을 제어 할 수 있음.
    - SYS, SYSTEM, SCOTT 유저가 있음
    - ROLE 을 이용해 권한 부여 
      + 일일히 사용자 별 권한 부여가 아닌 ROLE을 통해 권한을 부여하기 때문에 실수를 방지할 수 있음



- #### 절차형 SQL
  1. Oracle 의 PL/SQL
    - 특징
      + block(DML, QUERY, IF, LOOP 등으로 구성) 구조로 되어 있다. 
      + SQL 문장 간 값을 교환한다.
      + 모듈화가 가능하다
      + 사용자 정의 에러, DBMS 정의 에러를 사용 가능
      + Oracle 에 내장되어 있다. 
      + 응용프로그램 성능을 향상시킨다. 
      + block 을 이용한 통신으로 통신량을 줄일 수 있다. 

   2. SQL Server 의 T-SQL
    - 특징
      + 다양한 저장 모튤을 개발할 수 있다.
      + 지역변수와 전역변수가 있다
      - 데이터 유형, 연산자, 흐름제어, 주석 기능을 제공한다.

   3. 프로시저
    - 프로시저 작성시 주의할 점 
      + 다양한 변수가 존재
      + PL/SQL 에서는 SELECT 결과는 반드시 있어야 하며 대입연산자는 ':='를 사용한다. 
      + 에러를 처리할 때에는 상황을 특정짓는 WHEN THEN 절을 사용하는 것이 좋다. 

    4. 트리거
    - 특징
        + INSERT / UPDATE / DELETE 와 같은 DML 문이 수행될 때 자동으로 동작하도록 하는 프로그램
        + 테이블과 뷰, 데이터베이스 작업을 대상으로 정의가 가능하며 전체 트랜잭션 작업에서 발생하는 트리거, 각 행에 발생하는 트리거가 있다. 
        + 트랜잭션 안에서 일어나는 일련의 작업들
        + 데이터베이스 보안의 적용, 유효하지 않은 트랜잭션 예방, 업무 규칙 작용 제공 등에 사용 가능하다. 
           

- #### 정리



</br>






### **3 . 최적화 기본 원리** 


- #### 옵티마이저와 실행 계획

- #### 인덱스 기본

- #### 조인 수행 원리 

- #### 정리

