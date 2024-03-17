document.addEventListener("DOMContentLoaded", function () {
            const questionCards = document.querySelectorAll('.question-card');
            let currentCardIndex = 0;

            function showCard(index) {
                questionCards.forEach((card, idx) => {
                    if (idx === index) {
                        card.classList.add('active');
                    } else {
                        card.classList.remove('active');
                    }
                });
                toggleButtonState();
            }

            function toggleButtonState() {
                const prevBtn = document.querySelector('.prev-btn');
                const nextBtn = document.querySelector('.next-btn');

                prevBtn.disabled = currentCardIndex === 0;
                nextBtn.disabled = currentCardIndex === questionCards.length - 1;
            }

            function showNextCard() {
                if (currentCardIndex < questionCards.length - 1) {
                    currentCardIndex++;
                    showCard(currentCardIndex);
                }
            }

            function showPreviousCard() {
                if (currentCardIndex > 0) {
                    currentCardIndex--;
                    showCard(currentCardIndex);
                }
            }

            document.querySelector('.next-btn').addEventListener('click', showNextCard);
            document.querySelector('.prev-btn').addEventListener('click', showPreviousCard);

            // Show the initial card
            showCard(currentCardIndex);
        });




        // ------- video------- 

    