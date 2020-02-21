## 대학생 및 1인 가구를 위한 원룸 중개 및 정보 조회 사이트



### 프로토타입 기능

1. **지도 마커에 다가구(월세) 실거래가 띄우기**<img src="https://lh4.googleusercontent.com/ZYQEZhfBOleSL4ToY0Z05iw5DjuGGfHJ4VU3tbPCClKd_G2YKFr7c3vVXy2EyFtwu6t2xWctCXXMKsvZKt7XDV6YvAdiAaeh9tUANr06pSUUgwW5AH70q5VGk8yd6gNxfHJiq4Ev-6A" alt="img" style="zoom: 35%;" />

   

2. **줌 인/아웃 시 동, 구, 시 단위로 매물 평균가 보여주기**

   **[줌 인]**
   <img src="https://lh3.googleusercontent.com/l_yVKoY68iZfdcUiafZbxMceKfHx43e0h_6LeBsoEwPHPXuVbweLKklBRQcVZKBEvC4UhRPWPG08McNP07AsGvit85J54vrj4mVMe9mtXDfXUuVO8s1ZEb2EGLaBNJEeE9MN1Zlwgo0" alt="img" style="zoom: 78%;" />

   

   **[줌 아웃]**
   <img src="https://lh4.googleusercontent.com/q2CgYn5IFnMg95FDNbbjuzRCEleogKTEJNekuV4vYlkS8IQhJGHSQQ6RfNJj6DZKaUXcijgmrThlzjfPKBpHPKQP4DdRY1poMV3BAAoFjPT5njx5AiHvzS2A31y0Py_m-70MiLtoqFs" alt="img" style="zoom:55%;" />

   

3. **장소 검색 기능**
   <img src="https://lh4.googleusercontent.com/ovTbjXqTx57ltqUORmgmlKr_bbz7TqO-t4YCKt4kJbYBeRz9D4s8TNSWbxOPa6-brzjvv0kI0Zc--R-BEkn3nNZ3_9DztlnQReS1pPCsAvgs44sScn0sU5Srw26LWwAQSmIDzW-S6Zo" alt="img" style="zoom:35%;" />



### 추가 기능

4. **지도에 거리 표시하기**

   지도에서 선을 여러개 그어서 비교를 할 수 있도록 기능 제공
   <img src="https://lh3.googleusercontent.com/v-a0nx4OVbw8INaN4Cfjc5ER-iqv5CtOBXX4JaGWodJk2BJ6yNzTxGqLLsnHB5WbOcWvNtctS2KPJWX1u1Lmtycq6XdXhT45L3h7j-YgH5ITDCECvZlITb_863ESJ4QIr069fvvGNGc" alt="img" style="zoom: 67%;" />

5. **매물 비교 및 추천**

   자주 가야하는 **하나 이상의 장소**(ex. 학교, 아르바이트)를 등록 하여, **매물과 목적지 사이의 동선을 비교**하기 용이하도록 하는 기능을 추가
   <img src="https://lh6.googleusercontent.com/ZPLK2mmxuJyYcNrfZMwaWPe-kYUNURBVWYBzx4jfQ6f7Dzr7aeo0cqlJaOv9DTtDs4-WKuqD2CDycxSSaAIVGMRNHn2fmd4lotScq9rIskYLJJeSu6cHq0dL2-Ck-N_JpExyqcoWCTE" alt="img" style="zoom:60%;" />

   

6. **건물 근처 인프라 검색 기능**

   **건물 마커를 하나 선택**한 후, 자신이 원하는 인프라나 시설을 검색하면 **건물 기준**으로 가장 가까운 곳에 있는 **인프라와 시설 검색 결과 띄워주는 기능**
   <img src="https://lh5.googleusercontent.com/RiWOJBNNLh0Vtw3YhqQVe_g0llK4vizVaVLGkScPcMPcrNvD0FcvPYkXHvRzDQyRenjKBtdGz-CqgztrnUi-Jqo5CGif5z90U2THSLC_I2F7hmbCK5gjmR2_jNSv31K-KCipv8KADEI" alt="img" style="zoom:60%;" />

7. **사용자들의 리뷰 등록**

   프로토 타입에서 구현한 마커를 클릭하면, 상세 건물 정보가 나오고, 사용자들이 직접 건물에 대해 리뷰를 남길 수 있도록 기능 제공
   

8. **매물 등록 기능**

   거래를 원하는 사람(매매자)이 직접 매물을 등록하도록 함이 때, 등록자가 자신이 거래하는 부동산 또한 직접 등록하도록 함(부동산에 대한 평가 또한 동시에 발생 할 수 있도록 하고싶음)



### 사용 API 및 데이터

- 카카오 지도 API (마커 기능 사용)
- 데이터 공공 포털  (단독/다가구, 연립다세대, 실거래 자료/ 연립다세대, 단독/다가구 전월세 자료 / 오피스텔 매매 및 전월세 신고 조회 서비스) 
- 서울 열린 데이터 광장 (서울 특별시 전월세가 정보)

