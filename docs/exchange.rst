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

마켓별 주문 가능 정보를 확인한다. 

..  code-block:: python

    import pyupbit 

    access = "access key"  
    secret = "secret key"
    upbit = Upbit(access, secret)

    chance = upbit.get_chance("KRW-BTC")
    print(chance)


개별 주문 조회 
~~~~~~~~~~~~~~~~~~~~~~

주문 UUID 를 통해 개별 주문건을 조회한다.

..  code-block:: python

주문 리스트 조회
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

주문 취소 접수
~~~~~~~~~~~~~~~~~~~~~~

주문 UUID 를 통해 개별 주문건을 취소한다. 

..  code-block:: python

    import pyupbit 

    access = "access key"  
    secret = "secret key"
    upbit = Upbit(access, secret)

    uuid = "uuid"  # 취소하고자하는 주문의 uuid
    cancel_result = upbit.cancel_order(uuid)
    print(cancel_result)


주문하기 
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python


출금
----------------------
출금 리스트 조회
~~~~~~~~~~~~~~~~~~~~~~

출금 리스트를 조회한다.

..  code-block:: python

    import pyupbit 

    access = "access key"  
    secret = "secret key"
    upbit = Upbit(access, secret)

    currency = "KRW"    # 조회하려는 화폐 정보
    withdraw_list = upbit.get_withdraw_list(currency)
    print(withdraw_list)

개별 출금 조회 
~~~~~~~~~~~~~~~~~~~~~~

출금 UUID 를 통해 개별 출금건을 조회한다. 출금 UUID 는 출금 리스트 조회를 통해 확인할 수 있다.

..  code-block:: python
    import pyupbit 

    access = "access key"  
    secret = "secret key"
    upbit = Upbit(access, secret)

    uuid = "uuid"       # 조회하려는 출금 UUID
    currency = "KRW"    # 조회하려는 화폐 정보
    withdraw_order_info = upbit.get_individual_withdraw_order(uuid, currency)
    print(withdraw_order_info)


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

입금 리스트를 조회한다.

..  code-block:: python
    import pyupbit 

    access = "access key"  
    secret = "secret key"
    upbit = Upbit(access, secret)

    currency = "KRW"    # 조회하려는 화폐 정보
    deposit_list = upbit.get_deposit_list(currency)
    print(deposit_list)


개별 입금 조회 
~~~~~~~~~~~~~~~~~~~~~~

입금 UUID 를 통해 개별 입금건을 조회한다. 입금 UUID 는 입금 리스트 조회를 통해 확인할 수 있다.

..  code-block:: python
    import pyupbit 

    access = "access key"  
    secret = "secret key"
    upbit = Upbit(access, secret)

    uuid = "uuid"       # 조회하려는 입금 UUID
    currency = "KRW"    # 조회하려는 화폐 정보
    deposit_order_info = upbit.get_individual_deposit_order(uuid, currency)
    print(deposit_order_info)



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

API 키 목록 및 만료 일자를 조회한다.

..  code-block:: python
    import pyupbit 

    access = "access key"  
    secret = "secret key"
    upbit = Upbit(access, secret)

    api_key_info = upbit.get_api_key_list()
    print(api_key_info)