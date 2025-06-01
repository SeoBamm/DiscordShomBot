import math
import random

def get_subsidy(entirePoint: int, base=30000, k=-0.5):
    # 포인트가 0 이하일 경우 지원 없음
    if entirePoint <= 0:
        return 0 

    # 로그 함수 적용
    correction_factor = 1 + k * math.log(entirePoint / base)

    
        
    # 최소 보정치 설정 (너무 작아지는 것 방지)
    correction_factor = max(2/30, correction_factor)  # 최소 2000 p 보정 유지

    # 0.8 ~ 1.2 사이의 랜덤 가중치
    randomPointWeight = random.uniform(0.8, 1.2)

    # 최종 지원금 계산
    return int(base * correction_factor * randomPointWeight)

# 테스트할 포인트 리스트
points = [1000, 2000, 5000, 10000, 30000, 50000, 70000, 100000, 120000, 150000, 170000, 300000]

# 각 포인트에 대한 지원금 출력
subsidy_values = {point: get_subsidy(point) for point in points}
print(subsidy_values)
