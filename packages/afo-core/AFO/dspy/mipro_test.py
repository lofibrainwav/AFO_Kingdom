#!/usr/bin/env python3
"""
MIPROv2 멀티모달 테스트 스크립트
왕국 Trinity Score 기반 최적화 검증
"""

from afo.dspy.trinity_mipro_v2 import TrinityAwareMIPROv2, calculate_trinity_score


def create_test_image_base64():
    """테스트용 작은 이미지 base64 생성"""
    # 아주 작은 빨간 점 이미지 (1x1 픽셀)
    return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="


def create_multimodal_dataset():
    """멀티모달 테스트 데이터셋 생성"""
    img_base64 = create_test_image_base64()

    trainset = [
        {"question": "이 이미지에 뭐가 있어?", "images": [img_base64], "answer": "빨간 점 하나"},
        {"question": "이미지 색상은?", "images": [img_base64], "answer": "빨강"},
        {"question": "이미지 설명해", "images": [img_base64], "answer": "작은 빨간 점 이미지"},
    ]

    return trainset


def test_trinity_score():
    """Trinity Score 계산 테스트"""
    print("🏰 Trinity Score 계산 테스트")

    # 테스트 케이스들
    test_cases = [
        (1.0, 1.0, 1.0, 0.8, 0.9),  # 완벽 케이스
        (0.9, 0.8, 0.7, 0.8, 0.9),  # 보통 케이스
        (0.5, 0.5, 0.5, 0.8, 0.9),  # 중간 케이스
    ]

    for truth, goodness, beauty, serenity, eternity in test_cases:
        score = calculate_trinity_score(truth, goodness, beauty, serenity, eternity)
        print(".3f")


def main():
    """메인 테스트 함수"""
    print("🏰 MIPROv2 멀티모달 테스트 시작")
    print("=" * 50)

    # 1. Trinity Score 테스트
    test_trinity_score()
    print()

    # 2. 데이터셋 생성
    print("🏰 멀티모달 데이터셋 생성")
    dataset = create_multimodal_dataset()
    print(f"✅ 데이터셋 크기: {len(dataset)}")
    for i, item in enumerate(dataset):
        print(f"   {i + 1}. Q: {item['question'][:20]}... A: {item['answer']}")
    print()

    # 3. TrinityAwareMIPROv2 초기화 테스트
    print("🏰 TrinityAwareMIPROv2 초기화 테스트")

    def simple_metric(example, pred, trace=None):
        """간단한 메트릭 함수"""
        return 0.8

    try:
        optimizer = TrinityAwareMIPROv2(metric=simple_metric, num_trials=3)
        print("✅ TrinityAwareMIPROv2 초기화 성공")
        print(f"   Trinity 가중치: {optimizer.trinity_weights}")
    except Exception as e:
        print(f"❌ 초기화 실패: {e}")
        return

    print()
    print("🏰 MIPROv2 멀티모달 테스트 완료")
    print("=" * 50)


if __name__ == "__main__":
    main()
