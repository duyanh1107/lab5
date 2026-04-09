import random

class BKTModel:
    def __init__(self, p_init=0.3, p_learn=0.002, p_guess=0.25, p_slip=0.05):
        self.p_know = p_init
        self.p_learn = p_learn
        self.p_guess = p_guess
        self.p_slip = p_slip

    def update(self, correct):
        p = self.p_know

        if correct:
            num = p * (1 - self.p_slip)
            den = num + (1 - p) * self.p_guess
        else:
            num = p * self.p_slip
            den = num + (1 - p) * (1 - self.p_guess)

        p_given_obs = num / den

        # learning step
        self.p_know = p_given_obs + (1 - p_given_obs) * self.p_learn

        return self.p_know

# =========================
# 1. LEARNING MATERIAL DB
# =========================

class Question:
    def __init__(self, id, content, difficulty, correct_answer, options, hints):
        self.id = id
        self.content = content
        self.difficulty = difficulty
        self.correct_answer = correct_answer
        self.options = options
        self.hints = hints


class Lesson:
    def __init__(self, content):
        self.content = content


class Module:
    def __init__(self, name, lesson=None, questions=None):
        self.name = name
        self.lesson = lesson
        self.questions = questions or []


class Course:
    def __init__(self, name, modules):
        self.name = name
        self.modules = modules


# =========================
# 2. LEARNER PROFILE
# =========================

class Learner:
    def __init__(self, learner_id, level):
        self.id = learner_id
        self.level = level
        self.history = []
        self.correct_count = 0
        self.wrong_count = 0

        # 👉 thêm BKT
        self.bkt = BKTModel(p_init=level/5)

    def update(self, correct):
        self.history.append(correct)

        if correct:
            self.correct_count += 1
        else:
            self.wrong_count += 1

        # 👉 update BKT
        mastery = self.bkt.update(correct)
        self.level += mastery * 0.5  # level tăng dựa trên mastery
        return mastery


# =========================
# 3. DECISION ENGINE
# =========================

class DecisionEngine:
    
    def estimate_performance(self, learner):
        return learner.level

    def get_difficulty(self, performance):
        return max(1, min(5, round(performance)))

    def should_skip_module(self, performance):
        return performance >= 5

    def get_hint(self, question, performance):
        if performance <= 2:
            return question.hints[2]
        elif performance <= 4:
            return question.hints[1]
        return None


# =========================
# QUIZ INTERACTION
# =========================

def ask_question(learner, question, engine):
    # 👉 Lấy performance hiện tại (dựa trên BKT)
    performance = engine.estimate_performance(learner)

    print(f"\nQ: {question.content}")
    for opt in question.options:
        print(opt)

    attempts = 0

    while attempts < 2:
        ans = input("Your answer: ").strip().upper()

        # =========================
        # ✅ CASE: CORRECT
        # =========================
        if ans == question.correct_answer:
            print("✅ Correct!")

            # 🔥 UPDATE BKT HERE
            mastery = learner.update(True)

            print(f"📊 Mastery (P(Know)): {round(mastery, 2)}")
            print(f"📈 Performance: {round(engine.estimate_performance(learner), 2)}")

            return

        # =========================
        # ❌ CASE: WRONG
        # =========================
        else:
            print("❌ Wrong!")
            attempts += 1

            hint = engine.get_hint(question, performance)
            if hint:
                print(f"💡 Hint: {hint}")

    # =========================
    # ❌ CASE: FAILED AFTER 2 ATTEMPTS
    # =========================
    print(f"👉 Correct answer is: {question.correct_answer}")

    # 🔥 UPDATE BKT HERE
    mastery = learner.update(False)

    print(f"📊 Mastery (P(Know)): {round(mastery, 2)}")
    print(f"📈 Performance: {round(engine.estimate_performance(learner), 2)}")


# =========================
# RUN MODULE
# =========================


def run_module(learner, module, engine):
    print(f"\n📘 Module: {module.name}")

    performance = engine.estimate_performance(learner)

    # 👉 Adaptive: skip lesson nếu giỏi
    if performance < 5:
        print("\n📖 Lesson:")
        print(module.lesson.content)
    else:
        print("\n⏩ Skipping lesson (you are advanced)")

    # 👉 Adaptive pacing
    num_questions = 2 if performance <= 2 else 3

    questions = random.sample(module.questions, min(num_questions, len(module.questions)))

    for q in questions:
        ask_question(learner, q, engine)


# =========================
# RUN COURSE
# =========================

def run_course(learner, course, engine):
    print(f"\n🚀 Starting course: {course.name}")

    for module in course.modules:
        performance = engine.estimate_performance(learner)

        if engine.should_skip_module(performance):
            print(f"\n⏩ Skipping module {module.name} (you are strong)")
            continue

        run_module(learner, module, engine)

    print("\n🎯 SESSION SUMMARY")
    print(f"Correct: {learner.correct_count}")
    print(f"Wrong: {learner.wrong_count}")


# =========================
# DATA
# =========================

USER_DB = {
    1: {"name": "An", "level": 1},
    2: {"name": "Binh", "level": 2},
    3: {"name": "Chi", "level": 3},
    4: {"name": "Dung", "level": 4},
    5: {"name": "Em", "level": 5},
}

math_course = Course("Math", [

    Module("1. Matrix Basics",
        Lesson("A matrix is a rectangular array of numbers arranged in rows and columns."),
        [
            Question(1, "Matrix is?", 1, "A",
                     ["A. Table of numbers", "B. Function", "C. Scalar"],
                     {1: "Think table", 2: "Matrix = grid"}),
        ]
    ),

    Module("2. Matrix Dimensions",
        Lesson("Matrix dimensions are defined as rows × columns."),
        [
            Question(2, "2x2 matrix has?", 1, "B",
                     ["A. 2 elements", "B. 4 elements", "C. 6 elements"],
                     {1: "rows x cols", 2: "2*2"}),
        ]
    ),

    Module("3. Matrix Addition",
        Lesson("Matrices can be added only if they have the same dimensions."),
        [
            Question(3, "Matrix addition requires?", 2, "A",
                     ["A. Same size", "B. Same values", "C. Same rows only"],
                     {1: "same dimension", 2: "rows and columns must match"}),
        ]
    ),

    Module("4. Matrix Multiplication",
        Lesson("To multiply matrices, columns of A must equal rows of B."),
        [
            Question(4, "Condition to multiply?", 3, "A",
                     ["A. cols = rows", "B. rows = rows", "C. cols = cols"],
                     {1: "dimension match", 2: "A(mxn) * B(nxk)"}),
        ]
    ),

    Module("5. Identity Matrix",
        Lesson("Identity matrix has 1s on diagonal and 0s elsewhere."),
        [
            Question(5, "Identity matrix has?", 2, "A",
                     ["A. 1s diagonal", "B. All 1s", "C. All 0s"],
                     {1: "diagonal", 2: "only diagonal = 1"}),
        ]
    ),

    Module("6. Determinant",
        Lesson("Determinant is a scalar value derived from a square matrix."),
        [
            Question(6, "Determinant applies to?", 3, "B",
                     ["A. Any matrix", "B. Square matrix", "C. Vector"],
                     {1: "square only", 2: "n x n matrix"}),
        ]
    ),

    Module("7. Rank of Matrix",
        Lesson("Rank is the maximum number of linearly independent rows or columns."),
        [
            Question(7, "Rank represents?", 4, "A",
                     ["A. Independent rows", "B. Size", "C. Sum"],
                     {1: "independent", 2: "linear independence"}),
        ]
    ),

    Module("8. Inverse Matrix",
        Lesson("Inverse exists only for non-singular square matrices."),
        [
            Question(8, "Inverse exists when?", 5, "A",
                     ["A. determinant ≠ 0", "B. determinant = 0", "C. any matrix"],
                     {1: "non-zero determinant", 2: "must be invertible"}),
        ]
    ),

])

code_course = Course("Coding", [

    Module("1. Python Basics",
        Lesson("Python is a programming language. Use print() to display output."),
        [
            Question(9, "Print function?", 1, "A",
                     ["A. print()", "B. echo()", "C. log()"],
                     {1: "basic python", 2: "print()"}),
        ]
    ),

    Module("2. Variables",
        Lesson("Variables store values using = operator."),
        [
            Question(10, "Assign variable?", 1, "B",
                     ["A. x == 5", "B. x = 5", "C. x := 5"],
                     {1: "assignment", 2: "= is assignment"}),
        ]
    ),

    Module("3. Data Types",
        Lesson("Common types: int, float, string."),
        [
            Question(11, "Which is string?", 2, "C",
                     ["A. 10", "B. 3.14", "C. 'hello'"],
                     {1: "quotes", 2: "string has quotes"}),
        ]
    ),

    Module("4. If Conditions",
        Lesson("Use if statements for decision making."),
        [
            Question(12, "Condition keyword?", 2, "A",
                     ["A. if", "B. when", "C. check"],
                     {1: "common keyword", 2: "if statement"}),
        ]
    ),

    Module("5. Loops",
        Lesson("Use for loop to iterate."),
        [
            Question(13, "Loop keyword?", 2, "B",
                     ["A. repeat", "B. for", "C. loop"],
                     {1: "common keyword", 2: "for loop"}),
        ]
    ),

    Module("6. Functions",
        Lesson("Functions are defined using def."),
        [
            Question(14, "Define function?", 3, "A",
                     ["A. def", "B. func", "C. function"],
                     {1: "python syntax", 2: "def keyword"}),
        ]
    ),

    Module("7. Lists",
        Lesson("Lists store multiple items."),
        [
            Question(15, "List syntax?", 3, "B",
                     ["A. {}", "B. []", "C. ()"],
                     {1: "common structure", 2: "square brackets"}),
        ]
    ),

    Module("8. Dictionaries",
        Lesson("Dictionaries store key-value pairs."),
        [
            Question(16, "Dict syntax?", 4, "A",
                     ["A. {}", "B. []", "C. ()"],
                     {1: "curly braces", 2: "key-value structure"}),
        ]
    ),

])

courses = {
    "math": math_course,
    "code": code_course
}

# =========================
# MAIN AGENT
# =========================

def main():
    print("🤖 Adaptive Learning Agent")

    print("\nAvailable users:")
    for uid, info in USER_DB.items():
        print(f"{uid}: {info['name']} (Level {info['level']})")

    user_id = int(input("\nEnter your user ID: "))

    if user_id not in USER_DB:
        print("❌ Invalid user!")
        return

    user_info = USER_DB[user_id]

    learner = Learner(user_id, user_info["level"])

    print(f"\n👋 Hello {user_info['name']}!")
    print(f"📊 Your current level is: {learner.level}")

    print("\nWhat do you want to learn today?")
    print("Options: math / code")

    choice = input("Your choice: ").strip().lower()

    if choice not in courses:
        print("Invalid choice!")
        return

    course = courses[choice]
    engine = DecisionEngine()

    run_course(learner, course, engine)

if __name__ == "__main__":
    main()