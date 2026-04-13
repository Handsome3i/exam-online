document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.option-item').forEach(function(item) {
        item.addEventListener('click', function(e) {
            if (e.target.tagName === 'INPUT') return;
            const input = item.querySelector('input[type="radio"], input[type="checkbox"]');
            if (!input) return;

            if (input.type === 'radio') {
                const name = input.name;
                document.querySelectorAll('.option-item input[name="' + name + '"]').forEach(function(r) {
                    r.closest('.option-item').classList.remove('selected');
                });
                input.checked = true;
                item.classList.add('selected');
            } else {
                input.checked = !input.checked;
                item.classList.toggle('selected', input.checked);
            }
        });
    });

    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.querySelector('.sidebar');
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
        });
    }
});

function initTimer(seconds, displayEl, formEl) {
    let remaining = seconds;

    function update() {
        const m = Math.floor(remaining / 60);
        const s = remaining % 60;
        displayEl.textContent = String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
        if (remaining <= 300) {
            displayEl.classList.add('warning');
        }
        if (remaining <= 0) {
            clearInterval(timer);
            formEl.submit();
            return;
        }
        remaining--;
    }

    update();
    const timer = setInterval(update, 1000);
}

function validateAllAnswered() {
    var cards = document.querySelectorAll('.question-card');
    var unanswered = [];
    cards.forEach(function(card) {
        var inputs = card.querySelectorAll('input[type="radio"], input[type="checkbox"]');
        if (inputs.length === 0) return;
        var answered = false;
        inputs.forEach(function(inp) { if (inp.checked) answered = true; });
        if (!answered) {
            var num = card.querySelector('.question-number');
            unanswered.push(num ? num.textContent.trim() : '?');
            card.style.border = '2px solid var(--danger)';
        } else {
            card.style.border = '';
        }
    });
    if (unanswered.length > 0) {
        alert('以下题目尚未作答，请完成后再提交：\n第 ' + unanswered.join('、') + ' 题');
        var first = document.querySelector('.question-card[style*="danger"]');
        if (first) first.scrollIntoView({behavior: 'smooth', block: 'center'});
        return false;
    }
    return confirm('确认交卷吗？提交后不可修改。');
}
