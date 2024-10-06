document.addEventListener("DOMContentLoaded", function () {
    createOverallChart(overallPercentages);
    animateProgressBars();
    animateCounters();
});

function animateCounters() {
    const counters = document.querySelectorAll('.present-count, .percentage');
    counters.forEach(counter => {
        const target = +counter.getAttribute('data-target');
        const increment = target / 100;

        function updateCounter() {
            const value = +counter.innerText;

            if (value < target) {
                counter.innerText = Math.ceil(value + increment);
                setTimeout(updateCounter, 20);
            } else {
                counter.innerText = target;
            }
        }

        updateCounter();
    });
}

function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const target = +bar.getAttribute('data-target');
        bar.style.width = `${target}%`;
    });
}

function createOverallChart(overallPercentages) {
    const ctx = document.getElementById('overallChart').getContext('2d');
    const overallData = {
        labels: ['4ISEA', '4ISEB', '4CSDS', '2ISEA', '2ISEB'],
        datasets: [{
            data: overallPercentages,
            backgroundColor: [
                '#28a745',
                '#17a2b8',
                '#ffc107',
                '#dc3545',
                '#6c757d'
            ],
            hoverBackgroundColor: [
                '#28a745',
                '#17a2b8',
                '#ffc107',
                '#dc3545',
                '#6c757d'
            ]
        }]
    };

    new Chart(ctx, {
        type: 'pie',
        data: overallData,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            const dataset = tooltipItem.dataset;
                            const total = dataset.data.reduce((sum, value) => sum + value, 0);
                            const currentValue = dataset.data[tooltipItem.dataIndex];
                            const percentage = Math.floor(((currentValue / total) * 100) + 0.5);
                            return `${currentValue}% (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}
