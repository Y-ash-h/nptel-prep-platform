/**
 * NPTEL Exam PrepMaster — Frontend Application Logic
 * Scalable Data Science & Machine Learning for Earth System Sciences
 */

(function () {
  'use strict';

  // --- State Management ---
  const state = {
    course: 'scalable', // 'scalable' | 'ml'
    feedbackMode: 'exam', // 'exam' | 'practice'
    jumbleOptions: true,
    paletteFilter: 'all', // 'all' | 'unanswered' | 'flagged'
    reviewFilter: 'all',

    // Active Test State
    testActive: false,
    testType: 'random50',
    testTitle: '50 Random Questions',
    questions: [], // current prepared questions
    currentIndex: 0,
    userAnswers: {}, // index -> chosen option index
    flagged: new Set(),
    revealed: {}, // for practice mode: index -> true
    timerSeconds: 0,
    timerInterval: null,
    testCompleted: false,
    results: null
  };

  // --- DOM Elements ---
  const el = {
    // Views
    dashboardView: document.getElementById('view-dashboard'),
    testView: document.getElementById('view-test'),
    resultsView: document.getElementById('view-results'),

    // Course tabs
    courseTabs: document.querySelectorAll('.course-tab'),
    marathonMeta: document.getElementById('marathon-count-meta'),
    assignmentSectionInfo: document.getElementById('assignment-section-info'),
    assignmentsGrid: document.getElementById('assignments-grid'),

    // Global config
    cfgJumble: document.getElementById('cfg-jumble-options'),
    modeExamBtn: document.getElementById('mode-exam-btn'),
    modePracticeBtn: document.getElementById('mode-practice-btn'),
    themeToggle: document.getElementById('theme-toggle'),
    homeNavBtn: document.getElementById('home-nav-btn'),
    brandLink: document.getElementById('brand-link'),

    // Test Navigation & Header
    exitTestBtn: document.getElementById('exit-test-btn'),
    activeTestTitle: document.getElementById('active-test-title'),
    activeTestModePill: document.getElementById('active-test-mode-pill'),
    timerDisplay: document.getElementById('timer-display'),
    progressFill: document.getElementById('quiz-progress-fill'),
    finishTestBtn: document.getElementById('finish-test-btn'),
    togglePaletteBtn: document.getElementById('toggle-palette-btn'),
    paletteBtnText: document.getElementById('palette-btn-text'),
    totalQIndicator: document.getElementById('total-q-indicator'),

    // Question Main Pane
    qCounter: document.getElementById('q-counter'),
    qSourceTag: document.getElementById('q-source-tag'),
    qStatusPill: document.getElementById('q-status-pill'),
    flagQuestionBtn: document.getElementById('flag-question-btn'),
    flagBtnLabel: document.getElementById('flag-btn-label'),
    questionText: document.getElementById('question-text'),
    questionImageContainer: document.getElementById('question-image-container'),
    questionImage: document.getElementById('question-image'),
    optionsContainer: document.getElementById('options-container'),
    practiceExp: document.getElementById('practice-explanation'),
    practiceExpText: document.getElementById('practice-explanation-text'),
    expStatusBadge: document.getElementById('exp-status-badge'),
    prevQBtn: document.getElementById('prev-q-btn'),
    nextQBtn: document.getElementById('next-q-btn'),
    clearChoiceBtn: document.getElementById('clear-choice-btn'),

    // Palette
    paletteSidebar: document.getElementById('palette-sidebar'),
    closePaletteBtn: document.getElementById('close-palette-btn'),
    paletteGrid: document.getElementById('palette-grid'),
    countAnswered: document.getElementById('count-answered'),
    countFlagged: document.getElementById('count-flagged'),
    countUnanswered: document.getElementById('count-unanswered'),
    paletteFilters: document.querySelectorAll('.palette-filter'),

    // Results View
    resultsHeadline: document.getElementById('results-headline'),
    resultsTestName: document.getElementById('results-test-name'),
    scoreRaw: document.getElementById('score-raw'),
    scoreRawSub: document.getElementById('score-raw-sub'),
    scoreAccuracy: document.getElementById('score-accuracy'),
    scoreNptel: document.getElementById('score-nptel'),
    scoreTime: document.getElementById('score-time'),
    scoreSpeed: document.getElementById('score-speed'),
    bdCorrect: document.getElementById('bd-correct'),
    bdIncorrect: document.getElementById('bd-incorrect'),
    bdSkipped: document.getElementById('bd-skipped'),
    retakeTestBtn: document.getElementById('retake-test-btn'),
    backDashboardBtn: document.getElementById('back-dashboard-btn'),
    reviewList: document.getElementById('review-list'),
    rfAll: document.getElementById('rf-all'),
    rfIncorrect: document.getElementById('rf-incorrect'),
    rfCorrect: document.getElementById('rf-correct'),
    rfSkipped: document.getElementById('rf-skipped'),
    reviewFilterPills: document.querySelectorAll('.filter-pill'),

    // Submit Modal
    submitModal: document.getElementById('submit-modal'),
    modalAnswered: document.getElementById('modal-answered'),
    modalUnanswered: document.getElementById('modal-unanswered'),
    modalFlagged: document.getElementById('modal-flagged'),
    modalCancelBtn: document.getElementById('modal-cancel-btn'),
    modalConfirmBtn: document.getElementById('modal-confirm-btn')
  };

  // --- Ensure Question Data Available ---
  function getRawQuestions() {
    if (window.QUESTIONS_DATA && window.QUESTIONS_DATA.questions) {
      return window.QUESTIONS_DATA.questions;
    }
    return [];
  }

  // --- Fisher-Yates Shuffle ---
  function shuffleArray(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  // --- Mathematical Formula Formatting & KaTeX ---
  function renderMath(element) {
    if (!element) return;
    if (window.renderMathInElement) {
      try {
        window.renderMathInElement(element, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '$', right: '$', display: false },
            { left: '\\[', right: '\\]', display: true },
            { left: '\\(', right: '\\)', display: false }
          ],
          throwOnError: false
        });
      } catch (e) {
        console.warn('KaTeX rendering error:', e);
      }
    }
  }

  // Format inline text with code or math symbols if needed
  function formatDisplayText(text) {
    if (!text) return '';
    // Escape HTML safely
    const div = document.createElement('div');
    div.textContent = text;
    let safe = div.innerHTML;

    // Convert newlines to breaks
    return safe.replace(/\n/g, '<br>');
  }

  // --- Initialize UI & Event Handlers ---
  function init() {
    loadTheme();
    renderAssignmentsGrid();
    attachEventListeners();
    updateCourseUI();
  }

  // Theme Management
  function loadTheme() {
    const savedTheme = localStorage.getItem('nptel_prep_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('nptel_prep_theme', next);
  }

  // --- Attach Event Listeners ---
  function attachEventListeners() {
    // Theme toggle
    el.themeToggle.addEventListener('click', toggleTheme);

    // Nav home buttons
    el.homeNavBtn.addEventListener('click', () => showView('dashboard'));
    el.brandLink.addEventListener('click', (e) => {
      e.preventDefault();
      showView('dashboard');
    });

    // Course Selection
    el.courseTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const courseId = tab.dataset.course;
        if (state.course !== courseId) {
          state.course = courseId;
          updateCourseUI();
        }
      });
    });

    // Jumble Options Checkbox
    el.cfgJumble.addEventListener('change', (e) => {
      state.jumbleOptions = e.target.checked;
    });

    // Feedback Mode Segmented Control
    el.modeExamBtn.addEventListener('click', () => setFeedbackMode('exam'));
    el.modePracticeBtn.addEventListener('click', () => setFeedbackMode('practice'));

    // Test Launch Buttons
    document.querySelectorAll('.start-test-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const type = e.currentTarget.dataset.type;
        startTest(type);
      });
    });

    // Test View Controls
    el.exitTestBtn.addEventListener('click', () => {
      if (confirm('Are you sure you want to exit? Your current test progress will be lost.')) {
        stopTimer();
        showView('dashboard');
      }
    });

    el.prevQBtn.addEventListener('click', () => navigateQuestion(-1));
    el.nextQBtn.addEventListener('click', () => navigateQuestion(1));
    el.clearChoiceBtn.addEventListener('click', clearCurrentChoice);

    // Flag Question
    el.flagQuestionBtn.addEventListener('click', toggleFlagCurrentQuestion);

    // Question Palette Drawer Toggle
    el.togglePaletteBtn.addEventListener('click', () => {
      el.paletteSidebar.classList.toggle('open');
    });
    el.closePaletteBtn.addEventListener('click', () => {
      el.paletteSidebar.classList.remove('open');
    });

    // Palette Filters
    el.paletteFilters.forEach(btn => {
      btn.addEventListener('click', () => {
        el.paletteFilters.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.paletteFilter = btn.dataset.filter;
        renderPaletteGrid();
      });
    });

    // Finish / Submit Test
    el.finishTestBtn.addEventListener('click', promptSubmitTest);
    el.modalCancelBtn.addEventListener('click', () => {
      el.submitModal.style.display = 'none';
    });
    el.modalConfirmBtn.addEventListener('click', () => {
      el.submitModal.style.display = 'none';
      submitTest();
    });

    // Results View Actions
    el.retakeTestBtn.addEventListener('click', () => {
      startTest(state.testType, state.lastAssignmentNum);
    });
    el.backDashboardBtn.addEventListener('click', () => showView('dashboard'));

    // Review Filters
    el.reviewFilterPills.forEach(pill => {
      pill.addEventListener('click', () => {
        el.reviewFilterPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.reviewFilter = pill.dataset.reviewFilter;
        renderReviewList();
      });
    });

    // Keyboard Navigation
    document.addEventListener('keydown', (e) => {
      if (!state.testActive) return;
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      if (e.key === 'ArrowRight' || e.key === 'n' || e.key === 'N') {
        navigateQuestion(1);
      } else if (e.key === 'ArrowLeft' || e.key === 'p' || e.key === 'P') {
        navigateQuestion(-1);
      } else if (['1', '2', '3', '4'].includes(e.key)) {
        const optIndex = parseInt(e.key, 10) - 1;
        selectOption(optIndex);
      } else if (['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D'].includes(e.key)) {
        const optIndex = e.key.toUpperCase().charCodeAt(0) - 65;
        selectOption(optIndex);
      }
    });
  }

  // Set Feedback Mode
  function setFeedbackMode(mode) {
    state.feedbackMode = mode;
    if (mode === 'exam') {
      el.modeExamBtn.classList.add('active');
      el.modePracticeBtn.classList.remove('active');
    } else {
      el.modePracticeBtn.classList.add('active');
      el.modeExamBtn.classList.remove('active');
    }
  }

  // View Switching
  function showView(viewName) {
    el.dashboardView.className = viewName === 'dashboard' ? 'view-active' : 'view-hidden';
    el.testView.className = viewName === 'test' ? 'view-active' : 'view-hidden';
    el.resultsView.className = viewName === 'results' ? 'view-active' : 'view-hidden';

    if (viewName !== 'test') {
      state.testActive = false;
      stopTimer();
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // --- Course Selection & Assignment Grid UI ---
  function updateCourseUI() {
    el.courseTabs.forEach(t => {
      const active = t.dataset.course === state.course;
      t.classList.toggle('active', active);
      t.setAttribute('aria-selected', active);
    });

    const isScalable = state.course === 'scalable';
    const totalQ = isScalable ? 120 : 80;
    el.marathonMeta.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg> ${totalQ} Questions`;

    el.assignmentSectionInfo.textContent = `8 Assignments • ${totalQ} Total Questions`;

    renderAssignmentsGrid();
  }

  function renderAssignmentsGrid() {
    const raw = getRawQuestions();
    const courseQuestions = raw.filter(q => q.course_id === state.course);

    el.assignmentsGrid.innerHTML = '';

    for (let assNum = 1; assNum <= 8; assNum++) {
      const assQs = courseQuestions.filter(q => q.assignment === assNum);
      const count = assQs.length;

      let topicTitle = '';
      if (state.course === 'scalable') {
        if (assNum === 1) topicTitle = 'Probability, Linear Algebra & Optimization';
        else if (assNum === 2) topicTitle = 'Streaming Algorithms & Bloom Filters';
        else if (assNum === 3) topicTitle = 'Count-Min & Count Sketches';
        else if (assNum === 4) topicTitle = 'Locality Sensitive Hashing (LSH)';
        else if (assNum === 5) topicTitle = 'Dimensionality Reduction, SVD & Leverage Scores';
        else if (assNum === 6) topicTitle = 'Hadoop Ecosystem & MapReduce';
        else if (assNum === 7) topicTitle = 'Apache Spark & RDD Transformations';
        else if (assNum === 8) topicTitle = 'Distributed SGD, Clustering & Large-Scale ML';
      } else {
        if (assNum === 1) topicTitle = 'Autocorrelation, GPR & Spatial ML';
        else if (assNum === 2) topicTitle = 'Kalman Filters & Data Assimilation';
        else if (assNum === 3) topicTitle = 'Deep Learning Architectures & GMMs';
        else if (assNum === 4) topicTitle = 'Spatiotemporal Neural Modeling';
        else if (assNum === 5) topicTitle = 'Universal Kriging & Spatial ML';
        else if (assNum === 6) topicTitle = 'Physics-Guided Neural Networks (PGDL)';
        else if (assNum === 7) topicTitle = 'Extreme Events & Climate Dynamics';
        else if (assNum === 8) topicTitle = 'Convection, Surrogate Models & LSTMs';
      }

      const card = document.createElement('div');
      card.className = 'assignment-card glass-card hover-lift';
      card.innerHTML = `
        <div class="assignment-card-top">
          <div>
            <div class="assignment-num">Assignment ${assNum}</div>
            <div class="assignment-sub">${topicTitle}</div>
          </div>
          <span class="assignment-q-count">${count} Qs</span>
        </div>
        <button class="primary-btn assignment-btn" data-ass="${assNum}">
          <span>Take Test</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>
      `;

      card.querySelector('.assignment-btn').addEventListener('click', () => {
        startTest('assignment', assNum);
      });

      el.assignmentsGrid.appendChild(card);
    }
  }

  // --- Starting a Test ---
  function startTest(type, assignmentNum = null) {
    const raw = getRawQuestions();
    const courseQuestions = raw.filter(q => q.course_id === state.course);

    if (!courseQuestions.length) {
      alert('Error loading questions. Please ensure data/questions.js is available.');
      return;
    }

    state.testType = type;
    state.lastAssignmentNum = assignmentNum;
    state.testActive = true;
    state.testCompleted = false;
    state.currentIndex = 0;
    state.userAnswers = {};
    state.flagged = new Set();
    state.revealed = {};
    state.results = null;

    let selected = [];
    let title = '';

    if (type === 'random50') {
      title = '50 Random Questions';
      selected = shuffleArray(courseQuestions).slice(0, 50);
    } else if (type === 'random20') {
      title = '20 Random Questions';
      selected = shuffleArray(courseQuestions).slice(0, 20);
    } else if (type === 'marathon') {
      title = `All Questions Jumbled (${courseQuestions.length} Questions)`;
      selected = shuffleArray(courseQuestions);
    } else if (type === 'assignment') {
      title = `Assignment ${assignmentNum} Test`;
      selected = courseQuestions.filter(q => q.assignment === assignmentNum);
    }

    if (!selected.length) {
      alert('No questions found for this selection.');
      return;
    }

    // Process questions: if jumbleOptions is active, shuffle options while maintaining correct answer
    state.questions = selected.map((q, idx) => {
      const qCopy = { ...q, originalIndex: idx };
      if (state.jumbleOptions && q.options && q.options.length > 1) {
        // Create indexed options
        const indexedOpts = q.options.map((opt, i) => ({
          text: opt,
          isCorrect: i === q.correct_answer
        }));
        const shuffled = shuffleArray(indexedOpts);
        qCopy.options = shuffled.map(o => o.text);
        qCopy.correct_answer = shuffled.findIndex(o => o.isCorrect);
        qCopy.correct_letter = String.fromCharCode(65 + qCopy.correct_answer);
      }
      return qCopy;
    });

    state.testTitle = `${state.course === 'scalable' ? 'Scalable Data Science' : 'Machine Learning for Earth System Sciences'} • ${title}`;

    // Update Header
    el.activeTestTitle.textContent = title;
    el.activeTestModePill.textContent = state.feedbackMode === 'exam' ? 'Exam Mode' : 'Practice Mode';
    el.totalQIndicator.textContent = state.questions.length;

    // Reset and Start Timer
    startTimer();

    // Show Test View
    showView('test');

    // Render First Question
    renderCurrentQuestion();
    renderPaletteGrid();
    updatePaletteCounts();
  }

  // --- Timer Management ---
  function startTimer() {
    stopTimer();
    state.timerSeconds = 0;
    updateTimerDisplay();
    state.timerInterval = setInterval(() => {
      state.timerSeconds++;
      updateTimerDisplay();
    }, 1000);
  }

  function stopTimer() {
    if (state.timerInterval) {
      clearInterval(state.timerInterval);
      state.timerInterval = null;
    }
  }

  function formatTime(totalSec) {
    const mins = Math.floor(totalSec / 60);
    const secs = totalSec % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  function updateTimerDisplay() {
    el.timerDisplay.textContent = formatTime(state.timerSeconds);
  }

  // --- Question Display & Rendering ---
  function renderCurrentQuestion() {
    const q = state.questions[state.currentIndex];
    const total = state.questions.length;
    const isAnswered = state.userAnswers.hasOwnProperty(state.currentIndex);
    const isFlagged = state.flagged.has(state.currentIndex);

    // Counter & Header Badges
    el.qCounter.textContent = `Question ${state.currentIndex + 1} of ${total}`;
    el.qSourceTag.textContent = `Assignment ${q.assignment}`;
    el.paletteBtnText.textContent = `Questions (${state.currentIndex + 1}/${total})`;

    // Status pill
    if (isAnswered) {
      el.qStatusPill.className = 'q-status-badge status-answered';
      el.qStatusPill.textContent = 'Answered';
    } else {
      el.qStatusPill.className = 'q-status-badge status-unanswered';
      el.qStatusPill.textContent = 'Unanswered';
    }

    // Flag button
    el.flagQuestionBtn.classList.toggle('flagged', isFlagged);
    el.flagBtnLabel.textContent = isFlagged ? 'Flagged for Review' : 'Review Later';

    // Progress Bar Fill
    const progressPct = ((state.currentIndex + 1) / total) * 100;
    el.progressFill.style.width = `${progressPct}%`;

    // Question Text with KaTeX
    el.questionText.innerHTML = formatDisplayText(q.question);
    renderMath(el.questionText);

    // Diagram / Image
    if (q.image) {
      el.questionImage.src = q.image;
      el.questionImageContainer.style.display = 'flex';
    } else {
      el.questionImageContainer.style.display = 'none';
      el.questionImage.src = '';
    }

    // Render Options
    el.optionsContainer.innerHTML = '';
    const userChoice = state.userAnswers[state.currentIndex];
    const isRevealed = state.feedbackMode === 'practice' && state.revealed[state.currentIndex];

    q.options.forEach((optText, optIdx) => {
      const optLetter = String.fromCharCode(65 + optIdx);
      const optDiv = document.createElement('div');
      optDiv.className = 'option-item';
      optDiv.setAttribute('role', 'radio');
      optDiv.setAttribute('aria-checked', userChoice === optIdx);

      if (userChoice === optIdx) {
        optDiv.classList.add('selected');
      }

      // Practice mode reveals
      if (isRevealed) {
        if (optIdx === q.correct_answer) {
          optDiv.classList.add('reveal-correct');
        } else if (userChoice === optIdx) {
          optDiv.classList.add('reveal-wrong');
        }
      }

      optDiv.innerHTML = `
        <div class="option-indicator">${optLetter}</div>
        <div class="option-text">${formatDisplayText(optText)}</div>
      `;

      renderMath(optDiv.querySelector('.option-text'));

      optDiv.addEventListener('click', () => {
        selectOption(optIdx);
      });

      el.optionsContainer.appendChild(optDiv);
    });

    // Practice Mode Solution Box
    if (isRevealed) {
      const isCorrect = userChoice === q.correct_answer;
      el.practiceExp.style.display = 'block';
      el.practiceExp.className = `practice-explanation glass-card ${isCorrect ? '' : 'is-wrong'}`;
      el.expStatusBadge.textContent = isCorrect ? 'Correct ✓' : 'Incorrect ✗';
      el.practiceExpText.innerHTML = formatDisplayText(q.detailed_solution || 'No detailed solution provided.');
      renderMath(el.practiceExpText);
    } else {
      el.practiceExp.style.display = 'none';
    }

    // Prev / Next Button State
    el.prevQBtn.disabled = state.currentIndex === 0;
    if (state.currentIndex === total - 1) {
      el.nextQBtn.innerHTML = `<span>Submit</span><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
    } else {
      el.nextQBtn.innerHTML = `<span>Next</span><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>`;
    }

    // Update Palette Active Item
    updatePaletteActiveState();
  }

  // --- Option Selection ---
  function selectOption(optIndex) {
    const q = state.questions[state.currentIndex];
    if (!q || optIndex < 0 || optIndex >= q.options.length) return;

    state.userAnswers[state.currentIndex] = optIndex;

    if (state.feedbackMode === 'practice') {
      state.revealed[state.currentIndex] = true;
    }

    renderCurrentQuestion();
    updatePaletteCounts();
    renderPaletteGrid();
  }

  function clearCurrentChoice() {
    delete state.userAnswers[state.currentIndex];
    delete state.revealed[state.currentIndex];
    renderCurrentQuestion();
    updatePaletteCounts();
    renderPaletteGrid();
  }

  function toggleFlagCurrentQuestion() {
    if (state.flagged.has(state.currentIndex)) {
      state.flagged.delete(state.currentIndex);
    } else {
      state.flagged.add(state.currentIndex);
    }
    renderCurrentQuestion();
    updatePaletteCounts();
    renderPaletteGrid();
  }

  function navigateQuestion(delta) {
    const nextIdx = state.currentIndex + delta;
    if (nextIdx >= 0 && nextIdx < state.questions.length) {
      state.currentIndex = nextIdx;
      renderCurrentQuestion();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (nextIdx >= state.questions.length) {
      // Reached the end; prompt submit
      promptSubmitTest();
    }
  }

  // --- Question Palette Drawer ---
  function renderPaletteGrid() {
    el.paletteGrid.innerHTML = '';
    const total = state.questions.length;

    for (let i = 0; i < total; i++) {
      const isAnswered = state.userAnswers.hasOwnProperty(i);
      const isFlagged = state.flagged.has(i);

      // Filtering
      if (state.paletteFilter === 'unanswered' && isAnswered) continue;
      if (state.paletteFilter === 'flagged' && !isFlagged) continue;

      const btn = document.createElement('button');
      btn.className = 'palette-q-btn';
      btn.textContent = i + 1;

      if (i === state.currentIndex) btn.classList.add('current');
      if (isAnswered) btn.classList.add('answered');
      if (isFlagged) btn.classList.add('flagged');

      btn.addEventListener('click', () => {
        state.currentIndex = i;
        renderCurrentQuestion();
        // On mobile, close palette after selection
        if (window.innerWidth <= 900) {
          el.paletteSidebar.classList.remove('open');
        }
      });

      el.paletteGrid.appendChild(btn);
    }
  }

  function updatePaletteActiveState() {
    const btns = el.paletteGrid.querySelectorAll('.palette-q-btn');
    btns.forEach(b => {
      const num = parseInt(b.textContent, 10) - 1;
      b.classList.toggle('current', num === state.currentIndex);
    });
  }

  function updatePaletteCounts() {
    const total = state.questions.length;
    const answeredCount = Object.keys(state.userAnswers).length;
    const flaggedCount = state.flagged.size;
    const unansweredCount = total - answeredCount;

    el.countAnswered.textContent = answeredCount;
    el.countFlagged.textContent = flaggedCount;
    el.countUnanswered.textContent = unansweredCount;
  }

  // --- Test Submission & Scoring ---
  function promptSubmitTest() {
    const total = state.questions.length;
    const answeredCount = Object.keys(state.userAnswers).length;
    const unansweredCount = total - answeredCount;
    const flaggedCount = state.flagged.size;

    el.modalAnswered.textContent = answeredCount;
    el.modalUnanswered.textContent = unansweredCount;
    el.modalFlagged.textContent = flaggedCount;

    el.submitModal.style.display = 'flex';
  }

  function submitTest() {
    stopTimer();
    state.testActive = false;
    state.testCompleted = true;

    const totalQuestions = state.questions.length;
    let correctCount = 0;
    let incorrectCount = 0;
    let skippedCount = 0;

    const questionResults = state.questions.map((q, idx) => {
      const userChoice = state.userAnswers[idx];
      const isAnswered = userChoice !== undefined;
      const isCorrect = isAnswered && userChoice === q.correct_answer;

      if (!isAnswered) {
        skippedCount++;
      } else if (isCorrect) {
        correctCount++;
      } else {
        incorrectCount++;
      }

      return {
        question: q,
        userChoice: userChoice,
        isAnswered: isAnswered,
        isCorrect: isCorrect,
        isFlagged: state.flagged.has(idx)
      };
    });

    // Formulas requested by user:
    // User marks = correctCount (1 mark per question)
    // Total marks = totalQuestions
    // Accuracy = (user marks / total questions) * 100
    // Percentage = (user marks / total marks of assignment) * (3/4) * 100
    const rawMarks = correctCount;
    const accuracy = totalQuestions > 0 ? (rawMarks / totalQuestions) * 100 : 0;
    const nptelScaledScore = totalQuestions > 0 ? (rawMarks / totalQuestions) * (3 / 4) * 100 : 0;

    state.results = {
      rawMarks,
      totalQuestions,
      accuracy,
      nptelScaledScore,
      correctCount,
      incorrectCount,
      skippedCount,
      timeSeconds: state.timerSeconds,
      questionResults
    };

    renderResults();
    showView('results');
  }

  // --- Render Results & Detailed Review ---
  function renderResults() {
    const res = state.results;
    if (!res) return;

    el.resultsTestName.textContent = state.testTitle;

    // Headline message based on score
    if (res.accuracy >= 80) {
      el.resultsHeadline.textContent = 'Outstanding Performance! 🎉';
    } else if (res.accuracy >= 60) {
      el.resultsHeadline.textContent = 'Great Effort! Well Done 👏';
    } else if (res.accuracy >= 40) {
      el.resultsHeadline.textContent = 'Keep Practicing! You Are Getting There 📚';
    } else {
      el.resultsHeadline.textContent = 'Review Mistakes & Try Again! 💪';
    }

    // Numerical Metrics
    el.scoreRaw.textContent = `${res.rawMarks} / ${res.totalQuestions}`;
    el.scoreRawSub.textContent = `${res.correctCount} Correct • ${res.totalQuestions} Total`;
    el.scoreAccuracy.textContent = `${res.accuracy.toFixed(1)}%`;
    el.scoreNptel.textContent = `${res.nptelScaledScore.toFixed(2)}%`;

    el.scoreTime.textContent = formatTime(res.timeSeconds);
    const avgSec = res.totalQuestions > 0 ? Math.round(res.timeSeconds / res.totalQuestions) : 0;
    el.scoreSpeed.textContent = `${avgSec}s avg per question`;

    // Breakdown
    el.bdCorrect.textContent = res.correctCount;
    el.bdIncorrect.textContent = res.incorrectCount;
    el.bdSkipped.textContent = res.skippedCount;

    // Filter pill counts
    el.rfAll.textContent = res.totalQuestions;
    el.rfIncorrect.textContent = res.incorrectCount;
    el.rfCorrect.textContent = res.correctCount;
    el.rfSkipped.textContent = res.skippedCount;

    renderReviewList();
  }

  function renderReviewList() {
    const res = state.results;
    if (!res) return;

    el.reviewList.innerHTML = '';

    const filter = state.reviewFilter; // 'all' | 'incorrect' | 'correct' | 'skipped'
    const filtered = res.questionResults.filter(item => {
      if (filter === 'incorrect') return item.isAnswered && !item.isCorrect;
      if (filter === 'correct') return item.isCorrect;
      if (filter === 'skipped') return !item.isAnswered;
      return true;
    });

    if (filtered.length === 0) {
      el.reviewList.innerHTML = `
        <div class="glass-card" style="padding: 2.5rem; text-align: center; color: var(--text-muted);">
          No questions in this filter category.
        </div>
      `;
      return;
    }

    filtered.forEach((item, fIdx) => {
      const q = item.question;
      const card = document.createElement('div');
      card.className = 'review-card glass-card';

      let statusPill = '';
      if (!item.isAnswered) {
        statusPill = `<span class="review-pill pill-skipped">Skipped</span>`;
      } else if (item.isCorrect) {
        statusPill = `<span class="review-pill pill-correct">Correct ✓</span>`;
      } else {
        statusPill = `<span class="review-pill pill-incorrect">Incorrect ✗</span>`;
      }

      // Render options with styling
      let optsHtml = '';
      q.options.forEach((optText, optIdx) => {
        const letter = String.fromCharCode(65 + optIdx);
        let optClass = 'review-opt-item';
        let suffix = '';

        if (optIdx === q.correct_answer) {
          optClass += ' is-correct';
          suffix = ' <strong>(Correct Answer)</strong>';
        } else if (item.userChoice === optIdx && !item.isCorrect) {
          optClass += ' is-user-wrong';
          suffix = ' <strong>(Your Selection)</strong>';
        }

        optsHtml += `
          <div class="${optClass}">
            <span class="option-indicator">${letter}</span>
            <div class="opt-text">${formatDisplayText(optText)}${suffix}</div>
          </div>
        `;
      });

      // Optional image
      const imageHtml = q.image
        ? `<div class="question-image-container"><img src="${q.image}" alt="Diagram"></div>`
        : '';

      card.innerHTML = `
        <div class="review-card-top">
          <div class="review-meta">
            <span class="q-number-badge">#${fIdx + 1}</span>
            <span class="q-tag">Assignment ${q.assignment}</span>
          </div>
          <div>${statusPill}</div>
        </div>

        <div class="review-q-text">${formatDisplayText(q.question)}</div>
        ${imageHtml}
        <div class="review-options-list">${optsHtml}</div>

        <div class="review-solution-box">
          <div class="review-sol-label">Step-by-Step Solution & Rationale</div>
          <div class="review-sol-text">${formatDisplayText(q.detailed_solution || 'Answer verified from official NPTEL key.')}</div>
        </div>
      `;

      renderMath(card);
      el.reviewList.appendChild(card);
    });
  }

  // Initialize once DOM is loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
