# Artifact v0

## Run information

- Provider: `openai`
- Suite: `base`
- Run file: `runs/v1_B_base_openrouter_20260729T151853283420.json`
- Artifact version: `v1+p87d2e5cc289d+t011c271ef0bb`
- Prompt hash: `87d2e5cc289d016050b2283a93f1037b348e57b6528e16173ad026b8e8816c05`
- Tools hash: `011c271ef0bbad1e19a5d7b660b2ed481b7d72950f1faa8a0798c3bdd8784ee1`

## Metrics

- Total cases: 20
- Measured cases: 20
- Provider error cases: 0
- Passed cases: 18
- Case accuracy: 0.9
- Tool routing accuracy: 1.0
- Argument accuracy: 0.9
- Multiturn accuracy: 1.0

## Failed cases

- R08_out_of_scope
- R10_missing_handle
- R11_missing_url
- R12_confirm_before_send
- R13_parallel_web_and_tweets
- R14_out_of_scope_coding

## Baseline observation

Sau khi tinh chỉnh mô tả tool `lookup`, agent đạt độ chính xác 90% (18/20 case).
Khả năng định tuyến tool đạt 100% và hầu hết các tham số được suy luận chính xác.
Các lỗi còn lại chủ yếu liên quan đến:
- Thiếu `response_type` khi gọi `clarify` trong trường hợp thiếu URL.
- Chưa yêu cầu xác nhận dạng `yes_no` trước các hành động gửi nội dung.
Những vấn đề này sẽ được xử lý ở các phiên bản tiếp theo.