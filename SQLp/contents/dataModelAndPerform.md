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

- #### 조인 (JOIN)

- #### 정리

</br>



### **2 . SQL 활용** 


- #### 표준 조인 (STANDARD JOIN)


- #### 집합 연산자 (SET OPERATOR)

- #### 계층형 질의와 셀프 조인

- #### 서브쿼리

- #### 그룹함수 (GROUP FUNCTION)

- #### 윈도우 함수 (WINDOW FUNCTION)

- #### DCL (DATA CONTROL LANGUAGE)

- #### 절차형 SQL
- #### 정리



</br>






### **3 . 최적화 기본 원리** 


- #### 옵티마이저와 실행 계획

- #### 인덱스 기본

- #### 조인 수행 원리 

- #### 정리

