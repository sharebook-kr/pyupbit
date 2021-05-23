EXCHANGE API
======================
 
업비트에서 API 신청 후 사용할 수 있는 API 입니다. 주문, 출금, 입금, 자산 조회가 가능합니다.  

자산
----------------------
전체 계좌 조회 
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

    import pyupbit 

    access = "access key"  
    secret = "secret key"
    upbit = Upbit(access, secret)

    balance = upbit.get_balances()
    print(balance)


주문
----------------------
주문 가능 정보
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

개별 주문 조회 
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

주문 리스트 조회
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

주문 취소 접수
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

주문하기 
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python


출금
----------------------
출금 리스트 조회
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python


개별 출금 조회 
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

출금 가능 정보 
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

코인 출금하기
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

원화 출금하기 
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

입금
----------------------
입금 리스트 조회
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python


개별 입금 조회 
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

입금 주소 생성 요청 
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

전체 입금 주소 조회  
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

개별 입금 주소 조회 
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

원화 입금하기 
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

서비스 정보
----------------------
입출금 현황
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

API 키 리스트 조회
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python
