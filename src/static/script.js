document.addEventListener('DOMContentLoaded', () => {
    const titleInput = document.getElementById('news-title');
    const analyzeBtn = document.getElementById('analyze-btn');
    const loadingDiv = document.getElementById('loading');
    const resultContainer = document.getElementById('result-container');
    const resultBadge = document.getElementById('result-badge');
    const confidenceFill = document.getElementById('confidence-fill');
    const confidenceText = document.getElementById('confidence-text');
    const errorMsg = document.getElementById('error-message');

    analyzeBtn.addEventListener('click', async () => {
        const title = titleInput.value.trim();
        
        if (!title) {
            showError("Please enter a news title to analyze.");
            return;
        }

        // Reset UI
        hideError();
        resultContainer.classList.add('hidden');
        loadingDiv.classList.remove('hidden');
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title: title })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Something went wrong.");
            }

            displayResult(data.is_fake, data.confidence);
            
        } catch (error) {
            showError(error.message);
        } finally {
            loadingDiv.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    });

    function displayResult(isFake, confidence) {
        resultContainer.classList.remove('hidden');
        
        // Setup Badge
        resultBadge.className = 'badge';
        if (isFake) {
            resultBadge.textContent = 'Fake News Detected';
            resultBadge.classList.add('fake');
            confidenceFill.style.backgroundColor = 'var(--fake-color)';
            confidenceText.style.color = 'var(--fake-color)';
        } else {
            resultBadge.textContent = 'Reliable News';
            resultBadge.classList.add('real');
            confidenceFill.style.backgroundColor = 'var(--real-color)';
            confidenceText.style.color = 'var(--real-color)';
        }

        // Animate Confidence
        const confidencePct = (confidence * 100).toFixed(1);
        
        // Reset width to 0 for animation effect
        confidenceFill.style.width = '0%';
        
        setTimeout(() => {
            confidenceFill.style.width = `${confidencePct}%`;
            
            // Animate number
            animateValue(confidenceText, 0, parseFloat(confidencePct), 1500);
        }, 100);
    }

    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = (progress * (end - start) + start).toFixed(1) + '%';
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    function showError(message) {
        errorMsg.textContent = message;
        errorMsg.classList.remove('hidden');
    }

    function hideError() {
        errorMsg.classList.add('hidden');
    }
});
