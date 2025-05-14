notice_text = """
6/3(화, 대통령 선거) 휴강 및 국가공휴일 휴강에 따른 보강일(공휴일지정보강기간) 및 유의사항 안내
**대학원 수업문의는 대학원학사지원실로 문의하시기 바랍니다.
2025학년도1학기 국가공휴일 휴강에 따른 보강일(공휴일 지정보강기간)을 아래와 같이 안내 드리니 수업운영에 참고하시기 바랍니다.
공휴일
지정보강기간
휴‧보강일정
① 근로자의날
[휴강일]
5. 1.(목)
⇨
[보강일]
6. 11.(수)
 ② 어린이날
[휴강일]
5. 5.(월)
⇨
[보강일]
6. 16.(월)
③ 부처님오신날대체휴일
[휴강일]
5. 6.(화)
⇨
[보강일]
6. 10.(화)
④ 개교기념일
[휴강일]
5. 22.(목)
⇨
[보강일]
6. 12.(목)
⑤ 현충일
[휴강일]
6. 6.(금)
⇨
[보강일]
6. 13.(금)
⑥ 대통령선거
[휴강일]
6. 3.(화)
⇨
[보강일]
6. 17.(화)
** 6월 3일의 휴보강처리는 4월 11일 입력완료함
** 4월11일 이전에 이미 휴보강 처리된 경우 기존입력한 내역대로 진행
※   6월 3일(화)이 대통령선거일로 지정됨에 따라  6월 3일(화)의 수업이 공휴일지정보강기간인 6월 17일(화)로 일괄 보강입력되었으나
일괄 처리 일인 4월 11일 전에 미리 입력된 보강의 경우 보강일이 다를 수있으니,
수업일 전에 과목담당교수님에게 수업여부를 반드시 확인하시기 바랍니다.    
※   휴보강일괄입력 이후 재보강이 등록된 경우 위의 보강일자가 변경되므로, 수업 전 반드시 보강일자를 확인하여야 합니다. 
※  휴보강  내역조회 :  [통합정보시스템-학생서비스-학사행정-수업-개설강좌조회]의 해당과목 옆  '휴보강내역'을  "조회" 
※  기타 학사 일정은 홈페이지 교육 대학학사안내 - 학사일정 참조,  이외 휴보강관련 여부는 해당 과목 교수님께 확인 바랍니다.
※  대학원 학사일정은 대학원학사지원실  또는  소속  학과로 문의하시기 바랍니다.
** 공휴일 지정보강기간 유의사항
1)  공휴일 지정보강기간에는 원래 요일의 수업이 없고 지정된 일자의 보강수업만 운영되므로, 수강 시 착오없으시기 바랍니다. 
    - 휴강일 별로 보강일자가 상이하니 해당일자를  반드시 확인요망
2)  공휴일지정보강기간(6. 10 ~ 6.17)에는 시험실시가 불가하나, 부득이한 사정으로 해당주차에 기말 시험이 실시될 경우
      반드시 본인의 보강수업 유무를 확인하여 불이익을 받는 경우가 없도록 하여주시기 바랍니다.
           모든 수업의 휴보강은 통합정보시스템에 등록 후 운영함이 원칙입니다.  
        시험 또는 보강수업이 중복되는 경우 통합정소시스템에 등록된 수업이 우선이으로, 
        학생은 본인의 수업유무를 해당 과목 교수님에게 알려 등록되지 않은 시험(또는 보강수업)의 일자를 재지정하도록 요청하여야 합니다.
"""

from transformers import pipeline, AutoTokenizer
import torch

def summarize_with_huggingface(text, model_name="facebook/bart-large-cnn"):
    device = -1
    summarizer = pipeline("summarization", model=model_name, device=device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # 모델의 최대 입력 길이
    max_input_length = 1024
    inputs = tokenizer(text, return_tensors="pt", truncation=False)["input_ids"][0]

    # 토큰 단위로 슬라이스
    token_chunks = [inputs[i:i + max_input_length] for i in range(0, len(inputs), max_input_length)]

    summaries = []
    for idx, chunk in enumerate(token_chunks):
        input_text = tokenizer.decode(chunk, skip_special_tokens=True)
        print(f"▶ Chunk {idx}: {input_text[:60]}...")  # 일부만 출력
        result = summarizer(input_text, max_length=150, min_length=30, do_sample=False)[0]["summary_text"]
        summaries.append(result)
        print(f"✅ Summary {idx}: {result}\n")

    return summaries

# 테스트 실행
summary = summarize_with_huggingface(notice_text)
print("\n\n📌 최종 요약:")
print(summary)

