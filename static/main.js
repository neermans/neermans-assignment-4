document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault();
    let query = document.getElementById('query').value;
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
    let chartCanvas = document.getElementById('similarity-chart');
    chartCanvas.style.display = 'none';  // Hide the chart until the data is ready

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'query': query})
    })
    .then(response => response.json())
    .then(data => {
        displayResults(data);
        displayChart(data);
    })
    .catch(error => console.error('Error:', error));
});

function displayResults(data) {
    let resultsDiv = document.getElementById('results');
    resultsDiv.style.display = 'block'; // Make the results div visible
    resultsDiv.innerHTML = '<h2>Results</h2>';
    
    data.documents.forEach((doc, index) => {
        let docDiv = document.createElement('div');
        docDiv.innerHTML = `<strong>Document ${data.indices[index] + 1}</strong>: ${doc.text} <br><strong>Similarity: ${doc.similarity.toFixed(3)}</strong>`;
        resultsDiv.appendChild(docDiv);
    });
}

function displayChart(data) {
    let ctx = document.getElementById('similarity-chart').getContext('2d');
    if (window.barChart) {
        window.barChart.destroy(); // Destroy the previous chart if exists
    }
    window.barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.indices.map(idx => `Document ${idx + 1}`),
            datasets: [{
                label: 'Cosine Similarity',
                data: data.similarities,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    ctx.canvas.style.display = 'block'; // Display the chart canvas
}
