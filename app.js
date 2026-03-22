// ===== Animated Counter =====
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 1500;
        const start = performance.now();

        function update(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            counter.textContent = Math.round(target * eased);
            if (progress < 1) requestAnimationFrame(update);
        }

        requestAnimationFrame(update);
    });
}

// ===== Filter Capabilities =====
const filterBtns = document.querySelectorAll('.filter-btn');
const cards = document.querySelectorAll('.card');

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const filter = btn.getAttribute('data-filter');

        cards.forEach((card, i) => {
            const category = card.getAttribute('data-category');
            const show = filter === 'all' || category === filter;

            if (show) {
                card.classList.remove('hidden');
                card.style.animation = `fadeInUp 0.4s ease ${i * 0.05}s both`;
            } else {
                card.classList.add('hidden');
            }
        });
    });
});

// ===== Interactive Demo =====
const demos = {
    code: {
        input: `"Write a function that finds the\n most frequent element in an array\n and returns it along with its count."`,
        output: `<span class="kw">function</span> <span class="fn">mostFrequent</span>(arr) {
  <span class="kw">const</span> freq = <span class="kw">new</span> <span class="fn">Map</span>();
  <span class="kw">let</span> maxCount = <span class="num">0</span>;
  <span class="kw">let</span> maxItem = <span class="kw">null</span>;

  <span class="kw">for</span> (<span class="kw">const</span> item <span class="kw">of</span> arr) {
    <span class="kw">const</span> count = (freq.<span class="fn">get</span>(item) || <span class="num">0</span>) + <span class="num">1</span>;
    freq.<span class="fn">set</span>(item, count);
    <span class="kw">if</span> (count > maxCount) {
      maxCount = count;
      maxItem = item;
    }
  }

  <span class="kw">return</span> { item: maxItem, count: maxCount };
}

<span class="comment">// O(n) time, O(n) space</span>`
    },
    explain: {
        input: `"Explain this code:\n\n const debounce = (fn, ms) => {\n   let id;\n   return (...args) => {\n     clearTimeout(id);\n     id = setTimeout(() => fn(...args), ms);\n   };\n };"`,
        output: `<span class="comment">// This is a <b>debounce</b> function - a common pattern
// that limits how often a function executes.</span>

<span class="highlight-line"><b>How it works:</b></span>

<span class="num">1.</span> It wraps your function <span class="fn">fn</span> and returns
   a new function

<span class="num">2.</span> Each call <b>resets a timer</b> via clearTimeout

<span class="num">3.</span> The original function only runs after
   <span class="fn">ms</span> milliseconds of <b>inactivity</b>

<span class="highlight-line"><b>Use case:</b></span>  Search-as-you-type input
  where you don't want to fire an API
  call on every keystroke

<span class="comment">// Example:</span>
<span class="kw">const</span> search = <span class="fn">debounce</span>(callAPI, <span class="num">300</span>);
input.<span class="fn">addEventListener</span>(<span class="str">'input'</span>, search);`
    },
    refactor: {
        input: `"Refactor this code to be cleaner:\n\n function getDiscount(user) {\n   if (user.type == 'premium') {\n     if (user.years > 5) {\n       return 0.3;\n     } else {\n       return 0.2;\n     }\n   } else {\n     if (user.years > 5) {\n       return 0.1;\n     } else {\n       return 0;\n     }\n   }\n }"`,
        output: `<span class="kw">const</span> DISCOUNTS = {
  premium: { senior: <span class="num">0.3</span>, regular: <span class="num">0.2</span> },
  standard: { senior: <span class="num">0.1</span>, regular: <span class="num">0</span> },
};

<span class="kw">function</span> <span class="fn">getDiscount</span>(user) {
  <span class="kw">const</span> tier = user.type === <span class="str">'premium'</span>
    ? <span class="str">'premium'</span>
    : <span class="str">'standard'</span>;
  <span class="kw">const</span> level = user.years > <span class="num">5</span>
    ? <span class="str">'senior'</span>
    : <span class="str">'regular'</span>;

  <span class="kw">return</span> DISCOUNTS[tier][level];
}

<span class="comment">// Improvements:
// - Eliminated nested if/else
// - Data-driven approach with lookup table
// - Fixed == to === (strict equality)
// - Easy to extend with new tiers</span>`
    },
    test: {
        input: `"Write tests for this function:\n\n function isPalindrome(str) {\n   const clean = str\n     .toLowerCase()\n     .replace(/[^a-z0-9]/g, '');\n   return clean === \n     clean.split('').reverse().join('');\n }"`,
        output: `<span class="fn">describe</span>(<span class="str">'isPalindrome'</span>, () => {
  <span class="fn">it</span>(<span class="str">'returns true for palindromes'</span>, () => {
    <span class="fn">expect</span>(<span class="fn">isPalindrome</span>(<span class="str">'racecar'</span>))
      .toBe(<span class="num">true</span>);
  });

  <span class="fn">it</span>(<span class="str">'ignores case'</span>, () => {
    <span class="fn">expect</span>(<span class="fn">isPalindrome</span>(<span class="str">'RaceCar'</span>))
      .toBe(<span class="num">true</span>);
  });

  <span class="fn">it</span>(<span class="str">'ignores non-alphanumeric'</span>, () => {
    <span class="fn">expect</span>(<span class="fn">isPalindrome</span>(<span class="str">'A man, a plan, a canal: Panama'</span>))
      .toBe(<span class="num">true</span>);
  });

  <span class="fn">it</span>(<span class="str">'returns false for non-palindromes'</span>, () => {
    <span class="fn">expect</span>(<span class="fn">isPalindrome</span>(<span class="str">'hello'</span>))
      .toBe(<span class="num">false</span>);
  });

  <span class="fn">it</span>(<span class="str">'handles empty string'</span>, () => {
    <span class="fn">expect</span>(<span class="fn">isPalindrome</span>(<span class="str">''</span>))
      .toBe(<span class="num">true</span>);
  });
});`
    }
};

const demoBtns = document.querySelectorAll('.demo-btn');
const demoInput = document.getElementById('demoInput');
const demoOutput = document.getElementById('demoOutput');
const typingIndicator = document.getElementById('typingIndicator');

function showDemo(name) {
    const demo = demos[name];
    demoInput.innerHTML = demo.input;

    // Simulate typing effect
    demoOutput.innerHTML = '';
    typingIndicator.classList.add('visible');

    setTimeout(() => {
        typingIndicator.classList.remove('visible');
        demoOutput.innerHTML = demo.output;
        demoOutput.style.animation = 'fadeInUp 0.3s ease';
    }, 600);
}

demoBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        demoBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        showDemo(btn.getAttribute('data-demo'));
    });
});

// ===== Intersection Observer for Animations =====
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.5s ease both';
        }
    });
}, { threshold: 0.1 });

cards.forEach(card => observer.observe(card));

// ===== Initialize =====
document.addEventListener('DOMContentLoaded', () => {
    animateCounters();
    showDemo('code');
});
