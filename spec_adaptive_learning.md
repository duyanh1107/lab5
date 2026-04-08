**ADAPTIVE LEARNING SYSTEM**

**AI PRODUCT CANVAS**

AI cá nhân hóa lộ trình học theo từng người để tăng hiệu quả và giữ động lực học.

**1\. VALUE**

- **User:** Learners, Facilitators
- **Problem:** Nội dung không cá nhân hóa → quá dễ/khó, mất động lực
- **Value:** Cá nhân hóa difficulty + pacing → học nhanh hơn, tăng engagement
- **Key features:**
  - Adaptive learning path
  - Dynamic difficulty
  - Progress tracking dashboard
- **Metrics:** Completion ↑, engagement ↑, drop-off ↓

**2\. TRUST**

- **Risks:** Gợi ý sai level, bias, nội dung AI sai
- **Mitigation:**
  - Human override (facilitator)
  - Confidence score
  - Giới hạn difficulty jump
- **Transparency:** Giải thích "vì sao recommend bài này"
- **User control:** Cho phép chọn dễ/khó hơn

**3\. FEASIBILITY**

- **Data:** Score, time to learn, behavior
- **Approach:**
  - MVP: rule-based
  - Nâng cao: ML / RL + LLM
- **System:** Learner model + recommendation engine + dashboard
- **Constraints:** Cold start, thiếu data

**4\. LEARNING SIGNAL**

- **Signals:**
  - Accuracy, time, retry
  - Drop-off, completion
- **Feedback:**
  - Implicit (behavior)
  - Explicit ("too hard/easy")
- **Loop:** A/B test → improve model

**USER STORIES × 4 PATHS - ADAPTIVE LEARNING SYSTEM**

**User Story chính**

Là một learner, tôi muốn hệ thống đề xuất bài học phù hợp với trình độ của mình để học hiệu quả và không bị chán hoặc quá tải.

**1\. Happy Path (luồng lý tưởng)**

- User làm bài → hệ thống đánh giá đúng năng lực
- Recommend bài phù hợp (hơi thử thách)
- User hoàn thành tốt → tăng difficulty nhẹ
- User thấy "vừa sức" → tiếp tục học

✅ Outcome: Progress ổn định, engagement cao

**2\. Low-confidence Path (hệ thống không chắc chắn)**

- Data chưa đủ (user mới / hành vi ít)
- Model unsure về level

👉 System xử lý:

- Cho bài ở mức trung bình
- Hoặc hỏi thêm (diagnostic quiz ngắn)
- Hiển thị confidence thấp

➡️ Sau đó update lại learner model

**3\. Failure Path (sai / fail)**

- System recommend bài quá khó
- User fail nhiều lần / bỏ dở

❌ Outcome:

- Frustration
- Drop-off

**4\. Correction Path (sửa lỗi)**

- Detect: user fail / time quá lâu
- System phản ứng:
  - Giảm difficulty
  - Gợi ý review kiến thức cũ
  - Cho hint / explanation
- Có thể hỏi:

"Bài này quá khó không?"

✅ Outcome: User quay lại flow học bình thường

**Tóm tắt logic hệ thống**

- Happy → tiếp tục tăng nhẹ
- Low-confidence → hỏi thêm / chơi an toàn
- Failure → giảm difficulty
- Correction → đưa user về đúng quỹ đạo

**EVAL METRICS - ADAPTIVE LEARNING SYSTEM**

Một hệ adaptive tốt = **đúng độ khó (accuracy)** + **giữ được người học (engagement)** + **giúp họ đi đến cuối (retention)**.

**1\. Learning Performance (Hiệu quả học)**

- **Metric:** Quiz accuracy (%)
- **Threshold:** 70% - 85% (optimal learning zone)
- **Red flag:**
  - <50% → quá khó
  - 95% → quá dễ

**2\. Engagement (Mức độ tham gia)**

- **Metric:** Time on task / sessions per day
- **Threshold:**
  - ≥ X phút/session (tuỳ course, ví dụ ≥15 phút)
- **Red flag:**
  - Giảm mạnh theo thời gian
  - Session quá ngắn → mất tập trung / chán

**3\. Retention / Progress (Tiến độ & giữ chân)**

- **Metric:**
  - Completion rate (%)
  - Drop-off rate (%)
- **Threshold:**
  - Completion ≥ 60-70%
- **Red flag:**
  - Drop-off tăng mạnh tại 1 điểm → difficulty mismatch
  - User dừng sau vài bài đầu

**Tóm tắt logic**

- Accuracy → đo "đúng level chưa"
- Engagement → đo "có còn hứng học không"
- Retention → đo "có đi đến cuối không"

**TOP 3 EDGE CASES & FALLBACKS**

3 case này cover: data sai (false signal), data nhiễu (inconsistent), và data thiếu (cold start) → nếu xử lý tốt thì hệ adaptive sẽ rất robust.

**1\. False Skill Detection (đoán đúng / sai ngẫu nhiên)**

- **Edge case: User đoán đúng (hoặc sai do bất cẩn) → system hiểu sai năng lực**
- **Risk: Adapt sai → difficulty tăng/giảm không đúng**
- **Fallback:**
  - **Không update level dựa trên 1 lần (require consistency)**
  - **Kết hợp nhiều signal: accuracy + time + attempts**
  - **Thêm câu hỏi tương tự để verify**

**2\. Inconsistent Behavior (hành vi không ổn định)**

- **Edge case: Lúc rất tốt, lúc rất tệ (noise cao)**
- **Risk: System "giật", thay đổi difficulty liên tục**
- **Fallback:**
  - **Smoothing (moving average performance)**
  - **Batch update (mỗi vài bài mới adjust)**
  - **Nếu variance cao → trigger diagnostic lại**

**3\. Cold Start nhưng user outlier (quá giỏi / quá yếu)**

- **Edge case: User mới nhưng level lệch xa default**
- **Risk: Trải nghiệm đầu rất tệ → drop sớm**
- **Fallback:**
  - **Diagnostic quiz ngắn ban đầu**
  - **Cho skip / fast-track nếu làm quá tốt**
  - **Cho phép user chọn level manually**

**ROI**

Adaptive Learning không chỉ cải thiện trải nghiệm học mà còn trực tiếp tăng revenue thông qua completion và retention.

**Giả định chung**

- **1,000 learners**
- **Giá khóa học: \$100**
- **Baseline completion: 50%**

**1\. Conservative (thận trọng)**

- **Completion: 50% → 55% (+5%)**
- **Retention tăng nhẹ, engagement tăng ít**

**👉 Impact:**

- **+50 learners hoàn thành**
- **Revenue tăng: +\$5,000**

**2\. Realistic (thực tế)**

- **Completion: 50% → 65% (+15%)**
- **Engagement ↑ → ít drop giữa chừng**

**👉 Impact:**

- **+150 learners hoàn thành**
- **Revenue tăng: +\$15,000**

**3\. Optimistic (lạc quan)**

- **Completion: 50% → 80% (+30%)**
- **Strong personalization → giữ chân rất tốt**

**👉 Impact:**

- **+300 learners hoàn thành**
- **Revenue tăng: +\$30,000**

**Chi phí (ước tính đơn giản)**

- **Dev + infra + AI cost: ~\$10,000**

**ROI ước tính**

- **Conservative: ~50%**
- **Realistic: ~150%**
- **Optimistic: ~300%**

**Tóm tắt**

- **Giá trị chính đến từ: tăng completion + retention**
- **Adaptive learning càng tốt → ROI càng scale theo số learner**