import math

points = [10000, 30000, 50000, 100000, 150000, 300000, 700000, 1000000, 10000000]
points = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 130000, 140000, 150000, 160000, 170000, 180000, 190000, 200000, 10000000]
points = [999999999999999]
scaled_reward_exp_values = {point: 29 + int(math.log((point + 1)) / math.log(1.05) * 2.5) for point in points}

print(scaled_reward_exp_values)