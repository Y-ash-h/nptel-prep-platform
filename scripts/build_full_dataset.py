import json
import re
import pypdf

# -------------------------------------------------------------
# 1. MACHINE LEARNING ASSIGNMENTS 1 to 7 (PDFs)
# -------------------------------------------------------------

def clean_ml_text(t):
    t = re.sub(r'Course Name: Machine Learning for Earth System Sciences', '', t)
    t = re.sub(r'Week \d+ - Assignment \d+ - \(Jul-2026\)', '', t)
    t = re.sub(r'NPTEL ONLINE CERTIFICATION COURSES', '', t)
    t = re.sub(r'Indian Institute of Technology Kharagpur', '', t)
    t = re.sub(r'Jul-2026', '', t)
    t = re.sub(r'TYPE OF QUESTIONS:.*', '', t)
    t = re.sub(r'Number of questions:.*', '', t)
    t = re.sub(r'QUESTI\s+ON', 'QUESTION', t)
    return t.strip()

def extract_ml_1_to_7():
    results = []
    for ass_idx in range(1, 8):
        reader = pypdf.PdfReader(f'mlllllllll/Assignment{ass_idx}_noc26-cs121.pdf')
        raw_text = clean_ml_text('\n'.join([p.extract_text() or '' for p in reader.pages]))
        parts = re.split(r'QUESTION\s+\d+', raw_text)
        for q_idx in range(1, len(parts)):
            block = parts[q_idx].strip()
            ans_m = re.search(r'Answer:\s*\(?([A-Da-d])\)?', block)
            ans_letter = ans_m.group(1).upper() if ans_m else ''
            sol_m = re.search(r'Detailed Solution:\s*([\s\S]*)', block)
            sol = sol_m.group(1).strip() if sol_m else ''
            
            before_ans = block[:ans_m.start()].strip() if ans_m else block
            opt_matches = list(re.finditer(r'(?:\n|\A)\s*(\(?[a-dA-D]\)?[\.\)])\s*', before_ans))
            
            if len(opt_matches) >= 4:
                last_4 = opt_matches[-4:]
                q_text = before_ans[:last_4[0].start()].strip()
                opts = []
                for k in range(4):
                    o_start = last_4[k].end()
                    o_end = last_4[k+1].start() if k < 3 else len(before_ans)
                    opts.append(before_ans[o_start:o_end].strip())
            else:
                q_text = before_ans
                opts = []

            # Check image attachments
            image = None
            if ass_idx == 2 and q_idx == 6:
                image = "assets/ml_week2_kalman.png"
            elif ass_idx == 3 and q_idx == 2:
                image = "assets/ml_week3_distribution.png"

            ans_index = ord(ans_letter) - ord('A') if ans_letter in ['A', 'B', 'C', 'D'] else -1

            results.append({
                "id": f"ml_ass{ass_idx}_q{q_idx}",
                "course": "Machine Learning for Earth System Sciences",
                "course_id": "ml",
                "assignment": ass_idx,
                "question_number": q_idx,
                "question": q_text,
                "options": opts,
                "correct_answer": ans_index,
                "correct_letter": ans_letter,
                "detailed_solution": sol,
                "image": image
            })
    return results

# -------------------------------------------------------------
# 2. MACHINE LEARNING ASSIGNMENT 8 (Extracted from Screenshots)
# -------------------------------------------------------------

def get_ml_8():
    return [
        {
            "id": "ml_ass8_q1",
            "course": "Machine Learning for Earth System Sciences",
            "course_id": "ml",
            "assignment": 8,
            "question_number": 1,
            "question": "Match the studies in column - 1 with the machine learning models in column-2 used in that study for learning parameterization of convection.\n\nStudy:\nS1: Model CBRAIN proposed by Gentine et.al., 2018.\nS2: O'Gorman PA, Dwyer JG. Using machine learning to parameterize moist convection: Potential for modeling of climate, climate change, and extreme events. Journal of Advances in Modeling Earth Systems. 2018 Oct;10(10):2548-63.\nS3: Han Y, Zhang GJ, Huang X, Wang Y. A moist physics parameterization based on deep learning. Journal of Advances in Modeling Earth Systems. 2020 Sep;12(9):e2020MS002076.\n\nML Model:\n- ResNet\n- ANN\n- Random Forest",
            "options": [
                "(S1, ResNet), (S2, ANN), (S3, Random Forest)",
                "(S1, ResNet), (S2, Random Forest), (S3, ANN)",
                "(S1, ANN), (S2, Random Forest), (S3, ResNet)",
                "(S1, ANN), (S2, ResNet), (S3, Random Forest)"
            ],
            "correct_answer": 0,
            "correct_letter": "A",
            "detailed_solution": "In Gentine et al. (2018), CBRAIN uses ResNet; O'Gorman & Dwyer (2018) uses an Artificial Neural Network (ANN); Han et al. (2020) implements Random Forest parameterization.",
            "image": None
        },
        {
            "id": "ml_ass8_q2",
            "course": "Machine Learning for Earth System Sciences",
            "course_id": "ml",
            "assignment": 8,
            "question_number": 2,
            "question": "Which of the following is/are the justifications that even after the ready availability of three-dimensional hydrodynamical models, General Lake Model (GLM) was proposed as a one-dimensional model?\n\nI: One-dimensional models easily interface with biogeochemical and ecological modelling libraries for complex ecosystem simulations.\nII: GLM captures only the lake water balance and one-dimensional models are sufficient for this.\nIII: One-dimensional models have lower computational requirements.",
            "options": [
                "I only",
                "I and II",
                "II and III",
                "I and III"
            ],
            "correct_answer": 3,
            "correct_letter": "D",
            "detailed_solution": "1D lake models (like GLM) are computationally efficient (III) and readily interface with ecological and biogeochemical modules (I). Statement II is incorrect because GLM models thermodynamic and vertical thermal structure, not just water balance.",
            "image": None
        },
        {
            "id": "ml_ass8_q3",
            "course": "Machine Learning for Earth System Sciences",
            "course_id": "ml",
            "assignment": 8,
            "question_number": 3,
            "question": "In the study - Manepalli A, Albert A, Rhoades A, Feldman D, Jones AD. Emulating numeric hydroclimate models with physics-informed cGANs. In AGU fall meeting 2019 Dec 11, the authors have investigated upon the use of a deep generative model cGAN to simulate the output of a physics-based model for snow water equivalent (SWE). Which of the following is/are the domain knowledge that have been incorporated into the deep learning model via additional penalty terms?\n\nI. SWE increases with altitude\nII. Seasonal variations in SWE\nIII. Known portions of data that have no SWE",
            "options": [
                "I and II",
                "I and III",
                "II and III",
                "All"
            ],
            "correct_answer": 3,
            "correct_letter": "D",
            "detailed_solution": "The authors incorporated elevation/altitude gradients, seasonal temporal patterns, and zero-snow constraints (known snow-free regions) as physics-informed regularization penalties in the cGAN objective.",
            "image": None
        },
        {
            "id": "ml_ass8_q4",
            "course": "Machine Learning for Earth System Sciences",
            "course_id": "ml",
            "assignment": 8,
            "question_number": 4,
            "question": "In the study - Read JS, Jia X, Willard J, Appling AP, Zwart JA, Oliver SK, Karpatne A, Hansen G J, Hanson PC, Watkins W, Steinbach M. Process-guided deep learning predictions of lake water temperature. Water Resources Research. 2019 Nov;55(11):9173-90, the authors experimented with 3 models (Process Based Model, Deep Learning based empirical only model and Process-Guided Deep Learning model) to predict the lake temperatures for lake Mendota. Which of the following models suffered the most loss in accuracy when the amount of training data was artificially reduced?",
            "options": [
                "Process based Model.",
                "Deep Learning based empirical only model.",
                "Process-Guided Deep Learning Model",
                "Deep Learning based empirical only models and Process-Guided Deep Learning Models suffered the same loss of accuracy."
            ],
            "correct_answer": 1,
            "correct_letter": "B",
            "detailed_solution": "Pure empirical deep learning models lack physical inductive biases and degrade rapidly in low-data regimes. Process-guided models (PGDL) leverage physics principles to remain resilient even with limited training data.",
            "image": None
        },
        {
            "id": "ml_ass8_q5",
            "course": "Machine Learning for Earth System Sciences",
            "course_id": "ml",
            "assignment": 8,
            "question_number": 5,
            "question": "Which one of the following is generally not considered a limitation of process-based Earth system models?",
            "options": [
                "Requirement of Model Calibration",
                "Representation of unresolved processes through sub-grid parameterization",
                "High computational cost",
                "Use of physics-based governing equations"
            ],
            "correct_answer": 3,
            "correct_letter": "D",
            "detailed_solution": "The use of physics-based governing equations (conservation of mass, momentum, and energy) is the foundational strength and core principle of process-based models, not a limitation.",
            "image": None
        },
        {
            "id": "ml_ass8_q6",
            "course": "Machine Learning for Earth System Sciences",
            "course_id": "ml",
            "assignment": 8,
            "question_number": 6,
            "question": "In the study - Chen L, Fang B, Zhao L, Zang Y, Liu W, Chen Y, Wang C, Li J. DeepUrbanDownscale: A physics informed deep learning framework for high-resolution urban surface temperature estimation via 3D point clouds. International Journal of Applied Earth Observation and Geoinformation. 2022 Feb 1;106:102650, the role of the descriptor Local Spatial Coefficient Index (LSCI) is best described as:",
            "options": [
                "To aggregate the potential factors that influence the local-scale urban surface temperature.",
                "To incorporate the heterogeneity of the urban surface (water, building, vegetation, soil).",
                "To map the 3-D point cloud of the local region into the deep learning model",
                "To incorporate the verticality of the local urban surface"
            ],
            "correct_answer": 0,
            "correct_letter": "A",
            "detailed_solution": "The Local Spatial Coefficient Index (LSCI) aggregates diverse local-scale spatial driving factors (solar radiation, sky view factor, thermal properties) influencing urban surface temperature.",
            "image": None
        },
        {
            "id": "ml_ass8_q7",
            "course": "Machine Learning for Earth System Sciences",
            "course_id": "ml",
            "assignment": 8,
            "question_number": 7,
            "question": "In the study - Kratzert F, Klotz D, Brenner C, Schulz K, Herrnegger M. Rainfall-runoff modelling using long short-term memory (LSTM) networks. Hydrology and Earth System Sciences. 2018 Nov 22;22(11):6005-22, LSTMs have been found to be performing better than traditional RNNs when one single network is used for trained individually for each basin, both for snow-influenced catchments and arid catchments. Which one of the following is/are important contributor(s) to these results as stated by the authors?\n\nI. The inability of a traditional RNN to learn long-term dependencies as compared to LSTMs\nII. A traditional RNN is trained to minimize the average RMSE between observation and simulation\nIII. Catchments contain processes with long-term dependencies such as snow accumulation and amount of precipitation.",
            "options": [
                "I",
                "II",
                "II and III",
                "I and III"
            ],
            "correct_answer": 3,
            "correct_letter": "D",
            "detailed_solution": "Hydrological catchments inherently involve multi-scale lag effects (snowpack storage, groundwater release) requiring memory of long-term dependencies (III), which standard RNNs fail to capture due to vanishing gradients, whereas LSTMs excel (I).",
            "image": None
        },
        {
            "id": "ml_ass8_q8",
            "course": "Machine Learning for Earth System Sciences",
            "course_id": "ml",
            "assignment": 8,
            "question_number": 8,
            "question": "Which of the following is NOT a probable cause of bias arising in a numerical model for weather and climate modelling?",
            "options": [
                "Data Assimilation",
                "Imperfect initial conditions",
                "Inaccurate physical parameterization",
                "Unresolved sub grid processes"
            ],
            "correct_answer": 0,
            "correct_letter": "A",
            "detailed_solution": "Data assimilation is specifically used to combine observational data with model forecasts to reduce errors and eliminate systematic bias, rather than introducing it.",
            "image": None
        },
        {
            "id": "ml_ass8_q9",
            "course": "Machine Learning for Earth System Sciences",
            "course_id": "ml",
            "assignment": 8,
            "question_number": 9,
            "question": "Match the items in the abbreviations in column-1 with the most relevant interpretation in column-2 in the context of Earth system science.\n\nAbbreviations:\nA1: GRACE\nA2: 4D-Var\nA3: CMIP\nA4: IPCC\n\nInterpretations:\nI1: Framework for comparing Earth System Models\nI2: Organization studying climate change\nI3: Data Assimilation Algorithm\nI4: Surface Mass and Total Water Storage through changes in Earth's gravity field",
            "options": [
                "(A1, I4), (A2, I3), (A3, I2), (A4, I1)",
                "(A1, I4), (A2, I1), (A3, I3), (A4, I2)",
                "(A1, I4), (A2, I3), (A3, I1), (A4, I2)",
                "(A1, I3), (A2, I4), (A3, I1), (A4, I2)"
            ],
            "correct_answer": 2,
            "correct_letter": "C",
            "detailed_solution": "GRACE detects Earth gravity changes to quantify total water storage (I4); 4D-Var is a four-dimensional variational data assimilation scheme (I3); CMIP is the Coupled Model Intercomparison Project (I1); IPCC is the Intergovernmental Panel on Climate Change (I2).",
            "image": None
        },
        {
            "id": "ml_ass8_q10",
            "course": "Machine Learning for Earth System Sciences",
            "course_id": "ml",
            "assignment": 8,
            "question_number": 10,
            "question": "In the study - Mansfield LA, Nowack PJ, Kasoar M, Everitt RG, Collins WJ, Voulgarakis A. Predicting global patterns of long-term climate change from short-term simulations using machine learning. npj Climate and Atmospheric Science. 2020 Nov 19;3(1):1-9, the authors advocate the need of a surrogate model for studying the mapping between short-term and long-term response patterns against various forcings within a given GCM. What is the most important advantage of such a surrogate model?",
            "options": [
                "Once designed it can replace computationally expensive numerical models forever",
                "They are fast and more accurate than NWP models",
                "Once learned, this surrogate model can be used to rapidly predict long-term responses for unseen inputs (climate forcing scenarios).",
                "Surrogate models are always interpretable by design."
            ],
            "correct_answer": 2,
            "correct_letter": "C",
            "detailed_solution": "Surrogate/emulator models provide near-instantaneous approximations, allowing researchers to evaluate hundreds of unseen future emissions and forcing scenarios without executing multi-month supercomputer runs.",
            "image": None
        }
    ]

# -------------------------------------------------------------
# 3. SCALABLE DATA SCIENCE ASSIGNMENT 1 (20 Questions)
# -------------------------------------------------------------

def get_scalable_1():
    # Extracted from Assignment 1 PDF
    return [
        {
            "id": "scalable_ass1_q1",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 1,
            "question": "A data scientist launches four independent worker nodes in a distributed computing cluster. Each node processes between 1 and 6 GB of data per minute, depending on system load, with all rates equally likely. The total throughput is defined as the sum of the throughputs of the four nodes. What is the probability that the cluster achieves a throughput of at least 22 GB/min?",
            "options": [
                "10 / 1296",
                "15 / 1296",
                "20 / 1296"
            ],
            "correct_answer": 1,
            "correct_letter": "B",
            "detailed_solution": "Total outcomes = 6^4 = 1296. For total throughput >= 22, the possible sums are 22, 23, 24:\n• 24: (6,6,6,6) -> 1 way.\n• 23: one 5 and three 6's -> 4C1 = 4 ways.\n• 22: one 4 and three 6's -> 4C1 = 4 ways, or two 5's and two 6's -> 4C2 = 6 ways.\nThus favorable outcomes = 1 + 4 + 4 + 6 = 15.\nHence P(throughput >= 22) = 15 / 1296.",
            "image": None
        },
        {
            "id": "scalable_ass1_q2",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 2,
            "question": "Let A and B be two events such that P(A) = 0.7 and P(A ∩ B) = 0.25. What is P(A ∩ B^c)?",
            "options": [
                "0.45",
                "0.25",
                "0.70"
            ],
            "correct_answer": 0,
            "correct_letter": "A",
            "detailed_solution": "Since event A can be partitioned into disjoint events: A = (A ∩ B) ∪ (A ∩ B^c), we have P(A) = P(A ∩ B) + P(A ∩ B^c). Therefore, P(A ∩ B^c) = P(A) - P(A ∩ B) = 0.7 - 0.25 = 0.45.",
            "image": None
        },
        {
            "id": "scalable_ass1_q3",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 3,
            "question": "There are 200 students enrolled in the Scalable Data Science course. The average number of hours spent per week by a student on course-related activities is 15 hours. How many students could be spending 75 hours or more per week on the course?",
            "options": [
                "At least 45",
                "At most 40",
                "Can't say"
            ],
            "correct_answer": 1,
            "correct_letter": "B",
            "detailed_solution": "By Markov's inequality, P(X >= 75) <= E[X] / 75 = 15 / 75 = 1/5. Hence, the number of students spending at least 75 hours per week is at most 200 * (1/5) = 40.",
            "image": None
        },
        {
            "id": "scalable_ass1_q4",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 4,
            "question": "A machine learning algorithm is run independently n times, and each run succeeds with probability p. Let X be the number of successful runs. Assuming p < α < 1, which of the following bounds the probability that at least an α-fraction of the runs are successful?",
            "options": [
                "p(1 - p) / (n(α - p))",
                "p(1 - p) / (n(α - p)^2)",
                "Given information is incomplete"
            ],
            "correct_answer": 1,
            "correct_letter": "B",
            "detailed_solution": "Since E[X] = np and Var(X) = np(1 - p), by Chebyshev's inequality:\nP(X >= αn) <= P(|X - np| >= n(α - p)) <= Var(X) / (n^2 (α - p)^2) = p(1 - p) / (n(α - p)^2).",
            "image": None
        },
        {
            "id": "scalable_ass1_q5",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 5,
            "question": "Consider the following game of dice: A player begins with a score of 0. The player rolls two dice at each turn t, and all of the numbers 1, 2, 3, 4, 5 or 6 are equally likely to come up. This is followed by taking product of two numbers on the two dice. The game ends when product at one turn becomes > 20. On the contrary, if the product is <= 20, the product p gets added to their scores and a new turn t is awaited. What is the probability of the player's score to be zero at the end of the game?",
            "options": [
                "1 / 3",
                "1 / 6",
                "1 / 2"
            ],
            "correct_answer": 1,
            "correct_letter": "B",
            "detailed_solution": "The player's score is zero if the game ends on the very first turn. That happens when the product of the two dice > 20 on turn 1. The pairs with product > 20 are: (4,6), (6,4), (5,5), (5,6), (6,5), (6,6). Total 6 pairs out of 36. Probability = 6/36 = 1/6.",
            "image": None
        },
        {
            "id": "scalable_ass1_q6",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 6,
            "question": "Let A be a random variable such that E[A] = 50 and A > 10. Then, which of the following is correct?",
            "options": [
                "E[1 / (A - 10)] >= 1 / 40",
                "E[1 / (A - 10)] >= 1 / 10",
                "E[1 / (A - 10)] < 40",
                "E[1 / (A - 10)] = 40"
            ],
            "correct_answer": 0,
            "correct_letter": "A",
            "detailed_solution": "Since g(x) = 1/x is convex for x > 0, Jensen's inequality gives E[1 / (A - 10)] >= 1 / (E[A] - 10) = 1 / (50 - 10) = 1/40.",
            "image": None
        },
        {
            "id": "scalable_ass1_q7",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 7,
            "question": "A deck of 52 cards is shuffled followed by division into two halves of 26 cards each. From one of the halves, one card is drawn which turns out to be an ace. The ace is then put in the second half deck. This half is shuffled followed by drawing a card from it. What is the probability that the drawn card is an ace?",
            "options": [
                "0.094",
                "0.062",
                "0.071"
            ],
            "correct_answer": 0,
            "correct_letter": "A",
            "detailed_solution": "The original deck has 4 aces. By symmetry and linearity of expectation, the second half initially has an expected number of aces equal to 3 * (26/51) ≈ 1.529 aces. Adding the transferred ace gives 2.529 aces among 27 cards. The probability is (1 + 3 * 26/51) / 27 ≈ 0.094.",
            "image": None
        },
        {
            "id": "scalable_ass1_q8",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 8,
            "question": "Suppose there are 3 coins, out of which one is fair and rest two are biased. Let us pick one of the coins uniformly at random and flip it 3 times. The three coins come with heads with a probability of 0.6, 0.1 and 0.5. What is the probability of the event HTT where H stands for heads and T for tails?",
            "options": [
                "302 / 1000",
                "302 / 3000",
                "177 / 1000"
            ],
            "correct_answer": 1,
            "correct_letter": "B",
            "detailed_solution": "By the law of total probability:\nP(HTT) = (1/3) * [0.6 * 0.4^2 + 0.1 * 0.9^2 + 0.5 * 0.5^2]\n= (1/3) * [0.096 + 0.081 + 0.125] = (1/3) * 0.302 = 302 / 3000.",
            "image": None
        },
        {
            "id": "scalable_ass1_q9",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 9,
            "question": "For every real matrix A ∈ R^(m×n), the matrices A^T A and A A^T have exactly the same eigenvalues.",
            "options": [
                "True",
                "False"
            ],
            "correct_answer": 1,
            "correct_letter": "B",
            "detailed_solution": "False. The matrices A^T A and A A^T have the same non-zero eigenvalues, but they may have different numbers of zero eigenvalues since their dimensions (n×n vs m×m) can differ when m != n.",
            "image": None
        },
        {
            "id": "scalable_ass1_q10",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 10,
            "question": "A reflection matrix in R^n is given by R = I - 2 v v^T, where v is a unit vector. If the vector v itself is reflected by R, by what factor is it scaled?",
            "options": [
                "1",
                "-1",
                "2",
                "-2"
            ],
            "correct_answer": 1,
            "correct_letter": "B",
            "detailed_solution": "R v = (I - 2 v v^T) v = v - 2 v (v^T v). Since v is a unit vector, v^T v = 1. Thus R v = v - 2 v = -v = (-1) v. Hence it is scaled by -1.",
            "image": None
        },
        {
            "id": "scalable_ass1_q11",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 11,
            "question": "Let M be a 4 × 4 matrix with real values, and let x ∈ R^4 be a non-zero vector. What can we say about the vectors x, M x, M^2 x, M^3 x, and M^4 x?",
            "options": [
                "Linearly independent",
                "Linearly dependent",
                "Linearly independent iff M is a symmetric matrix",
                "Cannot be determined."
            ],
            "correct_answer": 1,
            "correct_letter": "B",
            "detailed_solution": "In R^4, the maximum number of linearly independent vectors is 4. Here we have 5 vectors in a 4-dimensional space, so they must be linearly dependent.",
            "image": None
        },
        {
            "id": "scalable_ass1_q12",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 12,
            "question": "Which of the following is equivalent to saying that B is a basis of a vector space V?",
            "options": [
                "B is a minimal generating set of V.",
                "B is a maximal linearly independent subset of V.",
                "Every vector in V has a unique representation as a linear combination of vectors in B.",
                "All of the above."
            ],
            "correct_answer": 3,
            "correct_letter": "D",
            "detailed_solution": "All statements are equivalent definitions/properties of a basis in linear algebra.",
            "image": None
        },
        {
            "id": "scalable_ass1_q13",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 13,
            "question": "Let X ∈ R^(n×d) be a mean-centered data matrix. Suppose you perform PCA by computing the eigenvectors of the covariance matrix and select the top k eigenvectors to form the projection matrix E ∈ R^(d×k). You obtain the lower-dimensional representation of the data as: Y = X E. Which of the following statements is correct regarding the ability to reconstruct X from Y?",
            "options": [
                "X can never be recovered from Y.",
                "X can always be recovered from Y.",
                "X can be exactly recovered from Y only if all d eigenvectors are used in E.",
                "X can be recovered even when only the top k < d eigenvectors are used."
            ],
            "correct_answer": 2,
            "correct_letter": "C",
            "detailed_solution": "Exact reconstruction X = Y E^T requires E to form a full orthonormal basis for R^d, which happens when all d eigenvectors are retained.",
            "image": None
        },
        {
            "id": "scalable_ass1_q14",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 14,
            "question": "A function f is known to be uniformly continuous on a closed interval [a, b]. Which of the following conclusions can always be drawn?",
            "options": [
                "f has an interior maximum.",
                "f is bounded.",
                "f is differentiable.",
                "f' is continuous."
            ],
            "correct_answer": 1,
            "correct_letter": "B",
            "detailed_solution": "A continuous (or uniformly continuous) function on a compact set [a, b] is always bounded (by the Extreme Value Theorem). It does not need to be differentiable.",
            "image": None
        },
        {
            "id": "scalable_ass1_q15",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 15,
            "question": "A dataset is generated from a nonlinear function with additive Gaussian noise. Polynomial regression models of degree 1, 2, and 10 are fitted using 20 training examples. Since higher-degree models contain all features of lower-degree models, which of the following statements is correct?",
            "options": [
                "The 1st-order model has the lowest training error.",
                "The 2nd-order model has the lowest training error and the 10th-order model has the lowest test error.",
                "The 1st-order model has the highest training error and the 10th-order model has the lowest training error.",
                "None of the above."
            ],
            "correct_answer": 2,
            "correct_letter": "C",
            "detailed_solution": "Since polynomial models are nested, increasing the degree expands the hypothesis class. Thus, training MSE monotonically decreases with degree: the 1st-order model has highest training error and 10th-order has lowest training error.",
            "image": None
        },
        {
            "id": "scalable_ass1_q16",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 16,
            "question": "A data scientist runs the k-means algorithm multiple times with different random initial centroids on the same unlabeled dataset. Which criterion should be used to select the best clustering among the different runs?",
            "options": [
                "Use the labels of the data.",
                "Select the clustering from the last run.",
                "Select the clustering that minimizes the within-cluster sum of squared distances.",
                "Any clustering is equally good."
            ],
            "correct_answer": 2,
            "correct_letter": "C",
            "detailed_solution": "The k-means objective is to minimize the within-cluster sum of squared errors (inertia). The best run is the one that achieves the minimum objective value.",
            "image": None
        },
        {
            "id": "scalable_ass1_q17",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 17,
            "question": "A machine learning engineer collects m training samples from a Gaussian distribution and computes the sample mean X̄. Which of the following statements about the squared error sum_{i=1}^m (X_i - a)^2 is true?",
            "options": [
                "It is minimized when a = X̄.",
                "It is minimized when a = μ.",
                "It has the same value for a = X̄ and a = μ.",
                "It is independent of a."
            ],
            "correct_answer": 0,
            "correct_letter": "A",
            "detailed_solution": "The sample mean X̄ = (1/m) sum X_i is the unique minimizer of the sum of squared deviations sum (X_i - a)^2.",
            "image": None
        },
        {
            "id": "scalable_ass1_q18",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 18,
            "question": "The closed-form solution for linear regression is given by β = (A^T A)^(-1) A^T Y. When A^T A is ill-conditioned due to multicollinearity, ridge regression adds an L2 penalty λ ||β||_2^2. What is the resulting closed-form solution?",
            "options": [
                "β = (A^T A + λ I)^(-1) A^T Y",
                "β = (A^T A)^(-1) A^T Y - λ I",
                "β = λ (A^T A)^(-1) A^T Y",
                "β = (A^T A - λ I)^(-1) A^T Y"
            ],
            "correct_answer": 0,
            "correct_letter": "A",
            "detailed_solution": "Minimizing ||A β - Y||_2^2 + λ ||β||_2^2 yields the gradient 2 A^T(A β - Y) + 2 λ β = 0 => (A^T A + λ I) β = A^T Y => β = (A^T A + λ I)^(-1) A^T Y.",
            "image": None
        },
        {
            "id": "scalable_ass1_q19",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 19,
            "question": "How can one solve a clustering algorithm stuck at a bad local optima?",
            "options": [
                "Fix a seed value.",
                "Use several random initialisations",
                "Increase the number of data points",
                "Both (a) and (b)"
            ],
            "correct_answer": 1,
            "correct_letter": "B",
            "detailed_solution": "Restarting the algorithm with multiple random initializations (e.g. k-means++) explores different basins of attraction and avoids poor local minima.",
            "image": None
        },
        {
            "id": "scalable_ass1_q20",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 1,
            "question_number": 20,
            "question": "Among all cylinders having the same volume V, which of the following conditions is satisfied by the cylinder with the smallest surface area?",
            "options": [
                "h = 2r",
                "h = sqrt(π r^2)",
                "h = V / (π r)",
                "There are infinitely many optimal solutions."
            ],
            "correct_answer": 0,
            "correct_letter": "A",
            "detailed_solution": "Surface area S = 2 π r^2 + 2 π r h with V = π r^2 h => h = V / (π r^2). Substituting gives S(r) = 2 π r^2 + 2 V / r. Setting dS/dr = 4 π r - 2 V / r^2 = 0 => 2 π r^3 = V = π r^2 h => h = 2r.",
            "image": None
        }
    ]

# -------------------------------------------------------------
# 4. SCALABLE DATA SCIENCE ASSIGNMENTS 2, 3, 4 (PDFs with Solutions)
# -------------------------------------------------------------

def extract_scalable_pdf(ass_num, path):
    reader = pypdf.PdfReader(path)
    text = '\n'.join([p.extract_text() or '' for p in reader.pages])

    indices = []
    curr = 1
    pos = 0
    while curr <= 20:
        pattern = rf'(?:^|\n)\s*{curr}\s*\.\s*'
        m = re.search(pattern, text[pos:])
        if m:
            actual_start = pos + m.start()
            indices.append((curr, actual_start, pos + m.end()))
            pos = pos + m.end()
            curr += 1
        else:
            break
            
    q_blocks = []
    for i in range(len(indices)):
        start = indices[i][2]
        end = indices[i+1][1] if i + 1 < len(indices) else len(text)
        q_blocks.append((indices[i][0], text[start:end].strip()))

    results = []
    for q_num, block in q_blocks:
        ans_letter = None
        sol = ''

        # Match Solution Answer: (B) or SolutionAnswer: (B)
        m_sol = re.search(r'Solution\s*(?:Answer\s*:?\s*)?\(?([A-Da-d])\)?(?:\s*[:\.\)]\s*)?([\s\S]*)', block)
        if m_sol:
            ans_letter = m_sol.group(1).upper()
            sol = m_sol.group(2).strip()
            q_and_opts = block[:m_sol.start()].strip()
        else:
            m_alt = re.search(r'\n\s*\(([A-Da-d])\)\s*\n([\s\S]*)', block)
            if m_alt:
                ans_letter = m_alt.group(1).upper()
                sol = m_alt.group(2).strip()
                q_and_opts = block[:m_alt.start()].strip()
            else:
                m_ans = re.search(r'Answer\s*:\s*\(?([A-Da-d])\)?', block)
                if m_ans:
                    ans_letter = m_ans.group(1).upper()
                    q_and_opts = block[:m_ans.start()].strip()
                else:
                    q_and_opts = block

        # Extract options
        # Options could be (a), (b), (c), (d) or A., B., C., D. or A, B, C, D
        opt_matches = list(re.finditer(r'(?:^|\n)\s*(\(?[A-Da-d]\)?[\.\)])\s*', q_and_opts))
        if len(opt_matches) >= 2:
            # use opt matches
            num_opts = 4 if len(opt_matches) >= 4 else len(opt_matches)
            # take the last num_opts matches
            selected_opts = opt_matches[-num_opts:]
            q_text = q_and_opts[:selected_opts[0].start()].strip()
            opts = []
            for k in range(len(selected_opts)):
                o_start = selected_opts[k].end()
                o_end = selected_opts[k+1].start() if k + 1 < len(selected_opts) else len(q_and_opts)
                opts.append(q_and_opts[o_start:o_end].strip())
        else:
            # Fallback for questions where options are formatted as A, B, C without dot
            opt_m2 = list(re.finditer(r'(?:^|\n)\s*([A-D])\s+(?=[^\n]+)', q_and_opts))
            if len(opt_m2) >= 2:
                num_opts = 4 if len(opt_m2) >= 4 else len(opt_m2)
                selected_opts = opt_m2[-num_opts:]
                q_text = q_and_opts[:selected_opts[0].start()].strip()
                opts = []
                for k in range(len(selected_opts)):
                    o_start = selected_opts[k].end()
                    o_end = selected_opts[k+1].start() if k + 1 < len(selected_opts) else len(q_and_opts)
                    opts.append(q_and_opts[o_start:o_end].strip())
            else:
                q_text = q_and_opts
                opts = []

        ans_index = ord(ans_letter) - ord('A') if ans_letter in ['A', 'B', 'C', 'D'] else -1

        results.append({
            "id": f"scalable_ass{ass_num}_q{q_num}",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": ass_num,
            "question_number": q_num,
            "question": q_text,
            "options": opts,
            "correct_answer": ans_index,
            "correct_letter": ans_letter,
            "detailed_solution": sol,
            "image": None
        })
    return results

# -------------------------------------------------------------
# 5. SCALABLE DATA SCIENCE ASSIGNMENTS 5, 6, 7, 8 (Screenshots Transcribed)
# -------------------------------------------------------------

def get_scalable_5():
    return [
        {
            "id": "scalable_ass5_q1",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 5,
            "question_number": 1,
            "question": "Given the matrix A = [[1, 2], [3, 4]], find matrices Q and R such that A = Q R, where Q has orthonormal columns and R is upper-triangular with positive diagonal entries. Which of the following pairs (Q, R) is the correct QR decomposition of A?",
            "options": [
                "Q = [[0.3162, 0.9487], [0.9487, -0.3162]], R = [[3.1623, 4.4271], [0, 0.6325]]",
                "Q = [[0.4472, 0.8944], [0.8944, -0.4472]], R = [[2.2361, 3.1305], [0, 0.8944]]",
                "Q = [[1, 0], [0, 1]], R = [[1, 2], [3, 4]]",
                "Q = [[0.7071, 0.7071], [0.7071, -0.7071]], R = [[2.8284, 4.2426], [0, 1.4142]]"
            ],
            "correct_answer": 0,
            "correct_letter": "A",
            "detailed_solution": "First column of A is [1, 3]^T with norm sqrt(10) ≈ 3.1623. First column of Q is [1, 3]^T / sqrt(10) ≈ [0.3162, 0.9487]^T. R_11 = 3.1623. Matching Q and R yields option A.",
            "image": None
        },
        {
            "id": "scalable_ass5_q2",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 5,
            "question_number": 2,
            "question": "For a dataset with n samples and d features, what is the standard space (memory) complexity required to compute PCA via the covariance-matrix approach?",
            "options": [
                "O(n + d)",
                "O(nd)",
                "O(nd + d^2)",
                "O(n^2 + d^2)"
            ],
            "correct_answer": 2,
            "correct_letter": "C",
            "detailed_solution": "Storing the dataset requires O(nd) memory, and storing the d × d sample covariance matrix requires O(d^2) memory. Thus total space is O(nd + d^2).",
            "image": None
        },
        {
            "id": "scalable_ass5_q3",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 5,
            "question_number": 3,
            "question": "The Johnson-Lindenstrauss lemma bounds the embedding dimension D needed for M points with error tolerance ε as D >= 4 log(M) / (ε^2 / 2 - ε^3 / 3). If D and ε are instead held fixed, what is the maximum number of points M that can be embedded while still preserving pairwise distances with high probability?",
            "options": [
                "M <= exp{ D(ε^2 / 2 - ε^3 / 3) / 4 }",
                "M >= exp{ D(ε^2 / 2 - ε^3 / 3) / 4 }",
                "M <= 4 log(D) / (ε^2 / 2 - ε^3 / 3)",
                "M <= D / (4 (ε^2 / 2 - ε^3 / 3))"
            ],
            "correct_answer": 0,
            "correct_letter": "A",
            "detailed_solution": "From D >= 4 log(M) / (ε^2 / 2 - ε^3 / 3), multiplying across yields log(M) <= D(ε^2 / 2 - ε^3 / 3) / 4, so M <= exp{ D(ε^2 / 2 - ε^3 / 3) / 4 }.",
            "image": None
        },
        {
            "id": "scalable_ass5_q4",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 5,
            "question_number": 4,
            "question": "In sparse random projection, each entry of the matrix R is set to +1/sqrt(s) with probability 1/(2s), to -1/sqrt(s) with probability 1/(2s), and to 0 otherwise. What is the probability that a given entry is strictly positive?",
            "options": [
                "1 / s",
                "1 / (2s)",
                "1 - 1/s",
                "(1/2)(1 - 1/s)"
            ],
            "correct_answer": 1,
            "correct_letter": "B",
            "detailed_solution": "The entry is strictly positive only when it equals +1/sqrt(s), which occurs with probability exactly 1/(2s).",
            "image": None
        },
        {
            "id": "scalable_ass5_q5",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 5,
            "question_number": 5,
            "question": "Using a randomized algorithm (e.g., a randomized range finder) to compute a rank-k truncated SVD of a general m × n matrix, what is the typical time complexity?",
            "options": [
                "O(mnk)",
                "O(mn log k + (m + n)k^2)",
                "O(m^2 n + mn^2)",
                "O(k^3)"
            ],
            "correct_answer": 1,
            "correct_letter": "B",
            "detailed_solution": "Randomized SVD with structured random projections runs in O(mn log k + (m + n)k^2) time, substantially faster than deterministic O(mnk) or O(mn min(m,n)).",
            "image": None
        },
        {
            "id": "scalable_ass5_q6",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 5,
            "question_number": 6,
            "question": "We form a 96 × 8 matrix M using the Kronecker product M = 1_12 ⊗ I_8, where 1_12 is a 12 × 1 column vector of all ones and I_8 is the 8 × 8 identity matrix. What is the leverage score of each row of M?",
            "options": [
                "12",
                "1",
                "1 / 12",
                "1 / 8"
            ],
            "correct_answer": 2,
            "correct_letter": "C",
            "detailed_solution": "The matrix M has orthogonal columns with M^T M = (1_12^T 1_12) ⊗ (I_8^T I_8) = 12 I_8. Orthonormal basis matrix U = M / sqrt(12). The leverage score of each row i is ||u_i||^2 = 1 / 12.",
            "image": None
        },
        {
            "id": "scalable_ass5_q7",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 5,
            "question_number": 7,
            "question": "In the randomized projection algorithm, rows are sampled with probability proportional to leverage scores π_i and then rescaled by (1 / (r π_i))^(1/2). If this rescaling step were omitted, what would be the effect on the induced smaller problem?",
            "options": [
                "It would remain an unbiased estimator, just with slightly higher computational cost.",
                "The induced problem would become biased, since high-leverage rows would be over-represented without correction.",
                "The solution accuracy would improve, since leverage-based sampling is already optimal.",
                "The induced problem would become singular and have no solution."
            ],
            "correct_answer": 1,
            "correct_letter": "B",
            "detailed_solution": "Non-uniform sampling without weight correction biases the expectation E[S^T S] != I, over-weighting high leverage rows and causing a biased estimate.",
            "image": None
        },
        {
            "id": "scalable_ass5_q8",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 5,
            "question_number": 8,
            "question": "We generate a 256 × 256 Hadamard matrix H (entries ±1) without any normalization. We then form a new matrix M by selecting the first 30 columns of H. What is the largest singular value of M?",
            "options": [
                "14.000",
                "15.000",
                "16.000",
                "17.000"
            ],
            "correct_answer": 2,
            "correct_letter": "C",
            "detailed_solution": "The columns of an unnormalized Hadamard matrix of order n are mutually orthogonal, and each column has norm sqrt(n). Here n = 256, so each column norm is sqrt(256) = 16. M^T M = 256 I_30, so every singular value of M is sqrt(256) = 16.000.",
            "image": None
        },
        {
            "id": "scalable_ass5_q9",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 5,
            "question_number": 9,
            "question": "In the Column Subset Selection Problem (CSSP), columns of a matrix A are sampled with probability proportional to their column leverage scores. The probability of sampling a specific column j is directly proportional to which of the following?",
            "options": [
                "The target rank, k.",
                "The Frobenius norm of the matrix of top k right singular vectors, V_k.",
                "The square of the Euclidean norm of the j-th row of the top k right singular vectors matrix V_k.",
                "The singular values of the original matrix A."
            ],
            "correct_answer": 2,
            "correct_letter": "C",
            "detailed_solution": "The column leverage scores of A with respect to rank k are given by the squared Euclidean norms of the rows of V_k (i.e. ||(V_k)_j,:||^2).",
            "image": None
        },
        {
            "id": "scalable_ass5_q10",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 5,
            "question_number": 10,
            "question": "An n × d orthogonal matrix U (where n >> d) is sampled via leverage-score sampling to form a smaller r × d matrix Ũ. As the number of sampled rows r increases (holding n and d fixed), what happens to the approximation error ||Ũ^T Ũ - I_d||?",
            "options": [
                "The error increases, since more sampling introduces more noise.",
                "The error decreases, as Ũ better approximates an orthogonal matrix, at the cost of higher computation and storage.",
                "The error stays exactly constant, independent of r.",
                "The error becomes exactly zero once r > d."
            ],
            "correct_answer": 1,
            "correct_letter": "B",
            "detailed_solution": "By matrix concentration inequalities (e.g. Matrix Chernoff), the spectral norm error ||Ũ^T Ũ - I_d|| decreases as O(sqrt(d log d / r)) as r increases.",
            "image": None
        }
    ]

def get_scalable_6():
    return [
        {
            "id": "scalable_ass6_q1",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 6,
            "question_number": 1,
            "question": "Which component of the Hadoop ecosystem is primarily responsible for reliably storing large files by splitting them into blocks distributed across the cluster?",
            "options": [
                "HDFS",
                "YARN",
                "MapReduce"
            ],
            "correct_answer": 0,
            "correct_letter": "a",
            "detailed_solution": "HDFS (Hadoop Distributed File System) stores large datasets reliably across machines by partitioning files into blocks and replicating them.",
            "image": None
        },
        {
            "id": "scalable_ass6_q2",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 6,
            "question_number": 2,
            "question": "A partitioner decides which reducer each mapper's key-value pair is sent to. Is it always safe to use any arbitrary hash function as the partitioner without further consideration?",
            "options": [
                "Yes.",
                "No."
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "No. An arbitrary hash function could create extreme data skew where one reducer is overwhelmed while others remain idle, or could produce negative hash values if not properly handled.",
            "image": None
        },
        {
            "id": "scalable_ass6_q3",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 6,
            "question_number": 3,
            "question": "If a worker node fails to report progress within a timeout period during task execution, the master simply waits indefinitely for that worker to recover before proceeding. True/False?",
            "options": [
                "True",
                "False"
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "False. When a heartbeat timeout expires, the master marks the worker as failed and re-schedules the in-progress tasks on other healthy worker nodes.",
            "image": None
        },
        {
            "id": "scalable_ass6_q4",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 6,
            "question_number": 4,
            "question": "What happens when a MapReduce job is configured with more reduce tasks than the number of distinct keys produced by the mappers?",
            "options": [
                "The job throws an error since reducers cannot exceed distinct keys.",
                "Some reduce tasks will receive no keys at all and complete with empty output.",
                "All reduce tasks are merged automatically into fewer reducers.",
                "The extra reduce tasks are ignored and never scheduled."
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "The partitioner hashes keys into buckets modulo the number of reducers. If reducers > distinct keys, empty partitions are created, and those reducers finish with 0 records and empty output files.",
            "image": None
        },
        {
            "id": "scalable_ass6_q5",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 6,
            "question_number": 5,
            "question": "During an HDFS read operation, is it the client's sole responsibility to fetch data directly from every replica of a block simultaneously and reconcile the results?",
            "options": [
                "True",
                "False"
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "False. The client asks the NameNode for block locations and streams data from the closest available replica, not from every replica simultaneously.",
            "image": None
        },
        {
            "id": "scalable_ass6_q6",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 6,
            "question_number": 6,
            "question": "Do DataNodes periodically send heartbeat and block-report messages to the NameNode to confirm their liveness and current block holdings?",
            "options": [
                "Yes.",
                "No."
            ],
            "correct_answer": 0,
            "correct_letter": "a",
            "detailed_solution": "Yes. DataNodes regularly send heartbeats (every 3 seconds by default) and periodic block reports to inform the NameNode of their status and stored blocks.",
            "image": None
        },
        {
            "id": "scalable_ass6_q7",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 6,
            "question_number": 7,
            "question": "A given key can be sent to different reducers across different runs of the same MapReduce job on the same cluster configuration, as long as the partitioning function is deterministic. True/False?",
            "options": [
                "True",
                "False"
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "False. A deterministic partitioning function with fixed reducer count guarantees that the same key always hashes to the exact same reducer partition index.",
            "image": None
        },
        {
            "id": "scalable_ass6_q8",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 6,
            "question_number": 8,
            "question": "Consider the same standard wordcount program with four mappers producing:\nMapper 1: (cat, 2) (dog, 4)\nMapper 2: (fox, 1) (fox, 9)\nMapper 3: (cat, 6) (fox, 3)\nMapper 4: (dog, 5) (fox, 7)\nWhat key-value pairs are fed as input to the reducer with a Combiner applied at each mapper (combiner sums values locally per mapper before shuffling)?",
            "options": [
                "(cat, 2) (dog, 4) (fox, 1) (fox, 9) (cat, 6) (fox, 3) (dog, 5) (fox, 7)",
                "(cat, [8]) (dog, [9]) (fox, [20])",
                "(cat, 2) (cat, 6) (dog, 4) (dog, 5) (fox, 10) (fox, 10)"
            ],
            "correct_answer": 2,
            "correct_letter": "c",
            "detailed_solution": "Combiner runs locally per mapper:\nMapper 1: (cat, 2), (dog, 4)\nMapper 2: (fox, 1+9 = 10)\nMapper 3: (cat, 6), (fox, 3)\nMapper 4: (dog, 5), (fox, 7)\nInput to reducers: (cat, 2), (cat, 6), (dog, 4), (dog, 5), (fox, 10), (fox, 10).",
            "image": None
        },
        {
            "id": "scalable_ass6_q9",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 6,
            "question_number": 9,
            "question": "Below is a sample map-reduce program that computes the product of two matrices of dimensions m × k and k × n, where mapper emits, for each entry of matrix 0, keys (row, i) for i = 1, ..., n, and for each entry of matrix 1, keys (i, col) for i = 1, ..., m. Complete the following reducer code, which receives all values sharing a key (an output cell) and must compute the corresponding dot-product entry:\n\nReducer Code:\nfor key, values in grouped_by_key:\n    row, col = key\n    entries_from_0 = {}\n    entries_from_1 = {}\n    for (matrixid, idx, value) in values:\n        if matrixid == 0:\n            entries_from_0[idx] = value\n        else:\n            entries_from_1[idx] = value\n    result = 0\n    for k in entries_from_0:\n        result += -------------\n    print((row, col), result, sep='\\t')",
            "options": [
                "entries_from_0[k]",
                "entries_from_1[k]",
                "entries_from_0[k] * entries_from_1[k]",
                "entries_from_0[k] + entries_from_1[k]"
            ],
            "correct_answer": 2,
            "correct_letter": "c",
            "detailed_solution": "Matrix multiplication computes C[row, col] = sum_k A[row, k] * B[k, col]. Hence each term is the product: entries_from_0[k] * entries_from_1[k].",
            "image": None
        },
        {
            "id": "scalable_ass6_q10",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 6,
            "question_number": 10,
            "question": "Consider a map-reduce program that finds the maximum value seen so far per word in a stream, where mapper output is (word, value, sep='\\t') for each word. Complete the reducer code:\n\nReducer Code:\nmaxval = None\nprevword = NULL\nfor line in sys.stdin:\n    word, value = line.split(\"\\t\")\n    if prevword == word:\n        ------------ (1)\n    else:\n        if prevword != NULL:\n            ------------ (2)\n        maxval = value\n        prevword = word",
            "options": [
                "(1) maxval = max(maxval, value)  (2) print(prevword, maxval)",
                "(1) print(maxval)  (2) print(prevword)",
                "(1) maxval = value  (2) print(prevword, maxval)",
                "(1) maxval = max(maxval, value)  (2) print(word, maxval)"
            ],
            "correct_answer": 0,
            "correct_letter": "a",
            "detailed_solution": "While continuing on the same word, update maxval with max(maxval, value). When transitioning to a new word, print the previous word's maximum: print(prevword, maxval).",
            "image": None
        }
    ]

def get_scalable_7():
    return [
        {
            "id": "scalable_ass7_q1",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 7,
            "question_number": 1,
            "question": "In Scala, which of the following is used to define a mutable variable whose value can be reassigned after initialization?",
            "options": [
                "val",
                "var",
                "def",
                "final"
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "In Scala, `var` declares a mutable variable that can be reassigned, whereas `val` defines an immutable constant.",
            "image": None
        },
        {
            "id": "scalable_ass7_q2",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 7,
            "question_number": 2,
            "question": "What will be the output of the following Scala code?\n\nval list = List(2, 3, 4)\nlist.map(x => List(x, x + 10))",
            "options": [
                "List(List(2, 12), List(3, 13), List(4, 14))",
                "List(2, 12, 3, 13, 4, 14)",
                "List(2, 3, 4)",
                "Compilation Error"
            ],
            "correct_answer": 0,
            "correct_letter": "a",
            "detailed_solution": "The `map` method preserves outer list structure and wraps each mapped element into a sublist, yielding `List(List(2, 12), List(3, 13), List(4, 14))`. (If `flatMap` had been used, it would flatten to `List(2, 12, 3, 13, 4, 14)`).",
            "image": None
        },
        {
            "id": "scalable_ass7_q3",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 7,
            "question_number": 3,
            "question": "Which of the following statements about RDD fault tolerance is correct?",
            "options": [
                "RDDs achieve fault tolerance by maintaining full data replicas on disk at all times.",
                "RDDs achieve fault tolerance through lineage, recomputing lost partitions from the sequence of transformations that created them.",
                "RDDs cannot recover from node failures once created.",
                "RDDs achieve fault tolerance only if explicitly checkpointed."
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "RDDs maintain a lineage graph (DAG) of transformations, allowing Spark to reconstruct only the lost partitions upon a worker failure.",
            "image": None
        },
        {
            "id": "scalable_ass7_q4",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 7,
            "question_number": 4,
            "question": "Which of the following statements is true about transformations in Spark?",
            "options": [
                "They immediately execute and return a result to the driver.",
                "They are lazily evaluated and only build up a DAG of computation until an action is called.",
                "They always trigger a shuffle across the network.",
                "They can only be applied to key-value pair RDDs."
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "Spark transformations are lazy; they build a directed acyclic graph (DAG) of execution plan and do not run until an action (like `count()` or `collect()`) is invoked.",
            "image": None
        },
        {
            "id": "scalable_ass7_q5",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 7,
            "question_number": 5,
            "question": "In Spark, a narrow dependency implies:",
            "options": [
                "Each child RDD partition may depend on multiple parent partitions, requiring a shuffle.",
                "Each child RDD partition depends on at most one parent partition, so no shuffle is required.",
                "No dependency exists between RDDs.",
                "Partitioning is disabled."
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "In a narrow dependency (e.g. `map`, `filter`), each parent partition is used by at most one child partition, enabling pipelined execution without network shuffling.",
            "image": None
        },
        {
            "id": "scalable_ass7_q6",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 7,
            "question_number": 6,
            "question": "Which of the following is NOT a valid way to create an RDD in Spark?",
            "options": [
                "val rdd = sc.textFile(\"input.txt\")",
                "val rdd = sc.parallelize(Array(4, 5, 6))",
                "val rdd = sc.createRDD(1 to 20)",
                "val rdd = sc.makeRDD(1 to 20)"
            ],
            "correct_answer": 2,
            "correct_letter": "c",
            "detailed_solution": "`sc.createRDD` does not exist on SparkContext. Valid methods are `textFile`, `parallelize`, and `makeRDD`.",
            "image": None
        },
        {
            "id": "scalable_ass7_q7",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 7,
            "question_number": 7,
            "question": "Which function is used in Spark to combine values for each key by shuffling all values across the network without any local pre-aggregation, making it less efficient than its alternative?",
            "options": [
                "reduceByKey()",
                "groupByKey()",
                "collect()",
                "distinct()"
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "`groupByKey()` shuffles all values for each key across the network without map-side combining, which can cause significant GC pressure and out-of-memory errors compared to `reduceByKey()`.",
            "image": None
        },
        {
            "id": "scalable_ass7_q8",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 7,
            "question_number": 8,
            "question": "Consider the code:\n\nval rdd = sc.parallelize(List(3, 6, 9, 12))\nrdd.reduce((x, y) => x * y)\n\nWhat is the output?",
            "options": [
                "30",
                "1944",
                "12",
                "Error"
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "3 * 6 * 9 * 12 = 18 * 108 = 1944.",
            "image": None
        },
        {
            "id": "scalable_ass7_q9",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 7,
            "question_number": 9,
            "question": "What will the following Spark code return?\n\nval data = sc.parallelize(1 to 12)\nval result = data.filter(_ % 4 == 0).collect()",
            "options": [
                "Array(1, 2, 3, 5, 6, 7, 9, 10, 11)",
                "Array(4, 8, 12)",
                "Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)",
                "Compilation Error"
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "Numbers from 1 to 12 divisible by 4 are 4, 8, and 12.",
            "image": None
        },
        {
            "id": "scalable_ass7_q10",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 7,
            "question_number": 10,
            "question": "Consider the code:\n\nval rdd = sc.parallelize(List(\"cat\", \"dog\", \"cat\", \"cat\", \"dog\", \"fox\"))\nval counts = rdd.map((_, 1)).reduceByKey(_ + _).collect()\n\nWhat is the result?",
            "options": [
                "(\"cat\", 1), (\"dog\", 1), (\"cat\", 1), (\"cat\", 1), (\"dog\", 1), (\"fox\", 1)",
                "(\"cat\", 3), (\"dog\", 2), (\"fox\", 1)",
                "(\"cat\", 2), (\"dog\", 3), (\"fox\", 1)",
                "Error"
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "\"cat\" appears 3 times, \"dog\" appears 2 times, and \"fox\" appears 1 time.",
            "image": None
        }
    ]

def get_scalable_8():
    return [
        {
            "id": "scalable_ass8_q1",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 8,
            "question_number": 1,
            "question": "In distributed stochastic gradient descent (SGD) with an asynchronous parameter-server, what is the primary risk introduced when scaling up the number of workers?",
            "options": [
                "Workers are forced to idle while waiting for the slowest worker",
                "Stale gradients from slow workers can corrupt or destabilize the global update",
                "The model loses its ability to be updated at all",
                "Communication with the parameter server is entirely eliminated"
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "In asynchronous SGD, workers compute gradients based on outdated parameters. If staleness is high, these stale gradient updates destabilize optimization or cause divergence.",
            "image": None
        },
        {
            "id": "scalable_ass8_q2",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 8,
            "question_number": 2,
            "question": "Which consistency model enforces that every worker must always read the most recently updated parameter values, sacrificing throughput for correctness?",
            "options": [
                "Stale Synchronous Parallel (SSP)",
                "Eventual consistency",
                "Strong (strict) consistency",
                "Bounded asynchrony"
            ],
            "correct_answer": 2,
            "correct_letter": "c",
            "detailed_solution": "Strong (strict) consistency guarantees that any read sees the absolute latest write across all nodes, requiring synchronization barriers and reducing throughput.",
            "image": None
        },
        {
            "id": "scalable_ass8_q3",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 8,
            "question_number": 3,
            "question": "Which statement about k-means clustering is FALSE?",
            "options": [
                "k-means minimizes the within-cluster sum of squared Euclidean distances.",
                "k-means can converge to different local minima depending on initialization.",
                "k-means is guaranteed to converge to the global optimum regardless of initialization.",
                "The number of clusters k must be specified in advance."
            ],
            "correct_answer": 2,
            "correct_letter": "c",
            "detailed_solution": "k-means is a non-convex heuristic that converges to a local minimum; it is NOT guaranteed to reach the global optimum.",
            "image": None
        },
        {
            "id": "scalable_ass8_q4",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 8,
            "question_number": 4,
            "question": "Beyond improving centroid initialization, which of the following techniques directly helps determine a good value of k (the number of clusters) in k-means?",
            "options": [
                "The elbow method / silhouette analysis over a range of k values",
                "Always setting k equal to the number of features",
                "Replacing Euclidean distance with cosine similarity",
                "Running k-means only once with a fixed random seed"
            ],
            "correct_answer": 0,
            "correct_letter": "a",
            "detailed_solution": "The elbow method (evaluating sum of squared errors) and silhouette analysis measure cluster cohesion and separation across different k to determine optimal k.",
            "image": None
        },
        {
            "id": "scalable_ass8_q5",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 8,
            "question_number": 5,
            "question": "In spectral clustering using the symmetric normalized Laplacian L_sym = I - D^(-1/2) A D^(-1/2), what must typically be done to the eigenvectors before applying k-means to obtain the final clusters?",
            "options": [
                "Each row of the eigenvector matrix must be normalized to unit norm.",
                "The eigenvectors must be discarded and replaced with the adjacency matrix directly.",
                "The eigenvectors must be converted into a distance matrix using cosine similarity only.",
                "No further processing is required; k-means is applied directly to A."
            ],
            "correct_answer": 0,
            "correct_letter": "a",
            "detailed_solution": "In standard normalized spectral clustering (Ng-Jordan-Weiss), the rows of the top k eigenvector matrix are normalized to unit Euclidean length before running k-means.",
            "image": None
        },
        {
            "id": "scalable_ass8_q6",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 8,
            "question_number": 6,
            "question": "When true class labels are not known and only the data and cluster assignments are available, which metric is most suitable for evaluating how well-separated and compact the clusters are?",
            "options": [
                "Adjusted Rand Index (ARI)",
                "Silhouette score",
                "Normalized Mutual Information (NMI)",
                "Purity score"
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "Silhouette score is an unsupervised intrinsic validation metric that does not require ground truth labels, unlike ARI, NMI, or Purity.",
            "image": None
        },
        {
            "id": "scalable_ass8_q7",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 8,
            "question_number": 7,
            "question": "Which technique is best suited for estimating the cosine similarity between high-dimensional vectors efficiently at scale, analogous to how Min-Hash estimates Jaccard similarity?",
            "options": [
                "Random hyperplane (SimHash) projections",
                "MD5 hash of the entire vector",
                "Modulo hashing of raw feature counts",
                "Sorting vectors lexicographically"
            ],
            "correct_answer": 0,
            "correct_letter": "a",
            "detailed_solution": "SimHash (random hyperplane rounding) maps vectors to bitstrings such that the collision probability is 1 - θ/π, directly capturing cosine similarity.",
            "image": None
        },
        {
            "id": "scalable_ass8_q8",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 8,
            "question_number": 8,
            "question": "(Coding) Write NumPy code to pick five random indices from 0..49 inclusive, where repetition (the same index appearing more than once) is allowed.",
            "options": [
                "np.random.choice(50, size=5, replace=False)",
                "np.random.choice(50, size=5, replace=True)",
                "np.random.permutation(50)[:5]",
                "np.random.randint(0, 49, size=5)"
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "`np.random.choice(50, size=5, replace=True)` samples 5 integers from 0 to 49 with replacement.",
            "image": None
        },
        {
            "id": "scalable_ass8_q9",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 8,
            "question_number": 9,
            "question": "Consider convex functions f and g. Which of the following statements about max{f(x), g(x)} and min{f(x), g(x)} is correct?",
            "options": [
                "min{f(x), g(x)} is always convex, while max{f(x), g(x)} is never convex.",
                "max{f(x), g(x)} is always convex, while min{f(x), g(x)} is not guaranteed to be convex.",
                "Both max{f(x), g(x)} and min{f(x), g(x)} are always convex.",
                "Neither max{f(x), g(x)} nor min{f(x), g(x)} is ever convex."
            ],
            "correct_answer": 1,
            "correct_letter": "b",
            "detailed_solution": "The pointwise maximum of convex functions is always convex. The pointwise minimum of convex functions is generally non-convex (for example, min(x^2, (x-2)^2) is not convex).",
            "image": None
        },
        {
            "id": "scalable_ass8_q10",
            "course": "Scalable Data Science",
            "course_id": "scalable",
            "assignment": 8,
            "question_number": 10,
            "question": "You are given a file of per-document word counts (docID, {word:count}), and you want to compute, for each pair of documents, whether they share at least one common word (a co-occurrence check), without computing full document frequency. Which mapper output and reducer logic correctly accomplishes this?",
            "options": [
                "Mapper emits (word, docID); reducer, for each word, emits all pairs of docIDs sharing that word",
                "Mapper emits (docID, word); reducer sums the word counts per document",
                "Mapper emits (word, count); reducer counts unique docIDs per word",
                "Mapper sends the entire dictionary of word counts to a single reducer for pairwise comparison"
            ],
            "correct_answer": 0,
            "correct_letter": "a",
            "detailed_solution": "Inverted indexing: mapper inverts mapping to emit (word, docID). The reducer receives all documents containing that word and emits pairs (doc_i, doc_j).",
            "image": None
        }
    ]

# -------------------------------------------------------------
# MAIN COMPILER
# -------------------------------------------------------------

def main():
    print("Extracting Machine Learning Assignments 1 to 7...")
    ml_1_7 = extract_ml_1_to_7()
    print(f"-> Extracted {len(ml_1_7)} questions.")

    print("Extracting Machine Learning Assignment 8...")
    ml_8 = get_ml_8()
    print(f"-> Extracted {len(ml_8)} questions.")

    all_ml = ml_1_7 + ml_8
    print(f"Total Machine Learning Questions: {len(all_ml)}")

    print("Extracting Scalable Data Science Assignment 1...")
    scalable_1 = get_scalable_1()
    print(f"-> Extracted {len(scalable_1)} questions.")

    print("Extracting Scalable Data Science Assignments 2, 3, 4...")
    scalable_2 = extract_scalable_pdf(2, 'scalableds/Assignment(2)_nptel_2026.pdf')
    scalable_3 = extract_scalable_pdf(3, 'scalableds/Assignment(3)_nptel_2026 (1).pdf')
    scalable_4 = extract_scalable_pdf(4, 'scalableds/Assignment(4)_nptel_2026.pdf')
    print(f"-> Scalable 2: {len(scalable_2)} questions")
    print(f"-> Scalable 3: {len(scalable_3)} questions")
    print(f"-> Scalable 4: {len(scalable_4)} questions")

    print("Extracting Scalable Data Science Assignments 5, 6, 7, 8...")
    scalable_5 = get_scalable_5()
    scalable_6 = get_scalable_6()
    scalable_7 = get_scalable_7()
    scalable_8 = get_scalable_8()
    print(f"-> Scalable 5: {len(scalable_5)} questions")
    print(f"-> Scalable 6: {len(scalable_6)} questions")
    print(f"-> Scalable 7: {len(scalable_7)} questions")
    print(f"-> Scalable 8: {len(scalable_8)} questions")

    all_scalable = scalable_1 + scalable_2 + scalable_3 + scalable_4 + scalable_5 + scalable_6 + scalable_7 + scalable_8
    print(f"Total Scalable Data Science Questions: {len(all_scalable)}")

    total_questions = all_ml + all_scalable
    print(f"Grand Total Questions: {len(total_questions)}")

    data = {
        "metadata": {
            "title": "NPTEL Quiz & Exam Preparation Bank",
            "courses": [
                {
                    "id": "scalable",
                    "name": "Scalable Data Science",
                    "total_assignments": 8,
                    "total_questions": len(all_scalable),
                    "assignment_counts": {
                        "1": len(scalable_1),
                        "2": len(scalable_2),
                        "3": len(scalable_3),
                        "4": len(scalable_4),
                        "5": len(scalable_5),
                        "6": len(scalable_6),
                        "7": len(scalable_7),
                        "8": len(scalable_8)
                    }
                },
                {
                    "id": "ml",
                    "name": "Machine Learning for Earth System Sciences",
                    "total_assignments": 8,
                    "total_questions": len(all_ml),
                    "assignment_counts": {
                        "1": 10, "2": 10, "3": 10, "4": 10,
                        "5": 10, "6": 10, "7": 10, "8": 10
                    }
                }
            ],
            "grand_total": len(total_questions)
        },
        "questions": total_questions
    }

    # --- Validation: ensure all correct_answer fields are integers ---
    bad_questions = [
        q for q in total_questions if not isinstance(q.get("correct_answer"), int)
    ]
    if bad_questions:
        for bq in bad_questions:
            print(f"  [ERROR] Non-integer correct_answer in {bq['id']}: {repr(bq['correct_answer'])}")
        raise ValueError(
            f"{len(bad_questions)} question(s) have non-integer correct_answer. "
            "Fix these before writing output."
        )
    print(f"Validation passed: all {len(total_questions)} questions have integer correct_answer.")

    # Write src/data/questions.json (build output)
    output_path = "src/data/questions.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Successfully saved question bank to {output_path}!")

    # Write data/questions.js (live app file consumed by index.html)
    js_output_path = "data/questions.js"
    js_content = "window.QUESTIONS_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";"
    with open(js_output_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Successfully saved question bank to {js_output_path}!")

    # Write data/questions.json (synced copy)
    json_output_path = "data/questions.json"
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Successfully saved question bank to {json_output_path}!")

if __name__ == "__main__":
    main()
