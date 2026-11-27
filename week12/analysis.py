from pathlib import Path

import pandas as pd


def 정제(df):
	결과 = df.copy()

	# 점수가 비어 있는 행을 삭제한다.
	결과 = 결과.dropna(subset=["점수"])
	print(f"점수 결측 행 삭제 후: {len(결과)}행")

	# 모든 열의 값이 같은 중복 행을 삭제한다.
	결과 = 결과.drop_duplicates()
	print(f"중복 행 삭제 후: {len(결과)}행")

	# 반과 과목의 앞뒤 공백을 제거한다.
	결과["반"] = 결과["반"].str.strip()
	결과["과목"] = 결과["과목"].str.strip()
	print(f"공백 정리 후: {len(결과)}행")

	# 점수가 0 이상 100 이하인 행만 남긴다.
	결과 = 결과[결과["점수"].between(0, 100)]
	print(f"점수 범위 정리 후: {len(결과)}행")

	return 결과

csv_path = Path(__file__).with_name("scores_2026.csv")
정제된_df = 정제(pd.read_csv(csv_path))

math_df = 정제된_df[정제된_df["과목"] == "수학"]
print(f"과목이 '수학'인 행 수: {len(math_df)}행")

반별_점수_평균 = 정제된_df.groupby("반")["점수"].mean()
print(f"반별 점수 평균:\n{반별_점수_평균}")

과목과_반별_점수_평균 = 정제된_df.groupby(["과목", "반"])["점수"].mean()
print(f"과목과 반별 점수 평균:\n{과목과_반별_점수_평균}")

반별_점수_요약 = 정제된_df.groupby("반")["점수"].agg(
	개수="count",
	평균="mean",
	중앙값="median",
	최댓값="max",
)
반별_점수_요약[["평균", "중앙값"]] = 반별_점수_요약[["평균", "중앙값"]].round(2)
print("반별 점수 요약:")
print(반별_점수_요약.to_string(float_format="{:.2f}".format))


