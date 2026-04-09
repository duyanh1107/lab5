import streamlit as st
from tools.learning_materials import generate_hint_llm, generate_explanation_llm, generate_lesson_llm, generate_question_llm, parse_question
from als_full_2 import DecisionEngine, Learner, courses

st.set_page_config(page_title="Adaptive Learning", layout="centered")

# =========================
# INIT STATE
# =========================

if "learner" not in st.session_state:
    st.session_state.learner = None
    st.session_state.course = None
    st.session_state.module_idx = 0
    st.session_state.question_idx = 0
    st.session_state.questions = []
    st.session_state.answered = False
    st.session_state.skip_message = None
    st.session_state.explanation = None

# =========================
# TITLE
# =========================

st.title("🤖 Adaptive Learning Demo")

if st.session_state.skip_message:
    st.success(st.session_state.skip_message)
    st.session_state.skip_message = None

# =========================
# USER SELECT
# =========================

USER_DB = {
    1: {"name": "An", "level": 1},
    2: {"name": "Binh", "level": 2},
    3: {"name": "Chi", "level": 3},
    4: {"name": "Dung", "level": 4},
    5: {"name": "Em", "level": 5},
}

user_id = st.selectbox("Select User", list(USER_DB.keys()))

if st.button("Start"):
    info = USER_DB[user_id]
    st.session_state.learner = Learner(user_id, info["level"])

# =========================
# COURSE SELECT
# =========================

if st.session_state.learner:

    learner = st.session_state.learner

    st.write(f"👋 Hello {USER_DB[user_id]['name']}")
    st.write(f"📊 Level: {round(learner.level,2)}")

    course_name = st.selectbox("Choose course", ["math", "code"])

    if st.button("Load Course"):
        st.session_state.course = courses[course_name]
        st.session_state.module_idx = 0
        st.session_state.question_idx = 0
        st.session_state.answered = False

# =========================
# RUN COURSE
# =========================

engine = DecisionEngine()

# init thêm state
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "show_result" not in st.session_state:
    st.session_state.show_result = False

if st.session_state.course:

    learner = st.session_state.learner
    course = st.session_state.course
    m_idx = st.session_state.module_idx

    if m_idx < len(course.modules):

        module = course.modules[m_idx]
        performance = engine.estimate_performance(learner)
        # 👉 Adaptive: skip lesson nếu giỏi
        # =========================
        # 🔥 REAL SKIP LOGIC
        # =========================

        if engine.should_skip_module(performance):

            st.session_state.skip_message = f"""
            🚀 You skipped **{module.name}** 
            because your performance is high ({round(performance,2)})
            """

            st.session_state.module_idx += 1
            st.session_state.question_idx = 0
            st.session_state.questions = []

            st.rerun()

        st.header(f"📘 {module.name}")

        # if performance < 5:
        #     st.info(module.lesson.content)

        if performance < 5:

            if "generated_lesson" not in st.session_state:
                st.session_state.generated_lesson = None

            if st.session_state.generated_lesson is None:

                lesson = generate_lesson_llm(
                    module.name,
                    module.lesson.content,
                    int(performance)
                )

                st.session_state.generated_lesson = lesson

            st.info(st.session_state.generated_lesson)
        else:
            st.warning("⏩ Skipped lesson (advanced)")

        if len(st.session_state.questions) == 0:
            st.session_state.questions = module.questions

        q_idx = st.session_state.question_idx

        if q_idx < len(st.session_state.questions):

            q = st.session_state.questions[q_idx]

            st.subheader(q.content)

            answer = st.radio("Choose answer", q.options, key=f"q_{m_idx}_{q_idx}")

            # =========================
            # SUBMIT
            # =========================

            if st.button("Submit") and not st.session_state.show_result:

                correct = answer[0] == q.correct_answer

                mastery = learner.update(correct)

                # lưu result vào state (quan trọng)
                st.session_state.last_mastery = mastery
                st.session_state.last_correct = correct
                st.session_state.correct_answer = q.correct_answer

                if correct:

                    explanation = generate_explanation_llm(
                        q.content,
                        q.correct_answer,
                        q.options
                    )

                    st.session_state.explanation = explanation   # 🔥 THÊM DÒNG NÀY

                    st.session_state.show_result = True
                    st.session_state.attempts = 0

                else:
                    st.session_state.attempts += 1

                    hint = engine.get_hint(q, performance)
                    
                    if hint:
                        hint = generate_hint_llm(q.content, performance, st.session_state.attempts)
                        st.info(f"💡 Hint: {hint}")

                    if st.session_state.attempts >= 2:

                        explanation = generate_explanation_llm(
                            q.content,
                            q.correct_answer,
                            q.options
                        )

                        st.session_state.explanation = explanation  # 🔥 lưu vào state

                        st.session_state.show_result = True
                        st.session_state.attempts = 0

            # =========================
            # SHOW RESULT (KHÔNG BỊ RERUN MẤT)
            # =========================

            if st.session_state.show_result:

                if st.session_state.last_correct:
                    st.success("✅ Correct!")
                else:
                    st.error("❌ Wrong!")
                    st.warning(f"👉 Correct answer: {st.session_state.correct_answer}")

                st.write(f"📊 Mastery: {round(st.session_state.last_mastery,2)}")
                st.write(f"📈 Level: {round(learner.level,2)}")
                
                if st.session_state.explanation:
                    st.info(f"📘 Explanation: {st.session_state.explanation}")

                if st.button("Continue"):
                    st.session_state.generated_lesson = None  # reset lesson khi qua câu mới
                    st.session_state.show_result = False
                    st.session_state.question_idx += 1
                    st.session_state.explanation = None  # reset explanation khi qua câu mới

                    if st.session_state.question_idx >= len(st.session_state.questions):
                        st.session_state.module_idx += 1
                        st.session_state.question_idx = 0
                        st.session_state.questions = []

                    st.rerun()

        else:
            st.session_state.module_idx += 1
            st.session_state.question_idx = 0
            st.session_state.questions = []
            st.rerun()

    else:
        st.success("🎯 Course completed!")

        st.write(f"✅ Correct: {learner.correct_count}")
        st.write(f"❌ Wrong: {learner.wrong_count}")