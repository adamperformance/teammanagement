document.addEventListener('DOMContentLoaded', () => {

    // hide the rows by setting the display property?

    // get json data from backend (format is date:picture url)
    fetch('//127.0.0.1:8000/bw_api')
    .then(response => response.json())
    .then(data => {
        
        bws = data

        dates = []
        day_dates = []
        weights = []
        bfs = []


        for (let i = 0; i < bws.length; i++) {
            x = bws[i]
            dates.push(x["date"])
            y = x["date"].split(",")
            day_dates.push(String((y[0])))
            weights.push(x["bodyweight"])
            bfs.push(x["bodyfat"])
        }


        const ctx = document.getElementById('myChart')

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: day_dates,
                datasets: [{
                    label: 'Testsúly',
                    data: weights,
                    borderWidth: 1
            }]
            },
            options: {
                scales: {
                    y: {
                        startarzero: false,
                    }
                },
                responsive: true,
                maintainAspectRatio: false
            }
        });
    })

    
})