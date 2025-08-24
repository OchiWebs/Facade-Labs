document.addEventListener('DOMContentLoaded', () => {
    const flagForm = document.getElementById('flag-form');
    if (flagForm) {
        flagForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const challengeId = flagForm.dataset.challengeId;
            const flagInput = document.getElementById('flag-input');
            const feedback = document.getElementById('feedback');
            
            const response = await fetch('/api/submit_flag', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    challenge_id: challengeId,
                    flag: flagInput.value
                })
            });
            const result = await response.json();

            if (result.correct) {
                feedback.textContent = '✅ Flag Benar! Tantangan Selesai.';
                feedback.className = 'feedback success';
                flagInput.disabled = true;
                
                let solved = JSON.parse(localStorage.getItem('solvedChallenges')) || [];
                if (!solved.includes(challengeId)) {
                    solved.push(challengeId);
                    localStorage.setItem('solvedChallenges', JSON.stringify(solved));
                }
            } else {
                feedback.textContent = '❌ Flag Salah. Coba lagi!';
                feedback.className = 'feedback error';
            }
            feedback.style.display = 'block';
        });
    }

    const challengeGrid = document.querySelector('.challenge-grid');
    if (challengeGrid) {
        const solved = JSON.parse(localStorage.getItem('solvedChallenges')) || [];
        solved.forEach(id => {
            const card = document.querySelector(`.challenge-card[data-challenge-id="${id}"]`);
            if (card) {
                card.classList.add('solved');
            }
        });
    }
});