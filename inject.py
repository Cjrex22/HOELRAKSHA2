import re

with open("/Users/churchil/Downloads/dsdsds/index.html", "r") as f:
    content = f.read()

# 1. Inject CSS right before </style>
css_code = """
        /* ─── NEW TESTIMONIALS SECTION ─── */
        .testimonials-section {
            width: 100%;
            background-color: #0E0D0B;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 140px 40px;
            box-sizing: border-box;
            position: relative;
            overflow: hidden;
        }

        .testimonials-inner {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            max-width: 820px;
            width: 100%;
            text-align: center;
            position: relative;
        }

        .testimonials-quote-mark {
            font-family: 'Playfair Display', serif;
            font-weight: 700;
            font-style: normal;
            font-size: 88px;
            color: #C9A96E;
            line-height: 1;
            margin-bottom: 36px;
            display: block;
            text-align: center;
            user-select: none;
        }

        .testimonials-slides {
            position: relative;
            width: 100%;
            min-height: 220px;
        }

        .testimonials-slide {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            opacity: 0;
            transition: opacity 0.85s cubic-bezier(0.4, 0, 0.2, 1);
            pointer-events: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0;
        }

        .testimonials-slide.active {
            opacity: 1;
            pointer-events: auto;
            position: relative;
        }

        .testimonials-quote-text {
            font-family: 'Playfair Display', serif;
            font-weight: 400;
            font-style: italic;
            font-size: clamp(24px, 2.6vw, 36px);
            color: #F0EBE0;
            line-height: 1.62;
            letter-spacing: 0.005em;
            text-align: center;
            max-width: 760px;
            margin: 0 auto 48px auto;
        }

        .testimonials-author {
            font-family: 'DM Sans', sans-serif;
            font-weight: 500;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.26em;
            color: #C9A96E;
            text-align: center;
            margin-bottom: 10px;
        }

        .testimonials-source {
            font-family: 'DM Sans', sans-serif;
            font-weight: 400;
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.20em;
            color: rgba(240, 235, 224, 0.38);
            text-align: center;
        }

        .testimonials-dots {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-top: 52px;
        }

        .t-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background-color: rgba(240, 235, 224, 0.22);
            transition: background-color 0.4s ease, transform 0.4s ease;
            cursor: pointer;
        }

        .t-dot.active {
            background-color: #C9A96E;
            transform: scale(1.2);
        }
    </style>"""

content = content.replace("</style>", css_code)

# 2. Inject HTML right after section-2
html_code = """</div>

<!-- SECTION: TESTIMONIALS -->
<section id="testimonials" class="testimonials-section">
    <div class="testimonials-inner">
        <div class="testimonials-quote-mark">&#8221;</div>
        
        <div class="testimonials-slides">
            <div class="testimonials-slide active" data-index="0">
                <div class="testimonials-quote-text">"An experience that transcends mere hospitality. Raksha is a study in silence, elegance, and the profound beauty of doing less, perfectly."</div>
                <div class="testimonials-author">JULIANNE V.</div>
                <div class="testimonials-source">GLOBAL EXPLORER MAGAZINE</div>
            </div>
            
            <div class="testimonials-slide" data-index="1">
                <div class="testimonials-quote-text">"Every space Raksha creates feels inevitable &mdash; as if it could not have existed any other way. Precision that makes you feel something."</div>
                <div class="testimonials-author">MARCUS T.</div>
                <div class="testimonials-source">ARCHITECTURAL DIGEST</div>
            </div>
            
            <div class="testimonials-slide" data-index="2">
                <div class="testimonials-quote-text">"Raksha does not simply design buildings. They sculpt the quality of light, of air, of time itself within a space. Nothing short of extraordinary."</div>
                <div class="testimonials-author">ELENA S.</div>
                <div class="testimonials-source">THE DESIGN OBSERVER</div>
            </div>
        </div>

        <div class="testimonials-dots">
            <span class="t-dot active" data-dot="0"></span>
            <span class="t-dot" data-dot="1"></span>
            <span class="t-dot" data-dot="2"></span>
        </div>
    </div>
</section>
"""

# Find the end of section-2. The previous edit deleted section 4, leaving section-2
# directly above the first script tag.
# Let's target the exact closing div of section 2.
# We will inject HTML right before the first <script> tag.
content = content.replace("<script>", html_code + "\n<script>", 1)

# 3. Inject JS at the bottom of the last script block
js_code = """

    // ─── TESTIMONIALS SLIDER ───
    (function() {
        const slides = document.querySelectorAll('.testimonials-slide');
        const dots = document.querySelectorAll('.t-dot');
        let currentSlide = 0;
        let testimonialTimer;

        function goToSlide(index) {
            slides[currentSlide].classList.remove('active');
            dots[currentSlide].classList.remove('active');
            currentSlide = index;
            slides[currentSlide].classList.add('active');
            dots[currentSlide].classList.add('active');
        }

        function nextSlide() {
            const next = (currentSlide + 1) % slides.length;
            goToSlide(next);
        }

        function startTimer() {
            testimonialTimer = setInterval(nextSlide, 2000);
        }

        function resetTimer() {
            clearInterval(testimonialTimer);
            startTimer();
        }

        // Dot click — manual override resets timer
        dots.forEach((dot, i) => {
            dot.addEventListener('click', () => {
                goToSlide(i);
                resetTimer();
            });
        });

        // Init
        if (slides.length) {
            startTimer();
        }
    })();
</script>"""

parts = content.rsplit("</script>", 1)
content = parts[0] + js_code + "\n" + (parts[1] if len(parts) > 1 else "")

with open("/Users/churchil/Downloads/dsdsds/index.html", "w") as f:
    f.write(content)

